GNU Bashin shell-syntaksissa välilyönti, tab, newline ja muut metamerkit (`|`, `&`, `;`, `(`,`)`, `<`, `>`) toimivat erottimina, jolla käyttäjän syöttämä (tai tiedosta luettu) syöte jaetaan osiksi, jotka sittemmin tunnistetaan joko komennoiksi tai operaattoreiksi. Komennot voivat olla sisäisiä (eng. built-in) kuten `cd` tai ulkoisia kuten `nano`. Ne voivat olla myös aliaksia tai funktioita. Tarkemmat shellin vaiheet [löytyvät ohjekirjasta](https://www.gnu.org/software/bash/manual/bash.html#Shell-Operation). Tärkeää on muistaa, että välilyönti ja newline ovat erottimia.

UNIX:stä periytyvissä käyttöjärjestelmissä komennot noudattavat tyypillisesti POSIX-standardiperheen ["utility argument syntax"-käytäntöä](https://pubs.opengroup.org/onlinepubs/9699919799/basedefs/V1_chap12.html). Mikäli käytössä on bash-yhteensopiva shell, kuten yleensä on, niin lisämauteena ovat [GNU:n lisäämät pitkät option-nimet](https://www.gnu.org/prep/standards/html_node/Command_002dLine-Interfaces.html#Command_002dLine-Interfaces). Mikäli käytät jotakin muuta shelliä kuin bashiä, toiminnallisuus voi poiketa.

Tutkitaan tätä käytännössä alla olevan syötteen avulla. Stdout on ignoorattu, jotta koodi pysyisi lyhyenä, mutta kokeile toki ajaa lokaalisti komennot:

```bash
# Lähtöpiste
# Huomaa, että pitkä option toimii sekä yhtäsuuruismerkin
# kuin välilyönnin avulla eli --ignore Desktop on myös ok.
$ ls -lah --inode --ignore=Desktop ~/

# Useimmille komennoille löytyy lyhyt ja pitkä option format
# Pitkä komento --inode on lyhennetty lyhyeksi -i:ksi
$ ls -lah -i --ignore=Desktop ~/

# Myös ignorelle löytyy lyhyt formaatti. Huomaa case sensitive.
$ ls -lah -i -I Desktop ~/

# Kaikki argumentteja odottamattomat lyhyet optionit voi kirjoittaa
# yhteen. Ne sisältävät aina vain yhden kirjaimen.
$ ls -lahi -I Desktop ~/

# Lyhyet optionit voi myös järjestää haluamallaan tavalla
$ ls -ihal -I Desktop ~/

# Ainoan argumentteja odottavan optionin voi jättää listan viimeksi.
$ ls -ihalI Desktop ~/

# Ja myös välilyönnin voi poistaa
ls -ihalIDesktop ~/
```

Syötteessä ei ole muita metamerkkejä kuin välilyönti, joten kyseessä on yksinkertainen komento. Bash etsii itse komentoa useista eri paikoista (funktioista, aliaksista, built-ineista, `$PATH`:sta) ja ajaa ensimmäisen löytyneen. Muut osat eli `-lah`, `--inode` ja ``--ignore=Desktop``  syötetään ohjelmalle, ja ohjelma parsii ne parhaaksi katsomallaan tavalla optionseiksi, optioneiden argumenteiksi, ja argumenteiksi. Lue lisää esimerkkejä täältä: [Conventions for Command Line Options (nullprogram.com)](https://nullprogram.com/blog/2020/08/01/)

Huomaa, että lyhyet komennot eivät ole mikään itsetarkoitus. Yllä olevan komennon voi kirjoittaa huomattavasti luettavammassa muodossa näin:

```bash
$ ls -l --all --human-readable --inode --ignore=Desktop ~
```

Todella pitkät komennot voi jakaa usealle riville `\` merkin avulla. Kyseinen merkki on Bashissä `ESCAPE`, ja se pakenee eli ignooraa seuraavan merkin, joka olisi tässä tapauksessa rivinaihto. Huomaathan, että escapen jälkeen ei saa olla välilyöntiä ennen ++enter++ painamista, tai välilyönti on se merkki, joka on `ESCAPE`:n kohde:

```bash
$ ls \
> -l --all \
> --human-readable \
> --inode \
> --ignore=Desktop ~
```

!!! question "Tehtävä"
    Kokeile yllä olevaa monirivistä komentoa shellissä. Kirjoita se rivi riviltä: älä yritä kopioida ja liittää rimpsua kokonaisuudessaan.



## Useat argumentti

Huomaa, että monet komennot huolivat useita argumentteja. Alla esimerkki:

```
$ ls ~/Downloads ~/Documents
Documents/:
my_file

Downloads/:
Pedra_Azul_Milky_Way.jpg.webp
```

Joskus, joskin harvoin, optioneiden päättymistä ja argumenttien alkamista erotetaan `--` merkeillä. Näinpä alla oleva komento on sama kuin yllä oleva:

```bash
$ ls -- ~/Downloads ~/Documents
```



## Komentojen löytäminen

Bashin tuntemat built-init löytää (built-in)-komennolla:

```bash
$ compgen -b
```

...ja kaikki komennot:

```bash
$ compgen -c
```

Bash etsii muita komentoja ympäristömuuttujasta $PATH. Ympäristömuutujat esitellään muualla, mutta voit listata sen sisällön näin:

```bash
$ echo $PATH
/usr/local/sbin:/usr/local/bin:/usr/sbin:/usr/bin:/sbin:/bin

$ echo $PATH | tr ":" "\n"   # Paranna luettavuutta (1)
/usr/local/sbin
/usr/local/bin
/usr/sbin
/usr/bin
/sbin
/bin
```

1. Komento tr vaihtaa tässä tapauksessa kaksoispisteen rivivaihdoksi. Tutustu komentoon `tr` alla olevien ohjeiden avulla.

Jos haluat selvittää, missä polussa jokin ajettava PATH:ssa oleva ohjelma on, tai mikä on jonkin aliaksen määritelmä, kokeile seuraavia komentoja:

```bash
# Tämä on deprekoitunut ainakin Debianissa mutta toimii yhä
$ which ls
ls: aliased to ls -G

# Tämä on ylemmän sijasta suositeltu komento
$ command -v ls
alias ls='ls -G'

# Myös type palauttaa polun. Alias vaatii -a flagin.
$ type -a ls
ls is an alias for ls -G
ls is /bin/ls
```

!!! question "Tehtävä"

    Kokeile yllä olevia komentoja jotakin toista ohjelmaa, kuten `bash` tai `nano` tai `python3` vasten.


## Komentojen ohjeiden löytäminen

Alla joitakin hyödyllisiä tapoja tutustua komennon sielunelämään.

1. Lähes jokainen ohjelma vastaa pitkään optioniin  `--help` tulostamalla oman helpin. 
2. Shellin omat built-init tyypillisesti tulostavat helpin komennolla `help <komento>`. Huomaa, että help itsessään on yksi built-in.
3. Komento `man <komento>` tulostaa komennon käyttöohjeen, mikäli se löytyy man pagesista (ks. `usr/share/man`). Komennon itsensä ohjeet löytyvät myös sieltä: kokeila ajaa `man man`.
4. Komento `man -k <hakusana>` palauttaa listan sivuista, jotka sisältävät hakusanan. Tätä voi käyttää myös komentojen etsimiseen.

    !!! tip
    
        Jos asennuksesi on kovin tuore, man-sivuston tietokantaa ei ole välttämättä päivitetty. Jos saat outputin `<hakusana>: nothing appropriate` sellaiselle hakusanalle, jolle voisi kuvitella löytyvän tietoa (esim. `user`), päivitä tietokanta komennolla `sudo mandb`.

5. Komento `info <komento>` palauttaa infosivuston, joka sisältää Internet-sivuilta tutun tavan linkittää documenteja yhteen. Voit navigoida linkkiin painamalla ++enter++.
6. Komento `type <komento>` paljastaa, onko komento alias, built-in vai jossakin PATH:n lokaatiossa oleva ohjelma.
7. Internetin hakukoneet. Varmistathan, että ymmärrät mitä komennot tekevät ennen kuin ajat niitä.



## Muuttujat

Voit luoda nykyisen shellin skooppiin muuttujia ja käyttää niitä muun muassa lyhentämään komentoja. Huomaa, että `=`-merkin ympärillä ei saa olla välilyöntejä. Alla esimerkki:

```bash
$ url="https://jsonplaceholder.typicode.com"
$ curl $url/posts/1   # GET data
{
  "id": 1,
  "body": "Some really long body."
}
```

Mikäli haluamme päivittää yllä näkyvän rivin lyhyemmäksi, voimme uusiokäyttää url-muuttujaa ja luoda pari uutta:

```bash
$ new_data='{"body": "This is a shorter body."}'
$ header='Content-Type: application/json'
$ curl -X PATCH -H "$header" -d "$new_data" $url/posts/1
{
  "id": 1,
  "body": "This is a shorter body."
}
```

Paikallisesta shell-muuttujasta voi muuntaa ympäristömuuttujan (eng. environment variable) komennolla `export <muuttuja>`, jolloin niihin pääsee käsiksi prosessit eli ohjelmat, joita käyttäjä ajaa. Näitä käytetään ajoittain konfiguraatiotiedoston jatkeena tai korvikkeena. Esimerkiksi Amazon AWS:n CLI etsii tokeneita sekä asetuksia ympäristömuuttujista. Ne voi asettaa näin:

```bash
$ AWS_ACCESS_KEY_ID=AKIAIOSFODNN7EXAMPLE
$ export AWS_ACCESS_KEY_ID 
```

Saman voi tehdä myös yhdellä rivillä:

```bash
$ export AWS_ACCESS_KEY_ID=AKIAIOSFODNN7EXAMPLE
```

Mikäli tunnuksia sisältävät ympäristömuuttujat ovat asetettuina, AWS CLI -komennot, kuten S3-bucketit listaava `aws s3 ls`, käyvät poimimassa itselleen tärkeitä arvoja ympäristömuuttujista. Huomaathan, että konfiguraatiotiedostot ovat yleisesti turvallisempina pidetty keino asettaa konfiguraatiot paikoilleen: jokin ohjelma saattaa vikatilanteessa tulostaa ympäristömuuttujia, ja näin vuotaa arkaluonteisia arvoja väärien silmäparien katseltaviksi.

!!! question "Tehtävä"
    Tutustu jo valmiiksi asetettuihin ympäristömuuttujiin komennolla `printenv`.



## Merkkijonot

Komennoissa käytetään usein argumentteina merkkijonoja, joten tässä välissä on hyvä oppia, kuinka shell reagoi tiettyihin metamerkkeihin aiheuttaen 

```bash
$ echo 'Onko $USER täällä?'     # ''-merkit tekevät merkkijonosta literaalin
Onko $USER täällä?

$ echo "Onko $USER täällä?"     # ""-merkit sallivat erilaiset substitutionit
Onko opettaja täällä?

$ echo "Tänään on: $(date -I)"  # Command substitution
Tänään on: 2023-12-31

$ echo "Sormia on: $((5 + 5))"  # Arithmetic substitution
Sormia on: 10

$ echo Liian \                  # Line continuation
> pitkä lause \
> yhdelle riville
Liian pitkä lause yhdelle riville

$ touch my/{tralala,dingdingdong}   # Brace expansion

echo Elämän tarkoitus: \        # Parameter expansion
> ${MEANING_OF_LIFE:-42}  
42

$ echo $'c\nb\na'               # ANSI-C Quoting (1)
c
b
a
```

1. Yksittäisten lainausmerkkien välissä oleva, dollareiden edeltävä merkkijono, voi sisältää poistumismerkillä (kenoviiva, `\`)   alkavia taikasanoja, joista dekoodataan myöhemmin haluttu merkki. Yleisesti tarpeellisin on rivinvaihto eli `\n`. Lue lisää: [Bash Reference Manual (gnu.org)](https://www.gnu.org/savannah-checkouts/gnu/bash/manual/bash.html#ANSI_002dC-Quoting)

Jos mietit, että mikä on `\n` yllä näkyvässä `echo $'c\nb\na'` komennossa, niin kyseessä on line feed eli newline character. Huomaa, että echo lisää vakiona newlinen aina rivin perään. Jos alla olevat komennot hämmentävät, kokeile `man xxd` ja esimerkiksi `xxd tiedosto.txt`.

```bash
# Echo ilman parametrejä sisältää newlinen
$ echo "" | xxd

# Echo -n poistaa newlinen
$ echo -n "" | xxd

# Huomaa, että ASCII:ta seuraavat merkit ovat UTF-8 enkoodattuja, monen tavun arvoja:
$ echo -n "ä" | xxd
```


![CR-LF](../images/CR-LF.png)

**Kuvio 1:** *Notepad++ Windowsissa tuottaa vakiona rivinvaihdossa kaksi merkkiä: CR (`\r`) sekä LF (`\n`). Linuxissa käytössä on tyypillisesti vain jälkimmäinen.*

!!! question "Tehtävä"

    Nämä merkit voivat joskus aiheuttaa hämmennystä, jos joku lähettää Linux-ympäristöön esimerkiksi konfiguraatiotiedoston, joka on luotu Windows-ympäristössä huolimattomasti. Selvitä, mikä on "CR LF":n historia rivivaihtona. Mitä CR ja LF käytännössä edustavat? 



## Hyödyllisiä komentoja

Ota selvää kustakin komennosta alla olevasta taulukosta.

| Käyttötarkoitus                          | Komentoja                                                                       |
| ---------------------------------------- | ------------------------------------------------------------------------------- |
| Avun etsiminen                           | `man`, `info`, `<komento> --help`                                               |
| Tiedostoissa ja hakemistoissa navigointi | `pwd`, `ls`, `cd`, `tree`, `clear`                                              |
| Tiedostojen pläräys                      | `less`, `cat`, `diff`, `head`, `tail`, `find`, `locate`, `file`, `type`, `stat` |
| Tiedostojen luominen ja muokkaus         | `touch`, `mkdir`, `nano`, `vi` tai `vim`, `vimtutor`, `cp`, `mv`, `ln`          |
| Tiedostojen ja kansioiden poisto         | `rm`, `rmdir`                                                                   |
| Tiedostojen prosessointi                 | `wc`, `tr`,  `sort`, `uniq`, `grep`, `aws`                                      |
| Käyttäjään tai ympäristöön liittyviä     | `id`, `who`, `whoami`, `groups`, `history`, `tty`, `exit`, `printenv`, `alias`  |
| Tiedostojen pakkaus                      | `gzip`, `tar`                                                                   |

!!! tip

    Komentoriviltä ajettavien käskyjen ajamiseen löydät reilusti esimerkkejä ja snippettejä Github-repositoriosta nimeltään [the-art-of-command-line](https://github.com/jlevy/the-art-of-command-line)
