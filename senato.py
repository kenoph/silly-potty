#!/usr/bin/env python

import json
import time

from lib import SimpleWrapper

sparql = SimpleWrapper("http://dati.senato.it/sparql")


def load_load_gruppo():
    results = sparql.query("""
    SELECT DISTINCT ?gruppo ?nome ?maxInizio ?descrizione
    WHERE
    {
        ?gruppo osr:denominazione ?denominazione.
        ?denominazione osr:titoloBreve ?nome.
        ?denominazione osr:titolo ?descrizione.
        ?denominazione osr:inizio ?maxInizio.
        {
            SELECT ?gruppo (MAX(?subInizio) AS ?maxInizio)
            WHERE
            {
                ?gruppo a ocd:gruppoParlamentare.
                ?gruppo osr:denominazione ?denominazione.
                ?denominazione osr:inizio ?subInizio.
            }
            GROUP BY ?gruppo
        }
    }
    ORDER BY ?gruppo
    """)

    return results


def load_senatori():
    results = sparql.query("""
    SELECT DISTINCT ?senatore ?nome ?cognome
    WHERE
    {
        ?senatore rdf:type osr:Senatore.
        ?senatore foaf:firstName ?nome.
        ?senatore foaf:lastName ?cognome.
        OPTIONAL
        {
            ?senatore bio:death ?morte.
        }
        FILTER (!BOUND(?morte)).
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
        OPTIONAL
        {
            ?senatore bio:death ?morte.
        }
        FILTER (!BOUND(?morte)).
    }
    ORDER BY ?senatore ?inizio
    """)

    rr = list()
    lastSenatore = ""
    lastGruppo = ""
    for result in results:
        if result["senatore"] == lastSenatore and result["gruppo"] == lastGruppo:
            continue

        lastSenatore = result["senatore"]
        lastGruppo = result["gruppo"]

        rr.append(result)

    return rr


if __name__ == "__main__":
    json.dump(load_senatori(), open("data/senato/senatori.json", "wb"))
    json.dump(load_adesioni(), open("data/senato/adesioni.json", "wb"))
    json.dump(load_load_gruppo(), open("data/senato/gruppi.json", "wb"))

#TODO: Capire cosa sono i senatori che non sono collegati a nulla :/
