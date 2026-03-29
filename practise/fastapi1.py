from fastapi import FastAPI
from fastapi.responses import HTMLResponse

app = FastAPI()

# ---------- Простой JSON ----------




@app.get("/hello")
def hello():
    return {"message": "Hello, FastAPI!"}




# ---------- Передача параметра ----------



@app.get("/greet")
def greet(name: str = "Student"):
    return {"greeting": f"Hello, {name}!"}





# ---------- HTML-страница ----------



@app.get("/html", response_class=HTMLResponse)
def html_page():
    return """
    <html>
        <head>
            <title>Simple Page</title>
        </head>
        <body>
            <h1 style="color:blue;">Hello from FastAPI!</h1>
            <p>This is a simple HTML page.</p>
            <a href="https://www.instagram.com/">Link to instagram</a>
        </body>
    </html>
    """




# ---------- Список фильмов без классов ----------
movies = [
    {"title": "Inception", "year": 2010},
    {"title": "Interstellar", "year": 2014},
    {"title": "The Dark Knight", "year": 2008}
]




@app.get("/movies")
def get_movies():
    return {"movies": movies}






@app.get("/movies/filter")
def filter_movies(year: int = 2000):
    filtered = [m for m in movies if m["year"] >= year]
    return {"filtered_movies": filtered}
