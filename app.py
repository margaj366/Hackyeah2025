from flask import Flask, render_template, request, redirect, url_for
from datetime import datetime, timedelta

app = Flask(__name__)

@app.route('/')
def home():
    return render_template('index.html',
                           title='Home',
                           week=calendar_data(),
                           today=datetime.today().date().day)

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


if __name__ == '__main__':
    app.run(debug=True)