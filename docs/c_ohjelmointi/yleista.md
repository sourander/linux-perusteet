# Yleistä

Tämä materiaali ei ole C-ohjelmointikielen kurssi, muttta C-kielen kirjoittaminen ja kääntäminen esitellään kurssilla Linuxin näkökulmasta. On oletus, että osaat ohjelmointia jo jollakin kielellä!

Mikäli funktiot ja kontrollirakenteet ja niihin liittyvät käskyt (if, while, for, break, continue) eivät ole tuoreessa muistissa, tämä materiaali toimii hyvänä muistinvirkistäjänä samalla. C-kieli on matalan abstraktiotason kieli, joten siinä pitää lähes kaikki se koodata itse (tai käyttää kirjaston implementointia), mikä on korkeamman tason kielessä (esim. Pythonissa) built-in ominaisuus.

Materiaalin tukena voi käyttää esimerkiksi seuraavia lähteitä:

* Online-tutoriaalit:
    * [W3Schools: C Tutorial](https://www.w3schools.com/c/index.php)
    * [Ohjelmointiputka: C-ohjelmointi](https://www.ohjelmointiputka.net/oppaat/sarja.php?tunnus=cohj)
* Kirjat
    * [C for Python Programmers](http://www.cburch.com/books/cpy/) (HTML, 2011)
    * [Modern C](https://gustedt.gitlabpages.inria.fr/modern-c/) (PDF, 2019 painos on saatavilla ilmaiseksi.)
    * ... ja monet muut kirjat [EbookFoundation free-programming-books](https://ebookfoundation.github.io/free-programming-books-search/?&sect=books&file=free-programming-books-langs.md#c)-listalla
* Haasteita ja tehtäviä
    * [Computer Science by Example](https://cscx.org/)
    * [Exercism: C](https://exercism.io/tracks/c)
    * [LeetCode: C](https://leetcode.com/problemset/all/?topicSlugs=c)

## Lähdekoodi

C-kielen lähdekoodi on tavallinen tekstitiedosto. Sen voit luoda Linuxissa esim. `nano` tai `vim` cli-tekstieditoreilla tai vaikkapa Visual Studio Code:lla. Tyypillisesti tiedostopääte on `.c`.

```c title="hello.c"
#include <stdio.h>

int main()
{
    puts("Hello, world!");
    return 0;
}
```

!!! question "Tehtävä"

    Tutustu siihen, mikä stdio.h on. Saat siitä lisää tietoa lukemalla `man 3 stdio` sivun tai vastaavan sivun Internetistä esimerkiksi [Die.net: stdio](https://linux.die.net/man/3/stdio)-sivustolta.

### Kääntäjä

Toisin kuin tulkattavat kielet (kuten Python ja JavaScript), C tulee kääntää binääritiedostoksi. Tätä varten tarvitset **kääntäjän**. Linuxissa kääntäjä on tyypillisesti GNU `gcc`, mutta myös muita vaihtoehtoja, kuten `clang` löytyy. Windowsissa tarvitset MinGW:n (Minimalistic GNU for Windows), jotta sinulla on käytössäsi `gcc`. Vaihtoehtoisesti voisit käyttää Microsoftin kaupallista C/C++-kääntäjää, joka asennetaan tyypillisesti Visual Studion mukana. Huomaa, että ==Visual Studio== ja ==Visual Studio Code== ovat eri ohjelmia.

```bash
# Käännä hello.c-tiedosto hello binääriksi
$ gcc -o hello hello.c
```

!!! tip

    Gcc:n optio `-o <tiedostonimi>` antaa sinun asettaa tiedostolle nimen. Windowsissa executable eli ajettava tiedosto olisi tyypillisesti päätteeltään `.exe`, mutta Linuxissa executable tunnistaa tiedosto-oikeuksista. Kokeile, mikä tiedostonimeksi tulee, jos jätät tiedostonimen kokonaan määrittelemättä eli ajat `gcc hello.c`.

### 03: Binäärin ajaminen

Kääntäjä luo ajettavan tiedoston. Voit tarkistaa tämän `ls -l tiedostonnimi` komennolla. Huomaat, millä käyttäjätyypeillä on `x`-oikeus tiedostoon. Tiedoston ajaminen itsessään on helppoa. Kuten kurssin muissa materiaaleissa on opetettu, sinun tulee antaa absoluuttinen tai relatiivinen polku binääriin, ellei tiedosto löydy `$PATH`:sta. Meidän nykyinen kansio ei oletettavasti ole PATH-ympäristömuuttujan kansioiden listassa, joten koodin voi ajaa relatiivisella polulla näin:

```bash
$ ./hello
```

!!! tip

    Huomaa, että `./`-merkintä tarkoittaa nykyistä kansioa. Voit ajaa toisessa hakemistossa olevan binäärin antamalla absoluuttisen tai relatiivisen polun binääriin.

    ```bash
    # Absoluuttinen polku
    $ /home/kayttaja/ohjelmat/hello

    # Relatiivinen polku
    $ ../toinenkansio/hello
    ```


## Syntaksiin tutustuminen

```c title="zorro.c"
/*
* Arvaa Zorron etunimen ensimmäinen kirjain ja voitat pelin haluamasi määrän kertoja.
*/

#include <stdio.h>
#include <stdlib.h>

void zorro(int n)
{
    for (int i = 0; i < n; i++)
    {
        printf("Zorro voitti %d. kerran!\n", i + 1);
    }
}

int main()
{
    char kirjain[2];
    char maara[3];
    int n;

    puts("Anna kirjain (vihje Z): ");
    scanf("%s", kirjain);


    if (kirjain[0] == 'Z')
    {
        puts("Kuinka monta kertaa haluat voittaa?: ");
        scanf("%s", maara);

        n = atoi(maara);
        if (n < 1)
        {
            printf("Epäsopiva määrä (%d)! Zorron pitää voittaa ", n);
            puts("vähintään kerran. Yritä uudelleen.");
            return EXIT_FAILURE;
        }
        zorro(n);
    }
    else
    {
        puts("Game over! Zorro hävisi.");
    }

    return 0;
}
```

!!! question "Tehtävä"

    Etsi koodista:

    1. Funktion `main` return type eli palautuvan muuttujan tietotyyppi
    2. Funktion `zorro` return type.
    3. Muuttujan `kirjain` tyyppi.
    4. Miksi kirjaimen perässä on `[2]`? Miksei `[1]`? Vihjesana: **sentinel**.
    5. Muuttujan `maara` tyyppi.
    6. Mitä atoi() funktio tekee ja missä se on määritelty? Voit etsiä C-kielen dokumentaatiota [DevDocs](https://devdocs.io/c/) sivustolla.
    7. Muuttujan `n` mahdollinen maksimiarvo käyttäjäsyötteen perusteella.
    8. Loopin `if` ehto
    9. Kuinka `puts` ja `printf` eroavat toisistaan? Missä funktiot on määritelty?
    10. Mikä on `EXIT_FAILURE`-muuttuja? Missä se on määritelty? Mikä sen arvo on numerona?

Kun olet suorittanut yllä olevan tehtävän, kokeile ajaa yllä oleva koodi siten, että ohjelma suoritetaan `return EXIT_FAILURE;` riviin. Kuinka ohjelma käyttäytyy kun ajat sitä? Kokeila alla olevia komentoja:

```bash
# Häviä peli tarkoituksella epäsopivaan määrään
$ ./zorro
Anna kirjain (vihje Z): <anna oikea kirjain>
Kuinka monta kertaa haluat voittaa?: <keksi epäsopiva vastaus>

# Katso, mitä tämä ympäristömuuttuja sisältää.
$ echo $?

# Vertaa tätä johonkin tutun applikaatioon vikatilanteessa (esim. ls)
$ ls /foldernotexists
$ echo $?
```

