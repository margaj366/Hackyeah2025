# --- Naprawa kompatybilności madmom z Pythonem 3.9+ ---
import collections
import math
from mutagen import File
import random
import pygame
import time
from exercise_base import exercise_40, exercise_60, exercise_80, exercise_100, exercise_120, exercise_140, exercise_160

if not hasattr(collections, 'MutableSequence'):
    import collections.abc
    collections.MutableSequence = collections.abc.MutableSequence

# --- Ukrycie ostrzeżeń o pkg_resources ---
import warnings
warnings.filterwarnings("ignore", category=UserWarning)

import numpy as np
# --- Łatka dla nowych wersji numpy ---
if not hasattr(np, 'float'):
    np.float = float
if not hasattr(np, 'int'):
    np.int = int
if not hasattr(np, 'bool'):
    np.bool = bool

import os
import madmom

playlist_name = input('Enter playlist name: ')
exercise_length = input('Enter exercise length: ')

# Path to the playlist
folder = f"playlists/{playlist_name}"

warmup_songs = {}
training_songs = {}
post_training_songs = {}

training_plan = {}

# Create madmom processor
beat_proc = madmom.features.beats.RNNBeatProcessor()
tempo_proc = madmom.features.tempo.TempoEstimationProcessor(fps=100, min_bpm=40, max_bpm=220)

# Iteration through files
for file in os.listdir(folder):
    if file.lower().endswith(('.mp3', '.wav', '.flac', '.ogg')):
        path = os.path.join(folder, file)
        print(f"Analizuję: {file}")

        #Get length of audio
        audio = File(path)
        length = audio.info.length
        exercise_length = float(exercise_length)
        exercise_num = max(1, math.floor(length / exercise_length))

        # Get rythm and pace
        act = beat_proc(path)
        tempo = tempo_proc(act)
        bpm = tempo[0][0]

        print(f"   → Wykryte tempo: {bpm:.2f} BPM")

        if bpm < 70:
            post_training_songs[file] = [bpm, exercise_num]
        elif bpm > 100:
            training_songs[file] = [bpm, exercise_num]
        else:
            warmup_songs[file] = [bpm, exercise_num]


for song, [bpm, exercise_num] in warmup_songs.items():
    exercise_list = []
    for i in range(exercise_num):
        if bpm <= 100:
            exercise_list.append(random.choice(exercise_80))
        else:
            exercise_list.append(random.choice(exercise_60))
    training_plan[song] = exercise_list

for song, [bpm, exercise_num] in training_songs.items():
    exercise_list = []
    for i in range(exercise_num):
        if bpm < 120:
            exercise_list.append(random.choice(exercise_100))
        elif bpm < 140:
            exercise_list.append(random.choice(exercise_120))
        elif bpm < 160:
            exercise_list.append(random.choice(exercise_140))
        else:
            exercise_list.append(random.choice(exercise_160))
    training_plan[song] = exercise_list

for song, [bpm, exercise_num] in post_training_songs.items():
    exercise_list = []
    for i in range(exercise_num):
        if bpm < 60:
            exercise_list.append(random.choice(exercise_40))
        else:
            exercise_list.append(random.choice(exercise_60))
    training_plan[song] = exercise_list

for song, exercise_list in training_plan.items():
    print(song)
    for exercise in exercise_list:
        print(exercise)
    print()

pygame.mixer.init()

for song, exercise in training_plan.items():
    print(f"Playing song: {song}")
    song_path = f"playlists/{playlist_name}/{song}"
    pygame.mixer.music.load(song_path)
    pygame.mixer.music.play()
    for e in exercise:
        print(f"Current exercise: {e}")
        start_time = time.time()
        while time.time() - start_time < exercise_length:
            time.sleep(1)
            remaining = exercise_length - int(time.time() - start_time)
            print(f"   {remaining}s left", end="\r")
    pygame.mixer.music.stop()