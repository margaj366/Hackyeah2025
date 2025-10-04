# --- Naprawa kompatybilności madmom z Pythonem 3.9+ ---
import collections
import random
from exercise_base import exercise_40, exercise_60, exercise_80, exercise_100, exercise_120, exercise_160

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
# Path to the playlist
folder = f"playlists/{playlist_name}"

matching_exercises = []

# Create madmom processor
beat_proc = madmom.features.beats.RNNBeatProcessor()
tempo_proc = madmom.features.tempo.TempoEstimationProcessor(fps=100, min_bpm=40, max_bpm=220)

# Przechodzimy po wszystkich plikach
for file in os.listdir(folder):
    if file.lower().endswith(('.mp3', '.wav', '.flac', '.ogg')):
        path = os.path.join(folder, file)
        print(f"Analizuję: {file}")

        # Wyodrębnienie rytmu i tempa
        act = beat_proc(path)
        tempo = tempo_proc(act)
        bpm = tempo[0][0]

        print(f"   → Wykryte tempo: {bpm:.2f} BPM")

        if bpm < 60:
            matching_exercises.append(random.choice(exercise_40))
        elif 60 <= bpm < 80:
            matching_exercises.append(random.choice(exercise_60))
        elif 80 <= bpm < 100:
            matching_exercises.append(random.choice(exercise_80))
        elif 100 <= bpm < 140:
            matching_exercises.append(random.choice(exercise_100))
        elif 140 <= bpm < 160:
            matching_exercises.append(random.choice(exercise_120))
        else:
            matching_exercises.append(random.choice(exercise_160))

print(matching_exercises)
