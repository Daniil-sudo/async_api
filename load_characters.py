import asyncio
import aiohttp
import aiosqlite

DB_NAME = "starwars.db"
BASE_URL = "https://www.swapi.tech/api"


async def fetch_json(session, url):
    try:
        async with session.get(url) as response:
            if response.status == 200:
                return await response.json()
    except Exception:
        return None
    return None


async def fetch_homeworld(session, url):
    if not url:
        return None

    data = await fetch_json(session, url)
    if data:
        return data["result"]["properties"]["name"]

    return None


async def fetch_character(session, url):
    data = await fetch_json(session, url)
    if not data:
        return None

    props = data["result"]["properties"]

    homeworld = await fetch_homeworld(session, props["homeworld"])

    return (
        int(data["result"]["uid"]),
        props["birth_year"],
        props["eye_color"],
        props["gender"],
        props["hair_color"],
        homeworld,
        props["mass"],
        props["name"],
        props["skin_color"],
    )


async def main():

    async with aiohttp.ClientSession() as session:

        # получаем список персонажей
        data = await fetch_json(session, f"{BASE_URL}/people?page=1&limit=100")
        characters = data["results"]

        tasks = [fetch_character(session, char["url"]) for char in characters]

        results = await asyncio.gather(*tasks)

        results = [r for r in results if r]

        async with aiosqlite.connect(DB_NAME) as db:

            await db.executemany(
                """
                INSERT OR REPLACE INTO characters
                (id, birth_year, eye_color, gender, hair_color, homeworld, mass, name, skin_color)
                VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
                """,
                results,
            )

            await db.commit()

    print(f"Загружено персонажей: {len(results)}")


if __name__ == "__main__":
    asyncio.run(main())