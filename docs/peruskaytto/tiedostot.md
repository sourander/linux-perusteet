---
priority: 200
---

# Tiedostot

## Linux vs. Windows

Linuxin (ja UNIX:n) hakemistorakenne voi tuntua oudolta, mikäli on aiemmin tottunut Windowsin vastaavaan. Windowsissa yksi fyysinen tallennuslaite (kiintolevy, optinen asema, muistikortinlukija) löytyy tyypillisesti asemasta, joka merkataan kirjaimella (eng. drive-letter). Kiintolevyn osio, jolle Windows on asennettu, löytyy usein C-asemasta eli polusta `C:\`. Mikäli tietokoneessa on toinen kiintolevy, sen osio voidaan tuntea esimerkiksi `D:\`-asemana. `E:\` on esimerkiksi CD-asema tai toinen kiintolevy/osio.

!!! note

    Tarkennuksena mainittakoon, että laite:osio:asema suhde ei ole aina välttämättä näin yksiselitteinen. Käyttäjä voi esimerkiksi luoda useasta kiintolevystä RAID-henkisen `Windows Storage Pool`:n, jolloin monta fyysistä levyä löytyy yhden aseman kirjaimen takaa.

    Lisäksi myös Windows-ympäristössä on osioita, joille ei ole tarkoitus tallentaa laisinkaan tietoa käsin. Näitä ovat esimerkiksi UEFI- ja Recovery-osiot. Jos osioit Dual Boot -asennuksen yhteydessä Linuxia varten käyttämätöntä tilaa, törmäsit näihin todennäköisesti. Huomaa, että nämä toki *voi* mountata asematunnukseen esimerkiksi debuggausta varten PowerShellillä.

Linuxissa tilanne on hyvin toinen. Asemia ja niiden kirjaimia ei ole olemassa. Hakemistorakenteen juuri ei siis ala laitteen/aseman kirjaimesta vaan `/`-merkistä, joka toimii Linuxissa hakemistoerottimena. Hakemistot muodostavat puurakenteen samalla tavalla kuin Windowsin hakemistot, joten on mahdollista, että `kissa.txt` sijaitsee polussa `/a/b/c/kissa.txt`. Yksittäinen hakemisto, kuten `/home` tai `/var`, voi sijaita saman levyn eri partitiolla tai jopa kokonaan eri levyllä kuin valtaosa käyttöjärjestelmästä.

Alla näkyy ajettuna komento `lsblk` eli List Block Devices. Tässä tapauksessa `sda` on laite eli kiintolevy. Sen osiot tunnistaa juoksevasta numerosta jälkiliitteessä. Lähes koko 30 Gt:n levy on varattu `/`-hakemistolle, pois lukien tietokoneen käynnistysprosessin tarvitsemat pikkuosiot, sekä virtuaalinen snap:n hallinnoima osio, joka on varattu Firefoxin oikolukuohjelmistolle.

```bash title="Bash"
$ lsblk /dev/sda
AME   MAJ:MIN RM  SIZE RO TYPE MOUNTPOINTS
sda      8:0    0   30G  0 disk 
├─sda1   8:1    0    1M  0 part 
├─sda2   8:2    0  513M  0 part /boot/efi
└─sda3   8:3    0 29,5G  0 part /var/snap/firefox/common/host-hunspell # (1)
                                /
```

1. Lue lisää: [Sdb5 mounted on firefox? - snap - snapcraft.io](https://forum.snapcraft.io/t/sdb5-mounted-on-firefox/31897)

Alla erittäin karkea taulukko Linuxin ja Windowsin tiedosto/kansiorakenteen eroista.

|                                   | Linux                         | Windows                 |
| --------------------------------- | ----------------------------- | ----------------------- |
| Kansiorakenteen standardi         | Filesystem Hierarchy Standard | Microsoft ja konventiot |
| Juuri                             | `/`                           | `C:\`                   |
| Kotihakemisto                     | `/home/username/`             | `C:\Users\username\`    |
| Kotihakemisto env                 | `$HOME`                       | `%homepath%`            |
| Todennäköinen tiedostojärjestelmä | ext4, XFS                     | NTFS                    |
| Tekstitiedoston pääte             | Ei mitään väliä               | .txt                    |
| Ajettavan tiedoston pääte         | Ei mitään väliä               | .exe                    |


## Spesifikaatiot

### Filesystem Hierarchy Standard

Linuxin tiedostojärjestelmän standardi löytyy [Filesystem Hierarchy Standard (linuxfoundation.org)](https://refspecs.linuxfoundation.org/FHS_3.0/fhs/index.html)-sivustolta, mutta alla on listattuna tärkeimmät juuritason kansiot taulukossa. On tärkeää kuitenkin huomioida, että vaikka kyseessä on standardi, ei se tarkoita, että kaikki Linux-jakelut noudattaisivat sitä. Esimerkiksi GoboLinux asentaa ohjelmat poikkeukselliseen `/Programs`-hakemistoon. Voit tutustua tähän FHS:stä poikkeavaan tapaan [GoboLinux at a glance](https://gobolinux.org/at_a_glance.html)-sivulla. Esimerkin mukaan esimerkiki Bash asentuisi `/usr/bin/bash` sijasta `/Programs/Bash/4.4/bin/bash`-hakemistoon, ja sen manuaalit olisivat tyypillisen `/usr/share/man` sijasta `/Programs/Bash/4.4/man/`-hakemistossa.

| Hakemisto    | Sisältää                                                                                                                                                                                                                        |
| ------------ | ------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| /bin, /sbin  | Useimmiten C-kielestä käännettynä ajettavia binääritiedostoja, kuten yllä käytetty `lsbkl` tai hakemistojen luontiin tarkoitettu `mkdir`. Tyypillisesti viittaa lokaatioon `/usr/bin/` sekä `/usr/sbin/`.                       |
| /boot        | Kernel image, jota käytetään konetta käynnistäessä.                                                                                                                                                                             |
| /dev         | Fyysisiä laitteita, kuten yllä näkyvä `sda`, tai loogisia/virtuaalisia laitteita kuten partitio `sda1` tai työpöytäympäristössä käyttämäsi terminaali `/dev/pts/0`.                                                             |
| /etc         | Koko järjestelmää koskevat konfiguraatiotiedostot, kuten `/etc/hosts`, josta tarkistetaan tunnetut hostnamet ennen DNS-kyselyitä, tai `/etc/passwd`, jossa määritellään käyttäjät ja aikoinaan jopa salasanat, tai `/etc/fstab` |
| /home        | Käyttäjien kotikansiot.                                                                                                                                                                                                         |
| /lib         | Jaettuja kirjastoja, joita `/bin`:ssä ja `/sbin`:ssä olevat ohjelmat tarvitsevat, kuten C-kielen kirjastot `libc.so`.                                                                                                           |
| /mnt, /media | Käsin tai automaattisesti mountattavat mediat kuten CD- sekä USB-asemat tai jopa verkkolevyt.                                                                                                                                   |
| /opt         | Jotkin kolmannen osapuolen eli jakelun ulkopuoliset ohjelmat. Opiskelijana saatat huomata, että sinne asentuu esimerkiksi Brave-selain, Cisco Packet Tracer tai Zoom omilla asennusohjelmillaan.                                |
| /proc, /sys  | Kernelin rajapintoja, kuten `/proc/version`, joka sisältää kernelin ja distron versioon liittyvää tietoa.                                                                                                                       |
| /tmp         | Väliaikaiset tiedostot. Eivät säily ikuisesti.                                                                                                                                                                                  |
| /usr         | Käyttäjien ohjelmat ja tiedostot.                                                                                                                                                                                               |
| /var         | Usein muuttuva, ohjelmien sisältämä data. Erikoimaininta lokitiedostoja sisältävä alihakemisto `/var/log/`                                                                                                                      |

!!! tip

    Tyypillisesti distribuution oma paketinhallinta (esim. apt) asentaa ohjelman eri tyyppiä edustavat tiedostot eri lokaatioihin: binääri `/usr/bin` hakemistoon, kirjastot `/usr/lib`-hakemistoon, konfiguraatiot `/etc`-hakemistoon, data `/var`-hakemistoon ja niin edelleen.

    Tälle on vaihtoehtona `/opt`, mihin ohjelmat asennetaan jonkin paketinhallinnan (esim. Homebrew) toimesta. Ohjelmat ovat tällöin self-contained, eivätkä ole pirstaloitu `/usr`-hakemistoon. Tämä on tyypilisesti Windows-käyttäjille tutumpi tapa (vrt. `C:\Program Files\Ohjelmannimi`).

### Base Directory Specification

XDG Base Directory Specification (XDG BDS) on FSH:een läheisesti liittyvä määrittely, joka määrittelee, missä käyttäjän tiedostot sijaitsevat. Tähän liittyvä konventio on tallentaa käyttäjän oman binääritiedostot `/home/username/.local/bin/`-hakemistoon. Jos esimerkiksi haluat luoda oman skriptin, jota **juuri sinä** voit ajaa mistä tahansa, voit tallentaa sen tähän hakemistoon. Samaan hakemistoon tallentuvat usein myös käyttäjän omat ohjelmat, jotka eivät ole distribuution paketinhallinnassa.

Aiemmin mainitun `~/.local/bin` lisäksi muita siihen liittyviä merkittäviä hakemistoja ovat:

* `$XDG_CONFIG_HOME` (oletus `~/.config/`) - Käyttäjän konfiguraatiotiedostot
* `XDG_DATA_HOME` (oletus `~/.local/share/`) - Käyttäjän data, kuten pelitallennukset

Jos ympäristömuuttujaa ei ole asetettu, käytetään oletusarvoja. On tyypillistä, että asentamasi ohjelma luo kotikansioosi binäärejä, konfiguraatioita ja dataa näihin hakemistoihin - ja joskus myös hakemistoon, joka on piilotettu hakemisto kotihakemistossa (esim. `.ohjelmanimi/`, kuten `.kube`, `.azure`, `.ssh`, ...).

## Tehtävät

!!! question "Tehtävä: Hakemistopuu"

    Piirrä valitsemallasi työkalulla hakemistopuu, joka alkaa juuresta, ja sisältää seuraavat tiedostot kaikkine hakemistoineen. Älä unohda juurihakemistoa.

    ```plaintext
    /home/pekka/.bashrc
    /home/pekka/Desktop/P.jpg
    /home/liisa/.bashrc
    /home/liisa/Desktop/L.jpg
    /etc/crontab
    /etc/cron.d/anacron
    /dev/
    ```

    Työkalu voi olla kynä ja paperi, Excalidraw, OpenOffice Draw tai vaikkapa ASCII Draw.

!!! question "Tehtävä: lsblk"

    Aja komento `lsblk` ja tarkastele tulosta. Mitä laitteita ja osioita löytyy. Jos olet asentanut Dual Bootin, missä näistä osioista on Windows ja missä Linux?