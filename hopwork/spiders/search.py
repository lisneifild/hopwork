# -*- coding: utf-8 -*-
import os
import bs4
import json
import scrapy
from hopwork.items import ProfileItem
from hopwork.settings import BASE_DIR
from hopwork.tools import SearchRequests


class SearchSpider(scrapy.Spider):
    # Spider name
    name = 'search'

    # Allowed to parse
    allowed_domains = ['www.hopwork.fr']

    # Initial search requests helper
    form = SearchRequests('https://www.hopwork.fr/')

    def __init__(self, name='results.csv', *args, **kwargs):
        """
        :param o: Output file name
        :param args:
        :param kwargs:
        """
        super(SearchSpider, self).__init__(*args, **kwargs)

        self.output_file = os.path.join(BASE_DIR, 'output', name)

    def start_requests(self):
        """
        Search keywords requests
        :return:
        """
        yield self.form.signup_request(self.search_requests)

    def search_requests(self, response):
        """
        Parse page list
        :param response:
        :return:
        """
        print('Signed up new user: {email}@{password}'.format(
            email=response.request.meta['email'],
            password=response.request.meta['password']
        ))

        # Search
        for request in self.form.requests(callback=self.page_request):
            yield request

    def page_request(self, response):
        """
        Request each search page
        :param response:
        :return:
        """
        bs = bs4.BeautifulSoup(response.body_as_unicode(), 'html.parser')

        # Find last page number
        try:
            last_page = int(bs.find_all('a', attrs={'class': 'results-pager__item'})[-1].text.strip())
            for page_number in range(1, last_page+1):
                yield self.form.profiles(
                    callback=self.parse_page,
                    keyword=response.meta['query'],
                    page=page_number
                )
        # Request only one page
        except:
            yield self.form.profiles(
                callback=self.parse_page,
                keyword=response.meta['query'],
                page=1
            )

    def parse_page(self, response):
        """
        Parses search response page
        :param response:
        :return:
        """
        data = json.loads(response.body_as_unicode())

        for profile in data['profiles']:
            yield self.form.profile_details(
                callback=self.parse_profile,
                canonical=profile['canonicalUrl'],
                meta={
                    'profile': profile
                },
            )

    def parse_profile(self, response):
        """
        Parse response of detailed profile page
        :param response:
        :return:
        """
        bs = bs4.BeautifulSoup(response.body_as_unicode(), 'html.parser')

        # Create empty item
        profile = ProfileItem()
        profile['url'] = response.request.url

        # Get json profile data
        json_profile = response.meta['profile']

        # Profile first name and name
        profile['first_name_profile'] = json_profile['firstName']
        profile['name_profile'] = json_profile['normalizedLastName']

        # Parse recommendations
        for rec in bs.find_all('section', attrs={'class': 'profile-listing-item'}):
            yield self.get_recommendation_info(profile.copy(), rec)

    def get_recommendation_info(self, item, html):
        """
        Parse information about recommendation
        :param item:
        :param html:
        :return:
        """
        # Parse job title
        try:
            item['job_title'] = html.find('p', attrs={'class': 'profile-listing-item__subtitle'}).text
        except Exception as e:
            pass

        # Parse skills
        try:
            item['job_skills'] = ', '.join(
                list(
                    map(
                        lambda x: x.text.strip(),
                        html.find('ul', attrs={'class': 'skill-list'}).find_all('span')
                    )
                )
            )
        except Exception as e:
            item['job_skills'] = ''

        # Parse company
        try:
            item['job_company'] = html.get('data-experiencecompany')
        except Exception as e:
            pass

        # Parse duration & location
        el = html.find('small', attrs={'class': 'secondary'}).text.split('|')
        try:
            item['job_duration'] = el[0].strip().split('-')[0].strip()
            item['job_location'] = el[1].strip() if len(el) > 1 else ''
        except Exception as e:
            pass

        # Parse description
        try:
            item['job_description'] = html.find('div', attrs={'class': 'u-mb3'}).text.strip()

            # Recommendation first_name & last_name
            try:
                rec = html.find('ul', attrs={'class': 'xp-reco__list'})
                if rec.text.strip():
                    el = rec.find('p', attrs={'class': 'u-mb1'}).find('strong').text.strip().split(' ')
                    item['recommendation_first_name'] = el[0].strip()
                    item['recommendation_last_name'] = el[1].strip()
            except Exception as e:
                pass
        except Exception as e:
            item['job_description'] = ''
            item['recommendation_first_name'] = ''
            item['recommendation_last_name'] = ''

        return item
