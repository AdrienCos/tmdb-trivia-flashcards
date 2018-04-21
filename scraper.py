#!/usr/bin/python3

import json
import os
from urllib.request import urlopen
from urllib.parse import quote
from multiprocessing import Pool
import argparse
from time import sleep
from random import random

# Create the argparser
parser = argparse.ArgumentParser()
parser.add_argument("api_key", help="Your TMDb API Key")
parser.add_argument("csv_path", help="Path to the CSV file to use")
args = parser.parse_args()

# Create the work variables
api_key = args.api_key
csv_path = args.csv_path
base_image_url = "https://image.tmdb.org/t/p/w500"
pics_folder = "./pics/"
if not os.path.exists(pics_folder):
    os.mkdir(pics_folder)

def read_csv(csv_path=csv_path):
    """Given the path to a csv file, returns a list of dicts 
    containing the movie name and release year"""
    movies = []
    file = open(csv_path, "r")
    lines = file.read().split('\n')[1:-1]
    for line in lines:
        line = line.split("\t")
        movie = {}
        movie["name"] = line[1]
        movie["year"] = line[2]
        movies += [movie]
    return movies

def get_poster_url(name, api_key=api_key):
    """Given the name of a movie, returns the url of this movie's poster"""
    URL = "https://api.themoviedb.org/3/search/movie?api_key=%s&language=en-US&query=%s&page=1&include_adult=false"\
        % (api_key, name)
    # Sanitize the URL
    URL = quote(URL, ":=&/?")
    # Keep querying the API until we get an answer
    res = False
    while not res:
        try:
            print("Searching for the movie %s" % (name))
            response = urlopen(URL)
            res = True
        except:
            print("Error with movie %s" % name)
            sleep(random()*10)
    status = response.getcode()
    # print(status)
    html = response.read()
    data = json.loads(html)
    result_movie = data["results"][0]
    return result_movie["poster_path"]

def download_poster(movie, api_key=api_key, base_url=base_image_url, pics_folder=pics_folder):
    """ Given the dict of a movie (name, year), downloads the poster image"""
    name = movie["name"]
    poster_path = get_poster_url(name, api_key)
    filename = poster_path.split("/")[1]
    URL = base_url + poster_path
    response = urlopen(URL)
    status = response.getcode()
    # print(status)
    img = response.read()
    file = open(pics_folder + filename, "wb")
    file.write(img)
    file.close
    return filename

def worker(movie, api_key=api_key, base_url=base_image_url):
    """Worker function for parallelization of the downloads"""
    filename = download_poster(movie, api_key, base_url)
    name = movie["name"]
    year = movie ["year"]
    img_field = "<img src='%s' />\n" % filename
    card = "%s\t%s\t%s" % (name, year, img_field)
    return card

def scrape(csv_path=csv_path, api_key=api_key, base_url=base_image_url, pics_folder=pics_folder):
    """Given the path to a CSV file, downloads every poster image related to
    the movies in the file, and creates a new CSV file suited for Anki import"""
    movies = read_csv(csv_path)
    with Pool(10) as p:
        cards = p.map(worker, movies)
    output = open("cards.csv", "w")
    for card in cards:
        output.write(card)
    output.close()
    return len(movies)

if __name__ == '__main__':
    scrape()