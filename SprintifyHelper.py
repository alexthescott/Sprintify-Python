"""
SprintifyHelper.py
Alexander Scott
October 2018
Functions written in conjunction with Sprintify.py
"""
import json

# Prints the BPM bounded tracks found in the 100 item page
# Fills uriArray with uri's of the bounded tracks
def filter_tracks(results, a, low, high, total, uriArray, spotify):
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
		tempFeature = spotify.audio_features(tempUri)
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
# Uses filter_tracks() to "flip through the pages" of the object to displace entire list
def get_playlist_tracks(username, playlist_id, low, high, total, spotify):
	uriArray = []
	print(str(total) + " songs to filter")
	print("")
	a = 0
	results = spotify.user_playlist(username, playlist_id)
	tracks = results['tracks']
	filter_tracks(tracks, a, low, high, total, uriArray, spotify)
	a = a + 1
	while tracks['next']:
    		tracks = spotify.next(tracks)
    		filter_tracks(tracks, a, low, high, total, uriArray, spotify)
    		a = a + 1
    	return uriArray

# Prints a user's playlist
def print_user_playlist(playlist):
	print("")
	print("Your Playlists" + '{:>55}'.format("# of Songs"))
	print("--------------" + '{:>55}'.format("----------"))
	for i, playlist in enumerate(playlist['items']):
		if i < 9:
			print(str(i + 1) + ") " + '{:<60}'.format(str(playlist['name'])) + '{:<10}'.format(str(playlist['tracks']['total'])))
		elif i < 100:
			print(str(i + 1) + ") " + '{:<59}'.format(str(playlist['name'])) + '{:<10}'.format(str(playlist['tracks']['total'])))
		else:
			print(str(i + 1) + ") " + '{:<58}'.format(str(playlist['name'])) + '{:<10}'.format(str(playlist['tracks']['total'])))

# Used to generate a filtered playlist of length n
def get_generated_list_uri(gLength, songChoice, tempoFloor, tempoCeiling, spotify):
	pUriArray = []
	tUriArray = []
	tempLenArray = len(pUriArray)
	tempGLenth = gLength
	while gLength > 0:
		results = spotify.recommendations(seed_tracks = songChoice, limit = 100, min_tempo = tempoFloor, max_tempo = tempoCeiling)
		for track in results['tracks']:
			if binarySearch(pUriArray, 0, len(pUriArray) - 1, track['uri']) == True:
				pUriArray.append(track['uri'])
				tUriArray.append(track['uri'])
				mergeSort(pUriArray, 0, len(pUriArray) - 1)
				print track['name'], '-', track['artists'][0]['name']
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
		filterOrGenerate = raw_input("Would you like to filter your existing playlist, or generate a new playlist ('G' or 'E'): ")
		if filterOrGenerate.upper() == 'G' or filterOrGenerate.upper() == 'E':
			return filterOrGenerate.upper()
		else:
			print("Incorrect input. Please enter 'G' or 'E'")

# Prompts User for Tempo Floor
def get_tempo_floor():
	while True:
		tempoFloor = raw_input("Enter Tempo Floor: ")
		if str(tempoFloor).isdigit() and int(tempoFloor) >= 0:
			return int(tempoFloor)
		else:
			print("Incorrect floor input. Please enter a positive number")

# Prompts User for Tempo Ceiling. Uses Tempo Floor to ensure that the ceiling is larger
def get_tempo_ceiling(tempoFloor):
	while True:
		tempoCeiling = raw_input("Enter Tempo Ceiling: ")
		if str(tempoCeiling).isdigit() and tempoCeiling > tempoFloor:
			return int(tempoCeiling)
		else:
			print("Incorrect ceiling input. Please enter a positive number larger than Tempo Floor")

# Promps User for playlistInput given list
def get_playlist_choice(pCount):
	while True:
		choiceP1 = raw_input('Enter Playlist Number: ')
		if choiceP1.isdigit() and float(choiceP1) > 0 and float(choiceP1) <= pCount:
			return int(choiceP1)
		else:
			print("Incorrect input. Please enter a positive number within range")

# Prompts User for number in range 0-100. Used to generate a playlist of gLenth
def get_generate_length():
	while True:
		gLength = raw_input("Enter generated playlist length (1-100): ")
		if gLength.isdigit()  and int(gLength) > 0 and int(gLength) < 100:
			return int(gLength)
		else:
			print("Incorrect length input. Please enter a positive number smaller than 100")

# Prompts User for TrackURI to generate playlist 1st
def get_song_uri():
	while True:
		songChoice = raw_input('Enter Song Uri: ')
		if len(songChoice) == 36 and songChoice[0:7] == 'spotify':
			return [songChoice]
		else:
			print("Incorrect input. Please enter a Spotify URI")

# Reworded prompt for TrackURI to generate playlist
def get_song_uri_more():
	while True:
		songChoice = raw_input("Enter Another Song Uri ('Q' to quit): ")
		if songChoice.upper() == 'Q':
			return 'Q'
		if len(songChoice) == 36 and songChoice[0:7] == 'spotify':
			return [songChoice]
		else:
			print("Incorrect input. Please enter a Spotify URI")

# Prompts User for 'N' or 'E' to add songs to a new or existing playlist
def get_new_or_existing(pUriArray):
	while True:
		choiceNE = raw_input("Would you like to add " + str(len(pUriArray)) + " tracks to a new or existing playlist? ('N' or 'E'): ")
		if choiceNE.upper() == 'N' or choiceNE.upper() == 'E':
			return choiceNE
		else:
			print("Incorrect input. Please enter 'N' or 'E'")

# Useful Functions --------------------------------------------------------------------------

# Used recursively in mergeSort()
def merge(list, l, m, r):
	n1 = m - l + 1
	n2 = r - m

	L = [0] * (n1)
	R = [0] * (n2)

	for i in range(0, n1):
		L[i] = list[l + i]

	for j in range(0, n2):
		R[j] = list[m + j + 1]

	i = 0
	j = 0
	k = l

	while i < n1 and j < n2:
		if L[i] < R[j]:
			list[k] = L[i]
			i += 1
		else:
			list[k] = R[j]
			j += 1
		k += 1

	while i < n1:
		list[k] = L[i]
		i += 1
		k += 1

	while j < n2:
		list[k] = R[j]
		j += 1
		k += 1

# Used to sort list of URIs
def mergeSort(list, l, r):
	if l < r:
		m = (l+(r-1))/2
		mergeSort(list, l, m)
		mergeSort(list, m + 1, r)
		merge(list, l, m, r)
	return list

# Used to check if an item already exists within a sorted array
# Return False if the item already exists
# Return True if the item does not already exist
def binarySearch(list, l, r, x):
	if r >= l:
		mid = l + (r - l)/2
		if list[mid] == x:
			return False
		elif list[mid] > x:
			return binarySearch(list, l, mid - 1, x)
		else:
			return binarySearch(list, mid + 1, r, x)
	else:
		return True