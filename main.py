from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
import uvicorn


from sql import anime, users, playlist

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


class Anime(BaseModel):
    user_uuid: str
    source: str
    external_anime_id: int

class User_uuid(BaseModel):
    user_uuid: str



@app.get("/")
def read_root():
    return {"Hello": "World"}


@app.post("/add")
def add_anime(data: Anime):
    return anime.add_new_anime_to_playlist(data.user_uuid, data. source, data.external_anime_id)


@app.post("/playlist")
def get_playlist(data: User_uuid):
    if data.user_uuid == '':
        sql_user = users.add_new_user()
        return {'user_uuid': sql_user.user_uuid, 'playlist': []}
    else:
        return  {'playlist': playlist.post_user_playlist(data.user_uuid)}


@app.post("/episode/{count}")
def change_episode(data: Anime, count:str):
    return anime.change_watched_episode(data.user_uuid, data.external_anime_id, count)


if __name__ == '__main__':
    config = uvicorn.Config("main:app", port=5000, log_level="info", debug=True, reload=True)
    server = uvicorn.Server(config)
    server.run()
