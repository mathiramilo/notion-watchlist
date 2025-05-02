import requests
from bs4 import BeautifulSoup


def get_imdb_rating(imdb_id: str) -> float:
    url = f"https://www.imdb.com/title/{imdb_id}/"

    try:
        res = requests.get(
            url,
            headers={"User-Agent": "Mozilla/5.0"},
        )
        res.raise_for_status()
        soup = BeautifulSoup(res.text, "html.parser")

        rating_div = soup.find(
            "div", {"data-testid": "hero-rating-bar__aggregate-rating__score"}
        )
        if rating_div:
            span = rating_div.find("span")
            if span and span.text:
                try:
                    return float(span.text.strip()).__round__(1)
                except ValueError:
                    return None
        return None
    except Exception as e:
        print(f"Error fetching IMDb rating: {e}")
        return None
