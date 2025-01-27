# Option B: VirtualBox

!!! tip

    Jos et jostain syystä voi asentaa Dual boottia (esim. et uskalla, tai sinulla on todella pieni SSD-levy), seuraavaksi suositelluin vaihtoehto on asentaa Linux Oracle Virtualboxin avulla. 
    
    Alla olevassa ohjeessa asennetaan Ubuntu 24.04 LTS. Varmista kurssilla suositeltu versio opettajalta.

!!! note

    Jos et saa Virtual Boxia jostain syystä toimimaan, älä jää toimettomaksi vaan ota opettajaan yhteyttä. Jos ongelma ei ratkea, etsitään vaihtoehtoinen tapa (esim. VMware vSphere tai WSL2).

## Video-ohje

VirtualBoxin ja tuoreimman Ubuntu LTS:n asennukseen löytyy niin reilusti valmiita videomuotoisia ohjeita, että en turhaan toista niitä. Alla yksi esimerkki.

<iframe width="560" height="315" src="https://www.youtube.com/embed/QXdFTEPXJ4M?si=Gd_08P0Ov-Z6nV0y" title="YouTube video player" frameborder="0" allow="accelerometer; autoplay; clipboard-write; encrypted-media; gyroscope; picture-in-picture; web-share" referrerpolicy="strict-origin-when-cross-origin" allowfullscreen></iframe>

**Video 1:** *Open Integrator -tilin ohje Windows 11:lle, jossa asennetaan VirtualBox ja Ubuntu 24.04 LTS.*

## Tekstiohje

### Esiasetukset

Alla oleva ohjeistus on testattu Windows 11 Home -versiossa. Mikäli sinulla on Windows Pro, voit käyttää Hyper-V:tä.

1. Etsi `Turn Windows features on or off`-ikkuna Windowsista.
2. Kytke `Virtual Machine Platform` päälle.

!!! note

    [Docker:n FAQ](https://docs.docker.com/desktop/troubleshoot-and-support/faqs/windowsfaqs/#can-i-use-virtualbox-alongside-docker-desktop) suosittelee kytkemään päälle myös `Windows Hypervisor Platform`, mikäli haluat käyttää VirtualBoxia ja Dockeria joskus rinnakkain.

!!! warning

    Tämä ohje ei käsittele Hyper-V:tä. Lyhyesti kuitenkin: se on Type-1 Hypervisor, ja tuoreet VirtualBox-versiot tukevat sitä backendinä (experimental feature). Vaihtoehtoisesti voit luoda Hyper-V -koneita Microsoftin omalla Hyper-V Managerilla. Jos käytät VirtualBoxia Windows Pro -versiossa, ja sinulla on suorituskykyongelmia, kokeile joko kytkeä Hyper-V pois päältä tai luo virtuaalikoneet Hyper-V Managerilla.


### Luo virtuaalikone

1. Asenna Oracle VM VirtualBox 7.x ([linkki](https://www.virtualbox.org/wiki/Downloads))
2. Lataa Ubuntu Desktop Image, 64-bit AMD ([linkki](https://ubuntu.com/download/desktop))
3. Valitse VirtualBoxissa `Machine => New` tai klikkaa ++ctrl+n++

Täytä VirtualBoxissa aukeavaan pop-uppiin tarvittavat tiedot: 

* Valitse koneelle nimi (esim. `ubuntu2204`), kansio johon virtuaalikoneen image sekä muut tiedostot tallennetaan (esim. `C:\Users\username\VirtualBox VMs`), sekä äsken lataamasi image.
* ⚠️ Laita ruksi kohtaan `Skip Unattended Installation`. Jos haluat kokeilla `Plug'n'Pray`-asennusta, voit jättää ruksin paikoilleen, mutta tulet kärsimään tästä myöhemmin. ⚠️
* Klikkaa Next.
* Kun kysytään, anna virtuaalikoneelle esimerkiksi `4 CPU`:ta ja `8 GB` muistia, olettaen että omassa tietokoneessasi on riittämiin tarjolla.
* Klikkaa Next.

!!! note

    Linux tulee olemaan virtuaalikoneessa hidas jos sitä vertaa dual boot -asennukseen. Jos haluat sukkelamman kokemuksen, asenna Linux suoraan koneellesi. Tätä varten on [Dual Boot -ohje](dualboot.md).


## Asenna OS

* Käynnistä VM Start-näppäimellä.
* Ruutuun ilmestyy GRUB.
    * Valitse `Try or Install Ubuntu`
* Ubuntu installer käynnistyy.
    * Valitse `Install Ubuntu`. Anna kielen olla `English`.
    * Klikkaa Next.
* Ubuntu installer kysyy tietoja:
    * Valitse näppäimistöasetteluksi `Finnish -> Finnish`.
    * Klikkaa Continue
* Ubuntu installer kysyy tietoja:
    * Valitse `Minimal Installation`
    * Valitse `Download updates while installing Ubuntu`
    * Klikkaa Continue
* Ubuntu installer kysyy tietoja:
    * Valitse `Erase disk and install Ubuntu`
    * Klikkaa Install Now.


Seuraavissa ruuduissa kysellään maakohtaisia asetuksia, nimeä, käyttäjätunnusta, salasanaa ja niin edelleen. Valitse ne mielihalujesi mukaan.

Kun odottelet hetken, Ubuntu Installer pyytää käynnistämään tietokoneen uusiksi, ja voit aloittaa käytön. Jos kone ei meinaa käynnistyä, poista asennusmedia CD/DVD-asemasta ja paina Restart VM.


## UKK

### K: Juuri asennettu Ubuntu ei käynnisty.

V: Käynnistä virtuaalikone uudelleen. Jos se ei auta, tarkista että asennusmedia (eli `.ISO`-tiedosto) on poistettu virtuaalikoneen CD/DVD-asemasta.

### K: Ruudun yllä kalenterissa näkyy kummallisia merkkejä. Terminaali ei myöskään aukea.

V: Tämä johtunee siitä, että `Skip Unattended Installation` ei ole ollut valittuna Ubuntua asentaessa. Asenna Ubuntu uusiksi.

### K: En voi kopioida leikepöydältä tietoa VM:n ja Hostin välillä

Asenna Guest Additions. Tämä hoituu näin:

1. Klikkaa VirtualBoxin menuista `Devices => Ingest Guest Additions CD Image...`
2. Pop-up aukeaa. Klikkaa `Run`.
3. Kun asennus on ohi, poista levyke. Tämä onnistuu klikkaamalla työpöydän CD ROM -ikonia ja valitsemalla ensin `Unmount` ja sitten `Eject`.
4. Käynnistä virtuaalikone uusiksi (tai vähintään loggaa ulos ja sisään.)

Jos kohta 2:n Pop-Up ei ilmesty, klikkaa työpöydältä CD ROM -ikonia, jolloin tiedostoselaimeen avautuu virtuaalisen CD:n sisältö kansionäkymänä. Klikkaa `autorun.sh` oikealla hiirenkorvalla, valitse `Run as a Program`, ja täytä kysyttäessä salasanasi. Jatka kohtaan 3.

Jos kohdan 3 ohje ei toimi, pakota levy ulos. Valitse VirtualBoxista `Devices => Optical Drives => Remove disk from virtual drive`. Klikkaa Force pop-uppiin jos ei muuten lähde.

### K: VM on päällä, mutta ruutu on musta.

Anna koneen näytönohjaimelle lisää muistia. Sammuta kone ja säädä sen asetuksista `Display => Video Memory: 64 MB`