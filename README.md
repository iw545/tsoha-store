# Verkkokauppasovellus
Päivitys 8.10.2023:
Suurin osa toiminnoista on nyt lisätty sovellukseen, mutta ne eivät toimi vielä täysin niin kuin pitää.
Tietokannan taulukoiden dataan viittaamisessa oli hankaluuksia, joten toiminnot eivät lisää käytettävää dataa aina muihin taulukoihin.
Toimintoja voi testata, vaikkei ne näytä tarvittavaa dataa oikein jokaisessa niistä.

Uudet toiminnot tässä versiossa:
- Tuotteiden lisääminen ostoskoriin. Jokaisella tuotteella on nyt oma sivu, jossa on vaihtoehto "Lisää ostoskoriin". Klikkaamalla tätä vaihtoehtoa tuote siirtyy ostoskoriin. Ostoskoria voi tarkastella "Ostoskori" vaihtoehdlla sovelluksen sivun ylälaidassa olevista vaihtoehdoista. Tällä hetkellä kuitenkaan tuotteiden nimiä, hintaa eikä niiden määrää näe. Tuotteita voi kuitenkin poistaa ostoskorista valitsemalla vaihtoehdon "Poista ostoskorista" sen tuotteen kohdalla minkä haluaa poistaa. Tuotteet voi myös ostaa valitsemalla "Osta tuotteet" vaihtoehdon, jolloin tuotteet siirtyvät ostettujen tuotteiden listaan (joita ei voi tässä versiossa vielä tarkastella).
- Tuotearvioiden lisääminen tuotteiden sivuille. Jokaisen tuotteen sivulla on kohta, johon käyttäjä voi kirjoittaa oman arvostelun tuotteesta sekä antaa tuotteelle arvosanan asteikolla 1-5. Kun arvostelun on kirjoittanut, sen voi lähettää klikkaamalla vaihtoehtoa "Lähetä arvostelu". Tässä versiossa arvosteluita eikä arvosanojen keskiarvoa kuitenkaan vielä näe tuotteiden sivuilla.

Edellisessä päivityksessä (Päivitys 24.9.2023) kohdassa voi lukea miten tuotteita voi lisätä tietokantaan, joka toimii samalla tavalla tässäkin versiossa.

Nykyisten toimintojen päivittämisen lisäksi sovellus tarvitsee vielä seuraavat päätoiminnot:
- Käyttäjä asetukset, joissa käyttäjä voi tarkastella aiemmin ostettuja tuotteitaan. Näissä asetuksissa ylläpitäjällä on vaihtoehto lisätä ja poistaa tuotteita tietokannasta.
- Tuotteiden selaaminen järjestämällä ne monella eri tavalla, kuten hinnan, tuotekategorian, uutuuden, suosituimpien tuotteiden mukaan.

-------------------------------------------------------------------------------------------------------------------------------------
Päivitys 24.9.2023:
Sovelluksessa toimii käyttäjätunnuksen tekeminen ja sovellukseen kirjautuminen luodulla käyttäjätunnuksella.
Tuotteita voi etsiä hakusanalla, mutta niitä ei vielä voi järjestää muilla eri tavoilla, kuten hinnan mukaan.
Tällä hetkellä sovellusta voi testata tuotannossa seuraavilla tavoilla:
- Tuotteiden etsiminen hakusanalla. Tuotteita etsitään "items" luettelosta.
- Käyttäjätunnuksen luomisella. "Luo käyttäjätunnus" valinnalla sovelluksen etusivulla voi testata käyttäjätunnuksen luomista. Kun käyttäjätunnus on luotu, sovellukseen pystyy kirjautumaan sisään luoduilla käyttäjätunnuksilla. Kun on kirjautunut sisään, pystyy kirjautumaan ulos valitsemalla "kirjaudu ulos" (muuta toiminnallisuutta ei vielä ole toteutettu).
-------------------------------------------------------------------------------------------------------------------------------------
Sovelluksen käynnistysohjeet (sama ohje kuin tsoha kurssin sivuilla: https://hy-tsoha.github.io/materiaali/aikataulu/):  
Kloonaa tämä repositorio omalle koneellesi ja siirry sen juurikansioon. Luo kansioon .env-tiedosto ja määritä sen sisältö seuraavanlaiseksi:

DATABASE_URL="tietokannan-paikallinen-osoite"  
SECRET_KEY="salainen-avain"

Seuraavaksi aktivoi virtuaaliympäristö ja asenna sovelluksen riippuvuudet komennoilla

$ python3 -m venv venv  
$ source venv/bin/activate  
$ pip install -r ./requirements.txt  

Määritä vielä tietokannan skeema komennolla  

$ psql < schema.sql  

Nyt voit käynnistää sovelluksen komennolla  

$ flask run  

-------------------------------------------------------------------------------------------------------------------------------------  


Tuotteita lisätään luetteloon seuraavasti PostgreSQL tulkilla (toiminnallisuutta ei vielä lisätty, jolla sovelluksen admin voi sovelluksessa suoraan lisätä tuotteita lomakkeella):

INSERT INTO items (name, price, category, time, sold, grades)
VALUES ('ItemName', 9.99, 'ItemCategory', CURRENT_DATE, 0, 0);

Name: tuotteen nimi  
Price: tuotteen hinta  
Category: tuotteen kategoria  
Time: tuotteen lisäämispäivä (älä muuta tätä, CURRENT_DATE asettaa nykyisen päivämäärän automaattisesti sillä hetkellä)  
Sold: myydyt tuotteet (alkaa 0 aina, tätä arvoa päivitetään kun tuotetta ostetaan (toiminnallisuutta ei vielä ole toteutettu))  
Grades: arvosana keskiarvo (1-5 välillä, alkaa 0 aina, tätä arvoa päivitetään kun tuotteelle annetaan arvosanoja ((toiminnallisuutta ei vielä ole toteutettu))  

"items" luettelon tuotteita voi myös katsoa "Tuote hakemisto" valinnasta, mikä sisältää kaikki tuotteet jotka sinne on lisätty yllä mainitulla tavalla.
Jos tuotteita hakee tyhjällä hakusanalla, yllä mainitulla tavalla tulee näkyviin kaikki tuotteet luettelossa.


-------------------------------------------------------------------------------------------------------------------------------------
Sovelluksen kuvaus:

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
