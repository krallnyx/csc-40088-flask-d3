import csv
import itertools

from flask import Flask, render_template, jsonify
import pandas as pd
import numpy as np
import logging

from test.sort import sort, build_table

logging.basicConfig(level=logging.DEBUG)

app = Flask(__name__)

# Reading data for Creative
data_df_creative = pd.read_csv("static/data/Kaggle_TwitterUSAirlineSentiment.csv")
# removing the lines for airline_sentiment != negative so we can display the reasons it's negative
cleaned_df_creative = data_df_creative[(data_df_creative['airline_sentiment'] == "negative")]


@app.route('/')
def index():
    """home page,with task2"""
    return render_template("index.html")


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


@app.route('/get_barchart_data')
def get_barchart_data():
    select_df = cleaned_df_creative[["airline", "negative_reason"]]
    airlines = ["American", "Delta", "Southwest", "United", "US Airways", "Virgin America"]
    barchart_data = []
    _ = select_df.groupby('negative_reason').size().values
    all_percent = calculate_percentage(_, np.sum(_))
    reason_labels = []
    reason_dict = {'Bad Flight': 'BadF', 'Cancelled Flight': 'CclF', "Can't Tell": 'CntT', 'Customer Service Issue': 'CSI',
                   'Damaged Luggage': 'DmgL', 'Flight Attendant Complaints': 'FAC', 'Flight Booking Problems': 'FBP',
                   'Late Flight': 'LatF', 'longlines': 'LgLi', 'Lost Luggage': 'Lost'}
    for _, row in select_df.iterrows():
        if row["negative_reason"] not in reason_labels:
            reason_labels.append(row["negative_reason"])
    short_label = []
    for long in reason_labels:
        short_label.append(reason_dict[long])
    data_creation(barchart_data, all_percent, short_label, "All")
    for airline in airlines:
        airline_data = select_df[select_df['airline'] == airline]
        _ = airline_data.groupby('negative_reason').size().values
        airline_percent = calculate_percentage(_, np.sum(_))
        reason_labels = []
        for _, row in airline_data.iterrows():
            if row["negative_reason"] not in reason_labels:
                reason_labels.append(row["negative_reason"])
        short_label = []
        for long in reason_labels:
            short_label.append(reason_dict[long])
        data_creation(barchart_data, airline_percent, short_label, airline)

    return jsonify(barchart_data)


if __name__ == "__main__":
    app.run(debug=True)
