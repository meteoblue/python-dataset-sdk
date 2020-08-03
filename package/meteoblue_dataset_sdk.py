""""
meteoblue dataset client
"""

import requests  # later use

class MeteoblueDatasetClient(object):

    def __init__(self, apikey: str):
        self.apiKey = apikey

    "Query async api dataset interface"
    def query(self, params: dict):
        """
        query async dataset api interface
        :param params: params for meteoblue dataset api
        :return: result data set
        """
        raise NotImplemented()
