---
priority: 520
---

# Cron

Kuten aiemmassa luvussa näimme, ajastetun tehtävän voi luoda systemd:n timerillä. Toinen - vanhempi mutta silti yhä käytössä oleva - keino on cron. Cron on ajastettujen tehtävien hallintaan tarkoitettu ohjelma, joka ajaa määriteltyjä tehtäviä määritellyin väliajoin.

Huomaa, että cron (kuten kaikki muutkin ohjelmat) ovat systemd:n käynnistämiä daemoneita tai servicejä:

```bash title="Bash"
$ systemctl status cron
```

## Cronin käyttö

Cronin käyttö on melko yksinkertaista. Cronin käyttöön liittyy kaksi komentoriviohjelmaa: `crontab` ja `cron`. `crontab`-ohjelmaa käytetään ajastettujen tehtävien hallintaan, kun taas `cron`-ohjelmaa käytetään ajastettujen tehtävien suorittamiseen. Aikoinaan cron-tehtävät määritettiin `/etc/crontab`-tiedostossa, mutta nykyään käytetään `crontab`-ohjelmaa, joka mahdollistaa käyttäjäkohtaiset cron-tehtävät. Käy kuitenkin kurkkaamassa, miltä `/etc/crontab` näyttää.

```bash title="Bash"
$ less /etc/crontab
```

Tiedostossa neuvotaan cron-tabin syntaksi, joka on muotoa `* * * * *` (at every minute), jossa minkä tahansa tähden voi korvata numerolla. Esimerkiksi `59 12 * 12 1` olisi lauseena *"joulukuun jokaisena maanantaina kello 12:59 (joka vuosi)"*.

!!! task

    Harjoittele cron-tabin syntaksi online-generaattorin avulla. Yksi monista on [Crontab.guru](https://crontab.guru/).

## crontab-ohjelma

`crontab`-ohjelmaa käytetään ajastettujen tehtävien hallintaan. `crontab`-ohjelmaa käytetään seuraavasti:

```bash title="Bash"
$ crontab [-u käyttäjä] [-l | -r | -e]
```

* `-u`-valitsimella voidaan määrittää käyttäjä (default: sinä)
* `-l`-valitsin listaa.
* `-e`-valitsin editoi (tai luo).
* `-r`-valitsin poistaa

### Luodaan uusi cron-tehtävä

Aluksi sinun käyttäjällä ei todennäköisesti ole laisinkaan cron-tehtäviä. Voit tarkistaa tämän `crontab -l` komennolla. Luodaan uusi tehtävä.

```bash title="Bash"
$ crontab -e
no crontab for <username> - using an empty one

Select an editor.  To change later, run 'select-editor'.
  1. /bin/nano        <---- easiest
  2. /usr/bin/vim.basic
...
```

Valitse haluamasi editori. Tässä esimerkissä valitsen `nano`-editorin. Tämän jälkeen näet tyhjän tiedoston, johon voit kirjoittaa cron-tehtävän. Muutokset kirjoitetaan tiedostoon `/var/spool/cron/crontabs/<username>`, mutta ethän muokkaa tiedostoa käsin. Lisää `crontab -e` komennon avulla tiedostoon seuraava rivi:

```bash title="Bash"
* * * * * echo "Time is $(date)" >> ~/crontesting
```

## Tehtävät

!!! question "Tehtävä: Cron toimii!"

    Käytä `crontab -e` -komentoa lisätäksesi ajastetun tehtävän, joka kirjoittaa "Cron toimii!" -viestin tiedostoon `~/cronlog.txt` kerran minuutissa.  
    Varmista, että tehtävä toimii tarkistamalla tiedoston sisältö muutaman minuutin kuluttua.

!!! question "Tehtävä: Docker Prune scheduled"

    Luo skripti [bobcares: Crontab Docker Prune Command](https://bobcares.com/blog/crontab-docker-prune/) ohjetta noudattaen, joka tuhoaa yli 30 päivää vanhat kontit ja imaget.

    Huomaa kuitenkin, että tämä vaatii hieman pohtimista. Et voi välttämättä noudattaa ohjetta aivan orjallisesti, jos ==sinulla on Rootless Docker==. Kyseinen `cron.daily` ajetaan root-käyttäjällä, joten kyseinen ohje toimii vain, 

    1. Jos sinun Docker ajetaan roottina, voit käyttää ohjetta sellaisenaan.
    2. Jos sinulla on rootless Docker, käytä sen sijaan sinun käyttäjän omaa cronia (`crontab -e`).

    Perustele valintasi.

    