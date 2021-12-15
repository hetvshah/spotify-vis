# Spotify Data Visualization

Enter an artist and see their data (danceability, energy, popularity, acousticness, etc) on their tracks visualized

<img width="1676" alt="Screen Shot 2021-12-14 at 8 50 15 PM" src="https://user-images.githubusercontent.com/68198839/146108200-3eec29fe-7b6f-445c-8d51-41289ee9f12e.png">

Built with Python (Flask, Matplotlib, Pandas)

### Data

All the data for each artist is taken from the Spotify API via Spotipy.

*Note:* It takes some time for the data to load, especially for larger, well-known artists.

### Implementation Requirements

- [x] One class definition (Artist class)
- [x] Two dunder methods (str, init)
- [x] One first-party module (os)
- [x] Two third-party modules (flask, matplotlib, pandas)
- [x] In-line documentation

### Description of Code Structure

The Artist class defines the artist and a list of their albums and tracks. The user is asked to input an artist on the "/" route, which will redirect to "/{artist}" if the artist they entered is valid. This route will search the artist in the Spotify library, retrieve their albums, and the tracks in these albums. Data regarding each track is retrieved, and Matplotlib is used to visualize this data. The code is broken into each route, data retrieval, and data visualization.

### Instructions to Run

To run, download the code. Create a .env file, get Spotify credentials, and put the client_id and client_secret in there. Run python3 spotify-vis.py in the root directory—this will open a local server where you can then interact with the frontend.
