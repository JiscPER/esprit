from copy import deepcopy
import string

unicode_punctuation_map = dict((ord(char), None) for char in string.punctuation)

class Query(object):
    _match_all = { "query" : { "match_all" : {} }}
    _query_string = {"query" : {"query_string" : {"query" : "<query string>"}}}
    _term = {"query": {"term": { } } } # term : {"<key>" : "<value>"}
    
    _terms_filter = { "query" : { "filtered" : { "filter" : { "terms" : { } } } } } # terms : {"<key>" : ["<value>"]}
    _term_filter = { "query" : { "filtered" : { "filter" : { "term" : { } } } } } # terms : {"<key>" : "<value>"}
    
    _fields_constraint = {"fields" : []}
    
    _special_chars = ["+", "-", "&&", "||", "!", "(", ")", "{", "}", "[", "]", "^", '"', "~", "*", "?", ":", "/"]
    _escape_char = "\\" # which is a special special character too!
    
    @classmethod
    def match_all(cls):
        return deepcopy(cls._match_all)
    
    @classmethod
    def query_string(cls, query):
        q = deepcopy(cls._query_string)
        q["query"]["query_string"]["query"] = query
        return q
        
    @classmethod
    def term(cls, key, value):
        q = deepcopy(cls._term) 
        q["query"]["term"][key] = value
        return q
    
    @classmethod
    def term_filter(cls, key, value):
        q = deepcopy(cls._term_filter)
        q["query"]["filtered"]["filter"]["term"][key] = value
        return q
    
    @classmethod
    def terms_filter(cls, key, values):
        if not isinstance(values, list):
            values = [values]
        q = deepcopy(cls._terms_filter)
        q["query"]["filtered"]["filter"]["terms"][key] = values
        return q
    
    @classmethod
    def fields(cls, query, fields=None):
        fields = [] if fields is None else fields if isinstance(fields, list) else [fields]
        fc = deepcopy(self._fields_constraint)
        fc["fields"] = fields
        query.update(fc)
        return query

    @classmethod
    def tokenise(cls, text_string):
        # FIXME: note that we don't do anything about stopwords right now.
        out = text_string
        if type(text_string) == "str":
            out = text_string.translate(string.maketrans("",""), string.punctuation)
        elif type(text_string) == "unicode":
            out = text_string.translate(unicode_punctuation_map)
        return list(set([o.lower() for o in out.split(" ") if o != ""]))
    
    @classmethod
    def escape(cls, query_string):
        qs = query_string.replace(cls._escape_char, cls._escape_char + cls._escape_char) # escape the escape char
        for sc in cls._special_chars:
            qs = qs.replace(sc, cls._escape_char + sc)
        return qs
    
    
