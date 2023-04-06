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

{
        'added_at': '2023-01-28T22:26:41Z', 
        'added_by': {
            'external_urls': {'spotify': 'https://open.spotify.com/user/22j3buggyjs7cml6r56vhggvq'}, 
            'href': 'https://api.spotify.com/v1/users/22j3buggyjs7cml6r56vhggvq', 
            'id': '22j3buggyjs7cml6r56vhggvq', 
            'type': 'user', 
            'uri': 'spotify:user:22j3buggyjs7cml6r56vhggvq'
            }, 
        'is_local': False, 
        'primary_color': None, 
        'track': {
            'album': {
                'album_group': 'album', 
                'album_type': 'album', 
                'artists': [
                    {
                        'external_urls': {'spotify': 'https://open.spotify.com/artist/5K4W6rqBFWDnAN6FQUkS6x'}, 
                        'href': 'https://api.spotify.com/v1/artists/5K4W6rqBFWDnAN6FQUkS6x', 
                        'id': '5K4W6rqBFWDnAN6FQUkS6x', 
                        'name': 'Kanye West', 
                        'type': 'artist', 
                        'uri': 'spotify:artist:5K4W6rqBFWDnAN6FQUkS6x'
                    }
                ], 
                'available_markets': ['AD', 'AE', 'AG', 'AL', 'AM', 'AO', 'AR', 'AT', 'AU', 'AZ', 'BA', 'BB', 'BD', 'BE', 'BF', 'BG', 'BH', 'BI', 'BJ', 'BN', 'BO', 'BR', 'BS', 'BT', 'BW', 'BY', 'BZ', 'CA', 'CD', 'CG', 'CH', 'CI', 'CL', 'CM', 'CO', 'CR', 'CV', 'CW', 'CY', 'CZ', 'DE', 'DJ', 'DK', 'DM', 'DO', 'DZ', 'EC', 'EE', 'EG', 'ES', 'ET', 'FI', 'FJ', 'FM', 'FR', 'GA', 'GB', 'GD', 'GE', 'GH', 'GM', 'GN', 'GQ', 'GR', 'GT', 'GW', 'GY', 'HK', 'HN', 'HR', 'HT', 'HU', 'ID', 'IE', 'IL', 'IN', 'IQ', 'IS', 'IT', 'JM', 'JO', 'JP', 'KE', 'KG', 'KH', 'KI', 'KM', 'KN', 'KR', 'KW', 'KZ', 'LA', 'LB', 'LC', 'LI', 'LK', 'LR', 'LS', 'LT', 'LU', 'LV', 'LY', 'MA', 'MC', 'MD', 'ME', 'MG', 'MH', 'MK', 'ML', 'MN', 'MO', 'MR', 'MT', 'MU', 'MV', 'MW', 'MX', 'MY', 'MZ', 'NA', 'NE', 'NG', 'NI', 'NL', 'NO', 'NP', 'NR', 'NZ', 'OM', 'PA', 'PE', 'PG', 'PH', 'PK', 'PL', 'PS', 'PT', 'PW', 'PY', 'QA', 'RO', 'RS', 'RW', 'SA', 'SB', 'SC', 'SE', 'SG', 'SI', 'SK', 'SL', 'SM', 'SN', 'SR', 'ST', 'SV', 'SZ', 'TD', 'TG', 'TH', 'TJ', 'TL', 'TN', 'TO', 'TR', 'TT', 'TV', 'TW', 'TZ', 'UA', 'UG', 'US', 'UY', 'UZ', 'VC', 'VE', 'VN', 'VU', 'WS', 'XK', 'ZA', 'ZM', 'ZW'], 
                'external_urls': {'spotify': 'https://open.spotify.com/album/4Uv86qWpGTxf7fU7lG5X6F'}, 
                'href': 'https://api.spotify.com/v1/albums/4Uv86qWpGTxf7fU7lG5X6F', 
                'id': '4Uv86qWpGTxf7fU7lG5X6F', 
                'images': [
                    {
                        'height': 640, 
                        'url': 'https://i.scdn.co/image/ab67616d0000b27325b055377757b3cdd6f26b78', 
                        'width': 640
                    }, 
                    {
                        'height': 300, 
                        'url': 'https://i.scdn.co/image/ab67616d00001e0225b055377757b3cdd6f26b78', 
                        'width': 300
                    }, 
                    {
                        'height': 64, 
                        'url': 'https://i.scdn.co/image/ab67616d0000485125b055377757b3cdd6f26b78', 
                        'width': 64
                    }
                ], 
                'is_playable': True, 
                'name': 'The College Dropout', 
                'release_date': '2004-02-10', 
                'release_date_precision': 'day', 
                'total_tracks': 21, 
                'type': 'album', 
                'uri': 'spotify:album:4Uv86qWpGTxf7fU7lG5X6F'
                }, 
            'artists': [
                {
                    'external_urls': {'spotify': 'https://open.spotify.com/artist/5K4W6rqBFWDnAN6FQUkS6x'}, 
                    'href': 'https://api.spotify.com/v1/artists/5K4W6rqBFWDnAN6FQUkS6x', 
                    'id': '5K4W6rqBFWDnAN6FQUkS6x', 
                    'name': 'Kanye West', 
                    'type': 'artist', 
                    'uri': 'spotify:artist:5K4W6rqBFWDnAN6FQUkS6x'
                }, 
                {
                    'external_urls': {'spotify': 'https://open.spotify.com/artist/1lE6SEy8f84Zhjvp7r8yTD'}, 
                    'href': 'https://api.spotify.com/v1/artists/1lE6SEy8f84Zhjvp7r8yTD', 
                    'id': '1lE6SEy8f84Zhjvp7r8yTD', 
                    'name': 'Syleena Johnson', 
                    'type': 'artist', 
                    'uri': 'spotify:artist:1lE6SEy8f84Zhjvp7r8yTD'
                }], 
            'available_markets': ['AR', 'AU', 'AT', 'BE', 'BO', 'BR', 'BG', 'CA', 'CL', 'CO', 'CR', 'CY', 'CZ', 'DK', 'DO', 'DE', 'EC', 'EE', 'SV', 'FI', 'FR', 'GR', 'GT', 'HN', 'HK', 'HU', 'IS', 'IE', 'IT', 'LV', 'LT', 'LU', 'MY', 'MT', 'MX', 'NL', 'NZ', 'NI', 'NO', 'PA', 'PY', 'PE', 'PH', 'PL', 'PT', 'SG', 'SK', 'ES', 'SE', 'CH', 'TW', 'TR', 'UY', 'US', 'GB', 'AD', 'LI', 'MC', 'ID', 'JP', 'TH', 'VN', 'RO', 'IL', 'ZA', 'SA', 'AE', 'BH', 'QA', 'OM', 'KW', 'EG', 'MA', 'DZ', 'TN', 'LB', 'JO', 'PS', 'IN', 'BY', 'KZ', 'MD', 'UA', 'AL', 'BA', 'HR', 'ME', 'MK', 'RS', 'SI', 'KR', 'BD', 'PK', 'LK', 'GH', 'KE', 'NG', 'TZ', 'UG', 'AG', 'AM', 'BS', 'BB', 'BZ', 'BT', 'BW', 'BF', 'CV', 'CW', 'DM', 'FJ', 'GM', 'GE', 'GD', 'GW', 'GY', 'HT', 'JM', 'KI', 'LS', 'LR', 'MW', 'MV', 'ML', 'MH', 'FM', 'NA', 'NR', 'NE', 'PW', 'PG', 'WS', 'SM', 'ST', 'SN', 'SC', 'SL', 'SB', 'KN', 'LC', 'VC', 'SR', 'TL', 'TO', 'TT', 'TV', 'VU', 'AZ', 'BN', 'BI', 'KH', 'CM', 'TD', 'KM', 'GQ', 'SZ', 'GA', 'GN', 'KG', 'LA', 'MO', 'MR', 'MN', 'NP', 'RW', 'TG', 'UZ', 'ZW', 'BJ', 'MG', 'MU', 'MZ', 'AO', 'CI', 'DJ', 'ZM', 'CD', 'CG', 'IQ', 'LY', 'TJ', 'VE', 'ET', 'XK'], 
            'disc_number': 1, 
            'duration_ms': 223506, 
            'episode': False, 
            'explicit': True, 
            'external_ids': {'isrc': 'USDJ20301703'}, 
            'external_urls': {'spotify': 'https://open.spotify.com/track/5SkRLpaGtvYPhw02vZhQQ9'}, 
            'href': 'https://api.spotify.com/v1/tracks/5SkRLpaGtvYPhw02vZhQQ9', 
            'id': '5SkRLpaGtvYPhw02vZhQQ9', 
            'is_local': False, 
            'name': 'All Falls Down', 
            'popularity': 79, 
            'preview_url': None, 
            'track': True, 
            'track_number': 4, 
            'type': 'track', 
            'uri': 'spotify:track:5SkRLpaGtvYPhw02vZhQQ9'
        }, 
        'video_thumbnail': {'url': None}
    }