import json

import asyncpg
from asyncpg import Pool

from data import config


class Database:
    def __init__(self, pool):
        self.pool: Pool = pool

    @classmethod
    async def create(cls):
        pool = await asyncpg.create_pool(
            user=config.PGUSER,
            password=config.PGPASSWORD,
            database=config.PGDATABASE,
            host=config.PGHOST,
            port=config.PGPORT
        )
        return cls(pool)

    @staticmethod
    def format_args(sql, parameters: dict):
        sql += " AND ".join([
            f"{item} = ${num + 1}" for num, item in enumerate(parameters)
        ])
        return sql, tuple(parameters.values())

    # Users
    async def sql_table_users(self):
        sql = """
        CREATE TABLE IF NOT EXISTS Users (
            id INT NOT NULL,
            login varchar(255),
            subscription BOOLEAN DEFAULT FALSE,
            PRIMARY KEY (id)
            );
"""
        await self.pool.execute(sql)

    async def sql_add_user(self, id: int, login: str, subscription: bool):
        sql = """
        INSERT INTO Users(id, login, subscription) VALUES($1, $2, $3)
        """
        await self.pool.execute(sql, id, login, subscription)

    async def sql_get_all_users(self):
        sql = """
        SELECT * FROM Users
        """
        return await self.pool.fetch(sql)

    async def sql_get_user(self, **kwargs):
        sql = f"""
        SELECT * FROM Users WHERE 
        """
        sql, parameters = self.format_args(sql, parameters=kwargs)
        return await self.pool.fetchrow(sql, *parameters)

    async def count_users(self):
        return await self.pool.fetchval("SELECT COUNT(*) FROM Users")

    async def sql_update_subscription(self, id, subscription=True):
        sql = f"""
        UPDATE Users SET subscription=$1 WHERE id=$2
        """
        return await self.pool.execute(sql, subscription, id)

    async def delete_users(self):
        await self.pool.execute("DELETE FROM Users WHERE TRUE")

    async def add_user(self, id: int, login: str, subscription: bool = False):
        if not await self.sql_get_user(id=id):
            await self.sql_add_user(id, login, subscription)

    # Keywords
    async def sql_table_keywords(self):
        sql = """
            CREATE TABLE IF NOT EXISTS keywords (
                id serial NOT NULL,
                title varchar(255) NOT NULL,
                PRIMARY KEY (id)
                );
        """
        await self.pool.execute(sql)

    async def add_keyword(self, title: str):
        sql = """
                INSERT INTO keywords(title) VALUES($1)
                """
        await self.pool.execute(sql, title)

    async def add_keywords(self, keyword_list):
        sql = """
                INSERT INTO keywords(title) VALUES
                """
        for i in range(len(keyword_list)):
            sql += f'(${i+1}),'
        await self.pool.execute(sql[:-1], *keyword_list)

    async def get_keywords(self):
        sql = u"""
        SELECT * FROM keywords 
        """
        return await self.pool.fetch(sql)

    async def delete_keyword(self, id: int):
        await self.pool.execute("DELETE FROM keywords WHERE id=$1", id)

    async def delete_keywords(self):
        await self.pool.execute("DELETE FROM keywords WHERE TRUE")

    # Websites
    async def sql_table_websites(self):
        sql = """
            CREATE TABLE IF NOT EXISTS websites (
                id serial NOT NULL,
                name varchar(255) NOT NULL,
                last_link varchar(255),
                PRIMARY KEY (id)
                );
        """
        await self.pool.execute(sql)

    async def add_website(self, name: str):
        sql = """
                INSERT INTO websites(name) VALUES($1)
                """
        await self.pool.execute(sql, name)

    async def add_websites(self, websites_list):
        sql = """
                INSERT INTO websites(name) VALUES
                """
        for num in range(len(websites_list)):
            sql += f'(${num+1}),'
        await self.pool.execute(sql[:-1], *websites_list)

    async def update_website(self, name: str, last_link: str):
        sql = f"""
        UPDATE websites SET last_link=$1 WHERE name=$2
        """
        return await self.pool.execute(sql, last_link, name)

    async def get_websites(self):
        sql = f"""
        SELECT * FROM websites 
        """
        return await self.pool.fetchrow(sql)

    async def get_website(self, **kwargs):
        sql = f"""
        SELECT * FROM websites WHERE 
        """
        sql, parameters = self.format_args(sql, parameters=kwargs)
        return await self.pool.fetchrow(sql, *parameters)

    async def delete_websites(self):
        await self.pool.execute("DELETE FROM websites WHERE TRUE")
