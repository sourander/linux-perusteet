---
priority: 400
---

# Ohjelmat

Jotta voimme käsitellä ohjelmien tai sovellusten asentamista paketinhallintajärjestelmän avulla, meidän pitää ensin selventää, mitä ohjelmalla tarkoitetaan.

Alla oleva lista on tiivistelmä Learning Modern Linux (Hausenblas 2022) -kirjan Chapterin 6 alusta.

| Termi                            | Selite                                                                                                                                                                                                                                                            |
| -------------------------------- | ----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| Program, ohjelma                 | Binääritiedosto tai executableksi (`chmod +x`) merkattu tekstitiedosto. Jälkimmäinen alkaa ensimmäisellä rivillä olevalla shebangillä, joka määrittää, millä ohjelmalla teksti pitää tulkita konekieleksi. Esimerkki: `#!/bin/bash` tai `#!/usr/bin/env python3`. |
| Process, prosessi                | Ohjelman instanssi, eli entiteetti, joka käyttää CPU:ta tai I/O:ta.                                                                                                                                                                                               |
| Daemon                           | Taustalla ajettava prosessi, jota kutsutaan myös *serviceksi*. Windowsissa vastaavat löytyvät Task Manager => Services. Linuxissa näitä ajaa useimmiten `systemd`. Katso `man daemon`.                                                                            |
| Application, sovellus tai app    | Ohjelma ja sen riippuvuudet (eng. dependencies) kokonaisuudessaan: sen konfiguraatiot, data, asennus, poisto, ajaminen.                                                                                                                                           |
| Package, ohjelmapaketti          | Tiedosto, joka sisältää ohjelmia tai applikaatioita. Applikaatiot jaellaan (eng. distribute) paketteina.                                                                                                                                                          |
| Package manager, paketinhallinta | Ohjelma, joka lukee ohjelmapaketteja, ja asentaa/päivittää/poistaa ohjelman ohjeiden mukaisesti. Esimerkkejä: Pythonissa `pip`, Debian-pohjaisissa järjestelmissä `apt`, Windowsissa `winget`.                                                                    |
| Repository                       | Repositorio on kirjasto, josta paketinhallinta(järjestelmä) noutaa ohjelmat, ja johon ohjelmistonkehittäjät julkaisevat ohjelmat.                                                                                                                                 |

Lisäksi ohjelmat käyttävät jaettuja kirjastoja. Yksi näistä on `libc.so`, joka on (useimmiten GCC:n) Standard C Library, ja sisältää esimerkiksi `printf`-funktion. Paketinhallinta huolehtii sinun puolestasi näiden kirjastojen asentamisesta, ja niiden riippuvuuksien hallinnasta. Alla olevalla komennoilla voit tarkistaa, mitä kirjastoja jokin binääri käyttää:

```bash title="Bash"
$ ldd $(which useradd)
```
