!!! tip "Huom!"
    Asennukseen liittyvät ohjeet vanhentuvat herkästi. Mikäli tämä dokumentti ei vastaa todellisuutta, olethan ystävällinen ja teet [linux-perusteet -Github-reposta](https://github.com/sourander/linux-perusteet/) Forkin, muokkaat ohjeet vastaamaan nykypäivää, ja pyydät Pull Requestia.



# Asennus

Alla olevassa ohjeessa asennetaan Ubuntu 22.04 LTS. Voit asentaa esimerkiksi Fedora 38:n hyvin pienin muutoksin.



## Esiasetukset

Alla oleva ohjeistus on testattu Windows 11 Home -versiossa.

1. Etsi `Turn Windows features on or off`-ikkuna Windowsista.
2. Kytke `Virtual Machine Platform` päälle.

[Docker:n FAQ](https://docs.docker.com/desktop/faqs/windowsfaqs/#can-i-use-virtualbox-alongside-docker-desktop) suosittelee kytkemään päälle myös `Windows Hypervisor Platform`, mikäli haluat käyttää VirtualBoxia ja Dockeria joskus rinnakkain. Sama feature neuvotaan kytkemään päälle, mikäli haluat käyttää `Hyper-V`:tä ja VirtualBoxia yhdessä. Hyper-V vaatii Windows Pro:n, ja VirtualBox on perinteisesti tullut sen kanssa huonosti toimeen - tai ollut kokonaan toimimatta mikäli se on ollut asennettuna.



## Luo virtuaalikone

1. Asenna Oracle VM VirtualBox 7.x ([linkki](https://www.virtualbox.org/wiki/Downloads))
2. Lataa Ubuntu 20.04 Desktop Image, 64-bit AMD ([linkki](https://releases.ubuntu.com/20.04/))
3. Valitse VirtualBoxissa `Machine => New` tai klikkaa ++ctrl+n++

Täytä VirtualBoxissa aukeavaan pop-uppiin tarvittavat tiedot: 

* Valitse koneelle nimi (esim. `ubuntu2204`), kansio johon virtuaalikoneen image sekä muut tiedostot tallennetaan (esim. `C:\Users\username\VirtualBox VMs`), sekä äsken lataamasi image.
* Laita ruksi kohtaan `Skip Unattended Installation`. Jos haluat kokeilla `Plug'n'Pray`-asennusta, voit jättää ruksin paikoilleen, mutta tulet kärsimään tästä myöhemmin.
* Klikkaa Next.
* Kun kysytään, anna virtuaalikoneelle esimerkiksi `4 CPU`:ta ja `8 GB` muistia, olettaen että omassa tietokoneessasi on riittämiin tarjolla.
* Klikkaa Next.



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

Ubuntu installer vahvistaa sinulta muutokset suunnilleen näin:
```
If you continue, the changes listed below will be written to the disk. Otherwise, you will be able to make further changes manually.

The partition tables of the following devices are changed:
SCSI3 (0,0,0)(sda)

The following partitions are going to be formatted
partition #2 of SCSI3 (0,0,0) (sda) as ESP
partition #3 of SCSI3 (0,0,0) (sda) as ext4
```

Et välttämättä tällä hetkellä ymmärrä yllä olevasta tekstiä, mutta kurssin edetessä opit mitä lyhenteet tarkoittavat.

Kun odottelet hetken, Ubuntu 22.04 pyytää käynnistämään tietokoneen uusiksi, ja voit aloittaa käytön.

## UKK


#### K: Käyttäjä ei ole sudoers-ryhmässä.

V: Tämä johtunee siitä, että `Skip Unattended Installation` ei ole ollut valittuna Ubuntua asentaessa, mutta voit yrittää korjata tilanteen. 

Avaa terminaali jommalla kummalla tavalla:
1. Klikkaa ++win++ -näppäintä ja kirjoita Terminal.
2. Klikkaa ++ctrl+alt+t++

Mikäli terminaali ei käynnisty jostain syystä, mene virtuaaliterminaaliin. Klikkaa ++ctrl+alt+f3++ vaihtaaksesi virtuaaliterminaaliin. Siinä pitäisi näkyä sisäänkirjautuminen tekstimuodossa. Kirjaudu sisään. Mikäli F3:lla ei löydy virtuaaliterminaalia, kokeile muut F-näppäimet läpi.

Kun sinulla on terminaali esissä ja olet kirjaunut sisään, kirjoita:

```sh
# Loggaa root-käyttäjälle
su -

# Lisää oma käyttäjä sudoers-ryhmään
usermod -aG sudo <tähän-käyttäjänimesi>

# Loggaa ulos root-käyttäjästä
exit

# Loggaa ulos myös omasta käyttäjästäsi
# Sudo toimii kun kirjaudut taas sisään
exit
```


#### K: Ruudun yllä kalenterissa näkyy kummallisia merkkejä. Terminaali ei myöskään aukea.

V: Tämä johtunee siitä, että `Skip Unattended Installation` ei ole ollut valittuna Ubuntua asentaessa, mutta se on helposti korjattavissa. Sinulla ovat kieliasetukset väärin. 

1. Klikkaa oikealla hiirenkorvalla työpöydän taustakuvaa, valitse `Settings`. 
2. Navigoi menuun `Region & Languages`.
3. Vaihda `Format => Finland`, `Input Sources => Finnish`.
4. Loggaa ulos ja sisään.


#### K: En voi kopioida leikepöydältä tietoa VM:n ja Hostin välillä

Asenna Guest Additions. Tämä hoituu näin:

1. Klikkaa VirtualBoxin menuista `Devices => Ingest Guest Additions CD Image...`
2. Pop-up aukeaa. Klikkaa `Run`.
3. Kun asennus on ohi, poista levyke. Tämä onnistuu klikkaamalla työpöydän CD ROM -ikonia ja valitsemalla ensin `Unmount` ja sitten `Eject`.
4. Käynnistä virtuaalikone uusiksi (tai vähintään loggaa ulos ja sisään.)

Jos kohta 2:n Pop-Up ei ilmesty, klikkaa työpöydältä CD ROM -ikonia, jolloin tiedostoselaimeen avautuu virtuaalisen CD:n sisältö kansionäkymänä. Klikkaa `autorun.sh` oikealla hiirenkorvalla, valitse `Run as a Program`, ja täytä kysyttäessä salasanasi. Jatka kohtaan 3.

Jos kohdan 3 ohje ei toimi, pakota levy ulos. Valitse VirtualBoxista `Devices => Optical Drives => Remove disk from virtual drive`. Klikkaa Force pop-uppiin jos ei muuten lähde.

#### K: VM on päällä, mutta ruutu on musta.

Anna koneelle lisää muistia. Sammuta kone ja säädä sen asetuksista `Display => Video Memory: 64 MB`