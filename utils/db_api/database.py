import sqlite3


class Database:
    def __init__(self):
        self.con = sqlite3.connect('database.db')
        self.cursor = self.con.cursor()

    def sql_table(self):
        with self.con:
            sql = """
            CREATE TABLE IF NOT EXISTS 'users' (
              `id` INTEGER PRIMARY KEY,
              `login` varchar(255),
              `subscription` boolean Default False
            );
            """
            self.cursor.execute(sql)
            self.con.commit()

    def sql_get_user(self, id):
        with self.con:
            sql = """
                SELECT * FROM users WHERE id=?
            """
            self.cursor.execute(sql, [(id)])
            row = self.cursor.fetchone()
            return row

    def sql_add(self, id, login):
        with self.con:
            sql = f"""
                INSERT INTO `users` (id, login) VALUES (?,?)
            """
            self.cursor.execute(sql, (id, login))
            self.con.commit()

    def sql_update(self, id, subscription):
        with self.con:
            sql = f"""
                UPDATE users
                SET subscription = ?
                WHERE id = ?
            """
            self.cursor.execute(sql, (subscription, id))
            self.con.commit()

    def sql_get_all_users(self):
        with self.con:
            sql = "SELECT * FROM users"
            self.cursor.execute(sql)
            rows = self.cursor.fetchall()
            return rows

    def add_user(self, id, login):
        if not self.sql_get_user(id):
            self.sql_add(id, login)

    def update_user(self, id, username, subscription=True):
        if not self.sql_get_user(id):
            self.sql_add(id, username)
        self.sql_update(id, subscription)
