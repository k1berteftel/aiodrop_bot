import datetime
from database.db_conf import database

db = database('users_database')

def get_state(user_id: int, db: database) -> bool:
    date = db.get_data(user_id)
    if date:
        date = date.split('-')
        last_date = datetime.date(year=int(date[0]), month=int(date[1]), day=int(date[2]))
        sept = str(last_date - datetime.date.today()).split(' ')
        if len(sept) != 1:
            return True
        return False
    return True