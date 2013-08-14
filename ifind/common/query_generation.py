"""
An abstract class to generate queries list
=============================
Author: rose : <Rosanne.English@glasgow.ac.uk>
Date:   08/08/2013
Version: 0.1
"""
ONLY_ALPHAS = False #bool to distinguish if only considering alphanumeric terms
AVOID_STOP = False #bool to distinguish if avoiding terms on the stop list
MIN_LENGTH = 1 # the minimum length of a term, if =1 then no min length

class QueryGeneration():
    """
    Abstract class to represent structure for a query generator
    """

    def __init__(self):
        """
        constructor for QueryGeneration
        """

    def _extract_queries_from_html(self, html):
        """
        :param url: the html from which the queries are to be constructed
        :return: list of queries
        """

    def extract_queries_from_text(self, text):
        """
        :param text: the text from which the queries are to be constructed
        :return: list of queries
        """
