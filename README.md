# Notion Watchlist

## Description

This is a python script that allows you to create a watchlist in Notion. It uses the Notion API to add items in your watchlist. The script is designed to be run from the command line.

## Requirements

- Python 3.8 or higher
- TMDB API key
- Notion account
- Notion page created for the watchlist

## Usage Guide

### Setup

1. Get a TMDB API key. Follow the instructions [here](https://developer.themoviedb.org/docs/authentication-application).
2. Create a Notion integration and get the token. Follow the instructions [here](https://developers.notion.com/docs/create-a-notion-integration).
3. Create a Notion page where you want to add the watchlist. Follow the instructions [here](https://www.notion.com/help/guides/creating-a-page).
4. Add connection to the Notion page. Follow the instructions [here](https://www.notion.com/help/add-and-manage-connections-with-the-api).

### Install `notion-watchlist`

#### Linux/MacOS

1. Install pipx
   ```bash
   brew install pipx
   pipx ensurepath
   exec $SHELL
   ```
2. Install `notion-watchlist`
   ```bash
   pipx install notion-watchlist
   ```

#### Windows

> [!NOTE]
> We're working on a Windows version. For now, you can use WSL or run the script in a virtual environment.

### Tutorial

1. Execute the script
   ```bash
   notion-watchlist <Movie/TV Show Name>
   ```
2. Enter the TMDB API key
   ```bash
   Enter your TMDB API key: <your_tmdb_api_key>
   ```
3. Enter the Notion token
   ```bash
    Enter your Notion token: <your_notion_token>
   ```
4. Enter the Notion page name
   ```bash
     Enter your Notion page name: <your_notion_page_name>
   ```
5. Key, token and page name are saved in the config file. You can use the script without entering them again.
6. Read the script instructions for more options.
   ```bash
   notion-watchlist --help
   ```

### Examples

1. Add a movie to the watchlist
   ```bash
   notion-watchlist "Inception"
   ```
2. Add a TV show to the watchlist
   ```bash
   notion-watchlist -t tv "Breaking Bad"
   ```

## Command-Line Arguments

| Argument           | Alias | Type          | Description                                                                          | Default      |
| ------------------ | ----- | ------------- | ------------------------------------------------------------------------------------ | ------------ |
| `name`             | —     | _positional_  | Name of the movie or TV show to add                                                  | _n/a_        |
| `-h`, `--help`     | —     | _flag_        | Show help message and exit                                                           | —            |
| `-v`, `--version`  | —     | _flag_        | Show script version and exit                                                         | —            |
| `-t`, `--type`     | —     | `movie \| tv` | Specify whether the title is a movie or TV show                                      | `movie`      |
| `--tmdb-key`       | —     | _string_      | TMDB API key (overrides stored key in `config.yaml`)                                 | stored value |
| `--notion-token`   | —     | _string_      | Notion integration token (overrides stored token in `config.yaml`)                   | stored value |
| `--page-name`      | —     | _string_      | Name of the Notion parent page where “Movies”/“TV Shows” DBs live (overrides config) | stored value |
| `-r`, `--recreate` | —     | _flag_        | Force re-creation of the Notion databases even if IDs are cached                     | `false`      |

## Notion Page Tips

### Turn into Inline Database

Press right-click on the database and select **_"Turn into inline database"_**. This will allow you to add the database to any page in Notion.
