# Muuttujat

Huomaa, että C-kielessä ei ole samanlaista yleispätevää äärettömältä tuntuvaa "integer"-tyyppiä kuin Pythonissa. Muuttuja tulee alustaa valitsemallasi tietotyypillä.

```c title="etumerkit.c"
#include <stdio.h>

int main() {
    
  	// Char on 1-tavuinen muuttuja: ASCII-merkin koodipiste tai
    // ihan vain pieni numero (-128...127)
    signed char num;
    num = 127;
    num += 1;
    printf("Num = %d\n", num);
    
  	// Unsigned muuttaa vasemmanpuoleisimman bitin negatiivisuuden
    // merkistä luvuksi. Tämä siirtää lukuavaruuden positiiviseksi (0...255).
    unsigned char b;
    b = 127;
    b += 1;
    printf("Num = %d\n", b);

    return 0;
}
```

Alla tyypillisiä C-kielen muuttujatyyppejä niiden tavumäärän sekä lukuavaruuden mukaan taulukossa. Huomaa, että `int` ja `float` tyyppien bittisyvyys voi vaihdella prosessoriarkkitehtuurista riippuen. Oletuksena luvut ovat `signed` eli vasemmanpuolimmaisin bitti määrittää, onko luku positiivinen vai negatiivinen. Jos pakotat muuttujasta positiivisen (esim. `unsigned int`), lukuavaruus alkaa 0:sta ja jatkuu `2 ** bittisyvyys` asti.


| Tyyppi        | Nimi   | Tavua | Lukuavaruus           | Printf |
| ------------- | ------ | ----- | --------------------- | ------ |
| ASCII-kirjain | char   | 1     | -128 to 127           | %c     |
| Kokonaisluku  | short  | 2     | -32,768 to 32,767     | %hd    |
| Kokonaisluku  | int    | 4     | -2.1E+9 to 2.1E+9     | %d     |
| Kokonaisluku  | long   | 8     | -9.2E+18 to 9.2E+18   | %ld    |
| Desimaaliluku | float  | 4     | -3.4E-38 to 3.4E+38   | %f     |
| Desimaaliluku | double | 8     | -1.7E-308 to 1.7E+308 | %lf    |


Mikäli haluat selvittää oman prosessoriarkkitehtuurisi mukaisen `int`- ja `float`-tyyppien bittisyvyyden, voit tehdä sen `sizeof()` funktiota käyttäen. Käännä ja aja alla näkyvä `limits.c`-tiedoston sisältö. (Koodi olettaa, että tavu on tasan 8 bittiä. Tavun leveys voi vaihdella eri arkkitehtuurien välillä. 🤓)

```c title="limits.c"
#include <stdio.h>

int main() {

    printf("Size of char: %zu bytes (%zu bits)\n", sizeof(char), sizeof(char) * 8);
    printf("Size of short: %zu bytes (%zu bits)\n", sizeof(short), sizeof(short) * 8);
    printf("Size of int: %zu bytes (%zu bits)\n", sizeof(int), sizeof(int) * 8);
    printf("Size of long: %zu bytes (%zu bits)\n", sizeof(long), sizeof(long) * 8);
    printf("Size of float: %zu bytes (%zu bits)\n", sizeof(float), sizeof(float) * 8);
    printf("Size of double: %zu bytes (%zu bits)\n", sizeof(double), sizeof(double) * 8);

    return 0;
}
```

## Formaatin määrittely tulostaessa

| Placeholder | Tulostettava      | Esimerkki                   |
| ----------- | ----------------- | --------------------------- |
| c           | kirjain           | `printf("%c", 'A')`         |
| d tai i     | kokoluku          | `printf("%d", 123)`         |
| f           | desimaaliluku     | `printf("%f", 3.14)`        |
| s           | merkkijono        | `printf("%s", "abc")`       |
| X tai x     | numero (heksaksi) | `printf("hex = %02x", 101)` |
| p           | pointteri         | `printf("%p", &my_integer)` |

## Muuttujan castaaminen toiseksi tyypiksi

Muuttujia voi castata muuttujatyypistä toiseen asettamalla haluttu muuttujatyyppi suluissa muuttajan eteen.

```c title="casting.c"
#include <stdio.h>

int main() {
    float f = 3.14;
    int i = (int)f;

    printf("float %f is %i as int\n", f, i);
}
```
