"""
SprintifyHelper.py
Alexander Scott
October 2018
Functions written in conjunction with Sprintify.py
"""
import json
import sys

# https://gist.github.com/vladignatyev/06860ec2040cb497f0f3
def progress(count, total, status=''):
    bar_len = 40
    filled_len = int(round(bar_len * count / float(total)))

    percents = round(100.0 * count / float(total), 1)
    bar = '=' * filled_len + '-' * (bar_len - filled_len)

    sys.stdout.write("\033[K" + '\r[%s] %s%s ...%s\r' % (bar, percents, '%', status))
    sys.stdout.flush()

# Prints the BPM bounded tracks found in the 100 item page
# Fills uriArray with uri's of the bounded tracks
def filter_tracks(results, a, low, high, total, uriArray, spotify):

	for i, item in enumerate(results['items']):
		lastTrack = ''
		track = item['track']
		tempTitle = track['name']
		tempArtist = json.dumps(track['artists'][0]['name'])
		tempUri = []
		tempUri.append(track['uri'])
		try: 
			tempFeature = spotify.audio_features(tempUri)
		except:
			print("ERROR: can't find tempFeature")
		tempBPM = float(json.dumps(tempFeature[0]['tempo']))
		tempCurrent = a * 100 + i

		progress(tempCurrent, total, lastTrack[:45])

		if float(tempBPM) >= float(low) and float(tempBPM) <= float(high):
			uriArray.append(tempUri)
			songQuotation = '"' + tempTitle + '" '
			artistQuotation = tempArtist[1:-1]
			lastTrack = songQuotation + " " + artistQuotation
			progress(tempCurrent, total, status=lastTrack[:45])
			#print('%06.2f' % (tempBPM) + ' - ' + u'{:<55}'.format(songQuotation) + 'by ' + artistQuotation)

# INPUT: username, Playlist_Id for analysis, TempoMin, TempoMax, # of songs in Playlist
# RETURNS: An array of Spotify Uri
# Uses filter_tracks() to "flip through the pages" of the object to displace entire list
def get_playlist_tracks(username, playlist_id, low, high, total, spotify):
	uriArray = []
	print(str(total) + " songs to filter")
	print("")
	a = 0
	results = spotify.user_playlist(username, playlist_id)
	tracks = results['tracks']
	progress(0, total, status='')
	filter_tracks(tracks, a, low, high, total, uriArray, spotify)
	a = a + 1
	while tracks['next']:
		tracks = spotify.next(tracks)
		filter_tracks(tracks, a, low, high, total, uriArray, spotify)
		a = a + 1
	progress(total, total, status= " " + str(len(uriArray)) + " tracks found")
	return uriArray

# Prints a user's playlist
def print_user_playlist(username, sp):
	playlists = sp.user_playlists(username)
	c = 0
	print("")
	print("Your Playlists" + '{:>55}'.format("# of Songs"))
	print("--------------" + '{:>55}'.format("----------"))
	while playlists:
		for i, playlist in enumerate(playlists['items']):
			index = i + c + 1
			if index < 9:
				print(str(index) + ") " + '{:<60}'.format(str(playlist['name'])) + '{:<10}'.format(str(playlist['tracks']['total'])))
			else:
				print(str(index) + ") " + '{:<59}'.format(str(playlist['name'])) + '{:<10}'.format(str(playlist['tracks']['total'])))
		if playlists['next']:
			c += 50
			playlists = sp.next(playlists)
		else:
			playlists = None

# Used to generate a filtered playlist of length n
def get_generated_list_uri(gLength, songChoice, tempoFloor, tempoCeiling, spotify):
	pUriArray = []
	tUriArray = []
	tempLenArray = len(pUriArray)
	tempGLenth = gLength
	while gLength > 0:
		results = spotify.recommendations(seed_tracks = songChoice, limit = 100, min_tempo = int(tempoFloor), max_tempo = int(tempoCeiling))
		for track in results['tracks']:
			if not track['uri'] in pUriArray:
				pUriArray.append(track['uri'])
				tUriArray.append(track['uri'])
				pUriArray.sort()
				print(track['name'], '-', track['artists'][0]['name'])
				gLength -= 1
			if gLength == 0:
				break
		print("")
		if gLength == 0:
			break
		if tempLenArray == len(pUriArray):
			print("No songs found within range " + str(tempoFloor) + '-' + str(tempoCeiling))
		print("There are " +str(len(pUriArray)) + "/" +  str(tempGLenth) + " spots in the playlists")
		print("")
		songChoice = get_song_uri_more()
		if songChoice == 'Q':
			break
	return tUriArray

# Functions that Prompt User ----------------------------------------------------------------

# Generate new Playlist from song seed, or Filter through a User's existing playlists
def get_generate_or_filter():
	while True:
		filterOrGenerate = input("Would you like to filter your existing playlist, or generate a new playlist ('G' or 'E'): ")
		if filterOrGenerate.upper() == 'G' or filterOrGenerate.upper() == 'E':
			return filterOrGenerate.upper()
		else:
			print("Incorrect input. Please enter 'G' or 'E'")

# Prompts User for Tempo Floor
def get_tempo_floor():
	while True:
		tempoFloor = input("Enter Tempo Floor: ")
		if str(tempoFloor).isdigit() and int(tempoFloor) >= 0:
			return int(tempoFloor)
		else:
			print("Incorrect floor input. Please enter a positive number")

# Prompts User for Tempo Ceiling. Uses Tempo Floor to ensure that the ceiling is larger
def get_tempo_ceiling(tempoFloor):
	while True:
		tempoCeiling = input("Enter Tempo Ceiling: ")
		if str(tempoCeiling).isdigit() and int(tempoCeiling) > int(tempoFloor):
			return int(tempoCeiling)
		else:
			print("Incorrect ceiling input. Please enter a positive number larger than Tempo Floor")

# Promps User for playlistInput given list
def get_playlist_choice(pCount):
	while True:
		choiceP1 = input('Enter Playlist Number: ')
		if choiceP1.isdigit() and float(choiceP1) > 0 and float(choiceP1) <= pCount:
			return int(choiceP1)
		else:
			print("Incorrect input. Please enter a positive number within range")

# Prompts User for number in range 0-100. Used to generate a playlist of gLenth
def get_generate_length():
	while True:
		gLength = input("Enter generated playlist length (1-100): ")
		if gLength.isdigit()  and int(gLength) > 0 and int(gLength) < 100:
			return int(gLength)
		else:
			print("Incorrect length input. Please enter a positive number smaller than 100")

# Prompts User for TrackURI to generate playlist 1st
def get_song_uri():
	while True:
		songChoice = input('Enter Song Uri: ')
		if len(songChoice) == 36 and songChoice[0:7] == 'spotify':
			return [songChoice]
		else:
			print("Incorrect input. Please enter a Spotify URI")

# Reworded prompt for TrackURI to generate playlist
def get_song_uri_more():
	while True:
		songChoice = input("Enter Another Song Uri ('Q' to quit): ")
		if songChoice.upper() == 'Q':
			return 'Q'
		if len(songChoice) == 36 and songChoice[0:7] == 'spotify':
			return [songChoice]
		else:
			print("Incorrect input. Please enter a Spotify URI")

# Prompts User for 'N' or 'E' to add songs to a new or existing playlist
def get_new_or_existing(pUriArray):
	while True:
		choiceNE = input("Would you like to add " + str(len(pUriArray)) + " tracks to a new or existing playlist? ('N' or 'E'): ")
		if choiceNE.upper() == 'N' or choiceNE.upper() == 'E':
			return choiceNE
		else:
			print("Incorrect input. Please enter 'N' or 'E'")

# Practice Functions --------------------------------------------------------------------------

# Used to check if an item already exists within a sorted array
# Return False if the item already exists
# Return True if the item does not already exist
def binarySearch(list, l, r, x):
	if r >= l:
		mid = l + (r - l)/2
		mid = int(mid)
		if list[mid] == x:
			return False
		elif list[mid] > x:
			return binarySearch(list, l, mid - 1, x)
		else:
			return binarySearch(list, mid + 1, r, x)
	else:
		return True