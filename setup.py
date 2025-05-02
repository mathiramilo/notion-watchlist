from setuptools import setup

setup(
    name="tmdb-to-notion",
    version="0.1.0",
    py_modules=["tmdb_to_notion"],
    install_requires=["requests", "notion-client", "pyyaml", "setuptools"],
    entry_points={
        "console_scripts": [
            "tmdb-to-notion=tmdb_to_notion:main",
        ],
    },
)
