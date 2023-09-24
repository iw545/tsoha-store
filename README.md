# Verkkokauppasovellus

Päivitys 24.9.2023:
Sovelluksessa toimii käyttäjätunnuksen tekeminen ja sovellukseen kirjautuminen luodulla käyttäjätunnuksella.
Tuotteita voi etsiä hakusanalla, mutta niitä ei vielä voi järjestää muilla eri tavoilla, kuten hinnan mukaan.
Tällä hetkellä sovellusta voi testata tuotannossa seuraavilla tavoilla:
- Tuotteiden etsiminen hakusanalla. Tuotteita etsitään "items" luettelosta, joka luodaan seuraavasti PostgreSQL tulkilla:



Tällä sovelluksella selataan yksittäisen verkkokaupan tuotteita. Sovelluksen ylläpitäjä voi lisätä uusia tuotteita
valikoimaan. Käyttäjät voivat selata tuotteita järjestämällä niitä useilla eri tavoilla. Valitsemalla tuotteen
käyttäjä voi tarkastella tarkemmin kyseisen tuotteen tietoja (esim. hinta, varastotilanne, käyttäjien antamat arvostelut).

Sovelluksen ominaisuuksia ovat:
* Käyttäjä voi kirjautua sisään ja luoda oman tunnuksen sovellukseen.
* Käyttäjä voi selata tuotteita ensisijaisesti tuotevalikoimaa selaamalla, joka sisältää kaikki verkkokaupan tuotteet.
Tämän lisäksi tuotteita voi etsiä tarkemmin esim. hakusanalla, tuotekategorialla, hinnan mukaan (halvimmasta kalliimpaan tai päinvastoin),
arvostelujen mukaan (suosituimmat tuotteet käyttäjäarvioiden mukaan), tuotteen vanhuuden mukaan (uusimmasta vanhimpaan tai päinvastoin) tai
myydyimpien tuotteiden mukaan.
* Käyttäjä voi lisätä tuotteita ostoskoriin, minkä kautta voi ostaa joko yksittäisen tai usean tuotteen kerralla.
* Käyttäjä voi halutessaan lisätä oman arvosanan tuotteelle ja tämän lisäksi vaihtoehtoisesti myös kommentin. Tuotteiden tiedoissa käyttäjä
voi myös lukea muiden antamia arvosteluja.
* Käyttäjä voi selata tuotteita, joita on itse aiemmin ostanut.
* Ylläpitäjä voi sekä lisätä tuotteita että poistaa niitä valikoimasta.
* Ylläpitäjä voi tarkastella listaa, jossa näkyy aina uusimmat käyttäjien tekemät ostokset käyttäjän mukaan.
