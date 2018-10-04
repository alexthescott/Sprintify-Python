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

# Assigns scope and creates token for Spotipy object
scope = "playlist-modify-private"
token = util.prompt_for_user_token(username, scope, client_id, client_secret, redirect_uri)

# Create Spotify Object
sp = spotipy.Spotify(auth=token)
playlists = sp.user_playlists(username)

# Functions --------------------------------------------------------------------------------------

# Prints the tracks found on the 100 item page
def show_tracks(results, a, low, high, total, uriArray):
	tempFiltered = []
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
			uriArray.append(json.dumps(tempUri))
			nameQuotation = '"' + tempTitle + '"'
			print("BPM: " + '%06.2f' % (tempBPM) + " - " + '{:<44}'.format(nameQuotation) + 'by ' + tempArtist[1:-1])


# INPUT: username, Playlist_Id for analysis, TempoMin, TempoMax, # of songs in Playlist
# OUTPUT: An array of Spotify Uri
# Uses show_tracks() to "flip through the pages" of the object to displace entire list
def get_playlist_tracks(username, playlist_id, low, high, total, uriArray):
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

# Main -------------------------------------------------------------------------------------------

print("")
print("Spotipy.py will find songs in a playlist that fit a user defined tempo range")
print("")
print("Your Playlists")
print("--------------")


pId = [] 
pTitles = []
pLength = []
pUriArray = []

# Assume 1st is a placeholder to avoid list off by one error
pId.append('NULL')
pTitles.append('NULL')
pLength.append(0)

# Print User's Playlists 
for i, playlist in enumerate(playlists['items']):
    print(str(i + 1) + ") " + str(playlist['name']))
    pTitles.append(playlist['name'])
    pLength.append(playlist['tracks']['total'])
    print("	" + str(playlist['tracks']['total']) + " Tracks")
    pId.append(playlist['id'])
    i += 1

# Record User's Playlist Choice
while True:
	pChoice = input('Enter Playlist Number: ')
	if isinstance(pChoice, int) and float(pChoice) > 0 and float(pChoice) <= i:
		break
	else:
		print('Incorrect input. Please enter a positive number within range')

print("")
print("Tempo Range")
print("-----------")

# Record User's tempoFloor
while True:
	tempoFloor = input('Enter Tempo Floor: ')
	if isinstance(tempoFloor, int) and float(tempoFloor) >= 0:
		break
	else:
		print('Incorrect floor input. Please enter a positive number')

# Record User's tempoCeiling
while True:
	tempoCeiling = input('Enter Tempo Ceiling: ')
	if isinstance(tempoCeiling, int) and float(tempoCeiling) >= 0:
		break
	else:
		print('Incorrect ceiling input. Please enter a positive number')

# Respond to Choice
print("")
print("Analyzing " + pTitles[pChoice] + " Playlist")
print("")

# Analyize and use Choice
get_playlist_tracks(username, pId[pChoice], tempoFloor, tempoCeiling, pLength[pChoice], pUriArray)

print("")
for t in pUriArray:
	print(t[2:-2])

print("")
percentInRange = len(pUriArray)/float(pLength[pChoice]) * 100
print('%.2f'%percentInRange + "% of songs in " + pTitles[pChoice] + " are in the range " + str(tempoFloor) + "-" + str(tempoCeiling) + (" (BPM)"))
print("")
