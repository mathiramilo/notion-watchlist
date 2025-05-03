from notion_client import Client

from scraper import get_imdb_rating
from tmdb import get_details, get_duration, get_external_ids, get_streaming_platforms


def get_page_id(notion: Client, title: str) -> str:
    res = notion.search(query=title, filter={"property": "object", "value": "page"})
    for r in res.get("results", []):
        props = r.get("properties", {}).get("title", {}).get("title", [])
        if props and props[0].get("text", {}).get("content") == title:
            return r["id"]
    raise ValueError(
        f"No Notion page found with title '{title}'. Please create it first."
    )


def get_or_create_movies_database(
    notion: Client, page_id: str, title: str
) -> str:
    res = notion.search(
        **{"query": title, "filter": {"property": "object", "value": "database"}}
    )

    for r in res.get("results", []):
        props = r.get("title", [])
        if props and props[0]["text"]["content"] == title:
            return r["id"]

    props = {
        "Title": {"title": {}},
        "Genres": {
            "multi_select": {
                "options": [
                    {"name": "Action", "color": "red"},
                    {"name": "Comedy", "color": "yellow"},
                    {"name": "Drama", "color": "blue"},
                    {"name": "Fantasy", "color": "green"},
                    {"name": "Horror", "color": "purple"},
                    {"name": "Romance", "color": "pink"},
                    {"name": "Sci-Fi", "color": "orange"},
                    {"name": "Thriller", "color": "gray"},
                ]
            }
        },
        "Status": {
            "select": {
                "options": [
                    {"name": "Want to Watch", "color": "gray"},
                    {"name": "Watching", "color": "blue"},
                    {"name": "Watched", "color": "green"},
                ]
            }
        },
        "Release Year": {"number": {}},
        "Duration": {"rich_text": {}},
        "Movie Status": {
            "select": {
                "options": [
                    {"name": "Released", "color": "green"},
                    {"name": "Post Production", "color": "purple"},
                    {"name": "In Production", "color": "blue"},
                    {"name": "Canceled", "color": "red"},
                ]
            }
        },
        "Rating": {"number": {}},
        "IMDB Rating": {"number": {}},
        "Streaming Platforms": {
            "multi_select": {
                "options": [
                    {"name": "Netflix", "color": "red"},
                    {"name": "Amazon Prime Video", "color": "blue"},
                    {"name": "Disney+", "color": "orange"},
                    {"name": "Max", "color": "purple"},
                    {"name": "Apple TV+", "color": "gray"},
                ]
            }
        },
    }

    db = notion.databases.create(
        parent={"page_id": page_id},
        title=[{"type": "text", "text": {"content": title}}],
        properties=props,
    )

    return db["id"]


def get_or_create_tv_database(notion: Client, page_id: str, title: str) -> str:
    res = notion.search(
        **{"query": title, "filter": {"property": "object", "value": "database"}}
    )

    for r in res.get("results", []):
        props = r.get("title", [])
        if props and props[0]["text"]["content"] == title:
            return r["id"]

    props = {
        "Name": {"title": {}},
        "Genres": {
            "multi_select": {
                "options": [
                    {"name": "Action", "color": "red"},
                    {"name": "Comedy", "color": "yellow"},
                    {"name": "Drama", "color": "blue"},
                    {"name": "Fantasy", "color": "green"},
                    {"name": "Horror", "color": "purple"},
                    {"name": "Romance", "color": "pink"},
                    {"name": "Sci-Fi", "color": "orange"},
                    {"name": "Thriller", "color": "gray"},
                ]
            }
        },
        "Status": {
            "select": {
                "options": [
                    {"name": "Want to Watch", "color": "gray"},
                    {"name": "Watching", "color": "blue"},
                    {"name": "Watched", "color": "green"},
                ]
            }
        },
        "Airing Period": {"rich_text": {}},
        "Seasons": {"number": {}},
        "Show Status": {
            "select": {
                "options": [
                    {"name": "Ended", "color": "green"},
                    {"name": "Returning Series", "color": "blue"},
                    {"name": "Canceled", "color": "red"},
                ]
            }
        },
        "Progress": {"rich_text": {}},
        "Rating": {"number": {}},
        "IMDB Rating": {"number": {}},
        "Streaming Platforms": {
            "multi_select": {
                "options": [
                    {"name": "Netflix", "color": "red"},
                    {"name": "Amazon Prime Video", "color": "blue"},
                    {"name": "Disney+", "color": "orange"},
                    {"name": "Max", "color": "purple"},
                    {"name": "Apple TV+", "color": "gray"},
                ]
            }
        },
    }

    db = notion.databases.create(
        parent={"page_id": page_id},
        title=[{"type": "text", "text": {"content": title}}],
        properties=props,
    )

    return db["id"]


def page_exists(notion: Client, database_id: str, title: str) -> bool:
    res = notion.databases.query(
        database_id=database_id,
        filter={"property": "Title", "title": {"equals": title}},
    )
    return bool(res.get("results"))


def create_movie_page(notion: Client, database_id: str, item: dict, api_key: str):
    details = get_details(item["id"], "movie", api_key)
    watch_providers = get_streaming_platforms(item["id"], "movie", api_key)

    title = details.get("title")
    genres = [genre["name"] for genre in details.get("genres", [])]
    release_year = int(details.get("release_date").split("-")[0])
    duration = get_duration(details.get("runtime"))
    movie_status = details.get("status", "Unknown")
    imdb_rating = get_imdb_rating(details.get("imdb_id"))

    streaming_platforms = [
        {"name": provider["provider_name"]} for provider in watch_providers
    ]
    props = {
        "Title": {"title": [{"text": {"content": title}}]},
        "Genres": {"multi_select": [{"name": genre} for genre in genres]},
        "Status": {"select": {"name": "Want to Watch"}},
        "Release Year": {"number": release_year},
        "Duration": {"rich_text": [{"text": {"content": duration}}]},
        "Movie Status": {"select": {"name": movie_status}},
        "Rating": {"number": None},
        "IMDB Rating": {"number": imdb_rating},
        "Streaming Platforms": {"multi_select": streaming_platforms},
    }
    notion.pages.create(parent={"database_id": database_id}, properties=props)


def create_tv_page(notion: Client, database_id: str, item: dict, api_key: str):
    details = get_details(item["id"], "tv", api_key)
    watch_providers = get_streaming_platforms(item["id"], "tv", api_key)
    external_ids = get_external_ids(item["id"], "tv", api_key)

    title = details.get("name")
    genres = [genre["name"] for genre in details.get("genres", [])]
    release_year = int(details.get("first_air_date").split("-")[0])
    last_air_year = int(details.get("last_air_date").split("-")[0])
    seasons = details.get("number_of_seasons", 0)
    show_status = details.get("status", "Unknown")
    imdb_rating = get_imdb_rating(external_ids.get("imdb_id"))

    airing_period = f"{release_year}—{last_air_year}" if show_status in ["Ended", "Canceled"] else f"{release_year}—"

    streaming_platforms = [
        {"name": provider["provider_name"]} for provider in watch_providers
    ]
    props = {
        "Name": {"title": [{"text": {"content": title}}]},
        "Genres": {"multi_select": [{"name": genre} for genre in genres]},
        "Status": {"select": {"name": "Want to Watch"}},
        "Airing Period": {"rich_text": [{"text": {"content": airing_period}}]},
        "Seasons": {"number": seasons},
        "Progress": {"rich_text": [{"text": {"content": ""}}]},
        "Show Status": {"select": {"name": show_status}},
        "Rating": {"number": None},
        "IMDB Rating": {"number": imdb_rating},
        "Streaming Platforms": {"multi_select": streaming_platforms},
    }
    notion.pages.create(parent={"database_id": database_id}, properties=props)
