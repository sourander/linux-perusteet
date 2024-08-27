!!! tip "Huom!"
    Asennukseen liittyvät ohjeet vanhentuvat herkästi. Mikäli tämä dokumentti ei vastaa todellisuutta, olethan ystävällinen ja teet [linux-perusteet -Github-reposta](https://github.com/sourander/linux-perusteet/) Forkin, muokkaat ohjeet vastaamaan nykypäivää, ja pyydät Pull Requestia.



# Asennus

Alla olevassa ohjeessa asennetaan Ubuntu 24.04 LTS Applen tietokoneeseen, jossa on 64-bittinen ARM-prosessori kuten Apple M2. Voit asentaa esimerkiksi Fedora 38:n hyvin pienin muutoksin, kuten myös minkä tahansa muunkin distribuution, josta löytyy 64-bittinen ARM build.

## Asenna UTM

Asenna UTM joko [UTM:n saitilta](https://mac.getutm.app/) lataamalla, App Storesta tai Homebrew:lla. Homebrew:lla sen asennus hoituu näin simppelisti:

```bash
$ brew install --cask utm
```

## Lataa image

Etsi haluamasi Ubuntun image. Huomaa, että tarvitset 64-bit ARM (`ARMv8/AArch64`) imagen. Mikäli lataat perinteisemmän `AMD64`:n, sinun tulee emuloida `x86_64`-prosessoria UTM:llä. Tämä hidastaa virtuaalikonetta merkittävästi.

## Luo virtuaalikone

1. Käynnistä UTM työpöytäsovellus
2. Klikkaa `Create a New Virtual Machine`
3. Valitse jänis eli `Virtualize`
4. Valitse Preconfigured: Linux
5. Anna defaulttien olla:

```
Virtualization Engine
[ ] Use Apple Virtualization

Boot Image Type
[ ] Boot from kernel image

Boot ISO Image:
Browse ... => Etsi lataamasi asennusmedia (esim. jammy-desktop-arm64.iso)
```   

* Kun asennusmedia on valittuna, klikkaa `Continue`. 
* Aukeaa uusi Hardware-näkymä. 
    * Valitse muistin määrä, esimerkiksi `8192 MB`, 
    * ... sekä CPU-ytimien määrä, esimerkiksi 4. 
    * Älä aktivoi hardware OpenGL accelerationia. 
* Klikkaa taas `Continue`
* Aukeaa uusi Storate-näkymä.
    * Valitse Storagen koko gigatavuina, esimerkiksi `64 GB`
* Klikkaa taas `Continue`
* Aukeaa uusi Shared Directory -näkymä
    * Aseta jaettu kansio jos tarvitset sen johonkin
* Klikkaa taas `Continue`
* Lue Summary läpi ja paina `Save`.



## Ubuntun asennus

Nyt sinulla on virtuaalikone. Paina Play-näppäintä ja Ubuntun asennus käynnistyy. Mikäli päädyt suoraan Try Ubuntu -tilassa Ubuntuun, tuplaklikkaa työpöydältä "Install Ubuntu"-kuvaketta.

* Ubuntu installer käynnistyy.
    * Anna kielen olla `English`.
    * Klikkaa Next.
* Ubuntu installer kysyy tietoja:
    * Valitse näppäimistöasetteluksi `Finnish -> Finnish (Macintosh)`.
    * Klikkaa Continue
* Ubuntu installer kysyy tietoja:
    * Valitse `Minimal Installation`
    * Valitse `Download updates while installing Ubuntu`
    * Klikkaa Continue
* Ubuntu installer kysyy tietoja:
    * Valitse `Erase disk and install Ubuntu`
    * Klikkaa Install Now.

Ubuntu installer vahvistaa sinulta muutokset suunnilleen näin:
```
If you continue, the changes listed below will be written to the disk. Otherwise, you will be able to make further changes manually.

The partition tables of the following devices are changed:
Virtual disk 1 (0,0,0)(vda)

The following partitions are going to be formatted
partition #1 of Virtual disk 1 (vda) as ESP
partition #2 of Virtual disk 1 (vda) as ext4
```

Seuraavissa ruuduissa kysellään maakohtaisia asetuksia, nimeä, käyttäjätunnusta, salasanaa ja niin edelleen. Valitse ne mielihalujesi mukaan.

Kun odottelet hetken, Ubuntu Installer pyytää käynnistämään tietokoneen uusiksi, ja voit aloittaa käytön. Mikäli kone ei muuten käynnisty, poista asennusmedia CD/DVD-asemasta ja paina Restart VM.