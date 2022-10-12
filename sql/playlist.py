from alchemy import session, Sql_anime, Sql_playlist, Sql_users

def post_user_playlist(user_uuid: str):
    sql_anime_list = session.query(
            Sql_anime.mal_id,
            Sql_anime.title,
            Sql_anime.description,
            Sql_anime.total_episodes,
            Sql_playlist.watched_episodes,
            Sql_anime.image
    )\
        .join(Sql_playlist, Sql_users) \
        .filter(Sql_users.user_uuid == user_uuid).all()  # type: [Sql_anime]

    response = []
    for sql_anime in sql_anime_list:
        sql_anime = sql_anime
        data = {
            'id': sql_anime[0],
            'title': sql_anime[1],
            'desc': sql_anime[2],
            'total_episodes': sql_anime[3],
            'watched_episodes': sql_anime[4],
            'image': sql_anime[5]
        }
        response.append(data)

    return response
