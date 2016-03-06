# Silly Potty

Ovvero, esperimenti di Data Visualization con gli Open Data del Parlamento Italiano.

...il tutto ovviamente fatto a tempo perso e con molto poco impegno.

[Sito Web](http://kenoph.github.io/silly-potty)

## Utilizzo

Il file [camera.py](camera.py) scarica i dati necessari e li salva in `www/data/camera/`.

Per visualizzare il grafico riguardante i cambi di partito dei vari deputati,
basta mettere i file contenuti in `www/` in un webserver.

**NOTA:** È fortemente consigliato l'utilizzo di Google Chrome per visualizzare le pagine,
          in quanto le animazioni in Mozilla Firefox risultano troppo lente.
          
**NOTA2:** Tempo permettendo, la visualizzazione sarà migrata da jsnetworkx a puro d3.js
           (o a dagre.js dove opportuno).

Esempio:
```sh
cd path/www
python -m SimpleHTTPServer 8080
# aprire un browser all'indirizzo http://localhost:8080/camera.html
```

![camera.html](/docs/camera.png)

# Autore

Paolo Montesel [(@pmontesel)](https://twitter.com/pmontesel)

# Licenza

Questo repository è coperto da licenza MIT, il cui testo è disponibile nel file [LICENSE](LICENSE)
o a questo [link](https://opensource.org/licenses/MIT).
