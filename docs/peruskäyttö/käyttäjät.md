Useimmissa Linux-distribuutioissa käyttäjien ID:t (eng. user id, UID) noudattavat seuraavaa numerointia:

| UID        | Käyttäjä                                          |
| ---------- | ------------------------------------------------- |
| 0          | root                                              |
| 1-999      | Järjestelmän omia "system usereita".              |
| 1000-59999 | Komennolla `adduser` luodut tavalliset käyttäjät. |
| 60000-     | Useita eri alueita ja poikkeustunnuksia.          |

Yllä mainittuihin poikkeustunnuksiin voit tutustua esimerkiksi lukemalla[debian policyn](https://www.debian.org/doc/debian-policy/ch-opersys.html#uid-and-gid-classes). Käyttäjät ja salasanat säilötään Linuxissa seuraaviin tiedostoihin:

| Käyttö               | Oikeudet | Tiedosto       |
| -------------------- | -------- | -------------- |
| Käyttäjät            | 644      | `/etc/passwd`  |
| Ryhmät               | 644      | `/etc/group`   |
| Käyttäjien salasanat | 640      | `/etc/shadow`  |
| Ryhmien salasanat    | 640      | `/etc/gshadow` |

Mikäli haluat tarkistaa, onko sinun järjestelmässäsi juuri sanat tiedostot samoine oikeuksineen, aja komento `stat -c '%a %n' /etc/passwd /etc/group /etc/shadow /etc/gshadow`.


## Passwd sisältö

Toisin kuin nimestä voisi päätellä, `passwd`-tiedosto ei sisällä salasanoja laisinkaan. Salasanat ovat `passwd`-tiedostossa, johon pureudutaan myöhemmin. Alla näkyy esimerkkinä kolme riviä `passwd`-tiedostosta.

```
root:x:0:0:root:/root:/bin/bash
nobody:x:65534:65534:nobody:/nonexistent:/usr/sbin/nologin
opettaja:x:1000:1000:Ope Opettaja,,,:/home/opettaja:/bin/bash
```

Riveissä toimii kenttien erottimena `:`-merkki. Esimerkiksi `opettaja`-nimisen käyttäjän rivin purkaa useaksi riviksi näin:

```bash
cat /etc/passwd | grep opettaja | tr : "\n"
```

Alla tulostuvat rivit selitettyinä:

| #   | Kenttä         | Selite                                                                                                                                                                                                       |
| --- | -------------- | ------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------ |
| 1   | username       | Uniikki tekstimuotoinen tunniste käyttäjälle. Tällä käyttäjä kirjautuu sisään. Primääriavain.                                                                                                                |
| 2   | password       | Käyttäjän salasana tai `x`-kirjain indikoimassa, että salasana löytyy `shadow`-tiedostosta.                                                                                                                  |
| 3   | user id, UID   | Ei-uniikki numeraalinen tunniste käyttäjälle tai käyttäjille. Yleensä jokaisella käyttäjällä on kuitenkin oma ID.                                                                                            |
| 4   | group id, GID  | Ei-uniikki numeraalinen tunniste käyttäjän ensisijaiselle groupille. Monta käyttäjää voi kuulua yhteen grouppiin.                                                                                            |
| 5   | contact, GECOS | Pilkulla erotettu lista arvoista: Full Name, Room number, Work phone, Home phone, Other. Komento `finger <username>` palauttaa tämän tiedon.                                                                 |
| 6   | home           | Käyttäjän kotikansio. Mikäli käyttäjällä ei ole kotikansiota, `/nonexistent` on arvona.                                                                                                                      |
| 7   | shell          | Shell (tai muu ohjelma) joka ajetaan aina kun käyttäjänä kirjaudutaan sisään. Mikäli käyttäjä on täysin ei-interaktiivinen käyttäjä, jolla ei koskaan kuulu kirjautua sisään, arvona on `/usr/sbin/nologin`. |

!!! question "Tehtävä"

    Kokeile ajaa ohjelma, joka ajetaan ei-interaktiivisilla käyttäjillä loginin yhteydessä eli `/usr/sbin/nologin`. Mitä näet?

!!! tip

    Voit katsella tai jopa muokata passwd tiedoston sisältöä komennolla `vipw`. Ulos editorista pääset painamalla ESC, minkä jälkeen `:q!` ja enteriä. Kyseessä on siis VIM-editori.


## Group sisältö

Tiedostosta `/etc/group` löytyvät aiemmin mainitut käyttäjien `root`,  `nobody` ja `opettaja` primääriryhmät. Taulukot joinataan yhteen GID:n eli group id:n avulla.

```
root:x:0:
nogroup:x:65534:
opettaja:x:1000:
```

Tämän lisäksi tiedostosta löytyy muutkin ryhmät; yksi käyttäjä voi kuulua moneen ryhmään. Käyttäjähallinta (eng. access control) on yleisesti järjestelmissä kannattavaa tehdä siten, että luo ryhmän, johon kiinnittää policyn ja/tai permissionit, joka sallii tekemään asioita x, y ja z. Käyttäjille ei anneta suoraan lupia mihinkään, vaan käyttäjä kiinnitetään ryhmään. Alla esimerkkinä neljä riviä tiedostosta, jotka sisältävät sanan "opettaja":

```
adm:x:4:syslog,opettaja
cdrom:x:24:opettaja
sudo:x:27:opettaja
opettaja:x:1000:
```

Alla rivien `:`-merkillä erotellut tiedot selitettyinä:

| #   | Kenttä         | Selite                                                                                                                     |
| --- | -------------- | -------------------------------------------------------------------------------------------------------------------------- |
| 1   | group name     | Ryhmän nimi, joka näkyy muun muassa `ls -la` komennon tulosteessa.                                                         |
| 2   | group password | Ryhmän salasana. Kuten käyttäjien kohdalla, myös täällä `x` tarkoittaa, että salasana löytyy muualta (ks. `/etc/gshadow`). |
| 3   | group id       | Ryhmän uniikki tunniste.                                                                                                   |
| 4   | users          | Pilkulla erotettu lista käyttäjänimistä, jotka kuuluvat ryhmään.                                                           |

Muistele aiempaa lukua käyttöoikeuksista. Jokaisella tiedostolla ja kansiolla on kolme permissionia: owner, group ja others. Jos `opettaja` kuuluu ryhmiin `cdrom` ja `adm`, niin mitä näillä voi tehdä? Tietenkin se, mitä permissionit sallivat. Sopivilla group-omistuksilla olevia tiedostoja voi etsiä seuraavanlaisilla komennoilla:

```sh
$ find /dev -group cdrom
/dev/sg0
/dev/sr0

$ find /var/log -group adm
/var/log/dmesg
/var/log/dmesg.0
/var/log/syslog.1
find: ‘/var/log/private’: Permission denied
/var/log/apt/term.log
...
```

!!! question "Tehtävä"

    Katso mihin ryhmiin kuulut ja selvitä, mitä oikeuksia sinulla on niiden puolesta. Muista, että sudo antaa pääsyn käytännössä kaikkialle.

!!! tip

    Voit katsella tai jopa muokata passwd tiedoston sisältöä komennolla `vigr`.


## Shadow sisältö

Tiedostosta `/etc/shadow` löytyvät aiemmin mainittujen käyttäjien salasanat. Ote tiedoston sisällöstä alla:

```
root:!:19598:0:99999:7:::
nobody:*:19576:0:99999:7:::
opettaja:$y$hidden:19598:0:99999:7:::
```

Yksittäisen rivin voi rikkoa osatekijöiksi tutulla komennolla, mutta tällä kertaa tarvitse root-oikeudet, tai sinun tulee kuulua ryhmään shadow: `´sudo cat /etc/shadow| grep opettaja | tr : "\n"`.

| #   | Kenttä               | Selite                                                                                                                                                                                                                                                                                                                                                                                                                                        |
| --- | -------------------- | --------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| 1   | username             | Käyttäjänimi kuten `opettaja`. (ks. `/etc/passwd`)                                                                                                                                                                                                                                                                                                                                                                                            |
| 2   | password             | Merkki `*` tai `!` tarkoittavat, että käyttäjänä ei voi kirjautua sisään salasanaa käyttäen, mutta esimerkiksi root-oikeuksin tai ssh-avainta käyttäen kirjautuminen voi yhä olla mahdollista. `*NP*` ja `!!` viittaavat siihen, että salasanaa ei ole (vielä) asetettu. `*LK*` tarkoittaa, että käyttäjä on lukittu. Mikäli kenttä sisältää jotain muuta, niin kyseessä on käyttäjän häshätty salasana. Lue alta **Salasanakentän sisältö**. |
| 3   | last password change | Päivä, jolloin salasana on edellisen kerran vaihdettu. Kyseessä ei ole päivämäärä vaan päivän lukujärjestys alkaen 1970-luvun alusta eli UNIX timestampin alkuhetkestä alkaen. Lue alta **Päivämäärän laskeminen**.                                                                                                                                                                                                                           |
| 4   | min days             | Minimi-intervalli salasanavaihtojen välillä. Katso `man chage`.                                                                                                                                                                                                                                                                                                                                                                               |
| 5   | max days             | Maksimi-intervalli salasanavaihtojen välillä. Katso `man chage`.                                                                                                                                                                                                                                                                                                                                                                              |
| 6   | warn days            | Varoituksen näyttämisen aloitus ennen salasanan vanhentumista.                                                                                                                                                                                                                                                                                                                                                                                |
| 7   | inactive days        | Käyttäjän deaktivoinnin päiväluku salasanan vanhentumisen jälkeen.                                                                                                                                                                                                                                                                                                                                                                            |
| 8   | expiry               | Päivä, jolloin käyttäjä on deaktivoitu. Käyttää samaa päivämääräkaavaa kuin kenttä `#3`.                                                                                                                                                                                                                                                                                                                                                      |



### Päivämäärän laskeminen

Last password change kentän arvon voi kääntää meille ihmiselle tutummaksi arvoksi `date`-komennon avulla.

```bash
$ date -d "1970-01-01 +19598 days" +%Y-%m-%d
2023-08-29
```



### Salasanakentän sisältö

Salasanakentän arvon erottajana toimii `$`-merkki, ja se noudattaa kaavaa `$id$salt$hash`, tai jos häshäykseen on käytetty custom-parametrejä, niin `$id$param=value,paramb=value$salt$hash`. Kenttä ID viittaa häshäykseen käytettyyn algoritmiin ja arvojen merkitys on:

| $ID$         | Häshäykseen käytetty algoritmi |
| ------------ | ------------------------------ |
| 1            | MD5                            |
| 2, 2a tai 2b | bcrypt                         |
| 5            | SHA-256                        |
| 6            | SHA-512                        |
| y            | yescrypt                       |

Salasanan häshäystä voi harjoitella `openssl`-kirjaston avulla.

```bash
$ openssl passwd -5 -salt "suola" "password123"
$5$suola$NkZwDPPEx8Q9XA2./QA2oJ4QA35JCL9ejielN9DOApD
```

Häshäyksessä (eli virallisesti suomeksi "tiivistämisessä") käytetty salt eli suola on arvo, joka ynnätään salasanaan ennen sen häshäystä. Tällä estetään suoraa rainbow table käyttöä: jos käyttäjän salasana olisi jotain turvatonta kuten `qwerty` tai `password123`,  salasanan häshätty arvo löytyisi suoraan jotakin tietokannasta, joka sisältää yleisimmän miljoonan salasanan häshit. Kun salt on käytössä, niin käyttäjan salasana on käytännössä "salt"+"password123". Naiivi esimerkki alla, jossa käytetään turvattomaksi luokiteltua MD5-algoritmia. Ethän käytä MD5:ttä missään tuotannossa! Tässä se on esimerkkinä, koska syntyvä häsh on mukavan lyhyt ruudulle tulostettavaksi.

```bash
$ salt=salt
$ password=password123
$ hashed=$(echo "$salt$password" | md5sum | base64)
$ echo "\$5\$$salt\$$hashed"
$5$salt$ZjhiY2I2NmVmOWMwMTRlYjRiMDBjZmY4N2U0YThhNjUgIC0K
```

Häshäämätöntä salasanaa ei siis tallenneta laisinkaan. Kun käyttäjä yrittää kirjautua sisään, järjestelmä häshää käyttäjän syötteen saltin kanssa, vertaa sitä `shadow`-tiedoston arvoon, ja joko päästää käyttäjän sisään tai ei päästä. Mikäli `shadow`-tiedosto vuotaa vääriin käsiin, ja joku ulkopuolinen yrittää päätellä mitä häshäämättömät salasanat ovat, hänellä ei ole käytännössä muuta vaihtoehtoa kuin kokeilla kaikki vaihtoehdot läpi.

!!! question "Tehtävä"

    Kuvittele tilanne, jossa salasana policy määrää, että salasanan pitää noudattaa kaavaa `^[a-zA-Z0-9]{8,32}$` (eli 8-32 symbolia, jotka ovat isoja tai pieniä kirjaimia tai numeroita; erikoismerkkejä tai suomalaisia ääkkösiä ei sallita). Kuinka monta eri vaihtoehtoa pitäisi enimmillään käydä läpi löytääkseen häshi, jos oikea salasana on 8 merkkiä pitkä? Entä jos salasana onkin 10 merkkiä pitkä?



## Käyttäjien luominen

Lokaaleja käyttäjiä voi luoda komennolla:

```bash
# Luo käyttäjä
# - Vertaa komentoon "adduser". Miten se eroaa tästä? Kokeile kumpaakin.
# - Selvitä, mitä -m optio tekee.
$ sudo useradd <-m> <username>

# Luo tarpeen mukaan uusi ryhmä
$ sudo groupadd <groupname>

# Jos loit ryhmän, lisää käyttäjä ryhmään
$ sudo usermod --append --groups <groupname> <username>
```

!!! tip

    Uuden käyttäjän luomiseen liittyy default-asetuksia. Käy katsomassa, mitä tiedosto `/etc/login.defs` sisältää. Mitä manuaali sanoo tiedostosta?

    Uuden käyttäjän kotihakemistolle voi luoda jonkin pohjarakenteen. Käy katsomassa, mitä kansio `/etc/skel` sisältää. Mitä manuaali sanoo siitä (ks. USERADD(8) )?

!!! warning

    Ethän luo tai poista käyttäjiä koulun ympäristöissä, joissa on keskitetty käyttäjänhallinta (LDAP, Kerberos, Ansible-skriptejä, ...). Tee uusiin käyttäjiin liittyvät kokeilut virtuaalikoneessa, joka on täysin sinun hallinnoima.

Tiedostojen omistajuutta voi vaihtaa komennolla `chown`. Alla lyhyt esimerkki.

```bash
# Vaihda owner
$ chown <username> kissa.txt

# Vaihda sekä owner että group
$ chown <username>:<group> kissa.tx
```

## Toisena käyttäjänä esiintyminen

Jos haluat kokeilla, kuinka tiedosto- sekä hakemisto-oikeudet käyttäytyvät toisen käyttäjän näkökulmasta, niin vaikea tapa on kirjautua graafisesta käyttöliittymästä ulos, ja tämän jälkeen kirjautua uudella käyttäjällä sisään. Helpompi tapa on käyttää `su`-komentoa (substitute user).

```bash
# Avaa toisen käyttäjän shell sinun shellisi prosessina
# Selvitä, mitä "-" eli "--login" optio tekee.
$ sudo su - <username>
```

!!! question "Tehtävä"

    Selvitä, kuinka käyttäjän voi poistaa kotihakemistoineen. Poista tämän jälkeen myös tyhjiksi jääneet ryhmät.