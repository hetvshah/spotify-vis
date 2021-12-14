"""
Final project: Spotify Visualization

Name: Hetvi Shah

PennKey: hetvis
"""

import spotipy
from spotipy.oauth2 import SpotifyClientCredentials

import json
import os

from dotenv import load_dotenv
load_dotenv()

from flask import Flask, flash, render_template, request, url_for, redirect

import matplotlib.pyplot as plt
import matplotlib
import numpy as np
import pandas as pd

matplotlib.use('agg')

# Flask constants
ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg'}
app = Flask(__name__)
app.secret_key = 'ax9o4klasi-0oakdn' 

# Spotify credentials
client_id=os.environ.get("client_id")
client_secret=os.environ.get("client_secret")

client_credentials_manager = SpotifyClientCredentials(client_id, client_secret)
sp = spotipy.Spotify(client_credentials_manager=client_credentials_manager)

class Artist:
    album = []
    track = []

    def __init__(self, artist):
        self.artist = artist

    def __str__(self):
        """ Pretty prints the Node's priority and value.
        """
        return "Artist: {}\nNumber of albums: {}\nNumber of tracks: {}".format(self.artist, len(album_results), len(track_ids))

    def get_albums(self):
        """ Requests a list of the artists albums

        Args:
            artist (str): the requested artist

        Returns:
            albums: all the albums and songs of this artist
        """
        #results = sp.search(q='artist:' + artist, type='artist')
        search_results = sp.search(self.artist,1,0,"artist")
        id = search_results['artists']['items'][0]['id']

        album_results = sp.artist_albums(id, limit=50)['items']

        track_names = set()
        track_ids = set()

        for album in album_results:
            album_id = album['id']
            album_name = album['name']

            track_results = sp.album_tracks(album_id)['items']

            for track in track_results:
                track_names.add(track['name'])
                track_ids.add(track['id'])

        album = album_results
        track = track_ids

        return list(track_ids)

    def get_track(self, id):
        """ 
        Args:
            id: a single id for a song

        Returns:
            features: list of features for this specific song
                (such as name, release date, album, length, danceability, energy, etc)
        """
        track = sp.track(id)
        audio_features = sp.audio_features(id)

        name = track['name']
        album = track['album']['name']
        artist = track['album']['artists'][0]['name']
        release_date = track['album']['release_date']
        length = track['duration_ms']
        popularity = track['popularity']

        acousticness = audio_features[0]['acousticness']
        danceability = audio_features[0]['danceability']
        energy = audio_features[0]['energy']
        instrumentalness = audio_features[0]['instrumentalness']
        liveness = audio_features[0]['liveness']
        loudness = audio_features[0]['loudness']
        speechiness = audio_features[0]['speechiness']
        tempo = audio_features[0]['tempo']
        time_signature = audio_features[0]['time_signature']

        track = [name, album, artist, release_date, length, popularity, danceability, acousticness, energy, instrumentalness, liveness, loudness, speechiness, tempo, time_signature]
        return track

    def data_vis(self, df):
        """ 
        Args:
            features: a list of a list of features for songs

        Returns:
            plots to display on the web 
        """
        # length
        plt.hist(df['length'], 50, facecolor='g', alpha=0.75)

        plt.xlabel('Length')
        plt.ylabel('Frequency Distribution')
        plt.title('Histogram of Length')

        plt.savefig('static/length.png')

        plt.clf()

        # popularity
        plt.hist(df['popularity'], 50, facecolor='g', alpha=0.75)

        plt.xlabel('Popularity')
        plt.ylabel('Frequency Distribution')
        plt.title('Histogram of Popularity')

        plt.savefig('static/popularity.png')

        plt.clf()

        # danceability
        plt.hist(df['danceability'], 50, facecolor='g', alpha=0.75)

        plt.xlabel('Danceability')
        plt.ylabel('Frequency Distribution')
        plt.title('Histogram of Danceability')

        plt.savefig('static/danceability.png')

        plt.clf()
        
        # acousticness
        plt.hist(df['acousticness'], 50, facecolor='g', alpha=0.75)

        plt.xlabel('Acousticness')
        plt.ylabel('Frequency Distribution')
        plt.title('Histogram of Acousticness')

        plt.savefig('static/acousticness.png')

        plt.clf()

        # energy
        plt.hist(df['energy'], 50, facecolor='g', alpha=0.75)

        plt.xlabel('Energy')
        plt.ylabel('Frequency Distribution')
        plt.title('Histogram of Energy')

        plt.savefig('static/energy.png')

        plt.clf()

        # instrumentalness
        plt.hist(df['instrumentalness'], 50, facecolor='g', alpha=0.75)

        plt.xlabel('Instrumentalness')
        plt.ylabel('Frequency Distribution')
        plt.title('Histogram of Instrumentalness')

        plt.savefig('static/instrumentalness.png')

        plt.clf()

        # liveness
        plt.hist(df['liveness'], 50, facecolor='g', alpha=0.75)

        plt.xlabel('Liveness')
        plt.ylabel('Frequency Distribution')
        plt.title('Histogram of Liveness')

        plt.savefig('static/liveness.png')

        plt.clf()

        # loudness
        plt.hist(df['loudness'], 50, facecolor='g', alpha=0.75)

        plt.xlabel('Loudness')
        plt.ylabel('Frequency Distribution')
        plt.title('Histogram of Loudness')

        plt.savefig('static/loudness.png')

        plt.clf()

        # speechiness
        plt.hist(df['speechiness'], 50, facecolor='g', alpha=0.75)

        plt.xlabel('Speechiness')
        plt.ylabel('Frequency Distribution')
        plt.title('Histogram of Speechiness')

        plt.savefig('static/speechiness.png')

        plt.clf()

        # tempo
        plt.hist(df['tempo'], 50, facecolor='g', alpha=0.75)

        plt.xlabel('Tempo')
        plt.ylabel('Frequency Distribution')
        plt.title('Histogram of Tempo')

        plt.savefig('static/tempo.png')

@app.route("/", methods=["GET", "POST"])
def home():
    """
    Display the home page to enter an artist and allow users to post

    Args:
        None

    Returns:
        Correct behavior for the GET and POST requests for "/"
    """
    if request.method == "GET":
        return render_template("home.html")
    elif request.method == "POST":
        artist = request.form.get("searchbar")

        search_results = sp.search(artist,1,0,"artist")

        if len(search_results['artists']['items']) == 0:
            flash("Please enter a valid artist.")
            return redirect("/")

        return redirect("/" + artist)

@app.route("/<artist>", methods=["GET"])
def render_vis(artist):
    """
    Method that handles the /{artist} route.

    The artist wanted should come as the query parameter

    Args:
        None

    Returns:
        Renders the /{artist} page correctly with data vis
    """

    artistObj = Artist(artist)

    tracks = []
    print(artist)
    track_ids = artistObj.get_albums()
    print("HI1")
    print(len(track_ids))
    for track_id in track_ids:
        tracks.append(artistObj.get_track(track_id))
    
    print("HI2")
    df = pd.DataFrame(tracks, columns = ['name', 'album', 'artist', 'release_date', 'length', 'popularity', 'danceability', 'acousticness', 'energy', 'instrumentalness', 'liveness', 'loudness', 'speechiness', 'tempo', 'time_signature'])

    artistObj.data_vis(df)

    return render_template("vis.html", artist=artist)

if __name__ == "__main__":
    app.run(port=5000, debug=True)