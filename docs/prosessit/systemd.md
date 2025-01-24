---
priority: 510
---

# Systemd

Systemd on Linux-järjestelmien init-prosessi, joka on korvannut sen edeltäjänsä (ks. Upstart: [init(8) - Linux man page](https://linux.die.net/man/8/init)). Systemd on ensimmäinen prosessi, joka käynnistetään (kernelin jälkeen) ja se on vastuussa muiden prosessien käynnistämisestä ja hallinnasta. Nämä asiat, joita se käynnistää, tunnetaan termillä ==unit==. Systemd reagoi eri triggeri-tapahtumiin ja on täten ==event-driven==. Tyypillisten deamon-prosessien hallinnan lisäksi sillä voi hallita myös muiden muassa mountteja ja laitteita. Tutustu systemd:n kontrollerin toimintaan joko kirjoittamalla `man 1 systemd` tai online-version avulla: [Ubuntu Manpages: systemctl - Control the systemd system and service manager](https://manpages.ubuntu.com/manpages/jammy/man1/systemctl.1.html)

```bash title="Bash"
# Tarkista kaikki saatavilla olevat komennot
$ systemctl --help

# Listaa unit-tyypit
$ systemctl -t help
```

Unit määritellään konfiguraatiotiedostossa, ja näitä sijaitsee useissa eri lokaatioissa:

1. `/etc/systemd/system/` - System-wide, admin-created
2. `/run/systemd/system/` - System-wide, runtime (dynaamiset, luodaan Linuxin ollessa ajossa)
3. `[/usr]/lib/systemd/system/` - System-wide, package-created (apt, dnf, pacman, yms.)
4. `/home/$USER/.config/systemd/user/` - Per-user, user-created
5. ks. lisää ajamalla komento `man 5 systemd.unit`

![Systemd visualisointi](../images/systemd_dalle.jpg)

**Kuvio 1:** *Systemd DALL-E 3:n näkemyksenä.*

## Peruskäyttö

Tyypillisesti Linux-käyttäjän ei välttämättä tarvitse luoda omia Unit-tiedostoja vaan paketinhallintaohjelmisto (apt, dnf, pacman, yms.) luo ne ohjelmaa asentaessa. On tärkeää osata kuitenkin peruskäyttö, eli daemonin käynnistäminen, pysäyttäminen, uudelleenkäynnistäminen, statuksen tarkistaminen ja lokien seuranta.

```bash title="Bash"
# Listaa kaikki daemon/service-tyyliset unitit
$ systemctl list-units --type=service

# Etsi hakusanalla (currently in memory)
$ systemctl list-units "*armor*"

# Etsi hakusanalla (tiedostot, ei välttämättä ajossa)
$ systemctl list-unit-files --type=service "*bolt*"
```

### Asennetaan uusi

Asennetaan nginx-palvelin, jotta meillä on jotain, mitä käynnistellä ja pysäytellä.

```bash title="Bash"
# Asenna nginx
$ sudo apt update
$ sudo apt install nginx

# Etsi, mitä kaikkea asentui
$ systemctl list-units "*nginx*"

# Voit käyttää tähän myös paketinhallintaa
$ dpkg -L nginx-common | grep systemd

# Tarkista, onko se käynnissä
$ systemctl status nginx

# Huomaa, että seuraavat kaksi komentoa tekevät saman asian
$ systemctl cat nginx
$ cat /lib/systemd/system/nginx.service

# Tarkista sen status
$ systemctl status nginx
```

Kokeile pysäyttää ja käynnistää nginx:

```bash title="Bash"
# Pysäytä ja tarkista vastaako portti 80
$ sudo systemctl stop nginx
$ curl localhost

# Käynnistä ja tarkista vastaako portti 80
$ sudo systemctl start nginx
$ curl localhost
```

!!! tip

    Ohjelmalla on erikseen status "started/stopped" ja "enabled/disabled". Ohjelman pysäytys stop-komennolla ei siis estä ohjelmaa käynnistymästä ensi bootissa! Sinun pitää erikseen asettaa `sudo systemctl disable <service>`.


### Muokataan oletussivua

Komento `curl localhost` palauttaa nginx:n oletussivun. Tutkitaan, mistä se löytyy ja muokataan sitä.

```bash title="Bash"
# Optional: Kaiva ilman dokumentaatiota tai ohjeistusta, että
#   missä nginx:n konfiguraatiotiedostot sijaitsevat. Tässä auttavat ainakin
#   alla olevat komennot:
$ dpkg -L nginx-common | grep conf
$ sudo nginx -T | grep "configuration file"
$ less /etc/nginx/nginx.conf
$ less /etc/nginx/sites-enabled/default

# Vaihda sana "Welcome" sanaksi "Tervetuloa"
$ sudo sed -i 's/Welcome/Tervetuloa/' /var/www/html/index.nginx-debian.html

# Kokeile päivittyikö sivu
$ curl localhost
```

### Service-tiedoston muokkaus

Service-tiedostot määrittelevät, miten ohjelma käynnistetään. Tiedostojen muokkaus suoraan tekstieditorilla ei ole suositeltavaa. Luo mieluummin uudet ==drop-in -tiedostot==, joissa määrittelet uudet asetukset.

```bash title="Bash"
# Luo uusi drop-in -tiedosto
$ sudo systemctl edit nginx
```

Tiedosto aukeaa systemctl:n vakioeditorilla (yleensä nano). Lisää tiedostoon seuraava sisältö (sille ohjeistettuun paikkaan - lue kommentit tiedostosta!):

```ini
[Unit]
Description=This is my fake description!
```

!!! tip 

    Tiedosto on niin sanottu `drop-in`-konfiguraatio. Linuxissa nämä toimivat yleensä siten, että `/etc/program`:n drop-in konfiguraatiotiedostot löytyvät hakemistosta `/etc/program.d/`. Tässä tapauksessa tiedosto löytyy hakemistosta `/etc/systemd/system/nginx.service.d/override.conf`. Joissakin tapauksissa drop-in -tiedostot ovat numeroituja, jolloin niiden suoritusjärjestys on määritelty tiedostonimessä.

    Järjestelmän käynnistyessä systemd lukee kaikki konfiguraatiotiedostot ja yhdistää ne yhdeksi kokonaisuudeksi. Mikäli samasta asetuksesta on useampi määritely, viimeisin voittaa. Drop-in -tiedostoilla voidaan siis ylikirjoittaa alkuperäisiä asetuksia.

```bash title="Bash"
# Tarpeen mukaan saatat joutua lataamaan systemd:n konffit uudelleen
$ sudo systemctl daemon-reload

# Kokeile käynnistää nginx uudelleen
$ sudo systemctl restart nginx

# Tarkista, että uusi kuvaus näkyy
$ systemctl status nginx

# Katso myös cat:lla
$ systemctl cat nginx
```

!!! tip

    Jos ihmettelet, mikä on service-konfiguraatiotiedossa näkynyt `After=network.target`, niin se tarkoittaa, että ohjelma käynnistyy vasta kun verkko on käytettävissä. Huomaa, että systemd itsessään on ensimmäinen käynnistettävä ohjelma, joten sen asetuksilla voi määrittää, mitä kaikkea käynnistetään ja missä järjestyksessä. Targetit ovat systemd:n tapa määritellä tämä.

    Jos haluat, että Linux ei käynnisty laisinkaan graafiseen käyttöliittymään, voit muuttaa `multi-user.target`-targetiksi. Tämä on hyödyllistä esimerkiksi palvelimilla, joissa ei ole tarvetta graafiselle käyttöliittymälle.

    ```bash title="Bash"
    $ sudo systemctl get-default
    $ sudo systemctl set-default multi-user.target # vaihtoehtona graphical.target
    $ sudo systemctl reboot
    ```

    Jos haluat ihan listata nykyisen targetin (eli yleensä `graphical.target` )riippuvuudet, voit käyttää `list-dependencies`-komennon.

    ```bash title="Bash"
    $ systemctl list-dependencies
    ```

!!! warning

    Jos et tarvitse NGINX:ää, kannattaa se poistaa tässä välissä. Tämä hoituu komennolla `sudo apt remove nginx`. Muista riippuvuuksista pääset eroon komennolla `sudo apt autoremove`. Huomaa, että konfiguraatiotiedostot jäävät kuitenkin paikoilleen (ks. `/etc/nginx/`).


## Esimerkki: Ajastettu Python-ohjelma

![Python TODO](../images/systemd_python_todo_dalle.jpg)

**Kuvio 2:** *Python TODO-ohjelma DALL-E 3:n piirtämänä.*

Luodaan esimerkin vuoksi ajastettu Python-ohjelma, joka annetaan systemd:n [per-user instanssin](https://wiki.archlinux.org/title/Systemd/User) ajettavaksi. Vaihtoehtona olisi lisätä konfiguraatiotiedostot `/run/systemd/system`-lokaatioon system-wide instanssin ajettavaksi.

Alla lyhyt kuvaus ohjelmasta, jonka luomme:

* Ohjelma etsii tiedostoja `todo`-kansiosta.
* ... jos se löytää, se:
    * siirtää tiedoston `doing`-kansioon.
    * vaihtaa sisällön `TODO`-sanat `DONE`-sanoiksi.
    * valmis tiedosto löytyy `done`-kansiosta.
* Ohjelma ajetaan minuutin välein käyttäjän ollessa kirjautuneena.
* Ohjelman working directory määritetään `.service`-tiedostossa.

#### Python

Luo Python-executable kotikansion alaisuuteen:

```bash title="Bash"
$ mkdir -p ~/.local/bin/testprocessor/
$ cd ~/.local/bin/testprocessor/
$ touch main.py
$ chmod u+x main.py
```

!!! question "Tehtävä"

    Muistele, miksi tiedostolle annetaan `u+x`-oikeus. Mikäli et muista, kertaa aiempia materiaaleja tiedostojen oikeuksista. Tiedostojen käyttöoikeuksien ymmärtäminen on Linux-perusteiden kannalta kriittistä.

Lisää seuraava sisältö `main.py`-tiedostoon:

```python
#!/usr/bin/python3

from pathlib import Path

# Define the folder names
todo, doing, done = "todo", "doing", "done"

# Create the folders if they don't exist
for folder in [todo, doing, done]:
    Path(folder).mkdir(parents=True, exist_ok=True)

print(f"[INFO] Scanning: {Path(todo).absolute()}")

# Get a list of files in the todo folder
files_to_process = list(Path(todo).glob("*.txt"))

print(f"[INFO] Processing {len(files_to_process)} files.")

# Process each file
for file_path in files_to_process:
    filename = file_path.name
    todo_path = Path(todo) / filename
    doing_path = Path(doing) / filename
    done_path = Path(done) / filename

    # Move from todo to doing
    todo_path.rename(doing_path)

    # Process
    with doing_path.open("r") as file:
        content = file.read()
        content = content.replace("TODO", "DONE")

    # Write the processed content to the done folder
    with done_path.open("w") as file:
        file.write(content)

    # Remove the file from the doing folder
    doing_path.unlink()

print("[INFO] Processing complete.")
```



#### Service ja Timer

Luo service ja timer konfiguraatiot paikkaan:

```bash title="Bash"
$ mkdir -p ~/.config/systemd/user/
$ cd ~/.config/systemd/user/
$ touch testprocessor.service
$ touch testprocessor.timer
```

Ajan syntaksin docs: [systemd.time (www.freedesktop.org)](https://www.freedesktop.org/software/systemd/man/systemd.time.html)

Lisää seuraava sisältö `testprocessor.service` tiedostoon:

```ini
[Unit]
Description=My Test Processor Service

[Service]
Type=oneshot
WorkingDirectory=%h/Documents/
ExecStart=%h/.local/bin/testprocessor/main.py
```

Lisää seuraava sisältö `testprocessor.timer` tiedostoon:

```ini
[Unit]
Description=Timer for My Test Processor Service

[Timer]
OnCalendar=minutely
```



#### Käynnistä

```bash title="Bash"
$ systemctl --user daemon-reload
$ systemctl --user start testprocessor.timer

# Tarkista myös statukset
$ systemctl --user status testprocessor.timer
$ systemctl --user status testprocessor.service

# Tarkista myös list:llä
$ systemctl --user list-units
$ systemctl --user list-timers
```

Mikäli teet muutoksia `main.py`-tiedostoon tai daemonin määritelytiedostoihin, aja komento `systemctl --user daemon-reload` uusiksi.



#### Testaus

Käynnistä uusi terminaali ++ctrl+alt+t++ näppäimillä ja käynnistä lokin seuranta (`-f` optionilla).

```bash title="Bash"
$ journalctl --user -u testprocessor.service -f
syys 08 16:28:25 opekone systemd[2415]: Starting My Test Processor Service...
syys 08 16:28:25 opekone main.py[3748]: [INFO] Scanning: /home/opettaja/Documents/todo
syys 08 16:28:25 opekone main.py[3748]: [INFO] Processing 0 files.
syys 08 16:28:25 opekone main.py[3748]: [INFO] Processing complete.
```

Lisää toisessa terminaalissa uusi tiedosto hakemistoon, jota skripti vahtii:

```bash title="Bash"
$ echo "TODO" > ~/Documents/todo/tester.txt
```



#### Pysäytä

```bash title="Bash"
$ systemctl --user stop testprocessor.timer

# Katso myös status
$ systemctl --user status testprocessor.timer
```