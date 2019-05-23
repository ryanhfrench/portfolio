# Import packages
import datetime
import os
import csv
from io import StringIO
import pandas as pd
import requests
import sys
import spotipy
import spotipy.util as util
import time
import plotly.dashboard_objs as dashboard
import IPython.display
from IPython.display import Image
import pymysql
import mysql.connector

# Set Spotify credentials
CLIENT_ID = 'YOUR_CLIENT_ID_HERE'
CLIENT_SECRET = 'YOUR_CLIENT_SECRET_HERE'
username = 'YOUR_SPOTIFY_USERNAME_HERE'
token = util.prompt_for_user_token(username, 'playlist-modify-public', CLIENT_ID, CLIENT_SECRET, 'http://localhost')

# Function to create 'data' folder to store song information
def create_data_directory():
    # Get current path
    path = os.getcwd()
    # Attempt to create 'data' folder if one does not exist
    try:
        os.mkdir(path + '/data')
    except:
        print('Path already exists.')
    return path

# Function to get data for each day
def get_daily_data(day):
    daily_data = datetime.date.today() + datetime.timedelta(days = -day)
    daily_data = daily_data.strftime("%Y-%m-%d")
    return daily_data

# Function to build URL to access Spotify data
def get_url(daily_data):
    # Set general URL parameters
    url_prefix = 'https://spotifycharts.com/regional/global/daily/'
    url_suffix = '/download'

    # Create URL to get data from date and URL prefix/suffix
    url = url_prefix + daily_data + url_suffix
    return url

# Function to pull down Spotify song data
def get_songs(url, daily_data):
    # Request song data using custom URL
    headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/56.0.2924.76 Safari/537.36'}
    request = requests.get(url, headers = headers).text
    # Create data frame from requested data
    songs = pd.read_csv(StringIO(request), sep = ',', header = 1)
    # Add date column to database with date of chart
    songs.insert(0, 'date', daily_data)
    # Initialize empty array to collect song information
    ID = []
    for i in songs['URL']:
        ID.append((i[-22:]))
    songs['ID'] = ID
    # Create data frame from collected songs
    songs = pd.DataFrame(songs)
    return songs

# Function to pull down audio features for each of the Spotify songs
def get_audio_features(songs):
    # Check for token and pull down audio features for each song collected
    if token:
        sp = spotipy.Spotify(auth = token)
        results_1 = sp.audio_features(tracks = songs['ID'][:51])
        results_2 = sp.audio_features(tracks = songs['ID'][51:101])
        results_3 = sp.audio_features(tracks = songs['ID'][101:151])
        results_4 = sp.audio_features(tracks = songs['ID'][151:201])
        results = results_1 + results_2 + results_3 + results_4
        audio_features = pd.DataFrame(results)
        # Remove unneeded columns after call
        drop_cols = ['id', 'type']
        audio_features = audio_features.drop(drop_cols, 1)
    else:
        print('Cant get token for', username)
    # Add song features to original data frame of songs
    songs_and_features = pd.concat([songs.reset_index(drop = True), audio_features], axis = 1)
    return songs_and_features

# Function to create composite primary key from song ID and date of download
def create_primary_key(songs_and_features):
    primary_key = []
    i = 0
    while i < len(songs_and_features['ID']):
        primary_key.append(songs_and_features['ID'][i] + '_' + songs_and_features['date'][i])
        i += 1
    songs_and_features.insert(0, 'primary_key', primary_key)
    return songs_and_features

# Function to create database to retain Spotify data
def create_db():
    try:
        # Set parameters for SQL data base
        db = pymysql.connect(host = 'localhost',
                               user = 'root',
                               passwd = 'toortoor')
        # Initialize cursor
        cursor = db.cursor()
        cursor.execute('CREATE DATABASE spotify_data')
    except:
        print('Database already exists or could not be created.')

def create_schema():
    try:
        # Set parameters for SQL data base
        db = pymysql.connect(host = 'localhost',
                               user = 'root',
                               passwd = 'toortoor',
                               db = 'spotify_data')
        # Initialize cursor
        cursor = db.cursor()
        cursor.execute('CREATE TABLE songs_and_features_db (primary_key VARCHAR(255), date_of_chart DATETIME, Position INTEGER(10), Track_Name VARCHAR(255), Artist VARCHAR(255), Streams INTEGER(15), URL VARCHAR(255), ID VARCHAR(255), acousticness DECIMAL(6, 5), analysis_url VARCHAR(255), danceability DECIMAL(6, 5), duration_ms INTEGER(10), energy DECIMAL(6, 5), instrumentalness DECIMAL(11, 10), song_key INTEGER(10), liveness DECIMAL(6, 5), loudness DECIMAL(7, 5), mode INTEGER(10), speechiness DECIMAL(6, 5), tempo DECIMAL(8, 5), time_signature INTEGER(10), track_href VARCHAR(255), uri VARCHAR(255), valence DECIMAL(6, 5), PRIMARY KEY (primary_key))')
        cursor.execute('ALTER TABLE spotify_data.songs_and_features_db CONVERT TO CHARACTER SET UTF8MB3;')
    except:
        print('Database already exists or could not be created.')

# Function to export CSV to data base
def export_to_db(csv_path):
    # Open created .CSV file
    csv_data = csv.reader(open(csv_path, encoding = 'utf8'))
    # Connect to SQL server
    db = pymysql.connect(host = 'localhost',
                           user = 'root',
                           passwd = 'toortoor',
                           db = 'spotify_data')
    # Initialize cursor
    cursor = db.cursor()
    row_count = 0
    # Add data frame information to SQL server
    row_count = 0
    for row in csv_data:
        if row_count != 0:
            try:
                cursor.execute('INSERT IGNORE INTO spotify_data.songs_and_features_db(primary_key, date_of_chart, Position, Track_Name, Artist, Streams, URL, ID, acousticness, analysis_url, danceability, duration_ms, energy, instrumentalness, song_key, liveness, loudness, mode, speechiness, tempo, time_signature, track_href, uri, valence) VALUES(%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s);', (row))
            except pymysql.IntegrityError:
                print('Entry is either a duplicate or could not be created.')
        row_count += 1
    # Commit changes to SQL server and close connection
    db.commit()
    cursor.close()

# Execute functions
# Create 'data' folder to store .CSV Spotify data
path = create_data_directory()
# Create SQL database
create_db()
# Create SQL schema
create_schema()
# Get Spotify data and related audio features for the past month
day = 2
while day <= 31:
    daily_data = get_daily_data(day)
    url = get_url(daily_data)
    songs = get_songs(url, daily_data)
    songs_and_features = get_audio_features(songs)
    songs_and_features = create_primary_key(songs_and_features)
    # Save resulting data frame as a .CSV file
    csv_path = path + '/data/spotify_top_200_' + daily_data + '.csv'
    songs_and_features.to_csv(r'' + csv_path, index = False)
    # Export resulting data to SQL server
    export_to_db(csv_path)
    time.sleep(3)
    day += 1
