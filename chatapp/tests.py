from django.test import TestCase


class ChatViewTests(TestCase):
    def test_rule_based_reply(self):
        resp = self.client.get('/chat/?message=hello')
        self.assertEqual(resp.status_code, 200)
        data = resp.json()
        self.assertIn('reply', data)
        self.assertIn('hello', data['message'].lower())

    def test_scrape_mode_without_url(self):
        resp = self.client.get('/chat/?mode=scrape')
        self.assertEqual(resp.status_code, 200)
        data = resp.json()
        self.assertEqual(data.get('mode'), 'scrape')

    def test_ai_mode_falls_back_without_key(self):
        resp = self.client.get('/chat/?message=test&mode=ai')
        self.assertEqual(resp.status_code, 200)
        data = resp.json()
        self.assertIn('reply', data)
