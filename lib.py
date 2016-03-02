from SPARQLWrapper import SPARQLWrapper, JSON


__all__ = [
    "DEFAULT_PREFIXES",
    "SimpleWrapper"
]


DEFAULT_PREFIXES = {
    "ocd": "http://dati.camera.it/ocd/",
    "osr": "http://dati.senato.it/osr/",
    "bio": "http://purl.org/vocab/bio/0.1/"
}


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

    def query(self, q, prefixes=DEFAULT_PREFIXES):
        q = create_query(q, prefixes)
        self.sparql.setQuery(q)
        return simplify(self.sparql.query().convert()["results"]["bindings"])
