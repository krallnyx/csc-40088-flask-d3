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
    tenure_labels = ['Bad Flight', 'Cancelled Flight', "Can't Tell", 'Customer Service Issue', 'Damaged Luggage',
                     'Flight Attendant Complaints', 'Flight Booking Problems', 'Late Flight', 'longlines',
                     'Lost Luggage']
    select_df = cleaned_df_creative[["airline", "negative_reason"]]
    # cleaned_df_creative['negative_reason'] = pd.cut(cleaned_df_creative.negative_reason, range(0, 81, 10), labels=tenure_labels)
    # select_df = cleaned_df_creative[['tenure_group','Contract']]
    american = select_df[select_df['airline'] == 'American']
    delta = select_df[select_df['airline'] == 'Delta']
    southwest = select_df[select_df['airline'] == 'Southwest']
    united = select_df[select_df['airline'] == 'United']
    us_airways = select_df[select_df['airline'] == 'US Airways']
    virgin_america = select_df[select_df['airline'] == 'Virgin America']
    _ = american.groupby('negative_reason').size().values
    american_percent = calculate_percentage(_, np.sum(_))
    _ = delta.groupby('negative_reason').size().values
    delta_percent = calculate_percentage(_, np.sum(_))
    _ = southwest.groupby('negative_reason').size().values
    southwest_percent = calculate_percentage(_, np.sum(_))
    _ = united.groupby('negative_reason').size().values
    united_percent = calculate_percentage(_, np.sum(_))
    _ = us_airways.groupby('negative_reason').size().values
    us_airways_percent = calculate_percentage(_, np.sum(_))
    _ = virgin_america.groupby('negative_reason').size().values
    virgin_america_percent = calculate_percentage(_, np.sum(_))
    _ = select_df.groupby('negative_reason').size().values
    all_percent = calculate_percentage(_, np.sum(_))

    barchart_data = []
    data_creation(barchart_data, all_percent, tenure_labels, "All")
    data_creation(barchart_data, american_percent, tenure_labels, "American")
    data_creation(barchart_data, delta_percent, tenure_labels, "Delta")
    data_creation(barchart_data, southwest_percent, tenure_labels, "Southwest")
    data_creation(barchart_data, united_percent, tenure_labels, "United")
    data_creation(barchart_data, us_airways_percent, tenure_labels, "US Airways")
    data_creation(barchart_data, virgin_america_percent, tenure_labels, "Virgin America")
    return jsonify(barchart_data)


if __name__ == "__main__":
    app.run(debug=True)
