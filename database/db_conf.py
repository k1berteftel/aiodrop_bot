import sqlite3

class database():
    def __init__(self, name):
        self.connection = sqlite3.connect(name)
        self.cursor = self.connection.cursor()

    def check_user(self, user_id) -> bool:
        with self.connection:
            result = self.cursor.execute('SELECT `user_id` FROM `users` WHERE `user_id` = ?', (user_id,)).fetchmany(1)
            return bool(len(result))

    def add_user(self, user_id: int, deep_link: str) -> None:
        with self.connection:
            self.cursor.execute('INSERT INTO `users` (`user_id`, `deep_link`) VALUES (?, ?)', (user_id, deep_link))

    def get_deeplinks(self) -> list:
        with self.connection:
            result = self.cursor.execute('SELECT `deep_link` FROM `users`').fetchall()
            return list(result)

    def get_deeplink(self, user_id) -> str:
        with self.connection:
            result = self.cursor.execute('SELECT `deep_link` FROM `users` WHERE `user_id` = ?', (user_id,)).fetchmany(1)
            return str(result[0][0])

    def get_balance(self, user_id) -> int:
        with self.connection:
            result = self.cursor.execute('SELECT `balance` FROM `users` WHERE `user_id` = ?', (user_id,)).fetchmany(1)
            return int(result[0][0])

    def update_balance(self, deep_link):
        with self.connection:
            self.cursor.execute('UPDATE `users` SET `balance` = `balance` + 200, `referrals` = `referrals` + 1 '
                                'WHERE `deep_link` = ?', (deep_link,))

    def update_balance_without_deeplink(self, user_id: int, balance: int):
        with self.connection:
            self.cursor.execute('UPDATE `users` SET `balance` = `balance` + ? WHERE `user_id` = ?', (balance, user_id,))


    def get_data(self, user_id) -> str|bool:
        with self.connection:
            result = self.cursor.execute('SELECT `datetime` FROM `users` WHERE `user_id` = ?', (user_id,)).fetchmany(1)
            return str(result[0][0]) if bool(result[0][0]) else False

    def update_data(self, data: str, user_id: int):
        with self.connection:
            self.cursor.execute('UPDATE `users` SET `datetime` = ? WHERE `user_id` = ?', (data, user_id,))

    def delete_data(self):
        with self.connection:
            self.cursor.execute('DELETE FROM `users`')


    def update_wallet(self, user_id: int, wallet_adress: str):
        with self.connection:
            self.cursor.execute('UPDATE `users` SET `wallet_adress` = ? WHERE `user_id` = ?', (wallet_adress, user_id))