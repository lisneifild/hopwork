# -*- coding: utf-8 -*-
import csv
import os


class HopworkPipeline(object):
    """
    Process items
    """
    def process_item(self, item, spider):
        """
        Save item
        :param hopwork.items.ProfileItem item:
        :param hopwork.spiders.search.SearchSpider spider:
        :return:
        """
        if not os.path.exists(spider.output_file):
            with open(spider.output_file, 'a') as csv_file:
                result_writer = csv.writer(csv_file, delimiter=',', quotechar='"', quoting=csv.QUOTE_MINIMAL)
                result_writer.writerow(item.csv_headline)
                csv_file.close()

        with open(spider.output_file, 'a') as csv_file:
            result_writer = csv.writer(csv_file, delimiter=',', quotechar='"', quoting=csv.QUOTE_MINIMAL)
            result_writer.writerow(item.csv_line)
            csv_file.close()
        return item
