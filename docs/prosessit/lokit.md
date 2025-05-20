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


!!! tip

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

## Tehtävät

!!! question "Tehtävä: Kirjoita oma lokimerkintä"

    Käytä `logger`-komentoa kirjoittaaksesi oman testiviestisi järjestelmälokeihin.  
    Tarkista sitten, että viesti on tallentunut oikein käyttämällä `journalctl --since "5 minutes ago"` -komentoa.

!!! question "Tehtävä: Tarkista palvelun lokit"

    Selvitä, miten voit tarkastella tietyn palvelun (esim. `cron` tai `sshd`) lokeja `journalctl`-komennolla.  
    Vihje: Käytä `-u`-valitsinta ja tutki, mitä tietoa saat irti esimerkiksi komennolla `journalctl -u cron --no-pager | tail -n 10`.

!!! question "Tehtävä: Todista tietyn palvelun event"

    Tee tarkoituksella jotakin, minkä saat näkymään lokissa, ja joka on monimutkaisempi event kuin `logger <viesti>` tai `cron`-palvelun tuloste. Huomaa, että etsi service, joka on vastuussa tapahtumasta, eli siis käytä lopulta komentoa:

    ```bash title="Bash"
    $ journalctl -f -u name-of-the-service
    ```

    Minkä servicen lokeissa mahtaa näkyä, jos tökkäät USB-muistitikun koneeseen?

    Minkä servicen lokeissa mahtaa näkyä, jos ajat komennon `ssh localhost`?

    Etsi jokin tällainen event, selvitä mikä service on vastuussa siitä, ja käytä `journalctl -f -u <service>`-komentoa nähdäksesi, mitä lokitietoja tulee näkyviin.

    !!! tip

        Jos olet epävarma, minkä servicen piiriin tietty tapahtuma kuuluu, voit käyttää `journalctl -f`-komentoa ilman `-u` optionia. Outputissa näkyy kaikkien servicejen eventit, joten siitä tunnistat helposti mikä service älähtää, kun teet jotakin, mikä näkyy varmana lokeissa! Rivi on syntaksiltaan jotakuinkin:

        ```
        <timestamp> <hostname> <service>: <message>
        ```
