import spotipy
import spotipy.util as util
import json

client_id = '0a6e845a19894708aadf65a22c4554e2'
client_secret = '056e4729129e4b35ac82ab808a5fff67'
redirect_uri = 'http://www.google.com/' 

"""
from spotipy.oauth2 import SpotifyClientCredentials

client_credentials_manager = SpotifyClientCredentials(client_id, client_secret)
spotify = spotipy.Spotify(client_credentials_manager=client_credentials_manager)
"""

uri = 'spotify:user:bassguitar1234:playlist:1ANQ989xbFw46QYyFJUy1j'
username = uri.split(':')[2]
playlist_id = uri.split(':')[4]

scope = "playlist-modify-private"
token = util.prompt_for_user_token(username, scope, client_id, client_secret, redirect_uri)

if token:
    spotify = spotipy.Spotify(auth=token)
    
    results = spotify.user_playlist(username, playlist_id)
    
    tids = []
    title = []

    for i, t in enumerate(results['tracks']['items']):
        track = t['track']
        title.append(str(i + 1) + " " + str(track['artists'][0]['name']) + " - "+ str(track['name']))
        tids.append(track['uri'])

        #print(track['uri'])
        #print("   %d %32.32s %s" % (i, track['artists'][0]['name'], track['name']))
        
    for temp in tids:
        print(temp)
    print()
        
    features = spotify.audio_features(tids)
    
    finalList = []
    finalListTitle = []

    a = 0
    for feature in features:
        tempBPM = json.dumps(feature['tempo'])
        print(title[a])
        print("TEMPO = " + tempBPM)
        print()
        """
        if float(tempBPM) < 180 and float(tempBPM) > 160:
            #spotify.user_playlist_add_tracks(username, "spotify:user:bassguitar1234:playlist:1ANQ989xbFw46QYyFJUy1j",tids[a])
            print(tids[a].split(":")[2])
            finalList.append(tids[a].split(":")[2])
            finalListTitle.append(title[a])
            print(title[a])
            print("TEMPO = " + tempBPM)
            print()
            #spotify.user_playlist_add_tracks(username,'spotify:user:bassguitar1234:playlist:1ANQ989xbFw46QYyFJUy1j', tids[a])
        """
        a = a + 1
    
    #spotify.user_playlist_add_tracks(username,'spotify:user:bassguitar1234:playlist:1ANQ989xbFw46QYyFJUy1j' , finalList)
