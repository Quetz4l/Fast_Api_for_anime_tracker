from alchemy import session,Sql_users


def add_new_user() -> Sql_users:
    # try:
    #     new_user = Sql_users(
    #             username=data['username'],
    #             password=data['password'],
    #     )
    #     session.add(new_user)
    #     session.commit()
    # except:
    #     return False

    new_user = Sql_users(
            username='Quetz4l',
            password='asd',
    )
    session.add(new_user)
    session.commit()

    return new_user




def get_user(uuid:str)->Sql_users:
    sql_user =  session.query(Sql_users).filter(Sql_users.user_uuid == uuid).first()
    return sql_user




def get_user_id(uuid:str):
    return get_user(uuid).id