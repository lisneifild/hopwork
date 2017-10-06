# -*- coding: utf-8 -*-
import scrapy


class ProfileItem(scrapy.Item):
    url = scrapy.Field()

    first_name_profile = scrapy.Field()
    name_profile = scrapy.Field()

    job_title = scrapy.Field()
    job_skills = scrapy.Field()
    job_company = scrapy.Field()
    job_duration = scrapy.Field()
    job_location = scrapy.Field()
    job_description = scrapy.Field()

    recommendation_first_name = scrapy.Field()
    recommendation_last_name = scrapy.Field()

    @property
    def csv_line(self):
        return [
            self._values.get('url', ''),
            self._values.get('first_name_profile', ''),
            self._values.get('name_profile', ''),
            self._values.get('job_title', ''),
            self._values.get('job_skills', ''),
            self._values.get('job_company', ''),
            self._values.get('job_duration', ''),
            self._values.get('job_description', ''),
            self._values.get('recommendation_first_name', ''),
            self._values.get('recommendation_last_name', ''),
        ]
