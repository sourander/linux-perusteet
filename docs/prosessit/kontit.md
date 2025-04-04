---
priority: 540
---

# Kontit

Tämä otsikko voi äkkiseltään tuntua aiheeseen liittymättömältä, mutta Linux-kontit ovat tavallisia prosesseja Linux-käyttöjärjestelmässä. Kerneliä voi käyttää konttien runtimenä. Tähän löytyy ainakin kaksi hyvinkin Linux-natiivia ratkaisua: LXC (LinuX Containers) sekä systemd-nspawn.

Mikäli sinulla on jossakin muussa käyttöjärjestelmässä (kuten Windows tai macOS) esimerkiksi Docker Desktop asennettuna, sinulla on käytännössä aina myös virtuaalikone, jossa pyörii Linux. Kontit ovat lähes poikkeuksetta Linux-kontteja.

## LXC

LXC on ainakin kirjoitushetkellä jäänyt pahasti Dockerin ja Podmanin jalkoihin, mutta kokeillaan sitä siitä huolimatta.

```bash title="Bash"
# Tarkista, että lxd on asennettuna
$ snap list lxd

# Jos ei, asenna
$ sudo snap install lxd

# Initoi lxd - vastaa default vastaus kaikkeen.
$ sudo lxd init

# Käynnistä hitusen vanhempi Ubuntu kontissa
$ lxc --help
$ lxc launch ubuntu:18.04 democontainer

# Tarkista että se on luotu
$ lxc list

# Käynnistä bash
$ lxc exec democontainer -- bash

# Loggaa ulos
$ exit
```

## Docker

Docker sinulla on jo asennettuna, jos olet noudattanut kurssin ohjeita. Docker on todennäköisesti myös ajossa siten, että sitä ajetaan rootless Dockerilla. Tämä tarkoittaa, että Dockerin kontit ajetaan sinun käyttäjän oikeuksilla, eivätkä ne voi vaikuttaa toisiinsa. 

## Tehtävät

!!! question "Tehtävä: Docker ps"

    Avaa ylimääräinen terminaali ja avaa siinä interaktiivinen kontti, jonka jätät käyntiin:

    ```bash title="Bash"
    $ docker run -it --rm python:3 python -m http.server 8080
    ```

    Tämän jälkeen avaa toinen terminaali-ikkuna ja pyri tutkimaan, missä kontti näkyy sinun prosesseissasi. Voit etsiä sitä esimerkiksi melko uniikilla `http.server`-merkkijonolla. Kenties `ps aux | grep http.server` voisi toimia? Toinen vaihtoehto on kysyä Dockerilta itselsään, esimerkiksi näin:

    ```console title="Bash"
    $ docker ps
    CONTAINER ID   IMAGE         COMMAND
    123afffff      python:3      "python -m http.server 8080"

    $ docker inspect 123afffff | grep -i pid
            "Pid": 9348,
            "PidMode": "",
            "PidsLimit": null,
    
    $ ps -fp 9348
    UID       PID    PPID  C STIME TTY          TIME CMD
    user      9348   9321  0 15:09 pts/0    00:00:00 python -m http.server 8080

    $ pstree 9321
    containerd-shim─┬─python
                └─11*[{containerd-shim}]

    $ lsns -p 9348
            NS TYPE   NPROCS   PID USER      COMMAND
    4026531834 time      109  2853 user rootlesskit --state-dir=/run/user/1000/
    4026533041 user        6  2901 user └─/proc/self/exe --state-dir=/run/user/
    4026532976 mnt         1  9348 user python -m http.server 8080
    4026532977 uts         1  9348 user python -m http.server 8080
    4026532979 ipc         1  9348 user python -m http.server 8080
    4026532980 pid         1  9348 user python -m http.server 8080
    4026532981 cgroup      1  9348 user python -m http.server 8080
    4026532982 net         1  9348 user python -m http.server 8080
    ```

    Huomaa, että prosessi on tavallinen prosessi muiden joukossa, jota ajetaan sinun oikeuksin, mutta:

    1. Sitä ajetaan `containerd-shim`:n lapsena, joka on Dockerin käyttämä prosessi, joka huolehtii konttien ajamisesta. `containerd` luo kutakin konttia varten oman `containerd-shim`-prosessin, joka huolehtii kontista ja sen elinkaaren hallinnasta.
    2. Kontitettu prosessi on eristyksissä muista prosesseista, koska se ajetaan omassa prosessiavaruudessaan (namespace) ja resurssirajoituksessaan (cgroup).
    
    Huomaa, että **kontin sisällä** PID on `1`, mutta **isäntäjärjestelmässä** se on `9348` (tai mikä se sinulla ikinä onkaan).

    **Jos olet kyberturvallisuudesta kiinnostunut**, voit tutustua [Docker Engine security](https://docs.docker.com/engine/security/) -sivustoon. Voit myös lukea lisää namespaces/groups ominaisuuksista esimerkiksi `man namespaces`- ja `man cgroups`-komentojen avulla. Kenties haluat myös tutustua siihen, kuinka docker client, dockerd, containerd, containerd-shim ja runc toimivat yhdessä esimerkiksi [containerd vs. Docker: Understanding Their Relationship and How They Work Together](https://www.docker.com/blog/containerd-vs-docker/)-blogipostauksen avulla.
    
    **Jos et olet kiinnostunut**, tai haluat sysätä tämän tehtävän myöhemmäksi, voit kuitata tämän tehtävän suoritetuksi, kunhan olet saanut onnistuneesti ajettua kontin ja löytänyt sen prosessin ID:n lokaalista järjestelmästäsi.


