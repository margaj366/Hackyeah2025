from flask import Flask, render_template, jsonify, request, send_from_directory, session
from datetime import timedelta
from collections import OrderedDict
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


def generate_training_plan(playlist_name, exercise_length):
    # Path to the playlist
    folder = f"playlists/{playlist_name}"

    warmup_songs = OrderedDict()
    training_songs = OrderedDict()
    post_training_songs = OrderedDict()

    training_plan = OrderedDict()

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

    return list(training_plan.items())


app = Flask(__name__)
app.secret_key = "super_secret_key"
app.permanent_session_lifetime = timedelta(minutes=30)


PLAYLISTS_DIR = "playlists"

from flask import Flask, render_template, request, redirect, url_for
from datetime import datetime, timedelta


# playlists = [d for d in os.listdir(PLAYLISTS_DIR) if os.path.isdir(os.path.join(PLAYLISTS_DIR, d))]

PLAYLISTS_DIR = "playlists"

GRADIENTS = [
    [
        'linear-gradient(135deg, #667eea 0%, #764ba2 100%)',
        'linear-gradient(135deg, #f093fb 0%, #f5576c 100%)',
        'linear-gradient(135deg, #4facfe 0%, #00f2fe 100%)',
        'linear-gradient(135deg, #43e97b 0%, #38f9d7 100%)'
    ],
    [
        'linear-gradient(135deg, #fa709a 0%, #fee140 100%)',
        'linear-gradient(135deg, #30cfd0 0%, #330867 100%)',
        'linear-gradient(135deg, #a8edea 0%, #fed6e3 100%)',
        'linear-gradient(135deg, #ff9a9e 0%, #fecfef 100%)'
    ]
]

# --- dynamiczne przypisywanie nazw i kolorów ---
def get_playlists():
    folder_names = [
        d for d in os.listdir(PLAYLISTS_DIR)
        if os.path.isdir(os.path.join(PLAYLISTS_DIR, d))
    ]

    playlists = []
    for i, name in enumerate(folder_names):
        # przypisanie kolorów cyklicznie (jeśli folderów więcej niż zestawów)
        color_scheme = GRADIENTS[i % len(GRADIENTS)]
        playlists.append({
            "name": name,
            "colors": color_scheme
        })
    return playlists


explore = [
        {'name': 'Funky HIIT'},
        {'name': 'POPs Cardio'}
        # {'name': 'Rock Strength'},
        # {'name': 'Chill Yoga'}
    ]

@app.route('/')
def home():

    return render_template('index.html',
                           title='Home',
                           week=calendar_data(),
                           today=datetime.today().date().day,
                           playlists=get_playlists(),
                           explore=explore)

def calendar_data():
    today = datetime.today()
    weekday = today.weekday()
    cnt = 0
    while weekday > 0:
        today -= timedelta(days=1)
        weekday -= 1
        cnt += 1
    weekdays = []
    for i in range(7):
        done = today.day % 2
        if today.day >= datetime.today().weekday():
            done = 0
        weekdays.append((today.day, today.strftime('%a'), done, today.weekday()))
        today += timedelta(days=1)
    return weekdays

@app.route("/playlist/<playlist>")
def show_playlist(playlist):
    length = request.args.get("length", 30)
    plan = generate_training_plan(playlist, length)

    # zapisz plan do sesji (jako JSON)
    session["last_plan"] = plan
    session["last_playlist"] = playlist
    session["last_length"] = length

    return render_template("playlist.html", playlist=playlist, plan=plan, length=length)
# def workout(playlist):
#     length = request.args.get("length", 30)
#     plan = generate_training_plan(playlist, length)
#     return render_template("playlist.html", playlist=playlist, plan= plan, length=length)

@app.route("/training/<playlist>")
def training_api(playlist):  # <-- zmieniona nazwa funkcji
    exercise_length = request.args.get("length", 30)
    plan = generate_training_plan(playlist, exercise_length)
    return jsonify(plan)

@app.route("/workout/<playlist>", endpoint="workout_page")
def workout(playlist):
    # pobierz dane z sesji, jeśli istnieją
    plan = session.get("last_plan")
    length = session.get("last_length", 30)
    saved_playlist = session.get("last_playlist")

    if not plan or saved_playlist != playlist:
        # fallback – jeśli użytkownik wszedł tu bez wcześniejszego planu
        plan = generate_training_plan(playlist, length)

    return render_template("workout.html", playlist=playlist, plan=plan, length=length, anim_file="animations/training.json")

@app.route("/songs/<playlist>/<filename>")
def serve_song(playlist, filename):
    folder = os.path.join("playlists", playlist)
    return send_from_directory(folder, filename)

#
# @app.route('/training')
# def training():
#     return render_template('index.html',
#                            title='Home',
#                            week=calendar_data(),
#                            today=datetime.today().date().day,
#                            playlists=playlists,
#                            explore=explore)
#
@app.route('/statistics')
def statistics():
    return render_template('statistics.html',
                           title='Home',
                           )
#
# @app.route('/settings')
# def settings():
#     return render_template('index.html',
#                            title='Home',
#                            week=calendar_data(),
#                            today=datetime.today().date().day,
#                            playlists=playlists,
#                            explore=explore)
@app.route('/training')
def training():
    return '', 204


@app.route('/settings')
def settings():
    return '', 204

if __name__ == '__main__':
    app.run(debug=True)