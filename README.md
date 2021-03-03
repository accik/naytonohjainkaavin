## Akselin näytönohjainkaavin(scraper)

Ohjelma hakee annetuista linkeistä tuotteen nimen, hinnan ja saatavuuden.

Ei ehkä näteintä tai parasta koodia, tehty harjoituksena! !

Ei takuuta tai lupausta toiminnasta.

**Vaatimukset**

 - Testattu python 3.9.1 64-bit, uusimmat kirjastot
 - Kirjastot: bs4/beautifulsoup4, urllib, re, time, sys (requirements.txt)

**Käyttö**

 - Asenna ylläolevat kirjastot (pip install)
 - Luo datatiedosto (tai käytä data.txt) ja merkitse sen nimi/sijainti riville 8.
 - Datatiedostoon laita yksi tuotelinkki per rivi, esimerkin mukaan.
 - Tuetut nettisivut ovat Verkkokauppa.com (*Vain* näytönohjaimet) ja Jimms.fi (muut tuotteet *saattavat* toimia)

**Huomautuksia**

 - Haut on tarkoituksella rajoitettu yksi per 5 sekuntia ("timelimit")
 - "user_agent" ja "headers" on valittu omien seikkojen mukaan, muokkaa tarvittaessa.
 - Gigantti kaavin ei helposti mahdollinen useiden seikkojen vuoksi

**Tulevia ominaisuuksia**

 - Muiden tuotteiden kaavin (Verkkokaupassa)
 - Laskuri tai ilmoitus jos tuote on saatavilla. Julkaistu nimellä MultiScraperV2.py
 - Tiedoston tai ominaisuuksien antaminen parametrinä ohjelmalle.
