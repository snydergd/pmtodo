#!/bin/env python

from flaskDB import db
from flask import Flask, render_template, request
app = Flask(__name__)
app.debug = True

@app.route('/task/<int:task>')
def task_view(task):
    if request.method == 'POST':
        if request.form['action'] == 'delete':
            pass
        elif request.form['action'] == 'rename':
            pass
        elif request.form['action'] == 'add':
            pass
    return render_template('task.html', task=task)

@app.route('/')
def task_list():
    return 'Hello world'

@app.route('/schedule_list')
def schedule_list():
    return 'Hello world'
    
if __name__ == '__main__':
    
    app.run()

