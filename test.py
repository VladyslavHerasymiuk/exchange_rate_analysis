import unittest
import main

class TestExchangeRateAnalysis(unittest.TestCase):

    def test_parse_rate_in_UniversalBank(self):
        text = open('static/universal.html', 'r')
        result = main.parse_rate_in_UniversalBank(text.read())
        self.assertEqual(result, {'USD': {'buy': '26.30', 'sell': '26.50'},
                                  'EUR': {'buy': '32.35', 'sell': '32.70'}})

    def test_parse_rate_in_OschadBank(self):
        text = open('static/oschad.html', 'r')
        result = main.parse_rate_in_OschadBank(text.read())
        self.assertEqual(result, {'USD': {'buy': '26,2000', 'sell': '26,8500'},
                                  'EUR': {'buy': '32,0000', 'sell': '32,8500'}})

    def test_parse_rate_in_PravexBank(self):
        text = open('static/pravex.html', 'r')
        result = main.parse_rate_in_PravexBank(text.read())
        self.assertEqual(result, {'USD': {'buy': '26.2', 'sell': '26.49'},
                                  'EUR': {'buy': '32.35', 'sell': '32.8'}})

if __name__ == '__main__':
    unittest.main()
