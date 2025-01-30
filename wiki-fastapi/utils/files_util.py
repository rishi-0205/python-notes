import os
from random import choice

ENTRIES = "entries"
os.makedirs(ENTRIES, exist_ok=True)

def get_list_of_entries() -> tuple:
    """Getting list of all the entries"""
    
    all_entries = os.listdir(ENTRIES)
    titles = [entry.split(".")[0] for entry in all_entries]
    slugs = [title.replace(" ", "-") for title in titles]
    return titles, slugs


def get_article_by_title(slug: str) -> str:
    """Getting article from the slug"""

    title = slug.replace("-", " ") + ".md"
    file_path = os.path.join(ENTRIES, title)
    with open(file_path, "r", encoding="utf-8") as f:
        return title.split(".")[0], f.read()
    

def get_random() -> str:
    """Getting random article"""

    all_entries = os.listdir(ENTRIES)
    titles = [entry.split(".")[0] for entry in all_entries]
    slugs = [title.replace(" ", "-") for title in titles]
    return choice(slugs)


def isExist(query: str) -> str:
    files_path = os.path.join(ENTRIES, query+".md")
    return os.path.exists(files_path)

def create_new_article(title: str, content: str) -> bool:
    if isExist(title):
        return False
    else:
        with open(f"{ENTRIES}/{title}.md", "w") as file:
            file.write(content)
        return True
    
def save_edit(title: str, content: str, slug: str) -> str:
    slug = slug.replace("-"," ")
    if(slug == title):
        with open(f"{ENTRIES}/{title}.md", "w") as file:
            file.write(content)
        return slug
    else:
        old_path = os.path.join(ENTRIES, slug+".md")
        new_path = os.path.join(ENTRIES, title+".md")
        os.rename(old_path, new_path)
        with open(f"{ENTRIES}/{title}.md", "w") as file:
            file.write(content)
        return title.replace(" ", "-")