from flask import Flask, render_template, request, redirect, url_for
from datetime import datetime, timedelta

app = Flask(__name__)

@app.route('/')
def home():
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
        }
    ]

    explore = [
        {'name': 'Funky HIIT'},
        {'name': 'POP Queens Cardio'}
    ]
    return render_template('index.html',
                           title='Home',
                           week=calendar_data(),
                           today=datetime.today().date().day,
                           playlists=playlists,
                           explore=explore)

def calendar_data():
    # Mock data to match the mockup
    weekdays = [
        (27, 'Mon', 0, 0),  # Past day
        (28, 'Tue', 0, 1),  # Past day
        (29, 'Wed', 1, 2),  # Completed day (with checkmark)
        (30, 'Thu', 0, 3),  # Past day
        (1, 'Fri', 0, 4),   # Current day (today)
        (2, 'Sat', 0, 5),   # Future day
        (3, 'Sun', 0, 6)    # Future day
    ]
    return weekdays


if __name__ == '__main__':
    app.run(debug=True)