import unittest
from sort import sort, build_table


def create_list_from_sample(sample) -> list:
    """Creates a mockup of the list of dict used in the app"""
    to_return_list = []
    for i in range(len(sample)):
        to_return_list.append({  # only the airline_sentiment_confidence is really used, the other lines are ignored
            "id": f"random with confidence {str(sample[i])}",
            "airline_sentiment": f"random with confidence {str(sample[i])}",
            "airline_sentiment_confidence": str(sample[i]),
            "airline": f"random with confidence {str(sample[i])}",
            "text": f"random with confidence {str(sample[i])}"
        })
    return to_return_list


class TestBubbleSort(unittest.TestCase):

    def test_bubble_sort_with_positive_numbers(self):
        """test if a given sample of 7 entries is sorted correctly"""
        sample = [5, 0.01, 4, 0, 2.5, 4, 1]
        sorted_sample = [0, 0.01, 1, 2.5, 4, 4, 5]
        to_sort_list = create_list_from_sample(sample)
        sorted_list = create_list_from_sample(sorted_sample)
        self.assertEqual(sort(to_sort_list), sorted_list)

    def test_bubble_sort_empty_list(self):
        """Check that empty list are managed correctly"""
        self.assertEqual(sort([]), [])

    def test_build_table_first_entry(self):
        """Test that the first entry of the table is what's expected"""
        table = build_table('../static/data/Kaggle_TwitterUSAirlineSentiment.csv')
        expected = {
            'id': '1',
            'airline_sentiment': 'positive',
            'airline_sentiment_confidence': '1',
            'airline': 'Virgin America',
            'text': '@VirginAmerica just got on the 1pm in Newark home to LA. Your folks at EWR are incredible #letsgohome'
            }
        self.assertEqual(table[0], expected)

    def test_build_table_last_entry(self):
        """Test that the last entry of the table is what's expected"""
        table = build_table('../static/data/Kaggle_TwitterUSAirlineSentiment.csv')
        expected = {
            'id': '200',
            'airline_sentiment': 'negative',
            'airline_sentiment_confidence': '1',
            'airline': 'American',
            'text': '@AmericanAir why would I even consider continuing your point program when I received no perks or continued bad customer service? #senseless'
        }
        self.assertEqual(table[len(table)-1], expected)


if __name__ == '__main__':
    unittest.main(verbosity=2)
