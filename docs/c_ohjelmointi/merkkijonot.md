# Merkkijonot

Mikäli et käytä kirjastoja, C-kielestä puuttuu tyystin merkkijono eli string muuttujatyyppi ja avustavat funktiot, joiden avulla voisi esimerkiksi selvittää merkkijonon pituuden tai liimata kaksi merkkijonoa yhteen.

Huomaa, että literaalit merkkijonot määritellään lainausmerkkien väliin: `"kissa"`. Yksittäiset heittomerkit on varattu kirjainten määrittelyyn: `'k'`. Lista kirjaimia olisi muotoa `char kissa[] = {'k', 'i', 's', 's', 'a', '\0'};`. Huomaa, että merkkijonon lopussa on aina nollamerkki, joka kertoo, että merkkijono on päättynyt. Merkkijonojen käsittelyyn löytyy C Standard Librarystä header file nimeltään `string.h`.

```c title="kirjaimet.c"
#include <stdio.h>

int main()
{
    char word[] = "Hello, wörld!"; // (1)!
    int length = sizeof(word) / sizeof(word[0]); // (2)!

    printf("Muuttujan word pituus on: %d \n", length);

    for (int i = 0; i < length; i++)
    {
        printf("%i: %c (0x%02X)\n", i, word[i], word[i]);
    }
}
```

1. Kokeile myös esimerkiksi word[5] ja word[20]
2. Muokkaa koodia siten, että käytät lenght muuttujan arvon laskemiseen `strlen()` funktiota, joka löytyy `string.h` kirjastosta.

!!! tip

    Voit kokeilla myös word-muuttujan luomista siten, että se on muotoa array of characters. Tämä hoituu seuraavalla tavalla:
    
    ```c
    char word[20] = {'H', 'e', 'l', 'l', 'o', ',', ' ', 'w', 'o', 'r', 'l', 'd', '!', '\0'};
    ```
    
    Mitä ongelmia ö-kirjain aiheuttaa? Toimiiko koodi jos korvaat sen o-kirjaimella?


## Standard inputin käsittely

Tutustu alla näkyvään koodiin (`reverser.c`). Ennen kuin kokeilet ajaa koodia, yritä päätellä mitä se tekee standard inputille, joka on vakiossa `stdin`, joka on määritelty `stdio.h` kirjastossa.

```c title="reverser.c"
#include <stdio.h>
#include <string.h>

#define MAX_LINE_LENGTH 100

void reverse(char str[]) {
    int length = strlen(str);
    for (int i = 0; i < length / 2; i++) {
        char temp = str[i];
        str[i] = str[length - i - 1];
        str[length - i - 1] = temp;
    }
}

int main() {
    char line[MAX_LINE_LENGTH];
    while (fgets(line, MAX_LINE_LENGTH, stdin) != NULL) {
        reverse(line);
        printf("%s", line);
    }
    return 0;
}
```

Kun olet lukenut koodin huolella, käännä se binääritiedostoksi ja selvitä, kuinka ohjelmaa käytetään. Kokeile ainakin seuraavia:

```bash
# Perus ajo. Lopeta CTRL+D tai CTRL+C.
$ ./reverser

# Heredoc-tyylinen syöte. Etsi lisätietoa Heredocista omatoimisesti.
$ ./reverser <<'EOF'
> kissa
> koira
> EOF

# Standard inputin syöttäminen putkittamalla
$ ls -1 | ./reverser

# Standard outputin jatkaminen putkittamalla
$ ls -1 | ./reverser | wc -l
```

