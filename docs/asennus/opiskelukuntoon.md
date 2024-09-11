Tämän ohjeen tarkoitus on auttaa sinua pika-asentamaan tarvittavat ohjelmat siten, että voit työstää oppimispäiväkirjaa Linuxista käsin. Pohjaoletus on, että sinulla on Ubuntu jo asennettuna. Mikäli sinulla ei ole aiempaa Linux-kokemusta, ohjeen komennot saattavat tuntua osittain heprealta. Kannattaa palata tähän materiaaliin kurssin lopuksi: todennäköisesti huomaat, että ohjeissa ei ole mitään, mitä et osaisi tehdä itsenäisesti, ohjelmien omia dokumentaatioita seuraamalla.

## Video-ohjeet

<iframe width="560" height="315" src="https://www.youtube.com/embed/cSvLAXpWsZg?si=WmTRMvGIeGyXMQJv" title="YouTube video player" frameborder="0" allow="accelerometer; autoplay; clipboard-write; encrypted-media; gyroscope; picture-in-picture; web-share" referrerpolicy="strict-origin-when-cross-origin" allowfullscreen></iframe>

**Video 1:** Linux Perusteet 2024 -toteutuksen asennusohjeet.

Yllä on upotettuna Youtube-video, jossa freesiin Ubuntu-asennukseen suoritetaan kaikki tämän ohjeen merkittävät vaiheet. Alla on tekstimuodossa lähes identtiset vaiheet sisältävä ohje. Voit valita, kumpaa haluat seurata - tai tutustutko kumpaankin.

!!! warning

    Huomaa, että videon kohdasta "Docker Engine" jäi uupumaan Rootless Moden asennus. Se paikataan hieman myöhemmin ajassa 27 minuuttia. Eroa kirjoitettuun ohjeeseen on myös siinä, että ensimmäistä oppimispäiväkirjaa ei koskaan kirjoiteta, eikä sisältöä pusketa myöskään Gitlabiin.

## Tekstiohjeet

### Vaihe 1: Joplin

Huomaa, että tämä vaihe on vaihtoehtoinen. Vaihe esiintyy videolla, jotta videon tallennuksen aikana olisi mahdollista luoda TODO-lista, jota seuraamme videon aikana. Päätä itse, tarvitsetko Joplin-sovellusta opiskelemiseen.

Se hoituu näin: 

1. Avaa App Center
2. Etsi Joplin
3. Klikkaa Install
4. Klikkaa Open

### Vaihe 2: Git

Avaa Terminal (gnome-terminal) eli pseudoterminaali. Tämä onnistuu monella eri tavalla:

* Pikanäppäin ++ctrl+alt+t++
* Hiiren oikealla korvalla työpöydän tyhjällä alueella ja valitsemalla "Open Terminal"
* Klikkaa ++win++ -näppäintä ja kirjoita hakukenttään "Terminal" ja paina enter.
* Avaa ruudun vasemmasta alalaidasta "Show Apps" ja kirjoita hakukenttään "Terminal" ja paina enter.

Kun Terminal on auki, aja seuraavat komennot, joskin siten, että korvaat oikeisiin paikkoihin oman nimesi ja oman sähköpostiosoitteesi:
    
```bash title="Bash"
# Upgrade software and install git
$ sudo apt update && sudo apt upgrade
$ sudo apt install git

# Set git configuration
$ git config --global user.name "Your Name"
$ git config --global user.email "your.name@kamk.fi"
$ git config --global core.autocrlf input
$ git config --global pull.ff only
$ git config --global init.defaultBranch main
```

!!! warning

    Ethän käytä ajamissasi komennoissa `$`-merkkiä. Se on yllä indikoimassa sitä, että komentoa ajetaan Bash-konsolissa tavallisella käyttäjällä. Se ei ole osa komentoa vaan osa promptia

### Vaihe 3: Luo avainpari

Luo avainpari SSH-yhteyksiä varten. Aja alla olevat komennot, mutta korvaa taas omat tietosi oikeisiin paikkoihin. Keksi tietokoneellesi jokin alias, jolla tunnistat avaimen. Esimerkiksi "dell-laptop" tai "hp-laptop" tai "opiskelulappari".

Komento `ssh-keygen` kysyy sinulta muutamia kysymyksiä. Voit jättää käytännössä kaikki tyhjiksi, jolloin se käyttää vakioasetuksia, mutta ==passphrase kannattaa asettaa==. Muuten olet alttiina sille, että joku voi esiintyä sinuna, mikäli avain joutuu vääriin käsiin.

```bash title="Bash"
# Create SSH key pair
$ ssh-keygen -t ed25519 -C "your.name@kamk.fi alias-for-computer"

# Install tool for managing clipboard
$ sudo apt install xclip

# Copy public key to clipboard
$ xclip -sel clip < ~/.ssh/id_ed25519.pub
```

### Vaihe 4: Lisää avain GitLabiin

Navigoi osoitteeseen: [repo.kamit.fi](https://repo.kamit.fi/)

1. Kirjaudu sisään
2. Klikkaa omaa etunimen alkukirjainta vasemmassa yläkulmassa
3. Valitse "Settings"
4. Valitse "SSH Keys"
5. Paina "Add SSH Key"

Liitä avain leikepöydältäsi ja paina "Add Key". Valitse jokin expiraatioaika, esimerkiksi vuoden tai lukuvuoden loppuun asti.

### Vaihe 5: Testaa yhteys ja tallenna passphrase

Tämän jälkeen testaa Terminaalissa yhteys komennolla:

```bash title="Bash"
# Test connection
$ ssh -T ssh://git@repo.kamit.fi:45065
```

Sinulle aukeaa seuraavanlainen pop-up -ikkuna, jossa pyydetään syöttämään avaimen salasana. Syötä valitsemasi passphrase, ==ruksaa päälle "Automatically unlock this key when I'm logged in"== ja paina "Unlock".

![Enter password prompt](../images/enter-password-to-unlock-private-key.png)

**Kuvio 1:** Avaimen salasanan syöttöikkuna.


### Vaihe 6: Asenna Visual Studio Code

Visual Studio Coden voi asentaa useallakin eri tavalla; me asennetaan se App Centeristä. 

1. Avaa App Center
2. Etsi "Visual Studio Code"
3. Asenna se ja avaa se.

### Vaihe 7: Asenna Pyenv

Alla olevat ohjeet perustuvat [Pyenv Wiki: Suggested build environmet](https://github.com/pyenv/pyenv/wiki#suggested-build-environment) sekä [Pyenv Installation](https://github.com/pyenv/pyenv?tab=readme-ov-file#installation) ohjeisiin, jotka kummatkin ovat luettavissa Pyenvin GitHub-projektin sivuilta.

!!!tip 

    Huomaa, että komennossa oleva `\`, jota seuraa välittömästi rivinvaihto, mahdollistaa rivin jakamisen useammalle riville.

```bash title="Bash"
# Install suggested build environment
sudo apt install build-essential libssl-dev \
    zlib1g-dev libbz2-dev libreadline-dev \
    libsqlite3-dev curl git libncursesw5-dev \
    xz-utils tk-dev libxml2-dev libxmlsec1-dev \
    libffi-dev liblzma-dev

# Run installation script
curl https://pyenv.run | bash
```

Kun pyenv on asentunut, lisää muutama rivi `.bashrc`-tiedostoon, jotta pyenv toimii oikein. Voit tehdä tämän helposti komennolla:

```bash title="Bash"
echo 'export PYENV_ROOT="$HOME/.pyenv"' >> ~/.bashrc
echo 'command -v pyenv >/dev/null || export PATH="$PYENV_ROOT/bin:$PATH"' >> ~/.bashrc
echo 'eval "$(pyenv init -)"' >> ~/.bashrc
```

!!! tip

    Jos haluat, että pyenv toimii kaikissa mahdollisissa tilanteissa, lisää samat rivit myös login-shellin konfiguraatiotiedostoon. Tähän löytyy ohjeet [Pyenvin GitHub-sivuilta](https://github.com/pyenv/pyenv?tab=readme-ov-file#set-up-your-shell-environment-for-pyenv). Tämä ei kuitenkaan ole välttämätöntä; todennäköisesti et tällä hetkellä ymmärrä, mitä eroa on interaktiivisella ja login shellilllä. Jälkimmäistä tuskin käytät vahingossa.


### Vaihe 8: Asenna Python

Nyt kun sinulla on pyenv, voit asentaa sillä Pythonin.

```bash title="Bash"
# Install Python 3.11.x
pyenv install 3.11

# Set is as a global default
pyenv global 3.11

# Check that it works
python --version
```

### Vaihe 9: Asenna Pipx

Pipx on työkalu, joka mahdollistaa globaalin scopen Python-pakettien asentamisen. Huomaa, että jälkimmäinen `pipx ensurepath` -komento lisää rivejä jo sinulle aiemmin tutuksi tulleeseen `.bashrc`-tiedostoon sekä `.profile`-tiedostoon.

```bash title="Bash"
# Install pipx
sudo apt install pipx

# Add to path
pipx ensurepath
```

!!!note 

    Pipx on erityisen hyödyllinen silloin, kun haluat asentaa työkaluja, jotka ovat käytössä useassa projektissa. Hyvä esimerkki tästä on `cookiecutter`, jota käytämme jo ennen kuin meillä edes on virtuaaliympäristöä (tai kenties koko projektikansiota.)

    Huomaa, että `pipx` ei siis ole `pip`:n korvaaja vaan täydentää sitä.

### Vaihe 10: Asenna Cookiecutter

Tämä vaihe on hyvinkin simppeli. Aja vain seuraava komento:

```bash title="Bash"
# Install cookiecutter
pipx install cookiecutter
```

### Vaihe 11: Asenna Docker Engine

Tässä ohjeessa ei asenneta graafista Docker Desktop -ohjelmaa, vaan Docker Engine. Kannattaa noudattaa Dockerin omia, ajan tasalla olevia ohjeita. Näistä tärkeimmät ovat [Install Docker Engine on Ubuntu](https://docs.docker.com/engine/install/ubuntu/) ja [Run the Docker daemon as a non-root user (Rootless mode)](https://docs.docker.com/engine/security/rootless/).

Tämän ohjeen kirjoitushetkellä toimivat komennot alla. Ensiksi lisätään Dockerin repositorio APT-paketinhallintaan.

```bash title="Bash"
# Add Docker's official GPG key:
sudo apt-get update
sudo apt-get install ca-certificates curl
sudo install -m 0755 -d /etc/apt/keyrings
sudo curl -fsSL https://download.docker.com/linux/ubuntu/gpg -o /etc/apt/keyrings/docker.asc
sudo chmod a+r /etc/apt/keyrings/docker.asc

# Add the repository to Apt sources:
echo \
  "deb [arch=$(dpkg --print-architecture) signed-by=/etc/apt/keyrings/docker.asc] https://download.docker.com/linux/ubuntu \
  $(. /etc/os-release && echo "$VERSION_CODENAME") stable" | \
  sudo tee /etc/apt/sources.list.d/docker.list > /dev/null
sudo apt-get update
```

Tämän jälkeen asennetaan Docker Engine ja Docker Compose.

```bash title="Bash"
# Install all Docker packages listed by the official documentation
sudo apt install docker-ce docker-ce-cli \
    containerd.io docker-buildx-plugin \
    docker-compose-plugin
```

Voit tarkistaa, että asennus meni oikein komennolla:

```bash title="Bash"
sudo docker run hello-world
```

!!! warning

    Huomaa, että komento vaati "sudo"-alun. Tähän löytyy hätäinen fix, joka on lisätä oma käyttäjä Docker-ryhmään. Dockerin suosittelema tapa on rootless mode. Tällöin Docker ei vaadi sudo-oikeuksia, mikä lisää järjestelmäsi turvallisuutta, kun ajat tuntemattomia kontteja.

    Huomaa myös, että video-ohjeessa tämä vaihe on osin vasta seuraavan vaiheen jälkeen, kun komento `docker compose -f docker-compose-docs.yml up -d` on ajettu ja se nostaa virheen, että kyseinen käyttäjä ei saa kajota socketiin. Tekstiohjeessa nuo vaiheet on korjattu samaan koodilohkoon.

Aktivoi rootless mode, jotta et jatkossa tarvitse sudo-oikeuksia Docker-konttien ajoon.

```bash title="Bash"
# Install prerequisites
sudo apt install uidmap

# Disable daemon
sudo systemctl disable --now docker.service docker.socket

# Delete socket file
sudo rm /var/run/docker.sock

# Run a script
dockerd-rootless-setuptool.sh install

# Add DOCKER_HOST environment variablle to startup script
echo "export DOCKER_HOST=unix:///run/user/${UID}/docker.sock" >> ~/.bashrc

# Enable the daemon in user-scope
systemctl --user enable docker.service
systemctl --user start docker.service
```

!!! tip

    Jos haluat, että Docker käynnistyy automaattisesti **ja pysyy päällä** vaikka et olisi kirjautunut sisään, aja myös seuraava rivi:

    ```bash title="Bash"
    sudo loginctl enable-linger $(whoami)
    ```

### Vaihe 12: Kloonaa repositorio

Jos et ole vielä alustanut repositorioosi oppimispäiväkirjaa, tee se nyt. Aloita luomalla tätä kurssia varten oma hakemisto. Täytä `<kurssin-nimi-tahan-2024>` oikealla kurssinimellä, kuten `linux-perusteet-2024`. Näet tuon Gitlab-urlin namespacesta, esimerkiksi: `https://repo.kamit.fi/linux-perusteet-2024`

!!! note

    Käytä URLia, jonka löydät Reppu Moodlesta tai jonka opettaja on sinulle neuvonut. Älä luo omia repositorioita omatoimisesti, sillä opettaja luo ne skriptillä Moodle-osallistujalistan perusteella. Jos olet hukassa, kysy opettajalta.

```bash title="Bash"
# Create directory for learning diary
mkdir -p ~/Code/kurssin-nimi-tahan-2024/

# Change directory
cd ~/Code/kurssin-nimi-tahan-2024/
```

Seuraavaksi kloonaa oppimispäiväkirjasi repositorio. Tämä on helppoa tehdä kopioimalla Gitlabin ohjeen tarjoamat komennot. Ohjeet löytyvät sinun tyhjästä repositoriostasi, joka on muotoa: `https://repo.kamit.fi/<kurssin-nimi-2024>/<etunimisukunimi>/`.

```bash title="Bash" title="Gitlabin komento"
git clone ssh://git@repo.kamit.fi:45065/.../etunimisukunimi/
cd etunimisukunimi
git switch --create main
touch README.md
git add README.md
git commit -m "add README"
git push --set-upstream origin main
```

### Vaihe 13: Alusta oppimispäiväkirja

Seuraa ohjeita, jotka löytyvät [kamk cookiecutters](https://github.com/sourander/kamk-cookiecutters) repositorion README.md-tiedostosta. Lyhyt vastaus on, että aja seuraava komento ja noudata ohjeita:

```bash title="Bash"
cookiecutter gh:sourander/kamk-cookiecutters -f
```

### Vaihe 14: Ensimäinen oppimispäiväkirjamerkintä

Avaa oppimispäiväkirja, eli nykyinen kansio, Visual Studio Codessa. Tämä onnistuu helposti komennolla:

```bash title="Bash"
code .
```

Tämän jälkeen toimi Visual Studio Codessa, kuten muilla kursseilla on opetettu. Oppimispäiväkirjan kirjoittamiseen löydät vinkkejä [Oppimispäiväkirja 101](https://sourander.github.io/oat/) -sivustolta.


### Vaihe 15: Aja oppimispäiväkirja

Aja oppimispäiväkirja komennoilla, jotka neuvotaan `HOW-TO-DOCS.md`-tiedostossa. Tämä tiedosto löytyy oppimispäiväkirjasi juuresta. Lyhyt vastaus on, että seuraavat komennot toimivat:

```bash title="Bash"
# Run docker compose project
docker compose -f docker-compose-docs.yml up -d
```

Avaa nettilelain, Firefox, ja navigoi osoitteeseen `http://localhost:8000`. Siellä pitäisi olla oppimispäiväkirjasi.

```bash title="Bash"
# Shut down the project
docker compose -f docker-compose-docs.yml down
```

### Vaihe 16: Muista versionhallinta!

Kun olet tehnyt ensimmäisen merkintäsi oppimispäiväkirjaan, puske muutokset Repo Kamit Gitlabiin. Tämä neuvotaan toisilla kursseilla, mutta on lyhyimmillään:

```bash title="Bash"
git add .
git commit -m "First learning diary entry"
git push
```
