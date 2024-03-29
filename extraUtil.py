from __future__ import unicode_literals
import os
import re
import unicodedata
from dotenv import load_dotenv

def prRed(skk,end="\n"): print("\033[91m{}\033[00m" .format(skk),end=end)
def prGreen(skk,end="\n"): print("\033[92m{}\033[00m" .format(skk),end=end)
def prYellow(skk,end="\n"): print("\033[93m{}\033[00m" .format(skk),end=end)
def prCyan(skk,end="\n"): print("\033[96m{}\033[00m" .format(skk),end=end)
def prLightPurple(skk,end="\n"): print("\033[94m{}\033[00m" .format(skk),end=end) 
def prPurple(skk,end="\n"): print("\033[95m{}\033[00m" .format(skk),end=end)

load_dotenv()
DEBUG_FOLDER_NAME = os.getenv("DEBUG_FOLDER_NAME", "")
OUTPUT_FOLDER_NAME = os.getenv("OUTPUT_FOLDER_NAME","")
CLIENT_ID = os.getenv("CLIENT_ID", "")
CLIENT_SECRET = os.getenv("CLIENT_SECRET", "")
USERNAME = os.getenv("USERNAME", "")
PLAYLIST_FILE_NAME = os.getenv("PLAYLIST_FILE_NAME", "")
COOKIE_FILE = os.getenv("COOKIE_FILE", "")
MAX_SEARCH_DEPTH = 5

def deleteBadCharacters(text):
    text = text.replace(",","")
    text = text.replace("’","'")
    return unicodedata.normalize('NFKD', text).encode('ascii', 'ignore').decode('ascii')

def removeSymbols(text):
    if r'\\' in text : text = re.sub(r'\\', '(Bslash)', text)
    if '<' in text : text = re.sub('\<', '(LAbracket)', text)
    if '>' in text : text = re.sub('\>', '(RAbracket)', text)
    if '*' in text : text = re.sub('\*', '(asterisk)', text)
    if '?' in text : text = re.sub('\?', '(Qmark)', text)
    if '/' in text : text = re.sub('\/', '(Fslash)', text)
    if '"' in text : text = re.sub('\"', '(Dquote)', text)
    if ':' in text : text = re.sub('\:', '(colon)', text)
    if '|' in text : text = re.sub('\|', '(pipe)', text)
    if '%' in text : text = re.sub('\%', '(percent)', text)
    return text