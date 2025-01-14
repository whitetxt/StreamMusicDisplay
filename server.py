print("Starting...")
import json
import signal
import time
import asyncio
import websockets
import spotipy
from threading import Thread, Lock
from spotipy.oauth2 import SpotifyOAuth

with open(".env") as f:
    lines = f.readlines()
    client_id = lines[0].strip()
    client_secret = lines[1].strip()

redirect_uri = "http://localhost:8888/callback"

sp = spotipy.Spotify(
    auth_manager=SpotifyOAuth(
        client_id=client_id,
        client_secret=client_secret,
        redirect_uri=redirect_uri,
        scope="user-read-currently-playing",
    )
)
print("Spotify authenticated")

last_track, last_artist, last_icon_url = "", "", ""

running = True
run_lock = Lock()

jobs = []
jobs_lock = Lock()


def get_playing():
    results = sp.currently_playing("GB")
    if results is None:
        return "No song playing", "", ""
    name = results["item"]["name"]
    artist = ", ".join(x["name"] for x in results["item"]["artists"])
    icon = results["item"]["album"]["images"][0]["url"]
    best_size = 10000
    for i in results["item"]["album"]["images"]:
        if i["height"] < best_size and i["height"] > 100:
            best_size = i["height"]
            icon = i["url"]
    return name, artist, icon


def track_info():
    global last_track, last_artist, last_icon_url
    while True:
        track, artist, icon_url = get_playing()
        if track != last_track or artist != last_artist or icon_url != last_icon_url:
            print("Waiting for lock to change")
            with jobs_lock:
                last_track, last_artist, last_icon_url = track, artist, icon_url
                print(f"Song changed: {track} - {artist} - {icon_url}")

        time.sleep(1)
        with run_lock:
            if not running:
                print("Track info quit")
                break


async def web_cb(websocket):
    global last_track, last_artist, last_icon_url
    last_sent = ""
    while not websocket.closed:
        with jobs_lock:
            song_json = json.dumps(
                {"title": last_track, "artist": last_artist, "icon": last_icon_url}
            )
            if last_sent != song_json:
                await websocket.send(song_json)
                last_sent = song_json

        await asyncio.sleep(1)
        with run_lock:
            if not running:
                print("Websocket connection quit")
                break


def sig_int(sig, frame):
    print("Stopping...")
    with run_lock:
        global running
        running = False


async def websocket():
    async with websockets.serve(web_cb, "localhost", 5678):
        while True:
            with run_lock:
                if not running:
                    print("Websocket quit")
                    break
            await asyncio.sleep(1)


if __name__ == "__main__":
    signal.signal(signal.SIGINT, sig_int)
    print("CTRL+C to stop.")
    thread = Thread(target=track_info)
    thread.start()
    asyncio.run(websocket())
    thread.join()
    print("Exit")

# import datetime

# import random


# async def show_time(websocket):

#     while True:

#         message = datetime.datetime.utcnow().isoformat() + "Z"

#         await websocket.send(message)

#         await asyncio.sleep(random.random() * 2 + 1)


# async def main():

#     async with websockets.serve(show_time, "localhost", 5678):

#         await asyncio.Future()  # run forever


# if __name__ == "__main__":

#     asyncio.run(main())
