# StreamMusicDisplay

A simple way to display the current Spotify song on your stream!

![The music display](/example/example.png)

## Features

- Fast song change detection
- Animations when changing songs
- Text Scrolling when song name is too long
- Loading animation for slow networks

## Usage

### Requirements

1. Python > 3.7, < 3.12
2. websockets
3. spotipy

### Installation Instructions

Ensure that a version of Python later than 3.7 and before 3.12 is installed.

Install the package requirements using:

```bash
pip install -r requirements.txt
```

Once pip has finished installing all the required packages, run server.py using:

```bash
python server.py
```

This will start the server needed for the webpage to communicate with it.

To integrate with OBS (or other similar streaming software), simply add `index.html` as a local file browser source.

## Showcase

### Song change animation

![An example of the song change animation](/example/animation.gif)

### Text scrolling

![An example of the text scrolling](/example/scrolling.gif)