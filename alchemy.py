from sqlalchemy import create_engine, Integer, Column, String, ForeignKey
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker, relationship, scoped_session
from time import time
from uuid import uuid4

# Соединение с базой данных
engine = create_engine('sqlite:///src/server.db', echo=False)
Base = declarative_base()


# Определение таблицы в базе данных
class Sql_users(Base):
    __tablename__ = 'users'

    id = Column(Integer, primary_key=True)
    user_uuid = Column(String, nullable=True)
    username = Column(String, nullable=False)
    password = Column(String, nullable=False)
    language = Column(String, nullable=False)
    permissions = Column(Integer, default=0)
    last_visit = Column(Integer, nullable=False)
    registration_date = Column(Integer, nullable=False)

    anime_playlist = relationship('Sql_playlist', lazy='joined')


    def __init__(self, username: str, password: str, language: str = 'eng'):
        timestamp_now = round(time())

        self.username = username
        self.language = language
        self.password = password
        self.registration_date = timestamp_now
        self.last_visit = timestamp_now
        self.user_uuid = uuid4().hex


class Sql_playlist(Base):
    __tablename__ = "playlist"

    id = Column(Integer, primary_key=True)
    watched_episodes = Column(Integer, nullable=False, default=0)
    state = Column(String, nullable=False, default='watching')

    user_id = Column(Integer, ForeignKey('users.id'))
    anime_id = Column(Integer, ForeignKey('anime.id'))


    def __init__(self, user_id: int, anime_id: int):
        self.anime_id = anime_id
        self.user_id = user_id


class Sql_anime(Base):
    __tablename__ = 'anime'

    id = Column(Integer, primary_key=True)
    mal_id = Column(Integer, nullable=False)
    title = Column(String, nullable=False)
    titles = Column(String)
    season = Column(String)
    total_episodes = Column(Integer, nullable=False)
    last_published_episode = Column(Integer)
    year = Column(Integer)
    genre = Column(String)
    country = Column(String)
    description = Column(String, nullable=False)
    anime_type = Column(String)
    image = Column(String, nullable=False)

    anime_urls = relationship('Sql_urls', lazy='joined')
    anime_playlist = relationship('Sql_playlist', lazy='joined')


    def __init__(self,
                 mal_id: int,
                 title: str,
                 titles: str,
                 season: int,
                 total_episodes: int,
                 last_published_episode: int,
                 year: int,
                 genre: str,
                 country: str,
                 description: str,
                 anime_type: str,
                 image: str,
                 ):
        self.mal_id = mal_id
        self.title = title
        self.titles = titles
        self.season = season
        self.total_episodes = total_episodes
        self.last_published_episode = last_published_episode
        self.year = year
        self.genre = genre
        self.country = country
        self.description = description
        self.anime_type = anime_type
        self.image = image


class Sql_urls(Base):
    __tablename__ = 'urls'

    id = Column(Integer, primary_key=True)
    source = Column(String, nullable=False)
    url = Column(String, nullable=False, unique=True)

    anime_id = Column(String, ForeignKey('anime.id'))


    def __init__(self, anime_id: int, url: str, source: str):
        self.anime_id = anime_id
        self.url = url
        self.source = source


class Sql_ids(Base):
    __tablename__ = 'ids'

    id = Column(Integer, primary_key=True)
    source = Column(String, nullable=False)
    url = Column(String, nullable=False, unique=True)
    another_id = Column(String, nullable=False)

    anime_id = Column(String, ForeignKey('anime.id'))


    def __init__(self, anime_id: int, another_id: int, source: str = 'jikan.moe'):
        self.anime_id = anime_id
        self.another_id = another_id
        self.source = source


# Создание таблицы
Base.metadata.create_all(engine)
session = scoped_session(sessionmaker(bind=engine))
