Linuxin (ja UNIX:n) hakemistorakenne voi tuntua oudolta, mikäli on aiemmin tottunut Windowsin vastaavaan. Windowsissa yksi fyysinen tallennuslaite (kiintolevy, optinen asema, muistikortinlukija) löytyy tyypillisesti asemasta, joka merkataan kirjaimella (eng. drive-letter). Kiintolevyn osio, jolle Windows on asennettu, löytyy usein C-asemasta eli polusta `C:\`. Mikäli tietokoneessa on toinen kiintolevy, se voidaan tuntea esimerkiksi `D:\`-asemana. `E:\` on esimerkiksi CD-asema tai toinen kiintolevy. Käyttäjä voi määrittää nämä levykohtaisesti itse. Tarnnuksena mainittakoon, että laite:asema ei ole aina välttämättä one-to-one suhde; käyttäjä voi esimerkiksi luoda useasta kiintolevystä RAID-henkisen `Windows Storage Pool`:n, jolloin monta fyysistä levyä löytyy yhden aseman kirjaimen takaa.

Linuxissa tilanne on hyvin toinen. Asemia ja niiden kirjaimia ei ole olemassa. Hakemistorakenteen juuri ei siis ala laitteen/aseman kirjaimesta vaan `/`-merkistä, joka toimii Linuxissa hakemistoerottimena. Hakemistot muodostavat puurakenteen samalla tavalla kuin Windowsin hakemistot, joten on mahdollista, että `kissa.txt` sijaitsee polussa `/a/b/c/kissa.txt`. Yksittäinen hakemisto, kuten `/home` tai `/var`, voi sijaita saman levyn eri partitiolla tai jopa kokonaan eri levyllä kuin valtaosa käyttöjärjestelmästä.

Alla näkyy ajettuna komento `lsblk` eli List Block Devices.

```sh
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



## Filesystem Hierarchy Standard

Linuxin tiedostojärjestelmän standardi löytyy [Filesystem Hierarchy Standard (linuxfoundation.org)](https://refspecs.linuxfoundation.org/FHS_3.0/fhs/index.html)-sivustolta, mutta alla on listattuna tärkeimmät juuritason kansiot:

| Hakemisto    | Sisältää                                                     |
| ------------ | ------------------------------------------------------------ |
| /bin, /sbin  | C-kielestä käännettynä ajettavia binääritiedostoja, kuten yllä käytetty `lsbkl` tai hakemistojen luontiin tarkoitettu `mkdir`. Tyypillisesti viittaa lokaatioon `/usr/bin/` sekä `usb/sbin`. |
| /boot        | Kernel image, jota käytetään konetta käynnistäessä.          |
| /dev         | Fyysisiä laitteita, kuten yllä näkyvä `sda`, tai loogisia/virtuaalisia laitteita kuten partitio `sda1` tai työpöytäympäristössä käyttämäsi terminaali `/dev/pts/0`. Kokeile ajaa komento `tty`. |
| /etc         | Koko järjestelmää koskevat konfiguraatiotiedostot, kuten `/etc/hosts`, josta tarkistetaan tunnetut hostnamet ennen DNS-kyselyitä, tai `/etc/passwd`, jossa määritellään käyttäjät ja aikoinaan jopa salasanat, tai `/etc/fstab/` |
| /home        | Käyttäjien kotikansiot.                                      |
| /lib         | Jaettuja kirjastoja, joita `/bin`:ssä ja `/sbin`:ssä olevat ohjelmat tarvitsevat, kuten C-kielen kirjastot `libc.so`. |
| /mnt, /media | Automaattisesti mountattavat mediat kuten CD- sekä USB-asemat tai jopa verkkolevyt. |
| /opt         | Riippuu distribuutiosta. Paketinhallinta käyttää tai on käyttämättä. |
| /proc, /sys  | Kernelin rajapintoja, kuten `/proc/version`, joka sisältää kernelin ja distron versioon liittyvää tietoa. |
| /tmp         | Väliaikaiset tiedostot. Eivät säily ikuisesti.               |
| /usr, /var   | Käyttäjille tarkoitettuna ohjelmia.                          |







