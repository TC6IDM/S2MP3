import re
from os.path import exists
import spotipy
from spotipy.oauth2 import SpotifyClientCredentials
from Song import Song
from extraUtil import *

def get_playlist_tracks(sp,username,playlist_id): #slowest part of the program
    results = sp.user_playlist_tracks(username,playlist_id)
    tracks = results['items']
    while results['next']:
        results = sp.next(results)
        tracks.extend(results['items'])
    return tracks

def checkPlaylist(playlist,session):
    if match := re.match(r"https://open.spotify.com/playlist/(.*)\?", playlist):
        playlist_uri = match.groups()[0]
    else:
        raise ValueError("Expected format: https://open.spotify.com/playlist/...")
    
    # get list of tracks in a given playlist (note: max playlist length 100)
    tracks = get_playlist_tracks(session,USERNAME,playlist_uri)
    playlistName =deleteBadCharacters(removeSymbols(session.user_playlist(USERNAME,playlist_uri)["name"]))
    print("\nFetching spotify playlist - "+playlistName+ " https://open.spotify.com/playlist/"+playlist_uri)
    songList =[]
    
    for index,track in enumerate(tracks,start=1):
        thisTrack = Song(track,index)
        thisTrack.setDestination(f'{OUTPUT_FOLDER_NAME}\\{playlistName}\\{thisTrack.destinationIndex} {thisTrack.cleanTrackName}')
        songList.append(thisTrack)
    prGreen(f'Playlist {playlistName} has ben fetched with {len(songList)} songs')
    return playlistName,songList


file = open(PLAYLIST_FILE_NAME,'r')
# authenticate
client_credentials_manager = SpotifyClientCredentials(
    client_id=CLIENT_ID, client_secret=CLIENT_SECRET
)
    
# create spotify session object
session = spotipy.Spotify(client_credentials_manager=client_credentials_manager)
    
# get uri from https link
for currentPlaylist in file.readlines():
    validPlaylist=True if currentPlaylist.startswith("https://open.spotify.com/playlist/") else False
    playlistName,songList = checkPlaylist(currentPlaylist,session)
    if validPlaylist:
        for i,song in enumerate(songList,start=1): 
            if (exists(song.destination+'.mp3')):
                prYellow("SKIP "+song.trackName+" Already Downloaded")
            else:
                song.get_videos()
                song.getBestVideo().download()
        prPurple("Playlist : "+playlistName+" Done\n") 

prPurple("DONE ALL PLAYLISTS")