from Song import Song, addZeros
from YoutubeSong import YoutubeSong
from pytube import Playlist
from pytube import YouTube
from spotipy.oauth2 import SpotifyClientCredentials
from extraUtil import *
import spotipy

from SpotifyToMp3 import removePartials,run

playlist_url = 'https://www.youtube.com/playlist?list=PLXOSYmGS3kcMNkl2mhpvf7GKamtnEwVAh'
playlist_title = 'Max Playlist'
playlist = Playlist(playlist_url)
parentFolder = f'{OUTPUT_FOLDER_NAME}\\{playlist_title}'
# removePartials(parentFolder)
RAM = True
print()
for index,video_url in enumerate(playlist,start=1):
    # if (index<=166): continue
    client_credentials_manager = SpotifyClientCredentials(
        client_id=CLIENT_ID, client_secret=CLIENT_SECRET
    )
    # create spotify session object
    session = spotipy.Spotify(client_credentials_manager=client_credentials_manager)
    video = YoutubeSong(None,YouTube(video_url))
    skip = False
    for file in os.listdir(parentFolder):
        if file.startswith(addZeros(index)):
            skip = True
            print(f"SKIP {addZeros(index)   }",end="\r")
            break
    if skip: continue
    results = session.search(q=video.title, limit=1)
    while results['tracks']['next']:
        if len(results['tracks']['items'])==0: break
        newsong = Song(results['tracks']['items'][0],index,playlist_title)
        newsong.setFolderInformation(removeSymbols(video.title))
        video.parent = newsong
        newsong.bestfit = video
        newsong.saveToDebug()
        if not RAM: userinput = input(f'{addZeros(index)} {video.title} Good? (Y/N/S):').lower() 
        else :userinput = "ram"
        if userinput == "ram": RAM = True
        if userinput == "y" or RAM: 
            video.download()
            break
        if userinput == "s": break
        results = session.next(results['tracks'])
run()