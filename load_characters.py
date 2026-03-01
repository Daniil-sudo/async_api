import asyncio
import aiohttp
import aiosqlite
import os

DB_NAME = "starwars.db"
API_URL = "https://www.swapi.tech/api/people/{}"


CREATE_TABLE_SQL = """
CREATE TABLE IF NOT EXISTS characters (
    id INTEGER PRIMARY KEY,
    birth_year TEXT,
    eye_color TEXT,
    gender TEXT,
    hair_color TEXT,
    homeworld TEXT,
    mass TEXT,
    name TEXT,
    skin_color TEXT
);
"""


async def fetch_character(session, char_id):
    async with session.get(API_URL.format(char_id)) as response:
        if response.status != 200:
            return None

        data = await response.json()
        props = data["result"]["properties"]

        return (
            int(data["result"]["uid"]),
            props["birth_year"],
            props["eye_color"],
            props["gender"],
            props["hair_color"],
            props["homeworld"],
            props["mass"],
            props["name"],
            props["skin_color"],
        )


async def main():
    print("Файл БД:", os.path.abspath(DB_NAME))

    async with aiosqlite.connect(DB_NAME) as db:
        await db.execute(CREATE_TABLE_SQL)
        await db.commit()

        async with aiohttp.ClientSession() as session:
            tasks = [fetch_character(session, i) for i in range(1, 84)]
            results = await asyncio.gather(*tasks)

            for character in results:
                if character:
                    await db.execute("""
                        INSERT OR REPLACE INTO characters
                        (id, birth_year, eye_color, gender, hair_color, homeworld, mass, name, skin_color)
                        VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
                    """, character)

            await db.commit()

    print("Все персонажи успешно загружены")


if __name__ == "__main__":
    asyncio.run(main())