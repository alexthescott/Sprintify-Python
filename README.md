
# Sprintify: Designed for runners to filter Spotify playlists by BPM

The goal of this project is to allow a user to define a tempo floor and ceiling, filtering a playlist so that only songs within that range are kept. The user has the option to create a new playlist, or add to an exising one. 

# Getting Started

This project uses Python 2.7. You will need to install the Python dependency spotipy. The easiest way to do this is by using pip. If you have pip installed, type

$   pip install spotipy

To check if you currently have pip installed, type

$   pip -- version 

to check which version of pip you have installed. If you do not have pip installed, visit https://packaging.python.org/tutorials/installing-packages/#id13 for instructions on how to do so.

In order to run this program, you will need to create a Spotify developer account at https://developer.spotify.com/dashboard/login. Once you have done so, create a Client Id titled "Sprintify" for a Desktop App.
Within Sprintfy.py, you will need to replace: 
* Client ID
* Client Secret

With the values you have just created. This will pair you Spotify account with your instance of Srintify.py, and will let you create and add to playlists.

If you do not know your Spotify username, copy one of your existing Spotify playlist Uri's, and locate your username. Go to the Spotify desktop application, click the three dots, select share, then select "Copy Spotify URI." Your username is after "user:"

In order to run the program, type

$   Python Sprintify.py

# Example Gif
<img src="Sprintify_Example.gif" width="75%">

# To-Do
* Update project to Python 3
