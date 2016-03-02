#!/usr/bin/env python

import json

from lib import SimpleWrapper

sparql = SimpleWrapper("http://dati.senato.it/sparql")


def load_partiti():
    results = sparql.query("""
    SELECT DISTINCT ?gruppo ?nome ?maxFine
    WHERE
    {
        ?gruppo a ocd:gruppoParlamentare.
        ?gruppo osr:denominazione ?denominazione.
        ?denominazione osr:titolo ?nome.
        {
            SELECT (MAX(?fine) AS ?maxFine)
            WHERE
            {
                ?denominazione osr:fine ?fine.
            }
            GROUP BY ?gruppo
        }
        ?denominazione osr:fine ?currFine.
        #?denominazione osr:fine ?maxFine.
        #FILTER (?currFine = ?maxFine)
    }
    LIMIT 10
    """)

    print json.dumps(results, indent=2)
    exit()

    partiti_dict = dict()
    for result in results:
        partiti_dict.setdefault(result['gruppo'], list()).append(result['nomeGruppo'])

    partiti = list()
    for k, v in partiti_dict.iteritems():
        partiti.append({
            "partito": k,
            "nomi": v
        });

    return partiti


def load_senatori():
    results = sparql.query("""
    SELECT DISTINCT *
    WHERE
    {
        ?senatore rdf:type <http://dati.senato.it/osr/Senatore>.
        ?senatore foaf:firstName ?nome.
        ?senatore foaf:lastName ?cognome.
    }
    """)

    return results


def load_adesioni():
    results = sparql.query("""
    SELECT DISTINCT ?senatore ?gruppo ?inizio ?fine
    WHERE
    {
        ?senatore a osr:Senatore.
        ?senatore ocd:aderisce ?adesione.
        ?adesione osr:gruppo ?gruppo.
        ?adesione osr:inizio ?inizio.
        ?adesione osr:fine ?fine.
    }
    ORDER BY ?senatore ?inizio
    """)

    return results


if __name__ == "__main__":
    # json.dump(load_senatori(), open("data/senato/senatori.json", "wb"))
    # json.dump(load_adesioni(), open("data/senato/adesioni.json", "wb"))
    json.dump(load_partiti(),  open("data/senato/partiti.json",  "wb"))
