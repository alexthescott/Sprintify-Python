"""
Spotipy.py for Python 3
Alex Scott
October 2018 - June 2019
Run faster
"""

import sys
import spotipy
import spotipy.util as util
import json
import SprintifyHelper

# Create Spotify Object --------------------------------------------------------------------------

# Ask for Spotify Username 
username = input('Enter Spotify Username:')

# Create @ https://developer.spotify.com/dashboard/login
client_id = ''
client_secret = ''
redirect_uri = 'http://www.google.com/'

# Assign scope and creates token for Spotipy object
scope = "playlist-modify-public"
token = util.prompt_for_user_token(username, scope, client_id, client_secret, redirect_uri)

# Create Spotify Object
sp = spotipy.Spotify(auth=token)

# Create Playlist Object
playlists = sp.user_playlists(username)

# Main -------------------------------------------------------------------------------------------

pId = [] 
pTitles = []
pLength = []
pCount = 0

# Assume 1st is a placeholder to avoid list off by one error
pId.append('NULL')
pTitles.append('NULL')
pLength.append(0)

while playlists:
	for i, playlist in enumerate(playlists['items']):
	    pTitles.append(playlist['name'])
	    pLength.append(playlist['tracks']['total'])
	    pId.append(playlist['id'])
	    pCount += 1
	if playlists['next']:
		playlists = sp.next(playlists)
	else:
		playlists = None

print("")
filterOrGenerate = SprintifyHelper.get_generate_or_filter()

# Filter Path 
if filterOrGenerate == 'E':
	SprintifyHelper.print_user_playlist(username, sp)

	# Record User's Playlist Choice
	choiceP1 = SprintifyHelper.get_playlist_choice(pCount)

	print("")
	print("Tempo Range")
	print("-----------")

	# Record User's tempoFloor
	tempoFloor = SprintifyHelper.get_tempo_floor()

	# Record User's tempoCeiling
	tempoCeiling = SprintifyHelper.get_tempo_ceiling(tempoFloor)

	# Respond to Choice
	print("")
	print("Analyzing " + pTitles[choiceP1] + " Playlist:")

	# Analyize and use Choice
	pUriArray = SprintifyHelper.get_playlist_tracks(username, pId[choiceP1], tempoFloor, tempoCeiling, pLength[choiceP1], sp)

	print("\n")
	percentInRange = len(pUriArray)/float(pLength[choiceP1]) * 100
	print('%.2f'%percentInRange + "% of songs in " + pTitles[choiceP1] + " are in the range " + str(tempoFloor) + "-" + str(tempoCeiling) + (" (BPM)"))
	print("")

	newPlaylistName = str(pTitles[choiceP1]) + " (" + str(tempoFloor) + "-" + str(tempoCeiling) + " BPM)"

# Generate Path
elif filterOrGenerate == 'G':
	print("")
	print("Spotipyv.01.py will output a playlist within a BPM")
	print("")
	print("Tempo Range")
	print("-----------")

	# Record User's tempoFloor
	tempoFloor = SprintifyHelper.get_tempo_floor()

	# Record User's tempoCeiling
	tempoCeiling = SprintifyHelper.get_tempo_ceiling(tempoFloor)

	# Record User's prefered playlist length
	gLength = SprintifyHelper.get_generate_length()

	# Record User's Playlist Choice
	songChoice = SprintifyHelper.get_song_uri()

	# Obtain list of song URIS from prompt function
	tUriArray = SprintifyHelper.get_generated_list_uri(gLength, songChoice, tempoFloor, tempoCeiling, sp)

	tempFirstTrack = sp.track(tUriArray[0])
	tempArtistId = tempFirstTrack['artists'][0]['uri']
	tempArtist = sp.artist(tempArtistId)
	tempArtistGenre = tempArtist['genres']

	pUriArray = []

	for tempUri in tUriArray: 
		pUriArray.append([tempUri[14:]])

	if len(tempArtistGenre) == 0:
		newPlaylistName = "Sprintify (" + str(tempoFloor) + '-' + str(tempoCeiling) + ")"
	else:
		newPlaylistName = str(tempArtistGenre[0]) + " (" + str(tempoFloor) + '-' + str(tempoCeiling) + " BPM)"

# Prompt 'N' or 'E'
choiceNE = SprintifyHelper.get_new_or_existing(pUriArray)


# Add songs to a new playlist
if choiceNE.upper() == 'N':
	playlists = sp.user_playlist_create(username, newPlaylistName, public = True)
	newPlaylistUri = json.dumps(playlists['id'], indent = 4)
	print("Adding songs to " + newPlaylistName)
	for tempUri in pUriArray:
		sp.user_playlist_add_tracks(username, newPlaylistUri[1:-1], tempUri)
	print("Successfully added " + str(len(pUriArray)) + " songs to " + newPlaylistName)

# Add songs to an existing playlist
else: 
	SprintifyHelper.print_user_playlist(username, sp)
	print("")
	print("Chose a playlist you would like to add the " + str(len(pUriArray)) + " songs")

	# Record User's Playlist Choice 2nd time
	while True:
		choiceP2 = input('Enter Playlist Number: ')
		if choiceP2.isdigit() and float(choiceP2) > 0 and float(choiceP2) <= pCount:
			choiceP2 = int(choiceP2)
			break
		else:
			print("Incorrect input. Please enter a positive number within range")
	print("Adding songs to " + pTitles[choiceP2])
	for tempUri in pUriArray:
		sp.user_playlist_add_tracks(username, pId[choiceP2], tempUri)
	print("Successfully added " + str(len(pUriArray)) + " songs to " + pTitles[choiceP2])