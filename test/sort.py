import itertools
import csv


def build_table(csv_file='static/data/Kaggle_TwitterUSAirlineSentiment.csv') -> list:
    """Function to read all the data from the CSV file and store it in an unsorted list"""
    with open(csv_file, encoding='utf-8-sig') as csv_file:
        data = csv.reader(csv_file, delimiter=',')
        first_line = True
        full_table = []
        for row in itertools.islice(data, 201):
            if not first_line:
                full_table.append({
                    "id": row[0],
                    "airline_sentiment": row[1],
                    "airline_sentiment_confidence": row[2],
                    "airline": row[4],
                    "text": row[6]
                })
            else:
                first_line = False
        return full_table


def sort(to_sort) -> list:
    """
    Function taking an unsorted list of dict
    sorting it on the value of the integer in position airline_sentiment_confidence
    """
    n = len(to_sort)
    for i in range(n):
        already_sorted = True
        for j in range(n - i - 1):
            if float(to_sort[j]['airline_sentiment_confidence']) > float(to_sort[j+1]['airline_sentiment_confidence']):
                to_sort[j], to_sort[j + 1] = to_sort[j + 1], to_sort[j]
                already_sorted = False
        if already_sorted:
            break
    return to_sort
