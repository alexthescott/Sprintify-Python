"""
Spotipy.py for Python 2.7
Alexander Scott
October 2018
Written to find songs in a playlist that are in a tempo range 
"""
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
def show_tracks(results, a, low, high, total):
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
		tempBPM = json.dumps(tempFeature[0]['tempo'])
		tempCurrent = a * 100 + i

		if twentyDone == False and tempCurrent == twentyPercent:
			print("")
			print("20% Complete")
			print("------------")
			twentyDone = True 

		if fourtyDone == False and tempCurrent == fourtyPercent:
			print("")
			print("40% Complete")
			print("------------")
			fourtyDone = True 

		if sixtyDone == False and tempCurrent == sixtyPercent:
			print("")
			print("60% Complete")
			print("------------")
			sixtyDone = True

		if eightyDone == False and tempCurrent == eightyPercent:
			print("")
			print("80% Complete")
			print("------------")
			eightyDone = True

		if tempBPM <= high and tempBPM >= low:
			print("BPM: " + str(tempBPM) + " - " + tempTitle + " by " + tempArtist)
			tempFiltered.append(tempUri)
	return tempFiltered 


# INPUT: username, Playlist_Id for analysis, TempoMin, TempoMax, # of songs in Playlist
# OUTPUT: An array of Spotify Uri
# Uses show_tracks() to "flip through the pages" of the object to displace entire list
def get_playlist_tracks(username, playlist_id, low, high, total):
	CollectedFilter = []
	print(str(total) + " songs to filter")
	a = 0
	results = sp.user_playlist(username, playlist_id)
	tracks = results['tracks']
	CollectedFilter.append(show_tracks(tracks, a, low, high, total))
	a = a + 1
	while tracks['next']:
    		tracks = sp.next(tracks)
    		CollectedFilter.append(show_tracks(tracks, a, low, high, total))
    		a = a + 1
	return CollectedFilter

# Input for playlist 0 < i <= n, where n is # of User's playlists
def askPlaylist():
	while True:
		# Ensure integer input
		try:
			choice = int(raw_input('Enter the number of the playlist you would like to analyze: '))
			break
		except:
			print("Please enter number")
	# Ensure choice is within range
	if choice >= i: 
		print("Your number is too high")
		askPlaylist()
	if choice <= 0:
		print("Your number is too low")
		askPlaylist()
	else:
		return choice

# Main -------------------------------------------------------------------------------------------

print("")
print("Spotipy.py will find songs in a playlist that fit a user defined tempo range")
print("")
print("Your Playlists")
print("--------------")


playlistId = [] 
playlistTitles = []
playlistLength = []

# Assume 1st is a placeholder to avoid list off by one error
playlistId.append('NULL')
playlistTitles.append('NULL')
playlistLength.append(0)

# Print User's Playlists 
for i, playlist in enumerate(playlists['items']):
    print(str(i + 1) + ") " + str(playlist['name']))
    playlistTitles.append(playlist['name'])
    playlistLength.append(playlist['tracks']['total'])
    print("	" + str(playlist['tracks']['total']) + " Tracks")
    playlistId.append(playlist['id'])
    i += 1

# Record User's Choice
playlistChoice = askPlaylist()

# Record User's tempoFloor
while True:
	tempoFloor = raw_input('Enter Tempo Floor: ')
	if tempoFloor.isdigit() and tempoFloor >= 0:
		break
	else:
		print('Incorrect floor input. Please enter a positive number')

# Record User's tempoCeiling
while True:
	tempoCeiling = raw_input('Enter Tempo Ceiling: ')
	if tempoCeiling.isdigit() and tempoCeiling >= 0:
		break
	else:
		print('Incorrect ceiling input. Please enter a positive number')

# Record User's new Playlist Preference

# Respond to Choice
print("")
print("Analyzing " + playlistTitles[playlistChoice] + " Playlist")
print("")

# Analyize and use Choice
Choice = get_playlist_tracks(username, playlistId[playlistChoice], tempoFloor, tempoCeiling, playlistLength[playlistChoice])
print(json.dumps(Choice[0], indent = 4))