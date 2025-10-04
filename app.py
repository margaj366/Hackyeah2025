from flask import Flask, render_template, request, redirect, url_for
from datetime import datetime, timedelta

app = Flask(__name__)

@app.route('/')
def home():
    week = calendar_date()
    today = datetime.today().date().day
    print("Week data:", week)  # Debug - sprawdź w konsoli
    print("Length:", len(week))
    print("Today: ", today)
    return render_template('index.html',
                           title='Home',
                           week=week,
                           today=today)

def calendar_date():
    today = datetime.today()
    weekday = today.weekday()
    cnt = 0
    while weekday > 0:
        today -= timedelta(days=1)
        weekday -= 1
        cnt += 1
    weekdays = []
    for i in range(7):
        weekdays.append((today.day, today.strftime('%a')))
        today += timedelta(days=1)
    return weekdays


if __name__ == '__main__':
    app.run(debug=True)