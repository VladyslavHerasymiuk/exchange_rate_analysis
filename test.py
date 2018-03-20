import unittest
from exchange_rate_analysis import functions
from mock import patch
import requests
import eventlet


class TestExchangeRateAnalysis(unittest.TestCase):

    @patch('sys.exit')
    @patch('sys.stdout')
    @patch('requests.get')
    def test_request_get_ConnectionError(self, mock_get,
                                         mock_stdout, mock_exit):
        mock_get.side_effect = requests.exceptions.ConnectionError
        functions.request_get('https://www.oschadgfbank.ua/')
        mock_exit.assert_called_once_with()
        self.assertIsNotNone(mock_stdout.getvalue())

    @patch('sys.exit')
    @patch('sys.stdout')
    @patch('requests.get')
    def test_request_get_RequestException(self, mock_get,
                                          mock_stdout, mock_exit):
        mock_get.side_effect = requests.exceptions.RequestException
        functions.request_get(1)
        mock_exit.assert_called_once_with()
        self.assertIsNotNone(mock_stdout.getvalue())

    @patch('sys.exit')
    @patch('sys.stdout')
    @patch('requests.get')
    def test_request_get_ReadTimeout(self, mock_get,
                                     mock_stdout, mock_exit):
        mock_get.side_effect = requests.exceptions.ReadTimeout
        functions.request_get('https://www.oschadbank.ua/')
        mock_exit.assert_called_once_with()
        self.assertIsNotNone(mock_stdout.getvalue())

    @patch('sys.exit')
    @patch('sys.stdout')
    @patch('requests.get')
    def test_request_get_Timeout(self, mock_get,
                                 mock_stdout, mock_exit):
        mock_get.side_effect = eventlet.timeout.Timeout
        functions.request_get('https://www.oschadbank.ua/')
        mock_exit.assert_called_once_with()
        self.assertIsNotNone(mock_stdout.getvalue())

    def test_request_get_200(self):
        with patch('requests.get') as mock_request:
            url = 'https://www.oschadbank.ua/'
            mock_request.return_value.status_code = 200
            self.assertTrue(functions.request_get(url))
            mock_request.assert_called_once_with(url)

    def test_parse_rate_in_UniversalBank(self):
        text = open('static/universal.html', 'r')
        result = functions.parse_rate_in_UniversalBank(text.read())
        self.assertEqual(result, {'USD': {'buy': '26.30', 'sell': '26.50'},
                                  'EUR': {'buy': '32.35', 'sell': '32.70'}})

    def test_parse_rate_in_OschadBank(self):
        text = open('static/oschad.html', 'r')
        result = functions.parse_rate_in_OschadBank(text.read())
        self.assertEqual(result, {'USD': {'buy': '26,2000',
                                          'sell': '26,8500'},
                                  'EUR': {'buy': '32,0000',
                                          'sell': '32,8500'}})

    def test_parse_rate_in_PravexBank(self):
        text = open('static/pravex.html', 'r')
        result = functions.parse_rate_in_PravexBank(text.read())
        self.assertEqual(result, {'USD': {'buy': '26.2', 'sell': '26.49'},
                                  'EUR': {'buy': '32.35', 'sell': '32.8'}})

    def test_readBanksUrls_withoutErr(self):
        result = functions.readBanksUrls('static/BanksUrls.xml')
        self.assertEqual(result, ('https://www.universalbank.com.ua/',
                                  'https://www.oschadbank.ua/',
                                  'https://www.pravex.com.ua/'))

    def test_readBanksUrls_withErr(self):
        self.assertFalse(functions.readBanksUrls('static/BankUrls.xml'))

    def test_from_dict_to_xml(self):
        self.assertIsNone(functions.from_dict_to_xml(({'USD': {'buy': '26.30',
                                                               'sell': '26.50'},
                                                       'EUR': {'buy': '32.35',
                                                               'sell': '32.70'}},
                                                      {'USD': {'buy': '26,2000',
                                                               'sell': '26,8500'},
                                                       'EUR': {'buy': '32,0000',
                                                               'sell': '32,8500'}},
                                                      {'USD': {'buy': '26.2',
                                                               'sell': '26.49'},
                                                       'EUR': {'buy': '32.35',
                                                               'sell': '32.8'}})))


if __name__ == '__main__':
    unittest.main()
