from alchemy import session, Sql_anime, Sql_playlist, Sql_users
from sql import users
from service import parsing



def add_new_anime_to_playlist(user_uuid,  source, external_anime_id):
    # try:
        user_id = users.get_user_id(user_uuid)
        sql_anime = get_anime(source, external_anime_id)

        sql_playlist = session.query(Sql_playlist).join(Sql_users, Sql_anime).filter(Sql_users.user_uuid == user_uuid, Sql_anime.mal_id == external_anime_id).first()
        if sql_playlist:
            return 'already in playlist'

        new_playlist = Sql_playlist(
                anime_id=sql_anime.id,
                user_id=user_id
        )
        session.add(new_playlist)
        session.commit()

    # except Exception:
    #     return False

        return True


def get_anime(source, external_anime_id):
    sql_anime = session.query(Sql_anime).filter(Sql_anime.mal_id == external_anime_id).first()
    if sql_anime is None:
        s =  add_new_anime(source, external_anime_id)
        return s
    else:
        return sql_anime


def add_new_anime(source, jikan_anime_id):
    if source == "jikan":
        anime = parsing.get_anime_from_jikan(jikan_anime_id)['data']
    else:
        return False

    new_anime = Sql_anime(
            mal_id=anime['mal_id'],
            title=anime['title'],
            titles='/'.join([title['title'] for title in anime['titles']]),
            season=anime['season'],
            total_episodes=anime['episodes'],
            last_published_episode=anime['episodes'] if anime['status'] == 'Finished Airing' else None,
            year=anime['year'],
            genre='/'.join([genre['name'] for genre in anime['genres']]),
            country='japan' if anime.get('title_japanese') else '???',
            description=anime['synopsis'],
            anime_type=anime['type'],
            image=anime['images']['jpg']['image_url'],
    )

    session.add(new_anime)
    session.commit()

    return new_anime


def get_my_anime(user_uuid: str, ):
    return session.query(
            Sql_anime.title,
            Sql_anime.image,
            Sql_anime.episodes,
            Sql_playlist.watched_episodes) \
        .join(Sql_playlist) \
        .join(Sql_users) \
        .filter(Sql_users.user_uuid == user_uuid, Sql_playlist.state == 'watching').all()


def change_watched_episode(user_uuid, anime_id, count):
    try:
        count = int(count)
    except:
        return

    sql_playlist = session.query(Sql_playlist).join(Sql_users, Sql_anime).filter(Sql_users.user_uuid == user_uuid, Sql_anime.mal_id == anime_id).first()
    if sql_playlist is not None:
        sql_playlist.watched_episodes += count

        if sql_playlist.watched_episodes > 0:
            session.commit()
            return True
    return False
