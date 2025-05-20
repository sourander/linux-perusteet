---
priority: 610
---

# Tmux

Tämä ohje on tarkoitettu SSH-yhteyttä käyttäville, jotka haluavat ratkaista seuraavia ongelmia:

* Pitkään ajettava ohjelma katkeaa kun SSH-yhteys katkeaa.
* Haluat ajaa useaa ohjelmaa rinnakkain tai jopa split screen -tilassa.
* Haluat voida jatkaa ensi kerralla siitä, mihin jäit.

Tähän löytyy ratkaisuja kuten `tmux` ja `screen`. Käytännön tasolla nämä ohjelmat multiplexaavat terminaalia, jolloin voit ajaa useita ohjelmia rinnakkain ja palata niihin myöhemmin. Multipleksaus on termi, jolla yhteen striimiin voidaan sisällyttää useita eri signaaleja (esimerkiksi DVD-levyssä on useita ääniraitoja ja tekstityksiä).

Tässä ohjeessa käydään läpi `tmux`-ohjelman käyttöönotto ja peruskäyttö.

!!! tip

    Voit käyttää tmuxia joko lokaalisti GNOME Terminaalissa tai SSH-yhteyden läpi.

## Asennus

Asenna `tmux` paketinhallinnan kautta:

```bash
$ sudo apt update
$ sudo apt install tmux
```

## Peruskäyttö

Käynnistä `tmux`-sessio komennolla `tmux`:

```bash
$ tmux
```

Nyt olet `tmux`-sessiossa. Tunnistat sen vihreästä palkista alhaalla. Voit ajaa komentoja kuten normaalissakin terminaalissa, mutta sinulla on apuna useita näppäinkomentoja.

### Prefix-näppäin

`tmux`-sessiossa ehdottomasti tärkein näppäinyhdistelmä on ++ctrl+b++. Kyseessä on `tmux` prefix, joka tarkoittaa, että seuraava klikattu näppäin on `tmux`:lle tarkoitettu komento eikä shellille ammuttava näppäinpainallus.

### Kokeillaan irroittautua sessiosta ja liittyä takaisin

Tyypillinen workflow on se, että luot sinulle session, johon palaat aina takaisin. Et siis suinkaan lue miljoonaa rinnakkaista sessiota, vaan palaat takaisin aiemmin luomaasi.

1. Olet `tmux`-sessiossa, jos ajoit aiemmin komennon `tmux`.
2. Paina ++ctrl+b++ ja sen jälkeen `d` tai vaihtoehtoisesti kirjoita `tmux detach`.

```bash title="stdout"
[detached (from session 0)]
```

Nyt olet palannut pois `tmux`-sessiosta. Voit listata kaikki sessiot seuraavalla tavalla:

```bash title="Bash"
$ tmux ls
```

```bash title="stdout"
0: 1 windows (created Wed Sep 18 10:44:00 2024)
```

Nyt voit liittyä takaisin sessioon:

```bash title="Bash"
# Liity viimeisimpään sessioon
$ tmux attach

# Tai pidemmällä komennolla
$ tmux attach-session

# Tai eksplisiittisesti
$ tmux attach -t 0
```

### Sessionin tuhoaminen

Voit tuhota sessiot seuraavalla tavalla:

```bash title="Bash"
# Listaa kaikki
$ tmux ls

# Tuhotaan sessio
$ tmux kill-session -t 0
```

### Nimetyn sessionin luominen

Voit luoda nimetyn session seuraavalla tavalla:

```bash title="Bash"
$ tmux new -s mysession
```

Jatkossa tähän liitytään komennolla

```bash title="Bash"
# Eksplisiittisesti
$ tmux attach -t mysession

# Tai edelliseen
$ tmux attach
```

### Asetustiedosto

Jos haluat muokata `tmux`-asetuksia, voit tehdä sen tiedostossa `~/.tmux.conf`. Vakiona tiedostoa ei ole, joten voit luoda sen itse. Tämä on kurssin skoopin ulkopuolella, mutta voit halutesssasi tutustua esimerkiksi [Make tmux Pretty and Usable - A Guide to Custom­izing your tmux.conf](https://hamvocke.com/blog/a-guide-to-customizing-your-tmux-conf/) ohjeeseen.

### Ikkunat

Session on jaettu ikkunoihin. Voit luoda uuden ikkunan painamalla ++ctrl+b++ ja sen jälkeen `c`. Voit vaihtaa ikkunaa painamalla ++ctrl+b++ ja sen jälkeen `n` tai `p` (next, previous). Vaihtoehtoisesti voit navigoida ikkunaan sen indeksiä käyttäen, esim. ++ctrl+b++ ja sen jälkeen `0`.

## Jatko-ohjeet

Tässä ohjeessa käytiin läpi `tmux`-ohjelman peruskäyttö. Mikäli haluat syventää osaamistasi, voit tutustua `man tmux`-ohjeeseen tai [tmux Wikiin](https://github.com/tmux/tmux/wiki) tai esimerkiksi käyttäjien luomiin [tmux cheat sheet](https://gist.github.com/scottjwood/9067d332f2933a0c0c0e)-tyyliisiin pikaohjeisiin.

## Tehtävät

!!! question "Tehtävä: tmuxin käyttö"

    Asenna tmux. Luo istunto (engl. session), ja splittaa istunnon ikkuna horisontaalisesti kahdeksi ruuduksi (*engl. panes*). Tähän löytyy netistä rutkasti ohjeita, kuten yllä mainittu cheat sheet. Otsikon "Managing split panes" alta löytyy tarvittavat ohjeet.

    Todista luomasi kokonaisuus kuvakaappauksin, aivan kuten edellisissäkin tehtävissä olet tehnyt.
