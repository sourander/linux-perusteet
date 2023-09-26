Ydin eli kernel on C-kielelllä ja pienissä määrin assemblyllä kirjoitettu, käyttämällesi prosessorille sopivaksi binääriksi käännetty ohjelma, joka ladataan muistiin tietokoneen käynnistyessä. Ensimmäisen kernelin on kirjoittanut Linux Torvals, joka yhä hallinnoi Linuxin ytimen kehitystä. Ytimen ensisijaiset tehtävät ovat kommunikoida raudan kanssa ja tarjota muille prosesseille pääsy näihin rajapintojen kautta sekä luoda ympäristö, jossa näitä muita ohjelmia voidaan ajaa. Sulautettu järjestelmä, jossa pyörii vain yksi ohjelma, ei tarvitse käyttöjärjestelmää laisinkaan. Termit "käyttöjärjestelmä" ja "kernel" voidaan käytännössä nähdä synonyymeina.

Ydin on avointa lähdekoodia ja sen voi ladata [kernel.org-sivustolta](https://kernel.org/). Huomaathan, että eli distribuutiot voivat halutessaan muokata ydintä. Esimerkiksi Ubuntu 22.04:n ytimen koodin voi ladata komennolla `sudo apt install linux-source`. Se asentuu lokaatioon `/usr/src/` tarballina.

Kun ajossa oleva ohjelma (eli prosessi) haluaa kommunikoida raudan kanssa, se luo ytimen määrittelemän rajapinnan mukaisen pyynnön, ja ydin joko sallii tai estää pääsyn. Tämä rajapinta on `syscall` eli `system call` ja rajapinta käyttää assembly-kieltä (ks. `man 2 intro`). Tyypillisesti ohjelmat kuitenkin käyttävät C Standard Libraryä (ks. `man 3 intro`).  Jos ydin sallii pääsyn, ydin kommunikoi raudan kanssa ja palauttaa vastauksen prosessille rajapinnan mukaisesti. Ydin siis piilottaa kaiken low-level toteutuksen taakseen eli *abstrahoi* sen.

Alla näkyy kartta ytimen sisuksista jaettuna ulkoisten rajapintojen mukaisiin kaistoihin.

![Linux Kernel Map](../images/linux-kernel-map.png)

**Kuvio 1**: *Kartta Linuxin kernelistä. Alkuperäinen, interaktiivinen kuva löytyy: [Interactive map of Linux kernel (makelinux.github.io)](https://makelinux.github.io/kernel/map/). Kuva tallennettu kurssimateriaaliin saatavuuden varmistamiseksi.*



## Ytimen ja käyttäjän avaruus

Ydin itsessään pyörii omana prosessina, joka luo käyttäjän avaruuden eli **"User spacen"**. Käyttäjän avaruudessa suoritetaan ohjelmat, jotka näkyvät tavalla tai toiselle käyttäjälle. Osa näkyy ilmiselvästi, kuten graafinen työpöytä, osa näkyy esimerkiksi komennon `ps aux` avulla. Huomaa, että vaikka avaruuden nimessä on termi käyttäjä, se ei tarkoita, että ohjelmat ovat nimenomaan ihmiskäyttäjän käynnistämiä ja käyttämiä. Myös vailla interaktiivista shelliä ohjelmia ajava Linux-palvelin suorittaa ohjelmat käyttäjäavaruudessa.

Ohjelmat, jotka suoritetaan ytimen avaruudessa, suoritetaan todella laajoilla käyttöoikeuksilla, ja ohjelmilla on lähes rajaton pääsy tietokoneen resursseihin. Käyttäjän avaruudessa suoritettavat ohjelmat ajetaan sen sijaan ytimen niille antamilla ehdoilla. Ohjelman pääsyä muistiin, massamuistiin, prosessoriaikaa, ja muita resursseja voidaan rajata. Käyttäjän näkökulmasta rinnakkain ajettavat ohjelmat ajetaan "yhtä aikaa", mutta käytännössä ohjelmat vuorottelevat CPU:n ytimen tai useiden ytimien laskenta-ajasta. Myös itse ydin tarvitsee CPU-aikaa ja muistia, luonnollisesti.

![user-space_kernel-space](../images/user-space_kernel-space.png)

**Kuvio 2**: *Käyttäjän avaruuden, ytimen avaruuden ja raudan kerrokset.*



## Laiteajurit

TODO