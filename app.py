import csv
import itertools

from flask import Flask, render_template, jsonify
import pandas as pd
import numpy as np

from test.sort import sort, build_table

app = Flask(__name__)

# Reading data for Creative
data_df_creative = pd.read_csv("static/data/Kaggle_TwitterUSAirlineSentiment.csv")
# removing the lines for airline_sentiment != negative so we can display the reasons it's negative
cleaned_df_creative = data_df_creative[(data_df_creative['airline_sentiment'] == "negative")]

@app.route('/')
def index():
    """home page, not in use"""
    return 'Welcome to Fundamentals of Computer Science'


@app.route('/basic')
def display_data_basic():
    """function rendering a table showing the first 40 entries of the lowest confidence (ascending)"""
    full_table = build_table()
    sorted_table = sort(full_table)
    return render_template("basic.html", tweetData=sorted_table[:40])


@app.route('/advanced')
def display_data_d3():
    """Function rendering a sortable table using d3.js"""
    return render_template("advanced.html")


@app.route('/creative')
def display_data_creative():
    return render_template("creative.html")


def calculate_percentage(val, total):
    """Calculates the percentage of a value over a total"""
    percent = np.round((np.divide(val, total) * 100), 2)
    return percent

def data_creation(data, percent, class_labels, group=None):
    for index, item in enumerate(percent):
        data_instance = {}
        data_instance['category'] = class_labels[index]
        data_instance['value'] = item
        data_instance['group'] = group
        data.append(data_instance)


@app.route('/get_piechart_data_creative')
def get_piechart_data_creative():
    airline_labels = ['American', 'Delta', 'Southwest', 'US Airways', 'United', 'Virgin America']
    view = cleaned_df_creative.groupby('airline').size().values
    class_percent = calculate_percentage(view, np.sum(view))  # Getting the value counts and total

    piechart_data = []
    data_creation(piechart_data, class_percent, airline_labels)
    return jsonify(piechart_data)


app.run(host='0.0.0.0', port=81)
