
# Sprintify: Designed for runners to create BPM oriented Spotify playlists 

Sprintify allow users to define a BPM floor and ceiling, filtering a Spotify playlist so songs within range are kept. Additionally, Sprintify allows users to generate a new playlist. This is accomplished by obtaining song recommendations based on a song seed, which is then filtered by BPM. For both features, users can create a new playlist, or add to one they've already made.

# Getting Started

This project uses Python 2.7. You will need to install the Python dependency spotipy. The easiest way to do this is by using pip. If you do not have pip installed, you can try bootstrap it from the standard library by typing:

```bash
python -m ensurepip --default-pip
```
To check if you currently have pip installed, type:
```bash
pip --version 
```
If you have pip installed, type:
```bash
pip install spotipy
```
Visit https://packaging.python.org/tutorials/installing-packages/#id13 if you have furthur issues. 

In order to run this program, you will need to create a Spotify developer account at https://developer.spotify.com/dashboard/login. Once you have done so, create a Client Id titled "Sprintify" for a Desktop App.
By doing so, you will have created: 
* Client ID
* Client Secret

Open Sprintify.py, and enter your newly created Client ID and Client Secret. This will pair you Spotify account with your instance of Sprintify.py, and will let you create and add to your playlists.

If you do not know your Spotify username, copy one of your existing Spotify playlist Uri's, and locate your username. Go to the Spotify desktop application, click the three dots, select share, then select "Copy Spotify URI." Your username is after "user:"

In order to run the program, type:
```bash
Python Sprintify.py
```
# Filter Existing Playlist
<img src="Sprintify_Example1.gif">

# Generate Playlist
<img src="Sprintify_Example2.gif">

# Spotipy
https://github.com/plamere/spotipy/blob/master/docs/index.rst

https://spotipy.readthedocs.io/en/latest/
