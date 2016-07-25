#!/usr/bin/env python
import web
import csv
import urllib2
import simplejson as json
import time

urls = ('/search/(.*)', 'search_items')

app = web.application(urls, globals())


class search_items:
    max_tries = 3
    tries = 0
    def GET(self, keyword):
        csv_file_path = "items.csv"
        api_url = "http://api.walmartlabs.com/v1/items/"
        api_parameters = "?format=json&apiKey=kjybrqfdgp3u4yv2qzcnjndj"
        search_array = []

        with open(csv_file_path, 'rb') as csvfile:
            line_reader = csv.reader(csvfile, delimiter=',', quotechar='|')
            for row in line_reader:
                meta_url = api_url + row[0] + api_parameters
                metadata = self.getData(meta_url)
                if metadata:
                    row[1] = metadata
                    search_array.append(row)

            search_array = self.searchRows(search_array, keyword)

        return json.dumps(search_array)

    def getData(self, url):
        metadata = False
        if self.tries <= self.max_tries:
            try:
                response = urllib2.urlopen(url)
                metadata = json.loads(response.read())
                self.tries = 0
            except Exception:
                self.tries += 1
                time.sleep(0.01)
                metadata = self.getData(url)
        else:
            self.tries = 0

        return metadata

    def searchRows(self, rows, keyword):
        results = []
        for row in rows:
            if keyword.lower() in row[1]["shortDescription"].lower() or keyword.lower() in row[1]["longDescription"].lower() \
             or keyword.lower() in row[1]["categoryPath"].lower() or keyword.lower() in row[1]["name"].lower():
                results.append(row[0])
        return results

if __name__ == "__main__":
    app.run()
