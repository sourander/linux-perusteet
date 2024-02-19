
# Otsikkotiedostot

Tähän asti kaikki esimerkit ovat sijainneet yhdessä C-tiedostossa. Tämä ei ole kovin käytännöllistä, jos ohjelma on suuri. Tässä tulevat apuun header-tiedostot.

## Simppeli esimerkki

Lue tiedostot `headerdemo.c` ja `headerdemo.h`. Lisää tiedostoihin sisältö alla näkyvästä koodista.

Tiedostojen kuvaus:

* `app_itself.c` on ohjelma itse. 
* `headerdemo.h` sisältää `printHello`-funktion prototyypin (declaration).
* `headerdemo.c` sisältää `printHello`-funktion toteutuksen (definition).

### Koodi

=== "app_itself.c"
    
    ```c
    #include "headerdemo.h"

    int main() {
        printHello();
        return 0;
    }
    ```

=== "headerdemo.c"

    ```c
    #include "headerdemo.h"
    #include <stdio.h>

    void printHello() { printf("Hello, World!\n"); }
    ```

=== "headerdemo.h"

    ```c
    void printHello();
    ```

!!! tip "Miksi <> merkit?"

    Huomaa lokaalin ja toisesta polusta löytyvän header-tiedoston ero. Lokaali header-tiedosto on sijoitettu lainausmerkkien sisään, kun taas toisesta polusta löytyvä tiedosto on sijoitettu kulmasulkeiden sisään.

    Jos haluat löytää `stdio.h`-tiedoston, jota GCC käyttää, voit ajaa seuraavan komennon:

    ```bash
    gcc -E -x c - -v < /dev/null
    ```

    Etsi outputista rivejä, jotka näyttävät tältä:

    ```bash
    #include <...> search starts here:
    /usr/lib/gcc/aarch64-linux-gnu/11/include
    /usr/local/include
    /usr/include/aarch64-linux-gnu
    /usr/include
    ```

    Tulet löytämään esimerkiksi tiedostot:
    
    * `/usr/include/stdio.h` (ASCII)
    * `/usr/lib/aarch64-linux-gnu/libc.so` (ASCII)
    * `/usr/lib/aarch64-linux-gnu/libc.so.6` (ELF)

    Yllä mainittu `.so`-tiedosto on dynaaminen kirjasto, joka sisältää koodia, jota voidaan ajaa ohjelman suorituksen. Windowsissa sen vastine on DLL-tiedosto.

## Kääntäminen

Koodi käännetään aivan kuten ennenkin, mutta sinun tulee listata kaikki tarvittavat `*.c`-tiedostot. Käännä ohjelma seuraavasti:

```bash
# Jos hakemistossa ei ole muita .c-tiedostoja
$ gcc *.c -o app_itself

# Jos on, määrittele lista
$ gcc app_itself.c headerdemo.c -o app_itself
```

!!! question "Tehtävä"

    Luo toinen ohjelma, nimeltään **Another App**, joka hyödyntää samaa kirjastoa.

## Objektitiedostot

Ohjelman kääntämisen sijasta voit kääntää kaikki `jotain.c`-tiedostot objektitiedostoiksi. Tästä on se hyöty, että mikäli jatkossa `egg.c` muuttuu, mutta `ham.c` ja `spam.c` eivät, sinun tarvitsee generoida vain `egg.o` uudelleen.

```bash
# Jos hakemistossa ei ole muita .c-tiedostoja
$ gcc -c *.c

# Jos on, määrittele lista
$ gcc -c app_itself.c headerdemo.c
```

??? tip "Miksi -c?"

    `-c`-flagi kertoo GCC:lle, että "Only run preprocess, compile, and assemble steps". Linkitys ja suoritettavan tiedoston luonti jäävät tekemättä.

Hakemistoon luodaan uudet objektitiedostot:

```bash
$ tree
.
├── app_itself.c
├── app_itself.o  <== tämä
├── headerdemo.c
├── headerdemo.h
└── headerdemo.o  <== tämä
```

Jatkossa, kun `headerdemo.c` muuttuu, sinun tarvitsee kääntää vain `headerdemo.o` uudelleen.

```bash
# Käännä
$ gcc *.o -o app_itself
$ ./app_itself
Hello, World!

# Muokkaa headerdemo.c:tä ja käännä uusiksi
$ sed -i 's/World/Humans/' headerdemo.c
$ gcc -c headerdemo.c
$ gcc *.o -o app_itself
Hello, Humans!
```

Säästö on tässä tapauksessa mitätön, koska lähdekoodissa on vain muutama rivi. Tilanne olisi toinen, jos lähdekoodia olisi tuhansia rivejä ja/tai jos käytössä oleva CPU olisi merkittävän hidas.

## Make 

TODO. Tähän tulee `make`-komennon käyttö.