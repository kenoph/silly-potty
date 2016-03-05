#!/usr/bin/env python

import json

import lib
from lib import SimpleWrapper, pretty_print as pp

sparql = SimpleWrapper("http://dati.camera.it/sparql")


def load_legislatura():
    return sparql.query("""
    SELECT DISTINCT *
    WHERE
    {
        ?legislatura a ocd:legislatura.
        ?legislatura dc:date ?data.
        OPTIONAL
        {
            ?legislatura dc:title ?titolo.
        }
    }
    ORDER BY DESC(?data)
    LIMIT 1
    """)[0]


def load_deputati(legislatura):
    """
    Carica lista dei deputati

    NOTA: Include anche i deputati che si sono dimessi e quindi raggiunge
          un numero totale maggiore di 630.

    :param legislatura: url identificativo della legislatura.
    :return: lista di deputati con nome e cognome, ordinata per cognome-nome
    """

    def fix(d):
        d["nome"] = d["nome"].title()
        d["cognome"] = d["cognome"].title()
        return d

    return map(fix, sparql.query("""
    SELECT DISTINCT ?deputato ?cognome ?nome
    WHERE
    {
        ?deputato a ocd:deputato.
        OPTIONAL
        {
            ?deputato foaf:firstName ?nome.
            ?deputato foaf:surname ?cognome.
        }
        ?deputato ocd:rif_leg ?legislatura.

        FILTER (?legislatura = <%(legislatura)s>)
    }
    ORDER BY ?cognome ?nome
    """ % {"legislatura": legislatura}))


def load_gruppi(legislatura):
    return sparql.query("""
    SELECT DISTINCT ?gruppo ?nome
    WHERE
    {
        ?deputato a ocd:deputato.
        ?deputato ocd:aderisce ?adesione.
        ?adesione ocd:rif_gruppoParlamentare ?gruppo.
        ?deputato ocd:rif_leg ?legislatura.
        ?gruppo dc:title ?nome.

        FILTER (?legislatura = <%(legislatura)s>)
    }
    ORDER BY ?nome
    """ % {"legislatura": legislatura})


def load_adesioni(legislatura):
    def cd(x):
        x["inizio"] = lib.parse_date(x["inizio"])
        return x

    return map(cd, sparql.query("""
    SELECT DISTINCT ?deputato ?gruppo ?inizio
    WHERE
    {
        ?deputato a ocd:deputato.
        ?deputato ocd:aderisce ?adesione.
        ?adesione ocd:rif_gruppoParlamentare ?gruppo.
        ?adesione ocd:startDate ?inizio.

        ?deputato ocd:rif_leg ?legislatura.

        OPTIONAL
        {
            ?deputato bio:death ?morte.
            ?adesione ocd:endDate ?fine.
        }

        FILTER (?legislatura = <%(legislatura)s>)
    }
    ORDER BY ?deputato ?gruppo ?inizio
    """ % {"legislatura": legislatura}))


def download():
    # legislatura = load_legislatura()
    legislatura = {
        "legislatura": u'http://dati.camera.it/ocd/legislatura.rdf/repubblica_17'
    }
    json.dump(load_deputati(legislatura["legislatura"]), open("data/camera/deputati.json", "wb"))
    # json.dump(load_gruppi(legislatura["legislatura"]), open("data/camera/gruppi.json", "wb"))
    # json.dump(load_adesioni(legislatura["legislatura"]), open("data/camera/adesioni.json", "wb"))

if __name__ == "__main__":
    download()
