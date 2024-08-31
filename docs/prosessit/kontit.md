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