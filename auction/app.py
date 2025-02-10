from fastapi import FastAPI, Depends, HTTPException, Form, Request, status
from fastapi.templating import Jinja2Templates
from fastapi.responses import HTMLResponse, RedirectResponse
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from sqlalchemy.orm import Session
from models.bid import Bid
from models.user_model import User
from models.listing import Listing
from models.comment import Comment
from models.wishlist import Wishlist
from database import SessionLocal, engine, Base
from passlib.context import CryptContext
from sqlalchemy.exc import IntegrityError
from fastapi.staticfiles import StaticFiles
import jwt

app = FastAPI()

# Serve static files from the 'static' folder
app.mount("/static", StaticFiles(directory="static"), name="static")

templates = Jinja2Templates(directory="templates")

# Dependency to get DB session
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

# User authentication setup
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="login")

# Create tables
Base.metadata.create_all(bind=engine)

# Utility function to get the current user from JWT
def get_current_user(token: str, db: Session):
    try:
        payload = jwt.decode(token, "auction_website_key", algorithms=["HS256"])
        user_id = payload.get("user_id")
        if not user_id:
            raise HTTPException(status_code=401, detail="Invalid token")
        
        user = db.query(User).filter(User.id == user_id).first()
        if not user:
            raise HTTPException(status_code=404, detail="User not found")
        
        return user
    except jwt.PyJWTError:
        raise HTTPException(status_code=401, detail="Could not validate credentials")

# Utility function to redirect to login if the user is not authenticated
def check_authenticated(request: Request):
    if "token" not in request.cookies:
        return RedirectResponse(url="/login")
    return None

# Reusable token retrieval
def get_token_from_cookies(request: Request):
    token = request.cookies.get("token")
    if not token:
        raise HTTPException(status_code=401, detail="Not authenticated")
    return token

@app.get("/", response_class=HTMLResponse)
async def home(request: Request, db: Session = Depends(get_db)):
    token = request.cookies.get("token")
    if not token:
        return RedirectResponse(url="/login")
    
    try:
        user = get_current_user(token, db)  # Get current user from token
    except HTTPException:
        return RedirectResponse(url="/login")
    
    listings = db.query(Listing).filter(Listing.active == True).all()
    return templates.TemplateResponse("home.html", {"request": request, "listings": listings, "user": user})

# Route for user registration
@app.get("/register", response_class=HTMLResponse)
async def register(request: Request):
    return templates.TemplateResponse("register.html", {"request": request})

@app.post("/register")
async def register(
    request: Request,
    username: str = Form(...),
    name: str = Form(...),
    email: str = Form(...),
    password: str = Form(...),
    db: Session = Depends(get_db)
):
    hashed_password = pwd_context.hash(password)
    
    try:
        user = User(username=username, name=name, email=email, password=hashed_password)
        db.add(user)
        db.commit()
        db.refresh(user)
        
        # Redirect to the login page after successful registration
        return RedirectResponse(url="/login", status_code=303)
    
    except IntegrityError:
        db.rollback()
        raise HTTPException(status_code=400, detail="User already exists.")

# Route for user login page (GET request)
@app.get("/login", response_class=HTMLResponse)
async def login_page(request: Request):
    return templates.TemplateResponse("login.html", {"request": request, "user": None})

# Route for user login (JWT token generation)
@app.post("/login")
async def login(request: Request, form_data: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(get_db)):
    user = db.query(User).filter(User.username == form_data.username).first()
    if not user or not pwd_context.verify(form_data.password, user.password):
        raise HTTPException(status_code=401, detail="Invalid credentials")
    
    # Create JWT token
    payload = {"user_id": user.id}
    token = jwt.encode(payload, "auction_website_key", algorithm="HS256")

    # Set token in cookies
    response = RedirectResponse(url="/", status_code=303)  # Redirect to home page after login
    response.set_cookie(key="token", value=token, httponly=True, secure=True, samesite="Strict")
    
    return response

# Route to create a new listing
@app.get("/create_listing", response_class=HTMLResponse)
async def create_listing(request: Request):
    token = request.cookies.get("token")
    if not token:
        return RedirectResponse(url="/login")  # Redirect if there's no token
    
    return templates.TemplateResponse("create_listing.html", {"request": request})

@app.post("/create_listing")
async def create_listing(request: Request, product_name: str = Form(...), description: str = Form(...), image: str = Form(...), starting_bid: float = Form(...), active: bool = Form(False), category: str = Form(...), db: Session = Depends(get_db)):
    check_authenticated(request)
    user = await get_current_user(request.cookies.get("token"), db)
    user_id = user.id
    
    listing = Listing(
        product_name=product_name,
        description=description,
        image=image,
        starting_bid=starting_bid,
        active=active,
        category=category,
        user_id=user_id
    )
    
    db.add(listing)
    db.commit()
    db.refresh(listing)
    return {"message": "Listing created successfully!"}

# Route for viewing individual listing (product page)
@app.get("/listing/{listing_id}", response_class=HTMLResponse)
async def view_listing(request: Request, listing_id: int, db: Session = Depends(get_db)):
    check_authenticated(request)

    listing = db.query(Listing).filter(Listing.id == listing_id).first()
    if not listing:
        raise HTTPException(status_code=404, detail="Listing not found")
    
    comments = db.query(Comment).filter(Comment.listing_id == listing_id).all()
    return templates.TemplateResponse("product.html", {"request": request, "listing": listing, "comments": comments})

# Route for placing a bid
@app.post("/bid/{listing_id}")
async def place_bid(request: Request, listing_id: int, bid_value: float = Form(...), db: Session = Depends(get_db)):
    check_authenticated(request)

    user = await get_current_user(request.cookies.get("token"), db)
    user_id = user.id
    
    bid = Bid(bid_value=bid_value, user_id=user_id, listing_id=listing_id)
    db.add(bid)
    db.commit()
    db.refresh(bid)
    
    return {"message": "Bid placed successfully!"}

# Route for posting a comment
@app.post("/comment/{listing_id}")
async def post_comment(request: Request, listing_id: int, comment: str = Form(...), db: Session = Depends(get_db)):
    check_authenticated(request)

    user = await get_current_user(request.cookies.get("token"), db)
    user_id = user.id
    
    new_comment = Comment(comment=comment, user_id=user_id, listing_id=listing_id)
    db.add(new_comment)
    db.commit()
    db.refresh(new_comment)
    
    return {"message": "Comment added successfully!"}

# Route for adding a product to the wishlist
@app.post("/wishlist/{listing_id}")
async def add_to_wishlist(request: Request, listing_id: int, db: Session = Depends(get_db)):
    check_authenticated(request)

    user = await get_current_user(request.cookies.get("token"), db)
    user_id = user.id

    existing_wishlist_item = db.query(Wishlist).filter(Wishlist.listing_id == listing_id, Wishlist.user_id == user_id).first()
    if existing_wishlist_item:
        raise HTTPException(status_code=400, detail="Product already in wishlist")
    
    new_wishlist_item = Wishlist(user_id=user_id, listing_id=listing_id)
    db.add(new_wishlist_item)
    db.commit()
    db.refresh(new_wishlist_item)

    return {"message": "Product added to wishlist"}
