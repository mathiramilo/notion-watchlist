from setuptools import find_packages, setup

setup(
    name="notion-watchlist",
    version="0.2.0",
    description="CLI tool for automating your movie & TV watchlist in Notion via TMDB and IMDb",
    author="Mathias Ramilo",
    author_email="mathiramilo2290@gmail.com",
    url="https://github.com/mathiramilo/notion-watchlist",
    py_modules=["main", "notion", "scraper", "tmdb"],
    package_dir={"": "src"},
    install_requires=[
        "requests>=2.25.1",
        "notion-client>=0.3.0",
        "pyyaml>=5.4.1",
        "beautifulsoup4>=4.9.3",
    ],
    entry_points={
        "console_scripts": [
            "notion-watchlist=main:main",
        ],
    },
)
