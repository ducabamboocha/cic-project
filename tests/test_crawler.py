import unittest
from unittest.mock import patch

from scripts import crawler

ACCESS_TOKEN_DATA = {"access_token": "test",
                     "token_type": "bearer",
                     "expires_in": 86399,
                     "scope": "services",
                     "iss": "IWT",
                     "creation_offset_date_time": "2022-04-27T19:19:36.513600+02:00",
                     "tenant": "immowelt",
                     "jti": "p4YoqRjCW9ww6ElSvrpe5ustQKo"}

LISTING_DATA = {'items': {}}


class TestCrawler(unittest.TestCase):

    @patch('scripts.crawler.requests.post')
    def test_get_access_token(self, mock_post):
        mock_post.return_value.json.return_value = ACCESS_TOKEN_DATA
        access_token_resp = crawler.get_access_token()
        self.assertEqual(access_token_resp, "test")

    @patch('scripts.crawler.requests.post')
    def test_get_access_token_invalid_response(self, mock_post):
        mock_post.return_value.json.return_value = "test"
        access_token_resp = crawler.get_access_token()
        self.assertEqual(access_token_resp, None)

    def test_get_listings(self):
        with patch('scripts.crawler.get_access_token') as mock_get_access_token:
            with patch('scripts.crawler.requests.post') as mock_post:
                mock_get_access_token.return_value = 'test'
                mock_post.return_value.json.return_value = LISTING_DATA

                listings = crawler.get_listings()
                self.assertEqual(listings, {})

    def test_get_listings_invalid_response(self):
        with patch('scripts.crawler.get_access_token') as mock_get_access_token:
            with patch('scripts.crawler.requests.post') as mock_post:
                mock_get_access_token.return_value = 'test'
                mock_post.return_value.json.return_value = {'error'}

                listings = crawler.get_listings()
                self.assertEqual(listings, [])


if __name__ == "__main__":
    unittest.main()
