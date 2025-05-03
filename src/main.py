import argparse
import os

import yaml
from notion_client import Client

from notion import (
    create_movie_page,
    create_tv_page,
    get_or_create_movies_database,
    get_or_create_tv_database,
    get_parent_page_id,
    page_exists,
)
from tmdb import fetch_tmdb_item

CONFIG_PATH = os.path.join(os.path.dirname(__file__), "../config.yaml")


def load_config():
    if os.path.exists(CONFIG_PATH):
        try:
            with open(CONFIG_PATH, "r") as f:
                return yaml.safe_load(f) or {}
        except Exception as e:
            pass
    return {}


def save_config(config):
    os.makedirs(os.path.dirname(CONFIG_PATH), exist_ok=True)
    with open(CONFIG_PATH, "w") as f:
        yaml.safe_dump(config, f)


def prompt_once(config, key, prompt):
    if key not in config or not config[key]:
        value = input(prompt).strip()
        config[key] = value
        save_config(config)
    return config[key]


def main():
    config = load_config()

    tmdb_key = prompt_once(config, "TMDB_API_KEY", "Enter your TMDB API key: ")
    notion_token = prompt_once(
        config, "NOTION_TOKEN", "Enter your Notion integration token: "
    )
    parent_page_name = prompt_once(
        config, "NOTION_PARENT_PAGE_NAME", "Enter the name of the Notion parent page: "
    )

    notion = Client(auth=notion_token)

    parser = argparse.ArgumentParser(
        description="Fetch TMDB data and create a Notion page for a movie or TV show"
    )
    parser.add_argument("name", help="Name of the movie or TV show")
    parser.add_argument(
        "--type",
        choices=["movie", "tv"],
        default="movie",
        help="Specify 'movie' or 'tv' to differentiate the API endpoint",
    )
    parser.add_argument(
        "--tmdb-key",
        default=tmdb_key,
        help="TMDB API key (overrides the one in config)",
    )
    parser.add_argument(
        "--notion-token",
        default=notion_token,
        help="Notion integration token (overrides the one in config)",
    )
    parser.add_argument(
        "--parent-page-name",
        default=parent_page_name,
        help="Name of the Notion parent page (overrides the one in config)",
    )
    parser.add_argument(
        "--recreate",
        action="store_true",
        help="Force re-creation of the Notion databases",
    )
    args = parser.parse_args()

    if args.tmdb_key:
        config["TMDB_API_KEY"] = args.tmdb_key
        save_config(config)
    if args.notion_token:
        config["NOTION_TOKEN"] = args.notion_token
        save_config(config)
    if args.parent_page_name:
        config["NOTION_PARENT_PAGE_NAME"] = args.parent_page_name
        save_config(config)
    if args.recreate:
        config.pop("NOTION_MOVIES_DB_ID", None)
        config.pop("NOTION_TV_DB_ID", None)
        save_config(config)

    parent_page_id = get_parent_page_id(notion, parent_page_name)
    config["NOTION_PARENT_PAGE_ID"] = parent_page_id
    save_config(config)

    if "NOTION_MOVIES_DB_ID" not in config or not config["NOTION_MOVIES_DB_ID"]:
        config["NOTION_MOVIES_DB_ID"] = get_or_create_movies_database(
            notion, parent_page_id, "Movies"
        )
        save_config(config)
    if "NOTION_TV_DB_ID" not in config or not config["NOTION_TV_DB_ID"]:
        config["NOTION_TV_DB_ID"] = get_or_create_tv_database(
            notion, parent_page_id, "TV Shows"
        )
        save_config(config)

    movies_db = config["NOTION_MOVIES_DB_ID"]
    tv_db = config["NOTION_TV_DB_ID"]

    item = fetch_tmdb_item(args.name, args.type, tmdb_key)

    if page_exists(notion, movies_db, item.get("title") or item.get("name")):
        print(f"Page for {item.get('title') or item.get('name')} already exists.")
        return

    if args.type == "movie":
        create_movie_page(notion, movies_db, item, tmdb_key)
        print(f"Created page for movie: {item.get('title')} in Notion.")
    else:
        create_tv_page(notion, tv_db, item, tmdb_key)
        print(f"Created page for TV show: {item.get('name')} in Notion.")


if __name__ == "__main__":
    main()
