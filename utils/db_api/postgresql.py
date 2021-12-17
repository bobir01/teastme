from typing import Union
from aiogram.types import user

import asyncpg
from asyncpg import Connection
from asyncpg.pool import Pool

from data import config

class Database:

    def __init__(self):
        self.pool: Union[Pool, None] = None

    async def create(self):
        self.pool = await asyncpg.create_pool(
            user=config.DB_USER,
            password=config.DB_PASS,
            host=config.DB_HOST,
            database=config.DB_NAME
        )

    async def execute(self, command, *args,
                      fetch: bool = False,
                      fetchval: bool = False,
                      fetchrow: bool = False,
                      execute: bool = False
                      ):
        async with self.pool.acquire() as connection:
            connection: Connection
            async with connection.transaction():
                if fetch:
                    result = await connection.fetch(command, *args)
                elif fetchval:
                    result = await connection.fetchval(command, *args)
                elif fetchrow:
                    result = await connection.fetchrow(command, *args)
                elif execute:
                    result = await connection.execute(command, *args)
            return result

    async def create_table_users(self):
        sql = """
        CREATE TABLE IF NOT EXISTS Users (
        id SERIAL PRIMARY KEY,
        full_name VARCHAR(255) NOT NULL,
        username varchar(255) NULL,
        telegram_id BIGINT NOT NULL UNIQUE,
        phone_number BIGINT NULL UNIQUE
        );
        """
        await self.execute(sql, execute=True)

    @staticmethod
    def format_args(sql, parameters: dict):
        sql += " AND ".join([
            f"{item} = ${num}" for num, item in enumerate(parameters.keys(),
                                                          start=1)
        ])
        return sql, tuple(parameters.values())

    async def add_user(self, full_name, username, telegram_id):
        sql = "INSERT INTO Users (full_name, username, telegram_id) VALUES($1, $2, $3) returning *"
        return await self.execute(sql, full_name, username, telegram_id, fetchrow=True)

    async def select_all_users(self):
        sql = "SELECT * FROM Users"
        return await self.execute(sql, fetch=True)

    async def select_user(self, **kwargs):
        sql = "SELECT * FROM Users WHERE "
        sql, parameters = self.format_args(sql, parameters=kwargs)
        return await self.execute(sql, *parameters, fetchrow=True)

    async def count_users(self):
        sql = "SELECT COUNT(*) FROM Users"
        return await self.execute(sql, fetchval=True)

    async def update_user_full_name(self, full_name, telegram_id):
        sql = "UPDATE Users SET full_name=$1 WHERE telegram_id=$2"
        return await self.execute(sql, full_name, telegram_id, execute=True)

    async def update_user_phone(self, phone_number, telegram_id):
        sql = "UPDATE Users SET phone_number=$1 WHERE telegram_id=$2"
        return await self.execute(sql, phone_number, telegram_id, execute=True)

    async def delete_users(self):
        await self.execute("DELETE FROM Users WHERE TRUE", execute=True)

    async def drop_users(self):
        await self.execute("DROP TABLE Users", execute=True)


#================================================================================================

# creating of test table 

    async def create_test_table(self):
        sql = """
        CREATE TABLE IF NOT EXISTS test_table(
            id SERIAL PRIMARY KEY,
            owner_id BIGINT NOT NULL ,
            test_name VARCHAR(100) NOT NULL,
            test_number SERIAL,
            answers VARCHAR(100),
            start_date VARCHAR(50) NULL,
            end_date VARCHAR(50) NULL,
            status VARCHAR(30) DEFAULT 'active'
        )
        """
        await self.execute(sql, execute=True)

# add_test to test_table 
    async def add_test(self, owner_id, test_name, answers, start_date=None, end_date=None):
        if start_date :
            sql = "INSERT INTO test_table(owner_id, test_name, answers ,start_date) VALUES($1, $2, $3, $4) "
            return await self.execute(sql, owner_id, test_name, answers, start_date,   fetchrow=True)
        elif end_date:
            sql = "INSERT INTO test_table(owner_id, test_name, answers ,end_date) VALUES($1, $2, $3, $4) "
            return await self.execute(sql, owner_id, test_name, answers, end_date ,  fetchrow=True)
        elif start_date and end_date:
            sql = "INSERT INTO test_table(owner_id, test_name, answers ,start_date, end_date) VALUES($1, $2, $3, $4, $5) "
            return await self.execute(sql, owner_id, test_name, answers, start_date, end_date ,  fetchrow=True)
        else:
            sql = "INSERT INTO test_table(owner_id, test_name, answers) VALUES($1, $2, $3) "
            return await self.execute(sql, owner_id, test_name, answers, fetchrow=True)

#selecting inserted_test_number() last test_number of added test,  last row

    async def select_inserted_test_number(self):
        sql = "select max(test_number) from test_table"
        return await self.execute(sql, fetchval=True)

# select_test

    async def select_test_all_data(self, **kwargs):
        sql = "SELECT test_number, test_name, answers, start_date, end_date FROM test_table WHERE "
        sql, parameters = self.format_args(sql, parameters=kwargs)
        return await self.execute(sql, *parameters, fetchrow=True)


# select test for dashborad
    async def select_test_with_results(self, owner_id, test_number):
        sql = "SELECT test_number, test_name, answers, start_date, end_date FROM test_table WHERE owner_id = $1 and test_number = $2"
        return await self.execute(sql,owner_id, test_number , fetchrow=True)



#update status if deadline is up 

    async def update_status(self, test_number, status='passive'):
        sql = "UPDATE test_table SET status = $2 WHERE test_number = $1"
        return await self.execute(sql, test_number, status, fetchrow=True)

# counting all number of tests return counts eg : 4 

    async def count_user_tests(self, owner_id):
        sql = "SELECT COUNT(test_number) FROM test_table WHERE owner_id = $1"

        return await self.execute(sql, owner_id,  fetchval=True)

#selecting number of tests with owner id 
    async def select_test_numbers(self, owner_id):
        sql = "SELECT test_number, test_name FROM test_table WHERE owner_id = $1"

        return await self.execute(sql, owner_id,  fetch=True)

    async def delete_test_table(self):
        await self.execute("DELETE FROM test_table WHERE TRUE", execute=True)
    
#=======================================================================================================

# creating table of test_config 

    async def create_test_config(self):
        sql = """
        CREATE TABLE IF NOT EXISTS test_config(
            id SERIAL PRIMARY KEY,
            test_number INTEGER,
            user_id INTEGER,
            answers VARCHAR(100),
            results INTEGER,
            submition_time TIMESTAMP
        )
        """
        await self.execute(sql, execute=True)

# inserting test participants and their results into db config 

    async def insert_test_config(self, test_number, user_id, answer, results, submition_time ):
        sql = "INSERT INTO test_config (test_number, user_id, answers, results, submition_time) VALUES ($1,$2,$3,$4,$5)"
        return await self.execute(sql, test_number, user_id, answer, results, submition_time, fetchrow=True)
   
# select_config with test

    async def select_test_config(self, test_number):
        sql = "SELECT * FROM test_config WHERE test_number = $1"
        return await self.execute(sql, test_number, fetch=True)

# count_paticipants correspondingly their test_numbers 
    async def count_participants_via_test(self, test_number):
        sql = "SELECT COUNT(user_id) FROM test_config WHERE test_number = $1"
        return await self.execute(sql, test_number, fetchval=True)

# count_test_participations() count times how many time participated in tests:

    async def count_test_participations(self, user_id, test_number):
        sql = "SELECT COUNT(test_number) FROM test_config WHERE user_id = $1 and where test_number = $2"
        return await self.execute(sql, user_id,test_number,  fetchval=True)


# dashboard sorted db by results and time 

    async def select_dashboard(self, test_number):
        sql = """select ROW_NUMBER () over (order by test_config.results desc), 
        users.full_name, test_config.answers, test_config.results, users.phone_number 
        from test_config 
        left outer join users on  test_config.user_id = users.telegram_id where test_config.test_number = $1"""
        return await self.execute(sql, test_number, fetch=True)

# check_config pariticipation 

    async def check_config_participation(self, user_id, test_number):

        sql = "select user_id from test_config where user_id = $1  and test_number = $2"
        check = await self.execute(sql, user_id, test_number, fetchval=True)
        if check:
            return True
        else:
            return False

    async def delete_config(self):
        await self.execute("DELETE FROM test_config WHERE TRUE", execute=True)

    async def participated_tests(self, user_id):
        sql = """
        select ROW_NUMBER () over (order by test_number), test_number, answers, results, submition_time from test_config
where user_id = $1 order by submition_time"""
        return await self.execute(sql, user_id, fetch=True)

    async def data_for_certi(self, user_id, test_number):
        sql = """
        select results from test_config  where user_id = $1  and  test_number = $2 """
        return await self.execute(sql, user_id, test_number, fetch=True)