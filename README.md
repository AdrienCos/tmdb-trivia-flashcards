# tmdb-trivia-flashcards
Scraper for the TMDb website to create Anki trivia flashcards based on a given list of movies.
As of now the scraper has only been tested on a CSV file from [Letterboxd](https://letterboxd.com).

# Use
## CSV requirements
The CSV in which the film posters to download are must follow the pattern:

| Unused column | Movie Title | Year of Release | Unused column |
|:---:|:---:|:---:|:---:|
| _ | Movie 1 | 2015 | _ |
| _ | Movie 2 | 1996 | _ |
| _ | Movie 3 | 1984 | _ |

Note that the file is assumed to have a header row.

## Running the scraper
From a terminal, run 

`python3 scraper.py api_key path_to_csv`

The poster images will be downloaded in a folder named `pics/`, where `scraper.py` is. 
A file named `cards.csv` will be created, it contains the following informations:

| Movie title | Year of Release | HTML img with the filename |
|:---:|:---:|:---:|
| Movie 1 | 2015 | `<img src="movie_1_poster.jpg" />` |
| Movie 2 | 1996 | `<img src="movie_2_poster.jpg" />` |
| Movie 3 | 1984 | `<img src="movie_3_poster.jpg" />` |

Note that the file does not have a header row.

# Credits
This product uses the TMDb API but is not endorsed or certified by TMDb

<a href="https://www.themoviedb.org/"><img src="https://www.themoviedb.org/static_cache/v4/logos/408x161-powered-by-rectangle-green-bb4301c10ddc749b4e79463811a68afebeae66ef43d17bcfd8ff0e60ded7ce99.png" alt="TMDb Logo" width= 160px/></a>
