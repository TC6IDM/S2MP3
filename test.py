import re
import urllib.request
from mutagen.easyid3 import EasyID3
from mutagen.flac import FLAC
from mutagen.id3 import APIC, ID3
from mutagen.mp3 import MP3

# path = '30 Hours.mp3'
# tags = EasyID3(path)
# # tags['title'] = 'new_title'
# print(tags)

def addZeros(number):
    if int(number)<10: return "(000"+number+")"
    if int(number)<100: return "(00"+number+")"
    if int(number)<1000: return "(0"+number+")"
    return"("+number+")"

def prRed(skk): print("\033[91m{}\033[00m" .format(skk))
def prGreen(skk): print("\033[92m{}\033[00m" .format(skk))
def prYellow(skk): print("\033[93m{}\033[00m" .format(skk))
def prCyan(skk): print("\033[96m{}\033[00m" .format(skk))
def prLightPurple(skk): print("\033[94m{}\033[00m" .format(skk)) 
def prPurple(skk): print("\033[95m{}\033[00m" .format(skk))
# html = urllib.request.urlopen("https://www.youtube.com/results?search_query=shorts").read().decode()
# with open(f"C:\\Users\\Owner\\Desktop\\Youtube-DL-Code\\LW6QSPI0NN8F197NF9LAQYQCF html.txt") as f:
#     html = f.readline()
# video_ids = re.findall(r'"videoRenderer":{"videoId":"(\S{11})',html)
# video_titles = re.findall(r'}]},"title":{"runs":\[{"text":"(.*?)"}]',html)
# video_lengths = re.findall(r'{"thumbnailOverlayTimeStatusRenderer":{"text":{"accessibility":{"accessibilityData":{"label":"(.*?)"}},',html) 

# with open(f"C:\\Users\\Owner\\Desktop\\Youtube-DL-Code\\LW6QSPI0NN8F197NF9LAQYQCF ids_titles_lengths.txt") as f:
#     lines = f.readlines()
#     lines[0] = lines[0].split("', '")
#     lines[1] = lines[1].split("', '")
#     lines[2] = lines[2].split("', '")
        
# for i in range(len(lines[1])):
#     print("https://www.youtube.com/watch?v="+lines[0][i],lines[1][i],lines[2][i])


# print(len(video_ids),len(video_titles),len(video_lengths))
# for i in range(len(video_ids)):
#     print("https://www.youtube.com/watch?v="+video_ids[i],video_titles[i],video_lengths[i])
import spotipy
from spotipy.oauth2 import SpotifyClientCredentials

birdy_uri = 'spotify:artist:2WX2uTcsvV5OnS0inACecP'
client_credentials_manager = SpotifyClientCredentials(
        client_id="1aade97b28854f0eb926ce48a12c1b7e", client_secret="baf7efc3cff3496ba9a4e7f108c45d98"
    )
    
    # create spotify session object
spotify = spotipy.Spotify(client_credentials_manager=client_credentials_manager)

results = spotify.artist_albums(birdy_uri, album_type='album')
albums = results['items']
while results['next']:
    results = spotify.next(results)
    albums.extend(results['items'])

for album in albums:
    print(album['name'])
    
def gatekeep(blacklist,artist,song,yttitle):
    for i in blacklist:
        if (not (i not in yttitle.lower() or (i in artist.lower() or i in song.lower()))): return False #if word is in the title, it must be in the artist or song name
    return True

blacklist = ["clean","8d"]

print(gatekeep(blacklist,"Clean Bandit","Solo (feat. Demi Lovato)","Clean Bandit - Solo (feat. Demi Lovato) (Official Video)")) #true
print(gatekeep(blacklist,"Bandit","Solo (feat. Demi Lovato)","Clean Bandit - Solo (feat. Demi Lovato) (Official Video)")) #false
print(gatekeep(blacklist,"Bandit","Solo (feat. Demi Lovato)","Bandit - Solo (feat. Demi Lovato) (Official Video)"))#true
print(gatekeep(blacklist,"Clean Bandit","Solo (feat. Demi Lovato)","Bandit - Solo (feat. Demi Lovato) (Official Video)"))#true

