import string
import random
from database.db_conf import database

def sub_check(chat_member):
    if chat_member.status != 'left':
        return True
    return False

def get_random_deeplink(db: database) -> str:
    fixture = 'https://t.me/cheburash_ton_bot?start='
    string.ascii_letter = 'abcdefghijklmnopqrstuvwxyz1234567890ABCDEFGHIJKLMNOPQRSTUVWXYZ'
    simvols = ''
    for i in range(0, 9):
        simvols += str(random.choice(string.ascii_letters))

    simvols = fixture + simvols
    if simvols not in db.get_deeplinks():
        return simvols
    get_random_deeplink(db=db)



def add_refferal(deeplink: str, db: database):
    fixture = 'https://t.me/floki_ton_bot?start='
    link = fixture + deeplink
    db.update_balance(link)
