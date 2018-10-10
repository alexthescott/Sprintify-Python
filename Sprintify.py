"""
Spotipy.py for Python 2.7
Alexander Scott
October 2018
Written to find songs in a playlist that are in a tempo range 
"""

import sys
import spotipy
import spotipy.util as util
import json

# Create Spotify Object --------------------------------------------------------------------------

# Ask for Spotify Username 
#username = raw_input('Enter Spotify Username:')
username = 'bassguitar1234'

client_id = '0a6e845a19894708aadf65a22c4554e2'
client_secret = '056e4729129e4b35ac82ab808a5fff67'
redirect_uri = 'http://www.google.com/'

# Assign scope and creates token for Spotipy object
scope = "playlist-modify-private"
token = util.prompt_for_user_token(username, scope, client_id, client_secret, redirect_uri)

# Create Spotify Object
sp = spotipy.Spotify(auth=token, requests_timeout=20)

# Create Playlist Object
playlists = sp.user_playlists(username)

# Functions --------------------------------------------------------------------------------------

# Prints the BPM bounded tracks found in the 100 item page
# Fills uriArray with uri's of the bounded tracks
def show_tracks(results, a, low, high, total, uriArray):
	twentyPercent = int(total/5)
	twentyDone = False
	fourtyPercent = twentyPercent * 2
	fourtyDone = False
	sixtyPercent = fourtyPercent + twentyPercent
	sixtyDone = False
	eightyPercent = sixtyPercent + twentyPercent
	eightyDone = False

	for i, item in enumerate(results['items']):
		track = item['track']
		tempTitle = track['name']
		tempArtist = json.dumps(track['artists'][0]['name'])
		tempUri = []
		tempUri.append(track['uri'])
		tempFeature = sp.audio_features(tempUri)
		tempBPM = float(json.dumps(tempFeature[0]['tempo']))
		tempCurrent = a * 100 + i

		if twentyDone == False and tempCurrent == twentyPercent:
			print("")
			print("20% Complete")
			print("------------")
			twentyDone = True 

		elif fourtyDone == False and tempCurrent == fourtyPercent:
			print("")
			print("40% Complete")
			print("------------")
			fourtyDone = True 

		elif sixtyDone == False and tempCurrent == sixtyPercent:
			print("")
			print("60% Complete")
			print("------------")
			sixtyDone = True

		elif eightyDone == False and tempCurrent == eightyPercent:
			print("")
			print("80% Complete")
			print("------------")
			eightyDone = True

		if float(tempBPM) >= float(low) and float(tempBPM) <= float(high):
			uriArray.append(tempUri)
			songQuotation = '"' + tempTitle + '" '
			artistQuotation = tempArtist[1:-1]
			print('%06.2f' % (tempBPM) + ' - ' + u'{:<55}'.format(songQuotation) + 'by ' + artistQuotation)


# INPUT: username, Playlist_Id for analysis, TempoMin, TempoMax, # of songs in Playlist
# RETURNS: An array of Spotify Uri
# Uses show_tracks() to "flip through the pages" of the object to displace entire list
def get_playlist_tracks(username, playlist_id, low, high, total):
	uriArray = []
	print(str(total) + " songs to filter")
	print("")
	a = 0
	results = sp.user_playlist(username, playlist_id)
	tracks = results['tracks']
	show_tracks(tracks, a, low, high, total, uriArray)
	a = a + 1
	while tracks['next']:
    		tracks = sp.next(tracks)
    		show_tracks(tracks, a, low, high, total, uriArray)
    		a = a + 1
    	return uriArray

# 
def print_user_playlist(playlist):
	for i, playlist in enumerate(playlists['items']):
		if i < 9:
			print(str(i + 1) + ") " + '{:<60}'.format(str(playlist['name'])) + '{:<10}'.format(str(playlist['tracks']['total'])))
		elif i < 100:
			print(str(i + 1) + ") " + '{:<59}'.format(str(playlist['name'])) + '{:<10}'.format(str(playlist['tracks']['total'])))
		else:
			print(str(i + 1) + ") " + '{:<58}'.format(str(playlist['name'])) + '{:<10}'.format(str(playlist['tracks']['total'])))

# Main -------------------------------------------------------------------------------------------

print("")
print("Spotipy.py will find songs in a playlist that fit a user defined tempo range")
print("")
print("Your Playlists" + '{:>55}'.format("# of Songs"))
print("--------------" + '{:>55}'.format("----------"))


pId = [] 
pTitles = []
pLength = []
pCount = 0


# Assume 1st is a placeholder to avoid list off by one error
pId.append('NULL')
pTitles.append('NULL')
pLength.append(0)


for pCount, playlist in enumerate(playlists['items']):
    pTitles.append(playlist['name'])
    pLength.append(playlist['tracks']['total'])
    pId.append(playlist['id'])
    pCount += 1

# Print User's Playlists 
print_user_playlist(playlists)

# Record User's Playlist Choice
while True:
	choiceP1 = raw_input('Enter Playlist Number: ')
	if choiceP1.isdigit() and float(choiceP1) > 0 and float(choiceP1) <= pCount:
		choiceP1 = int(choiceP1)
		break
	else:
		print("Incorrect input. Please enter a positive number within range")

print("")
print("Tempo Range")
print("-----------")

# Record User's tempoFloor
while True:
	tempoFloor = input("Enter Tempo Floor: ")
	if isinstance(tempoFloor, int) and float(tempoFloor) >= 0:
		break
	else:
		print("Incorrect floor input. Please enter a positive number")

# Record User's tempoCeiling
while True:
	tempoCeiling = input("Enter Tempo Ceiling: ")
	if isinstance(tempoCeiling, int) and float(tempoCeiling) >= 0 and tempoCeiling > tempoFloor:
		break
	else:
		print("Incorrect ceiling input. Please enter a positive number greater than Tempo Floor")

# Respond to Choice
print("")
print("Analyzing " + pTitles[choiceP1] + " Playlist:")

# Analyize and use Choice
pUriArray = get_playlist_tracks(username, pId[choiceP1], tempoFloor, tempoCeiling, pLength[choiceP1])

print("")
print("100% Complete")
print("------------")
print("")
percentInRange = len(pUriArray)/float(pLength[choiceP1]) * 100
print('%.2f'%percentInRange + "% of songs in " + pTitles[choiceP1] + " are in the range " + str(tempoFloor) + "-" + str(tempoCeiling) + (" (BPM)"))
print("")

# User's preference for adding songs to (newPlaylist or existingPlaylist)
while True:
	choiceNE = raw_input("Would you like to add " + str(len(pUriArray)) + " tracks to a new or existing playlist? ('N' or 'E'): ")
	if choiceNE.upper() == 'N' or choiceNE.upper() == 'E':
		break
	else:
		print("Incorrect input. Please enter 'N' or 'E'")

# Add songs to a new playlist
if choiceNE.upper() == 'N':
	newPlaylistName = str(pTitles[choiceP1]) + " (" + str(tempoFloor) + "-" + str(tempoCeiling) + " BPM)"
	playlists = sp.user_playlist_create(username, newPlaylistName, public = False)
	newPlaylistUri = json.dumps(playlists['id'], indent = 4)
	print("Adding songs to " + newPlaylistName)
	for tempUri in pUriArray:
		sp.user_playlist_add_tracks(username, newPlaylistUri[1:-1], tempUri)
	print("Successfully added " + str(len(pUriArray)) + " songs to " + newPlaylistName)

# Add songs to an existing playlist
else: 
	print_user_playlist(playlists)
	print("")
	print("Chose a playlist you would like to add the " + str(len(pUriArray)) + " songs")

	# Record User's Playlist Choice 2nd time
	while True:
		choiceP2 = raw_input('Enter Playlist Number: ')
		if choiceP2.isdigit() and float(choiceP2) > 0 and float(choiceP2) <= pCount:
			choiceP2 = int(choiceP2)
			break
		else:
			print("Incorrect input. Please enter a positive number within range")
	print("Adding songs to " + pTitles[choiceP2])
	for tempUri in pUriArray:
		sp.user_playlist_add_tracks(username, pId[choiceP2], tempUri)
	print("Successfully added " + str(len(pUriArray)) + " songs to " + pTitles[choiceP2])

	#add songs to playlist chosen



