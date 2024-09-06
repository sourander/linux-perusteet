Tässä luvussa käsittelemme shellin startup-tiedostoja (engl. startup files, initialization files). Nämä tiedostot määrittävät ympäristön, jossa shell käynnistyy. 

!!! tip

    Olet jo itse asiassa muokannut näitä! Aiemmassa luvussa [Ubuntu opiskelukuntoon](../asennus/opiskelukuntoon.md) muokkasit tiedostoa `~/.bashrc` useassakin eri kohtaa. Selkein muutos on `.bashrc`-tiedostoon tehdyt muutokset **pyenv**-ohjelman asennuksen yhteydessä.

    Alla kertauksen vuoksi:

    ```bash title="Bash (kertausta!)"
    echo 'export PYENV_ROOT="$HOME/.pyenv"' >> ~/.bashrc
    echo 'command -v pyenv >/dev/null || export PATH="$PYENV_ROOT/bin:$PATH"' >> ~/.bashrc
    echo 'eval "$(pyenv init -)"' >> ~/.bashrc
    ```

Aiemmat luvut ovat esitelleen sinulle perusteet Bash-komennoista, tiedostoista ja terminaalista, joten on sopiva aika tutustua lähemmin shelliin. Emme käsittele shelliä erityisen yleismaailmallisesti vaan keskitymme lähinnä startup-tiedostoihin, koska näiden muokkaaminen on ==hyvinkin Linux perusteet -tason taito==.

!!! warning

    Tässä luvussa mainittujen tiedostojen muokkaamisen kanssa kannattaa olla tarkkana. Jos aiheutat tiedostoon ikuisen tai syktaksivirheestä johtuvan muun ongelman, voi olla, että et saa esimerkiksi Terminaali-sovellusta auki, koska se ajaa startup-tiedostot. Tällöin joudut käyttämään virtuaaliterminaalia, joka on käytettävissä painamalla `ctrl+alt+F3` ja kirjautumalla sisään.
    
    Jos et pääse edes tähän, saatat joutua käyttää Live-USB:ltä käynnistettyä Linuxia tai Recovery Modea.

## Eri shellit

Shellin startup-tiedostot vaihtelevat käytetyn shellin mukaan. Tässä dokumentissa tutustutaan rinnakkain kahteen suosituimpaan shelliin: **bash** ja **zsh**. Bash on oletusshelli useimmissa Linux-jakeluissa. Bash on tästä syystä tämän dokumentin keskiössä, mutta sivussa käsitellään myös Z-shelliä.

### Ohjekirjat

Tulet tarvitsemaan avuksi näiden kummankin ohjekirjat. Alla on linkit näiden PDF-versioihin. Kummastakin löytyy myös HTML-versiot, jos kyseinen formaatti on sinulle sopivampi.

* [PDF: Bash Reference Manual](https://www.gnu.org/software/bash/manual/bash.pdf)
* [PDF: A User's Guide to the Z-Shell](https://zsh.sourceforge.io/Guide/zshguide.pdf)

### Eri tiedostot

Se, mitä startup-tiedostoja ajetaan, riippuu siitä, kuinka Bash tai Zsh on käynnistetty. Kaksi tärkeintä tekijää ovat se, onko shell käynnistetty "login shellinä" ja onko se "interaktiivinen". Tiivistetty selitys näistä on:

* **Login shell**: Bash on käynnistynyt login-prosessin yhteydessä. Tämä tapahtuu esimerkiksi, kun kirjaudut sisään terminaaliin. Tämä on helpointa tehdä painamalla ++ctrl+alt+F3++ ja kirjautumalla sisään. Huomaa, että gnome-terminal ei tyypillisesti käynnistä Bashia login-shellinä: GNOME on jo itsessään tehdä loginin, ja pseudoterminaali on sen child-prosessi.
* **Interactive shell**: Shell on käynnistetty niin, että käyttäjä voi syöttää komentoja eli sen stdin, stdout ja stderr ovat kiinnitetty terminaaliin.
  
Näihin tutustutaan alla tarkemmin.


## Asetusten kaivaminen esille

Selvitetään shell-komentojen avulla, onko nykyinen istuntosi login että onko se interaktiivinen.

### Interaktiivinen?

Muuttuja `-` kertoo, onko shell interaktiivinen. Voit tarkistaa sen seuraavalla komennolla:

```bash title="Bash tai Zsh"
echo $-
```

Ympäristöstä riippuen tämä voi palauttaa eri arvoja. Alla on tuoreen Ubuntu 24.04:n tuloste sekä macOS:n Zsh:n tuloste siten, että Zsh:llä on Oh My Zsh -lisäosa asennettuna.

=== "Bash"
    ```bash title="stdout"
    himBHs
    ```

=== "Zsh"
    ```bash title="stdout"
    569JNRXZghiklms
    ```

Lista on pitkä ja reilusti tämän kurssin skoopin ulkopuolella. Tässä materiaalissa keskitymme lähinnä yhteen: `i`-kirjain tarkoittaa, että shell on interaktiivinen. Ja kumpikin näistä on, minkä voisi myös arvata siitä, että käytät sitä ==interaktiivisesti terminaalissa==.

### Login?

Z-shellin tapauksessa me tietäisimme tämän jo. Yllä olevassa esimerkissä Zsh on käynnistetty login-shellinä, koska `l`-kirjain on mukana. Vaihtoehtoisesti voit ajaa tämän komennon, joka löytyy Z-shellin manuaalista:

```bash title="Zsh"
if [[ -o login ]]; then; print yes; else; print no; fi
```

```plaintext title="stdout"
yes
```

Bash ei ilmoita "login"-tietoa l-kirjaimella, joten sitä pitää kaivaa vähän kauempaa. Se löytyy muun muassa ympäristömuuttujasta BASHOPTS:

```bash title="Bash"
echo $BASHOPTS | tr ":" "\n"
```

Jos kokeilet yllä olevaa komentoa **virtuaaliterminaalissa** (esim. ++ctrl+alt+F3++), saat tulosteen, josta löytyy myös `login_shell`.

!!! warning

    Huomaa, että login-shellin voi käynnistää myös mikä tahansa prosessi, mikä käynnistää shellin. Esimerkiksi jokin terminaalisovellus voi antaa shellille `--login`-argumentin, jolloin se käynnistyy login-shellinä.

## Mitä ajetaan milloin?

### Bash

Nyt kun ymmärrämme, mikä on login shell ja interaktiivinen shell, voimme tarkastella, mitä startup-tiedostoja Bash lukee missäkin tilanteessa. Tähän auttaa yllä mainitun manuaalin luku 6.2, joka käsittelee Bashin käynnistystä.

* **Login shell, interaktiivinen**: 
    * Ensin ajetaan: `/etc/profile`
    * Sitten ajetaan, jos löytyy: `.bash_profile`
    * ... jos ei löytynyt:  `.bash_login`
    * ... jos ei löytynyt: `.profile`
* **Non-login shell, interaktiivinen**:
    * Ensin ajetaan: `.bashrc`
* **Non-login shell, ei interaktiivinen**:
    * Ei ajeta mitään startup-tiedostoja.

Jos mietit, missä tilanteessa sinulla on non-login ei-interaktiivinen shell, niin se on esimerkiksi silloin, kun annat sille tiedoston tai komennon inputtina. Tyypillisin tilanne on Bash-skriptin ajaminen.

!!! tip

    Olet ainakin kerran jo ajanut scriptin! Ubuntu opiskelukäyttöön ohjeesta löytyy seuraava rivi:

    ```bash title="Bash"
    # Run installation script
    curl https://pyenv.run | bash
    ```

    Olet myös saattanut ajaa skriptin harhoitustöiden ohessa, kuten:

    ```bash title="Bash"
    # Make it executable
    chmod +x script_given_by_teacher.sh
    # Run it like this:
    ./script_given_by_teacher.sh
    # Or like this:
    bash script_given_by_teacher.sh
    ```

### Zsh

Aivan kuten Bashin kanssa, myös Z-shellin kohdalla manuaalin lukeminen auttaa. Luvun 2, *What to put in your startup files*, alla on selitetty, mitä tiedostoja Zsh lukee. Tarkastellaan tätä taulukkona, jossa vasen sarake on login shell ja oikea sarake on interaktiivinen shell. Skriptit ajetaan ylhäältä alas järjestyksessä sen mukaan, löytyykö niitä vai ei.

| Script          | Login | Interactive |
| --------------- | ----- | ----------- |
| `/etc/zshenv`   | X     | X           |
| `~/.zshenv`     | X     | X           |
| `/etc/zprofile` | X     |             |
| `~/.zprofile`   | X     |             |
| `/etc/zshrc`    |       | X           |
| `~/.zshrc`      |       | X           |
| `/etc/zlogin`   | X     |             |
| `~/.zlogin`     | X     |             |

## Yhteenveto

Mikä siis kuuluu minne? Jos tarvitset jotakin pysyvää, joka on saatavilla myös virtuaaliterminaalissa (eli GNOME:n ulkopuolella), laita se:

* Bash: `.bash_profile` tai `.bash_login` tai `.profile`
* Zsh: `.zprofile` tai `.zlogin`

Jos tarvitset jotakin, joka on saatavilla ainakin pseudoterminaalissa, laita se:

* Bash: `.bashrc`
* Zsh: `.zshrc`

Z-shellin tapauksessa voit myös käyttää `.zshenv`-tiedostoa, joka ajetaan aina, kun Zsh käynnistyy. Tämä on hyvä paikka asettaa ympäristömuuttujia, jotka ovat käytettävissä kaikissa Zsh-sessioissa. Tämän käyttö ei kuitenkaan ole millään tavoin pakollista.

## Extra: Zsh asentaminen

Ubuntu 24.04:ssä saat Zsh:n näin käyttöön:

```bash
# Update
sudo apt update && sudo apt upgrade -y

# Install 
sudo apt install zsh

# Change your default shell
chsh -s $(which zsh)

# Notice that it appeared in passwd
grep $USER /etc/passwd
```

Huomaa, että tämä ei tule välittömästi käytäntöön. Sinun tulee vähintään logata ulos ja sisään.