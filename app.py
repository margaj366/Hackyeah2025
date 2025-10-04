from flask import Flask, render_template, request, redirect, url_for
from datetime import datetime, timedelta

app = Flask(__name__)

playlists = [
        {
            'name': 'Wild Dances',
            'colors': [
                'linear-gradient(135deg, #667eea 0%, #764ba2 100%)',
                'linear-gradient(135deg, #f093fb 0%, #f5576c 100%)',
                'linear-gradient(135deg, #4facfe 0%, #00f2fe 100%)',
                'linear-gradient(135deg, #43e97b 0%, #38f9d7 100%)'
            ]
        },
        {
            'name': 'Cooldown Beats',
            'colors': [
                'linear-gradient(135deg, #fa709a 0%, #fee140 100%)',
                'linear-gradient(135deg, #30cfd0 0%, #330867 100%)',
                'linear-gradient(135deg, #a8edea 0%, #fed6e3 100%)',
                'linear-gradient(135deg, #ff9a9e 0%, #fecfef 100%)'
            ]
        },
        {
            'name': 'Summer Vibes',
            'colors': [
                'linear-gradient(135deg, #667eea 0%, #764ba2 100%)',
                'linear-gradient(135deg, #f093fb 0%, #f5576c 100%)',
                'linear-gradient(135deg, #4facfe 0%, #00f2fe 100%)',
                'linear-gradient(135deg, #43e97b 0%, #38f9d7 100%)'
            ]
        },
        {
            'name': 'Workout Power',
            'colors': [
                'linear-gradient(135deg, #fa709a 0%, #fee140 100%)',
                'linear-gradient(135deg, #30cfd0 0%, #330867 100%)',
                'linear-gradient(135deg, #a8edea 0%, #fed6e3 100%)',
                'linear-gradient(135deg, #ff9a9e 0%, #fecfef 100%)'
            ]
        }
    ]

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
                           playlists=playlists,
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


@app.route('/training')
def training():
    return render_template('index.html',
                           title='Home',
                           week=calendar_data(),
                           today=datetime.today().date().day,
                           playlists=playlists,
                           explore=explore)

@app.route('/statistics')
def statistics():
    return render_template('index.html',
                           title='Home',
                           week=calendar_data(),
                           today=datetime.today().date().day,
                           playlists=playlists,
                           explore=explore)

@app.route('/settings')
def settings():
    return render_template('index.html',
                           title='Home',
                           week=calendar_data(),
                           today=datetime.today().date().day,
                           playlists=playlists,
                           explore=explore)

if __name__ == '__main__':
    app.run(debug=True)