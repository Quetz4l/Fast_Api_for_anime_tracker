import uvicorn
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
import anime
import users

app = FastAPI()

origins = [
    "*"
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)



@app.get("/")
def read_root():
    return {"Hello": "World"}

@app.get("/anime")
def get_my_anime():
    return anime.get_my_anime()

@app.post("/anime")
def add_anime(new_anime: anime.Anime):
    return anime.add_new_anime(new_anime)


@app.post("/inc/{anime_id}")
def increase(anime_id):
    return anime.increaseWatch(anime_id)


@app.post("/dec/{anime_id}")
def decrease(anime_id):
    return anime.decreaseWatch(anime_id)


if __name__ == '__main__':
    config = uvicorn.Config("main:app", port=5000, log_level="info", debug=True, reload=True)
    server = uvicorn.Server(config)
    server.run()