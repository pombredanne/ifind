class Query(object):
    """
    Models a Query object for use with ifind SearchEngine interface.

    Query Attributes:
        terms:  a string of search terms
        lang:   a string defining the language of the results
        format: a string defining the result format (json, xml)
        top:   an integer specifying the number of results to return
        skip:  an integer specifying the offset of starting point for results returned
        source_type: a string defining the type of query (web, image, video)
    """
    def __init__(self, terms, lang='EN', format='JSON', top=20, skip=0, source_type='web', **kwargs):
        """
        Constructs Query object, creating instance attributes from optional keyword parameters (**kwargs).

        """
        self.terms = terms
        self.source_type = source_type
        self.format = format
        self.lang = lang
        self.top = top
        self.skip = skip

        for key, value in kwargs.iteritems():
            setattr(self, key, value)

    def __str__(self):
        """
        Returns human-readable string representation of query object.

        """
        return '\n'.join(['{0}: {1}'.format(key, value) for (key, value) in self.__dict__.items()])

    def __eq__(self, other):
        """
        Returns True if both querys' attributes are identical, False otherwise.

        """
        return tuple(self.__dict__.items()) == tuple(other.__dict__.items())