import os
import time

import pyttsx3
import spotipy
import spotipy.util as util
import queue
import json
from subprocess import Popen


# def play_all_playlist_names():
#     clear_queue()
#
#     playlists = sp.user_playlists(user=sp.current_user()['display_name'])
#     indexed_playlists = zip(playlists['items'], range(1, len(playlists['items'])))
#     convert = lambda playlist, index: str(index) + " " + playlist['name']
#
#     [q.put(convert(playlist, index)) for (playlist, index) in indexed_playlists]
#     play_all_playlist_names_thread(q)
#
#
# def clear_queue():
#     with q.mutex:
#         q.queue.clear()
#
#
# def playlist_selected(number):
#     playlists = sp.user_playlists(user=sp.current_user()['display_name'])
#     if len(playlists['items']) > 0 and number < len(playlists['items']):
#         playlist_to_play = sp.playlist(playlists['items'][number]['id'])
#         for track in playlist_to_play['tracks']['items']:
#             sp.add_to_queue(track['track']['uri'])
#
#
# def play_all_playlist_names_thread(queue_of_names: 'queue.Queue[str]'):
#     while not queue_of_names.empty():
#         engine.say(queue_of_names.get())
#     engine.runAndWait()


def get_device_id():
    if is_active():
        return sp.devices()['devices'][0]['id']


def clear_queue():
    sp.shuffle(get_device_id())


def next_track():
    sp.next_track(get_device_id())


def set_volume(percentage):
    sp.volume(percentage, get_device_id())


def previous_track():
    sp.previous_track(get_device_id())


def is_active():
    devices = sp.devices()
    if len(devices['devices']) == 0:
        open_spotify()
    return True


def open_spotify():
    while True:
        Popen([r"" + spotify_home_url], close_fds=True, stdin=None, stdout=None,
              stderr=None)
        time.sleep(5)
        if len(sp.devices()['devices']) == 0:
            print('Spotify isnt starting')
            print('trying again')
        else:
            return


def pause_playback():
    if is_active():
        if sp.currently_playing()['is_playing']:
            sp.pause_playback(get_device_id())


def start_playback():
    if is_active():
        if sp.currently_playing() is None:
            sp.add_to_queue(sp.current_user_recently_played()['items'][0]['track']['uri'], get_device_id())
            sp.start_playback(get_device_id())
        else:
            if not sp.currently_playing()['is_playing']:
                sp.start_playback(get_device_id())


username = "9J9BwPhlT96qBagKnJUu7w"

scope = 'ugc-image-upload,' \
        'user-read-recently-played,' \
        'user-read-playback-state,' \
        'user-top-read,' \
        'app-remote-control,' \
        'playlist-modify-public,' \
        'user-modify-playback-state,' \
        'playlist-modify-private,' \
        'user-follow-modify,' \
        'user-read-currently-playing,' \
        'user-follow-read,' \
        'user-library-modify,' \
        'user-read-playback-position,' \
        'playlist-read-private,' \
        'user-read-email,' \
        'user-read-private,' \
        'user-library-read,' \
        'playlist-read-collaborative,' \
        'streaming'

with open('Controlify_Config') as json_file:
    data = json.load(json_file)
    client_id = data['client_id']
    client_secret = data['client_secret']
    spotify_home_url = data['spotify_home_url']

try:
    token = util.prompt_for_user_token(username, scope=scope,
                                       client_id=client_id,
                                       client_secret=client_secret,
                                       redirect_uri='http://google.com/')
except Exception as ex:
    os.remove(f".cache-{username}")
    token = util.prompt_for_user_token(username, scope=scope,
                                       client_id=client_id,
                                       client_secret=client_secret,
                                       redirect_uri='http://google.com/')

sp = spotipy.Spotify(auth=token)
device_id = get_device_id()

q = queue.Queue()
engine = pyttsx3.init()
engine.setProperty('rate', 125)
engine.setProperty('volume', 0.7)
voices = engine.getProperty('voices')
engine.setProperty('voice', voices[1].id)

