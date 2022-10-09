from pydantic import BaseModel
import alchemy

class Anime(BaseModel):
    id: str
    title: str
    image: str
    total_episodes: int
    watched_episodes: int


ALL_ANIME = []


def add_new_anime(anime: Anime):
    ALL_ANIME.append(anime)
    return anime


def get_my_anime():
    return ALL_ANIME


def increaseWatch(anime_id: str) -> Anime:
    anime = find_anime(anime_id)
    if anime is not None:
        anime.watched_episodes += 1
    return anime


def decreaseWatch(anime_id: str) -> Anime:
    anime = find_anime(anime_id)
    if anime is not None:
        anime.watched_episodes -= 1
    return anime


def find_anime(anime_id: str) -> Anime:
    for anime in ALL_ANIME:
        if anime.id == anime_id:
            return anime
    return None
