#!/usr/bin/env python
"""
This example module reads a list of product ids, gets their metadata from an API, and allows them to be searched.
To generate HTML documentation for this module issue the
command:

    pydoc -w test

"""

import web
import csv
import urllib2
import simplejson as json
import time
# import dependencies

urls = ('/search/(.*)', 'SearchItems')
# setup the url schema

app = web.application(urls, globals())


class SearchItems:
    """
    SearchItems handles the request from the /search/* url.
    """
    max_tries = 3
    tries = 0

    def __init__(self):
        """
        Initialize a SearchItems object
        """

    def GET(self, keyword):
        """
        Handle the GET method of our API

        :param keyword: the search term passed in from GET method
        :return: a json formatted list of ids that match the search term
        """
        csv_file_path = "items.csv"
        api_url = "http://api.walmartlabs.com/v1/items/"
        api_parameters = "?format=json&apiKey=kjybrqfdgp3u4yv2qzcnjndj"
        search_array = []

        with open(csv_file_path, 'rb') as csvfile:
            line_reader = csv.reader(csvfile, delimiter=',', quotechar='|')
            for row in line_reader:
                meta_url = api_url + row[0] + api_parameters
                # create URL for each id and get metadata from Walmart API
                metadata = self.get_data(meta_url)
                if metadata:
                    row[1] = metadata
                    search_array.append(row)

            search_array = self.search_rows(search_array, keyword)

        return json.dumps(search_array)

    def get_data(self, url):
        """
        Gets data from the given URL
        Recursively tries 3 times before giving up

        :param url:
        :return: json decoded array from url response
        """
        metadata = False
        if self.tries <= self.max_tries:
            try:
                response = urllib2.urlopen(url)
                metadata = json.loads(response.read())
                self.tries = 0
            except Exception:
                self.tries += 1
                time.sleep(0.01) #had to add this to avoid 403 errors, not optimal
                metadata = self.get_data(url)
        else:
            self.tries = 0

        return metadata

    def search_rows(self, rows, keyword):
        """
        Searches an array of walmart api metadata listings for the given keyword

        :param rows: Walmart metadata rows
        :param keyword: search term
        :return: an array of matching product IDs
        """
        results = []
        for row in rows:
            # use .lower() to ensure case-insensitivity
            if keyword.lower() in row[1]["shortDescription"].lower() or keyword.lower() in row[1]["longDescription"].lower() \
             or keyword.lower() in row[1]["categoryPath"].lower() or keyword.lower() in row[1]["name"].lower():
                results.append(row[0])
        return results

if __name__ == "__main__":
    app.run()
    # run built in webserver
