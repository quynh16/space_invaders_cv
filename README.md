# Space Invaders with Computer Vision

This Python application is a simple implementation of the classic game Space Invaders, except it is played using only hand gestures.

![Demo of game play](./demo_short.gif)

# Setup

### Dependencies
[Python 3](https://www.python.org/downloads/)
[pipenv](https://pipenv.pypa.io/en/latest/installation/)

### Install
Clone this repository. Then from inside the repository, run:

```
pipenv install
```

to install all dependencies.

### Run
Navigate into the `src` directory and run:

```
python3 main.py
```

to run the app.

# How to Play

The game is played with both hands. To ensure a smooth experience, try to keep both hands on screen at all times.

### Moving

To move, move your `right hand` left and right.

### Shooting

To shoot, pinch your `left hand`'s index and thumb together. Ensure your left hand is fully open when not shooting to allow the program to more easily detect and track your hand.
