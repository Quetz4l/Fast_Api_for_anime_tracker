from sqlalchemy import create_engine, Integer, Column, String, Boolean, ForeignKey
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker, relationship
from time import time

# Соединение с базой данных
engine = create_engine('sqlite:///server.db', echo=False)
Base = declarative_base()


# Определение таблицы в базе данных
class Sql_users(Base):
    __tablename__ = 'users'

    id = Column(Integer, primary_key=True)
    username = Column(String, nullable=False)
    password = Column(String, nullable=False)
    language = Column(String, nullable=False)
    permissions = Column(Integer, default=0)
    last_visit = Column(Integer, nullable=False)
    registration_date = Column(Integer, nullable=False)

    anime_playlist = relationship('Sql_playlist', lazy='joined')


    def __init__(self, username: str, password: str, language: str):
        timestamp_now = round(time())

        self.username = username
        self.registration_date = timestamp_now
        self.last_visit = timestamp_now
        self.language = language
        self.password = password


class Sql_playlist(Base):
    __tablename__ = "anime_playlist"

    id = Column(Integer, primary_key=True)
    episodes = Column(Integer, nullable=False, default=1)
    state = Column(String, nullable=False, default='watching')

    user_id = Column(Integer, ForeignKey('users.id'))
    anime_id: int = Column(Integer, ForeignKey('anime.id'))


    def __init__(self, episodes: int, state: str, user_id: int, anime_id: int):
        self.episodes = episodes
        self.state = state
        self.user_id = user_id
        self.anime_id = anime_id


class Sql_anime(Base):
    __tablename__ = 'anime'

    id = Column(Integer, primary_key=True)
    name = Column(String, nullable=False)
    names = Column(String)
    season = Column(Integer, nullable=False)
    episodes = Column(Integer, nullable=False)
    more_series = Column(Boolean, nullable=False)

    last_published_episode = Column(Integer, nullable=False)
    year = Column(Integer, nullable=False)
    genre = Column(String, nullable=False)
    country = Column(String, nullable=False)
    description = Column(String, nullable=False)
    anime_type = Column(String, nullable=False)
    image = Column(String, nullable=False)

    anime_urls = relationship('Sql_anime_urls', lazy='joined')
    anime_playlist = relationship('Sql_anime_playlist', lazy='joined')


    def __init__(self,
                 name: str,
                 names: str,
                 season: int,
                 episodes: int,
                 last_published_episode: int,
                 year: int,
                 genre: str,
                 country: str,
                 description: str,
                 anime_type: str,
                 image: str,
                 more_series: bool
                 ):
        self.name = name
        self.names = names
        self.season = season
        self.episodes = episodes
        self.last_published_episode = last_published_episode
        self.year = year
        self.genre = genre
        self.country = country
        self.description = description
        self.anime_type = anime_type
        self.image = image
        self.more_series = more_series


class Sql_anime_urls(Base):
    __tablename__ = 'anime_urls'

    id = Column(Integer, primary_key=True)
    source = Column(String, nullable=False)
    url = Column(String, nullable=False, unique=True)

    anime_id = Column(String, ForeignKey('anime.id'))


    def __init__(self, anime_id: int, url: str, source: str):
        self.anime_id = anime_id
        self.url = url
        self.source = source


# Создание таблицы
Base.metadata.create_all(engine)
Session = sessionmaker(bind=engine)

session = Session()
