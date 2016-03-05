import datetime
import json
import time
from SPARQLWrapper import SPARQLWrapper, JSON


__all__ = [
    "DEFAULT_PREFIXES",
    "SimpleWrapper"
]


DEFAULT_PREFIXES = {
    "bio": "http://purl.org/vocab/bio/0.1/",
    "dc": "http://purl.org/dc/elements/1.1/",
    "foaf": "http://xmlns.com/foaf/0.1/",
    "ocd": "http://dati.camera.it/ocd/",
    "osr": "http://dati.senato.it/osr/",
    "rdfs": "http://www.w3.org/2000/01/rdf-schema#"
}


def serialize_date(d):
    return int(time.mktime(d.timetuple()) * 1000 + d.microsecond)


def parse_date(s):
    return serialize_date(datetime.datetime.strptime(s, "%Y%m%d"))


def pretty_print(data):
    print json.dumps(data, indent=2)


def create_prefix(short_name, url):
    return "PREFIX {}: <{}>".format(short_name, url)


def create_prefixes(pd):
    return "\n".join([create_prefix(sn, url) for sn, url in pd.iteritems()])


def create_query(q, prefixes=DEFAULT_PREFIXES):
    return create_prefixes(prefixes) + "\n\n" + q


def simplify_item(item):
    ret = dict()
    for k, v in item.iteritems():
        ret[k] = v["value"]
    return ret


def simplify(data):
    return map(simplify_item, data)


class SimpleWrapper:
    def __init__(self, endpoint):
        self.endpoint = endpoint
        self.sparql = SPARQLWrapper(endpoint)
        self.sparql.setReturnFormat(JSON)

    def dir(self, elem):
        pretty_print(self.query("""
        SELECT DISTINCT ?t
        WHERE
        {
          ?gruppo a %(elem)s.
          ?gruppo ?t [].
        }
        """ % {"elem": elem}))

    def query(self, q, prefixes=DEFAULT_PREFIXES):
        q = create_query(q, prefixes)
        self.sparql.setQuery(q)
        return simplify(self.sparql.query().convert()["results"]["bindings"])
