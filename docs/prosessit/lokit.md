---
priority: 530
---

# Lokit

Linuxissa on kattavat lokit lähes kaikesta tapahtuneesta, mikä mahdollistaa vianselvityksen. Lokitiedostot ovat yleensä `/var/log`-hakemistossa. Tässä luvussa käymme läpi, miten voit lukea lokitiedostoja ja miten voit seurata prosessien lokitapahtumia.

## Lokit

### Lokiin käsin kirjoittaminen ja sen lukeminen

```bash title="Bash"
# Kirjoita merkkijono system logiin
$ logger "Tämä on testi"

# Käy lukemassa systemd journalia - olettaen että käytössä on systemd-journald
journalctl --since "5 minutes ago"
```

### Systemd-journald

Teoriassa kukin Linux-distribuutio voi käyttää omaa lokijärjestelmäänsä, mutta käytännössä suurin osa käyttää `systemd-journald`-järjestelmää ja/tai `rsyslogd`-järjestelmää.

Perinteinen Linuxin lokijärjestelmä on `syslog`, mutta systemd on tuonut mukanaan oman journalinsa. `systemd-journald` on järjestelmäpalvelu, joka kerää ja tallentaa lokitietoja. Se luo ja ylläpitää strukturoituja, indeksoituja lokia, jotka perustuvat lokitietoon, joka on saatu monista eri lähteistä. Nämä lähteet listataan sivulla `man 8 systemd-journald`. Distribuutiosta riippuen sinulla voi olla joko pelkästään `systemd-journald` tai lisäksi myös `rsyslogd`. Esimerkiksi Ubuntussa komennolla `sudo systemctl list-units *log*` löytyy kummatkin.

    * Kernel log messages, via kmsg
    * Simple system log messages, via the libc syslog(3) call
    * Structured system log messages via the native Journal API, see sd_journal_print(3) and Native Journal Protocol[1]
    * Standard output and standard error of service units. For further details see below.
    * Audit records, originating from the kernel audit subsystem

Systemd:n journalia luetaan komennolla `journalctl` (`/usr/bin/journalctl`). 

!!! tip

    Tätä serviceä, kuten yleensä muitakin, voi konfiguroida tiedostojen avulla, jotka sijaitsevat `/etc`-hakemiston alaisuudessa. Tarkempi ohjeistus löytyy `man 8 journalctl`-sivulta.

### Rsyslogd

Kuten yllä mainittiin, sinulla saattaa olla `systemd-journald`:n kyljessä tai tilalla `rsyslodg`. Tästä löydät lisätietoa `man rsyslogd`.

!!! tip

    Käy kurkkaamassa `man rsyslogd`:ssa mainittua konfiguraatiotiedostoa `/etc/rsyslog.conf` ja `/etc/rsyslog.d/`-hakemistoa.


!!! question "Tehtävä"

    Rsyslog ja muut lokeja kirjoittavat sovellukset luovat lokinsa yleensä `/var/log`-hakemistoon. Kokeile listata kaikki kyseisen hakemiston tiedostot ja kansiot, joissa ei ole numeroita, ja näet mitä kaikkea siellä on. Alla on komento tätä varten.

    ```bash title="Bash"
    $ ls -1F --group-directories-first /var/log | grep -v '[0-9]'
    ```

    Vertaa näitä tiedostoja ja kansioita rsyslog.conf-tiedostossa listattuihin tiedostoihin.

Huomaat, että tyypillisiä tiedostoja ovat esimerkiksi:

* `auth.log` - käyttäjän kirjautumiset
* `syslog` - järjestelmän lokit
* `dmesg` - kernel ring buffer

Binäärimuotoiset tiedostot eivät ole suoraan luettavissa, mutta niitä voi lukea komennolla `dmesg` tai `journalctl`.

### Keskitetty lokitus

Keskitetty lokitus tarkoittaa, että lokitiedostot kerätään yhteen paikkaan. Tämä on hyödyllistä, jos sinulla on useita palvelimia, joista haluat kerätä lokit yhteen paikkaan. Tämä onnistuu esimerkiksi `rsyslog`:n avulla. Nämä asetukset säädetään `rsyslog.conf`-tiedostossa tai drop-in -tiedostoissa `/etc/rsyslog.d/`-hakemistossa.

Lähettävän koneen konfiguraatio, joka neuvotaan [Rsyslog: Sending Messages to a Remote Syslog Server](https://www.rsyslog.com/sending-messages-to-a-remote-syslog-server/)-ohjeessa, voisi olla:

```bash title="Bash"
# This could be in this file, for example:
# /etc/rsyslog.d/99-forward.conf
*.* @somehost.example.com:514
# or like this:
*.* action(type="omfwd" target="somehost.example.com" port="514" protocol="tcp")
```

Käy katsomassa vastaanottavan koneen konfiguraatio, joka neuvotaan [Rsyslog: Receiving Messages from a Remote System](https://www.rsyslog.com/receiving-messages-from-a-remote-system/)-ohjeessa.

Lokien keskittämisen voi hoitaa myös muilla avoimen lähdekoodin ratkaisuilla tai kaupallisilla ratkaisuilla. Lisäksi eri pilvipalveluntarjoajat tarjoavat omia ratkaisujaan. Näiden käsittely on tämän kurssin skoopin ulkopuolella.

## Case: tracker-extract-3

Tässä esimerkissä seuraamme `tracker-extract-3`-prosessia. Tracker on tiedostojen indeksointiin tarkoitettu ohjelma, joka on oletuksena asennettuna monissa Linux-jakeluissa. Trackerin tarkoitus on indeksoida tiedostojärjestelmää, jotta käyttäjä voi helposti löytää tiedostoja. Lokista paljastuu (ks. code block alla), että kyseinen prosessi ei käynnisty, koska se yrittää suorittaa kiellettyjä systeemikutsuja. Tämä luonnollisesti syö turhaan resursseja ja aiheuttaa turhia rivejä lokiin.

```log
helmi 07 10:15:11 opettajakone systemd[1280]: Starting Tracker metadata extractor...
helmi 07 10:15:11 opettajakone tracker-extract-3[3116]: Disallowed syscall "epoll_create1" caught in sandbox
helmi 07 10:15:12 opettajakone systemd[1280]: tracker-extract-3.service: Main process exited, code=dumped, status=31/SYS
helmi 07 10:15:12 opettajakone systemd[1280]: tracker-extract-3.service: Failed with result 'core-dump'.
helmi 07 10:15:12 opettajakone systemd[1280]: Failed to start Tracker metadata extractor.
helmi 07 10:15:12 opettajakone systemd[1280]: tracker-extract-3.service: Scheduled restart job, restart counter is at 5.
```

Palvelu ajetaan minun käyttäjäni nimissä, joten se löytyy komennoilla:

```bash title="Bash"
$ systemctl --user status tracker-extract-3
$ systemctl --user cat tracker-extract-3
```

En koe tarvitsevani kyseistä palvelua. Voin etsiä tiedostoja `find` komennolla tai `locate`-komennolla, joista jälkimmäisellä on oma indeksinsä, joka päivitetään komennolla `updatedb`. Tämän vuoksi poistan palvelun käytöstä maskaamalla sen. Tähän, kuten moniin muihinkin Linux-ongelmiin, löytyy hyvää apua Internetistä. Tässä tapauksessa ohje löytyy muun muassa sivustolta [Linux Uprising: How To Completely Disable Tracker, GNOME's File Indexing And Search Tool](https://www.linuxuprising.com/2019/07/how-to-completely-disable-tracker.html)

Ensimmäiseksi ohje käskee maskaamaan servicet eli luomaan symbolisen linkin `/dev/null`-tiedostoon. Tämä estää palvelua käynnistymästä. Tämän voi myöhemmin purkaa komennolla `unmask`.

```bash title="Bash"
systemctl --user mask tracker-extract-3.service \
tracker-miner-fs-3.service \
tracker-miner-rss-3.service \
tracker-writeback-3.service \
tracker-xdg-portal-3.service \
tracker-miner-fs-control-3.service
```

Lopulta palvelu tulee pysäyttää komennolla:

```bash title="Bash"
tracker3 reset -s -r
```