from fastapi import FastAPI
from fastapi.templating import Jinja2Templates
from fastapi.responses import RedirectResponse
from fastapi import Request, Form
from utils.files_util import get_list_of_entries, get_article_by_title, get_random, isExist, create_new_article, save_edit
from utils.markdown_util import markdown_to_html

app = FastAPI()

templates = Jinja2Templates(directory="templates")

@app.get("/")
def home(request: Request):
    titles, slugs = get_list_of_entries()
    
    entries = list(zip(titles, slugs))
    
    return templates.TemplateResponse("index.html", {"request": request, "entries": entries})

@app.get("/wiki/{slug}")
def display_article(request: Request, slug: str):
    title, articlemd = get_article_by_title(slug)
    articlehtml = markdown_to_html(articlemd)
    return templates.TemplateResponse("display.html", {"request": request, "title":title, "content": articlehtml, "slug": slug})

@app.get("/random")
def display_random_article(request: Request):
    slug = get_random()
    title, articlemd = get_article_by_title(slug)
    articlehtml = markdown_to_html(articlemd)
    return RedirectResponse(url=f"/wiki/{slug}", status_code=302)

@app.get("/search")
def search(request: Request, query: str):
    if isExist(query):
        slug = query.replace(" ", "-")
        title, articlemd = get_article_by_title(slug)
        articlehtml = markdown_to_html(articlemd)
        return templates.TemplateResponse("display.html", {"request": request, "title":title, "content": articlehtml})

    else:
        er = "<h1>404</h1><p>No such Article Exists</p>"
        return templates.TemplateResponse("display.html", {"request": request, "title":"404", "content": er})
    
@app.get("/create")
def get_create_page(request: Request):
    return templates.TemplateResponse("create.html", {"request": request})

@app.post("/create_new")
def create_new(request: Request, title: str = Form(...), content: str = Form(...)):
    res = create_new_article(title, content)
    if res:
        slug = title.replace(" ", "-")
        return RedirectResponse(url=f"/wiki/{slug}", status_code=302)
    else:
        er = "<h1>400</h1><p>Article with same name Exists</p>"
        return templates.TemplateResponse("display.html", {"request": request, "title":"400", "content": er})
    
@app.get("/edit/{slug}")
def get_edit_page(request: Request, slug: str):
    title, articlemd = get_article_by_title(slug)
    articlehtml = markdown_to_html(articlemd)
    return templates.TemplateResponse("edit.html", {"request": request, "title": title, "content": articlehtml, "slug": slug})

@app.post("/edit_save/{slug}")
def save_article(request: Request, slug: str, content: str = Form(...), title: str = Form(...)):
    new_slug = save_edit(title, content, slug)
    return RedirectResponse(url=f"/wiki/{new_slug}", status_code=302)
