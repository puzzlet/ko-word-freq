from ko_word_freq import webapp


def test_null():
    client = webapp.app.test_client()
    client.get('/')
