# Tervetuloa kurssille

Oppimateriaali on tarkoitettu Kajaanin Ammattikorkeakoulun ensimmäisen tai toisen vuoden opiskelijoille. Kurssilla tutustutaan Linuxiin käyttöliittymänä sekä graafiseen ympäristöön että komentoriviin. Kurssin esimerkit ovat pääosin ajettu Ubuntu distribuutiota käyttäen, mutta liiallista "distribution-lockia" vältellään parhaan mukaan. Aiempi kokemus Linuxista ei ole millään tavoin vaadittua.

![Superhero penguin](images/dalle-sudo-penguin.jpg)

**Kuvio 1:** *DALL-E 3:n näkymys `sudo`-oikeuksin varustetusta pingviinistä.*

## Koodin lukuohje

Kurssin komennot esitetään koodisnippeteissä siten, että rivi alkaa tyypillisesti `$`-merkillä. Tuloste kirjoitetaan alle ilman etuliitteitä. Ennen seuraavaa komentoa jätetään tyhjä rivi. Kommentit alkavat `#`-merkillä, ja ne voivat olla joko omina riveinään tai koodirivin perässä. Mikäli kommentin vieressä on ristipääruuvia muistutava ikoni, sitä klikkaamalla aukeaa pidempi kommentti.

```bash title="Bash"
$ komento
tuloste

# Omalla rivillä oleva kommentti
$ komento-kaksi --parametri
tuloste
tuloste jatkuu

$ komento # kommentti (1)
tuloste
```

1. Tämä tässä on pidempi kommentti, mikäli yhden tai kahden sanan seloste ei riitä.



## Faktavirheet

Mikäli kurssimateriaali sisältää virheellistä tietoa, tee jompi kumpi:

* Forkkaa GitHubin repository ja tarjoa Pull Request, joka sisältää korjausehdotukset.
* Ota yhteyttä ylläpitoon ja esittele virheellisen tiedon korjaus.