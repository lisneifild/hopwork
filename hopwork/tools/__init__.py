# -*- coding: utf-8 -*-
import os
import json
from faker import Faker
from hopwork.settings import BASE_DIR
from scrapy import Request, FormRequest

try:
    # Python 2.7
    from urllib import urlencode
    from urlparse import urljoin
except ImportError:
    # Python 3+
    from urllib.parse import urlencode, urljoin


class ConfigurationFailed(Exception):
    pass


class SearchRequests(object):
    """
    Search keywords generator
    """
    # File with the default request filter configured
    FILTER_FILE = os.path.join(BASE_DIR, 'filter.json')

    # File with the search keywords
    KEYWORDS_FILE = os.path.join(BASE_DIR, 'keywords.csv')

    # Endpoints
    SEARCH_ENDPOINT = '/s'
    SIGNUP_ENDPOINT = '/api/account/signup'
    PROFILE_ENDPOINT = '/search/api/profiles/v2'

    def __init__(self, base_url):
        """
        Create requests helper
        :param str base_url:
        """
        self._base_url = base_url
        self._keywords = []
        self._request_params = {}

        # Load request params
        try:
            with open(SearchRequests.FILTER_FILE, 'r') as f:
                self._request_params = json.loads(f.read())
                f.close()
        except Exception as e:
            raise ConfigurationFailed('Failed to load filter configurations: {}'.format(str(e)))

        # Load keywords
        try:
            with open(SearchRequests.KEYWORDS_FILE, 'r') as k:
                self._keywords = map(lambda x: x.strip().lower(), k.readlines())
                k.close()
        except Exception as e:
            raise ConfigurationFailed('Failed to load keywords list: {}'.format(str(e)))

    def request_params(self, custom):
        """
        Returns request params
        :param dict custom:
        :return dict:
        """
        params = self._request_params or dict()
        params.update(custom)
        return params

    def requests(self, callback):
        """
        Returns search Requests generator
        :return:
        """
        return [
            Request(
                method='GET',
                callback=callback,
                url='{url}?{query}'.format(
                    url=urljoin(self._base_url, self.SEARCH_ENDPOINT),
                    query=urlencode(self.request_params({'q': q}))
                ),
                meta={
                    'query': q,
                },
            ) for q in self._keywords
        ]

    def profile_url(self, canonical):
        """
        Returns absolute profile url
        :param canonical:
        :return:
        """
        return urljoin(self._base_url, canonical)

    def profile_details(self, callback, canonical, meta):
        """
        Returns profile detailed page request
        :param callable callback:
        :param str canonical:
        :param dict meta:
        :return:
        """
        return Request(
            method='GET',
            callback=callback,
            url=self.profile_url(canonical),
            meta=meta
        )

    def profiles(self, callback, keyword, page=1):
        """
        Returns profiles requests generator
        :param callable callback:
        :param str keyword:
        :param int page:
        :return:
        """
        return Request(
            method='GET',
            callback=callback,
            url='{url}?{query}'.format(
                url=urljoin(self._base_url, self.PROFILE_ENDPOINT),
                query=urlencode(self.request_params({'q': keyword, 'p': page}))
            ),
            meta={
                'query': keyword,
                'page': page
            },
        )

    def signup_request(self, callback):
        """
        Sends sign up request to parse other pages
        :return:
        """
        fake = Faker('fr_FR')

        user_data = {
            'email': fake.free_email(),
            'firstName': fake.first_name(),
            'lastName': fake.last_name(),
            'legals': True,
            'password': fake.password(length=10, special_chars=True, digits=True, upper_case=True, lower_case=True),
        }

        return Request(
            url=urljoin(self._base_url, self.SIGNUP_ENDPOINT),
            method='POST',
            callback=callback,
            body=json.dumps(user_data),
            meta=user_data,
            headers={'Content-Type': 'application/json'}
        )
