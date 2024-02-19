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

## Merkkijonot listassa

Lista voi sisältää listoja. Selvitä, mitä alla oleva koodi tekee:

```c
#include <stdio.h>
#include <string.h>

char imdb_top_movies[][50] = {
    "The Shawshank Redemption",
    "The Godfather",
    "The Dark Knight",
    "The Godfather: Part II",
    "12 Angry Men",
    "Schindler's List",
    "The Lord of the Rings: The Return of the King",
    "Pulp Fiction",
    "The Lord of the Rings: The Fellowship of the Ring",
    "The Good, the Bad and the Ugly",
};

int n = sizeof(imdb_top_movies) / sizeof(imdb_top_movies[0]);

int main() {
    
    char search_word[50];
    printf("Search for a movie title: ");
    scanf("%s", search_word);

    for (int i = 0; i < n; i++) {

        if (strstr(imdb_top_movies[i], search_word)) {
            printf("Found: %s\n", imdb_top_movies[i]);
        }
    }
}
```
