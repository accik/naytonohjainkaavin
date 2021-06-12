## Akselin näytönohjainkaavin(scraper)

Ohjelma hakee annetuista linkeistä tuotteen nimen, hinnan ja saatavuuden.

Ei ehkä näteintä tai parasta koodia, tehty harjoituksena! !

Ei takuuta tai lupausta toiminnasta.

**Vaatimukset**

 - Testattu python 3.9.1 64-bit, uusimmat kirjastot
 - Kirjastot: bs4/beautifulsoup4, urllib, re, time, sys

**Käyttö**

 - Asenna ylläolevat kirjastot (``` pip3 install -r requirements.txt ```)
 - Luo datatiedosto tai käytä esimerkkinä data.txt
 - Datatiedostoon laita yksi tuotelinkki per rivi, esimerkin mukaan. Mahdolliset verkkokaupan linkit ensin.
 - Laita tiedoston sijainti riville 11 tai käytä argumenttia ```
 -f <datatiedosto>```
 - Esimerkiksi: ```python3 MultiScraperV2.py -f example_datafiles/full_list.txt -t 3```
 - Uusimmat päivitykset saat suoraan komennolla ```git pull origin master```

**Huomautuksia**

 - Tuetut nettisivut ovat Verkkokauppa.com (*Vain* näytönohjaimet), Jimms.fi (muut tuotteet *saattavat* toimia) ja alustavasti Proshop.fi (*Vain* näytönohjaimet)
 - Haut on tarkoituksella rajoitettu yksi per 3 sekuntia ("timelimit", ```-t```)
 - "user_agent" ja "headers" on valittu omien seikkojen mukaan, muokkaa tarvittaessa.
 - Gigantti kaavin ei helposti mahdollinen useiden teknisten asioiden vuoksi

**Valmiit listat**
 - Mukana tulevat listat ovat seuraavat: data.txt, full_list.txt ja shorttestdata.txt
 - Nopeaan testaamiseen suosittelen data.txt. 
 - Full_list.txt sisältää kaikki 3060ti, 3070 ja 3080 Verkkokaupalta, Jimmssiltä ja Proshopista. Nämä voisi nimetä toki paremmin...

**Tulevia ominaisuuksia**

 - Muiden tuotteiden kaavin (Verkkokaupassa) Ei testattu
 - Datalistojen uudelleen nimeäminen ja paremmat listat. + Niille oma .md tiedosto.
 - Automaattinen päivitysominaisuus kuten esim. zsh käyttää.
 - ~~Laskuri tai ilmoitus jos tuote on saatavilla. Julkaistu nimellä MultiScraperV2.py~~ Valmis
 - ~~Tiedoston tai ominaisuuksien antaminen parametrinä ohjelmalle.~~ Valmis: ```-f, -d, -t```
