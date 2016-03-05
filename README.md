# VizLamento

Ovvero, esperimenti di Data Visualization con gli Open Data del Parlamento Italiano.

...il tutto ovviamente fatto a tempo perso e con molto poco impegno.

## Utilizzo

Il file [camera.py](camera.py) scarica i dati necessari e li salva in `www/data/camera/`.

Per visualizzare il grafico riguardante i cambi di partito dei vari deputati,
basta mettere i file contenuti in `www/` in un webserver.

Esempio:
  cd path/www
  python -m SimpleHTTPServer 8080
  # aprire un browser all'indirizzo http://localhost:8080/camera.html

# Licenza

Questo repository è coperto da licenza MIT, il cui testo è disponibile nel file [LICENSE](LICENSE)
o a questo [link](https://opensource.org/licenses/MIT).
