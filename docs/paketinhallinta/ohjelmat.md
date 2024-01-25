Jotta voimme käsitellä ohjelmien tai sovellusten asentamista paketinhallintajärjestelmän avulla, meidän pitää ensin selventää, mitä ohjelmalla tarkoitetaan.

Alla oleva lista on tiivistelmä Learning Modern Linux (Hausenblas 2022) -kirjan Chapterin 6 alusta.

| Termi                            | Selite                                                                                                                                                                                                                                                           |
| -------------------------------- | ---------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| Program, ohjelma                 | Binääritiedosto tai executableksi (`chmod +x`) merkattu tekstitiedosto. Jälkimmäinen alkaa ensimmäisellä rivillä olevalla shebangillä, joka määrittää, millä ohjelmalla teksti pitää tulkita konekieleksi. Esimerkki: `#!/bin/bash` tai `#!usr/bin/env python3`. |
| Process, prosessi                | Ohjelman instanssi, eli entiteetti, joka käyttää CPU:ta tai I/O:ta.                                                                                                                                                                                              |
| Daemon                           | Taustalla ajettava prosessi, jota kutsutaan myös *serviceksi*. Windowsissa vastaavat löytyvät Task Manager => Services. Linuxissa näitä ajaa useimmiten `systemd`. Katso `man daemon`.                                                                           |
| Application, sovellus tai app    | Ohjelma ja sen riippuvuudet (eng. dependencies) kokonaisuudessaan: sen konfiguraatiot, data, asennus, poisto, ajaminen.                                                                                                                                          |
| Package, ohjelmapaketti          | Tiedosto, joka sisältää ohjelmia tai applikaatioita. Applikaatiot jaellaan (eng. distribute) paketteina.                                                                                                                                                         |
| Package manager, paketinhallinta | Ohjelma, joka lukee ohjelmapaketteja, ja asentaa/päivittää/poistaa ohjelman ohjeiden mukaisesti. Esimerkkejä: Pythonissa `pip`, Debian-pohjaisissa järjestelmissä `apt`, Windowsissa `winget`.                                                                   |
| Repository                       | Repositorio on kirjasto, josta paketinhallinta(järjestelmä) noutaa ohjelmat, ja johon ohjelmistonkehittäjät julkaisevat ohjelmat.                                                                                                                                |

Lisäksi ohjelmat käyttävät jaettuja kirjastoja. Yksi näistä on `libc.so`, joka on (useimmiten GCC:n) Standard C Library, ja sisältää esimerkiksi `printf`-funktion. Paketinhallinta huolehtii sinun puolestasi näiden kirjastojen asentamisesta, ja niiden riippuvuuksien hallinnasta. Alla olevalla komennoilla voit tarkistaa, mitä kirjastoja jokin binääri käyttää:

```bash
$ ldd $(which useradd)
```

## Ajastettu Python-ohjelma

Luodaan esimerkin vuoksi ajastettu Python-ohjelma, joka annetaan systemd:n [per-user instanssin](https://wiki.archlinux.org/title/Systemd/User) ajettavaksi. Vaihtoehtona olisi lisätä konfiguraatiotiedostot `/run/systemd/system`-lokaatioon system-wide instanssin ajettavaksi.

#### Python

Luo Python-executable kotikansion alaisuuteen:

```bash
$ mkdir -p ~/.local/bin/testprocessor/
$ cd ~/.local/bin/testprocessor/
$ touch main.py
$ chmod u+x main.py
```

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

```bash
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

```bash
$ systemctl --user daemon-reload
$ systemctl --user start testprocessor.timer

# Tarkista myös statukset
$ systemctl --user status testprocessor.timer
$ systemctl --user status testprocessor.service
```

Mikäli teet muutoksia `main.py`-tiedostoon tai daemonin määritelytiedostoihin, aja komento `systemctl --user daemon-reload` uusiksi.



#### Testaus

Käynnistä uusi terminaali ++ctrl+alt+t++ näppäimillä ja käynnistä lokin seuranta (`-f` optionilla).

```bash
$ journalctl --user -u testprocessor.service -f
syys 08 16:28:25 opekone systemd[2415]: Starting My Test Processor Service...
syys 08 16:28:25 opekone main.py[3748]: [INFO] Scanning: /home/opettaja/Documents/todo
syys 08 16:28:25 opekone main.py[3748]: [INFO] Processing 0 files.
syys 08 16:28:25 opekone main.py[3748]: [INFO] Processing complete.
```

Lisää toisessa terminaalissa uusi tiedosto hakemistoon, jota skripti vahtii:

```bash
$ echo "TODO" > ~/Documents/todo/tester.txt
```



#### Pysäytä

```bash
$ systemctl --user stop testprocessor.timer

# Katso myös status
$ systemctl --user status testprocessor.timer
```

