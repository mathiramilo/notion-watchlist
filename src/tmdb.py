import requests


def fetch_tmdb_item(name: str, media_type: str, api_key: str) -> dict:
    url = f"https://api.themoviedb.org/3/search/{media_type}"
    params = {"query": name}
    headers = {"Authorization": f"Bearer {api_key}"}

    res = requests.get(url, params=params, headers=headers)
    res.raise_for_status()

    results = res.json().get("results", [])
    if not results:
        raise ValueError(f"No {media_type} found with name '{name}'")
    return results[0]


def get_details(item_id: int, media_type: str, api_key: str) -> dict:
    url = f"https://api.themoviedb.org/3/{media_type}/{item_id}"
    headers = {"Authorization": f"Bearer {api_key}"}
    res = requests.get(url, headers=headers)
    res.raise_for_status()
    return res.json()


def get_streaming_platforms(item_id: int, media_type: str, api_key: str) -> list:
    url = f"https://api.themoviedb.org/3/{media_type}/{item_id}/watch/providers"
    headers = {"Authorization": f"Bearer {api_key}"}
    res = requests.get(url, headers=headers)
    res.raise_for_status()
    return res.json().get("results", {}).get("UY", {}).get("flatrate", [])


def get_external_ids(item_id: int, media_type: str, api_key: str) -> dict:
    url = f"https://api.themoviedb.org/3/{media_type}/{item_id}/external_ids"
    headers = {"Authorization": f"Bearer {api_key}"}
    res = requests.get(url, headers=headers)
    res.raise_for_status()
    return res.json()


def get_duration(runtime: int) -> str:
    if runtime is None:
        return "N/A"
    hours = runtime // 60
    minutes = runtime % 60
    return f"{hours}h {minutes}m"
