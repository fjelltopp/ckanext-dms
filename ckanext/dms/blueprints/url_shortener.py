import string
import random
from flask import Blueprint
from flask.views import MethodView
from ckan.plugins.toolkit import request


def _generate_random_string(string_length=6):
    # taken from https://bit.ly/3nxGSMo
    alphanumeric_chars = string.ascii_lowercase + string.digits
    return ''.join(
        random.SystemRandom().choice(alphanumeric_chars)
        for _ in range(string_length)
    )


class CreateShortenedUrl(MethodView):
    def get(self):  # TODO: change to post
        post_body = request.args  # TODO: change to request.get_json()
        url = post_body['url']
        get_shortened_url = _generate_random_string()
        # TODO: interact with database
        # and return JSON of {'url_hash': 'xxxxxx'}
        return f'{get_shortened_url} should be used as the url_hash for {url}'


class GetShortenedUrl(MethodView):
    def get(self, url_hash):
        # TODO: interact with database
        # and replace with h.redirect
        return f'Searching database for Url with hash: {url_hash}'


url_shortener = Blueprint(
    u'url_shortener',
    __name__
)

url_shortener.add_url_rule(
    u'/link/create',
    view_func=CreateShortenedUrl.as_view('create_shortened_url')
)
url_shortener.add_url_rule(
    u'/link/<url_hash>',
    view_func=GetShortenedUrl.as_view('get_shortened_url')
)
