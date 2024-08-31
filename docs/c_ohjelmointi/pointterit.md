# Osoittimet

Osoitin (engl. pointer) on muistiosoite. Sen sijaan, että toimitat funktiolle kopion datasta, voit toimittaa funktiolle pointterin. Tällöin säästyy muistia.

Osoitin voidaan alustaa samalla tavalla kuin tyypilliset muuttujat, mutta muuttujan nimeä edustava tähti tekee siitä osoittimen eli pointterin. Pointterin `int`-tyyppimäärittely ei suinkaan tarkoita että muistiavaruuden osoite olisi kokonaisluku, vaan että muistiavaruudesta pitää nimittää sellainen lokaatio, johon mahtuu kokonaisluku. Kuten aiemmin opimme, tämä on todennäköisimmin sinun järjestelmässäsi 4 tavua eli 32 bittiä.

```c
int* my_pointer;  // Näin ..
int *my_pointer;  // Tai näin
int * my_pointer; // .. tai näin
```

Kaikki muuttujat sisältävät sekä pointterin että arvon. Kuvitteellisen muuttujan `my_num` osoitteeseen muistiavaruudessa voidaan viitata liittämällä `&`-symboli sen alkuun.

```c
int my_num = 5;
int* my_pointer = &my_num;
```

Huomaa, että alustettu pointteri, jolle ei ole vielä osoitettu sille kuuluvaa arvoa, osoittaa *johonkin paikkaan* muistiavaruudessa. Minne? Vaikea sanoa. Satunnaiseen muistiavaruuden lokaatioon osoittavan pointterin käyttöä tulisi välttää.

Alla termit taulukkomuodossa.

| Symboli | Nimi        |
| ------- | ----------- |
| &       | Address of  |
| *       | Dereference |

Kokeile ajaa alla oleva koodi. Tutki, mitä tulostuu.

```c title="arvo-osoite.c"
#include <stdio.h>

// Alustetaan kokonaisluvun muuttuja
int my_num;

// Alustetaan osoittimen muuttuja (osoittaa kokonaislukuun)
int* my_pointer;

int main() {

    my_num = 5;
    my_pointer = &my_num;

    printf("myNum = %d\n", my_num);
    printf("myPointer value = %d\n", *my_pointer);

  	// %p on formatter pointterin osoitteen tulostamiseen heksana
    printf("myNum address = %p\n", &my_num);
    printf("myPointer = %p\n", my_pointer);
}
```

Alla vielä vaihtoehto, joka saattaa auttaa hahmottamaan, kuinka `*` ja `&` käyttäytyvät:

```c title="pointer-tulostin.c"
#include <stdio.h>

int main() {
    int x = 5;
    int* p = &x;

    printf("x = %d\n", x);
    printf("p = %p\n", p);
    printf("*p = %d\n", *p);
    printf("&x = %p\n", &x);
    printf("&p = %p\n", &p);

    return 0;
}
```

## Osoittimet ja funktiokutsut

Huomaa, että jos toimitat funktiolle pointterin, niin muistiosoitteen sisältävän arvon muokkaaminen muokkaa sitä kaikissa niissä muuttujissa, joiden osoitin viittaa tuohon muistiavaruuteen.

```c title="pointer-funktio.c"
#include <stdio.h>

void add_one(int *x) {
    puts("Increasing x by 1 inside a function.");
    *x = *x + 1;
}

int main() {
    int x = 5;
    int* y = &x;

    printf("x = %d\n", x);
    printf("y = %d\n", *y);
    add_one(&x);
    printf("x = %d\n", x);
    printf("y = %d\n", *y);

    return 0;
}
```

## Osoittimet ja merkkijonot

Luo uusi tiedosto, esimerkiksi `strings.c`, sisällöltään:

```c title="strings.c"
#include <stdio.h>

void print_in_function(char word[]) {
    puts("In function:");
    printf("word: %s (%lu bytes)\n", word, sizeof(word));
    printf("Pointer address: %p\n", word);
}

int main() {
    char word[] = "Hello world! I am a array of characters.";

    printf("word: %s (%lu bytes)\n", word, sizeof(word));
    printf("Pointer address: %p\n", word);
    print_in_function(word);

    return 0;
}
```

Aja koodi näin:

```bash title="Bash"
$ gcc strings.c -o strings -Wno-sizeof-array-argument && ./strings
```

Koodi kääntyy varoituksesta huolimatta. Tutkitaan hieman tilannetta.

* Käytämämme "merkkijono" on array merkkejä (Char[])
* GCC tietää, että teemme jotain typerää, joten warning on ignoorattu `-Wno-sizeof-array-argument` parametrilla. Kokeile ajaa koodi myös ilman sitä.
* Array käyttäytyy main funktiossa `printf()` osalta kuin pointer (`%p`), mutta on kuitenkin array.
* Funktiolle syötetty array kääntyy pointteriksi. Pointterin koko on 64-bittisessä järjestelmässä 8 tavua (`8 * 8 = 64`).

## Osoittimet ja listat

Arrayn elementin voi tulostaa samalla tavalla kuin listan elementin Pythonissa eli `somethings[index]`. Huomaa, että `*nums` viittaa arrayn pointteriin eli muistiavaruuden ensimmäiseen integeriin, joten `*nums == 1` ja `*(nums + 1) == 2`.

```c title="pointer-array.c"
#include <stdio.h>

int main() {
    int nums[] = {1, 2, 3, 4, 5};

    printf("Pointer address: %p\n", nums);
    puts("Different ways of printing the second value:");

    printf("A: %d\n", nums[1]);
    printf("B: %d\n", *(nums + 1));
    printf("C: %d\n", 1[nums]);

    return 0;
}
```

Kokeile, mitä tulostuu, jos haet jonkin sellaisen arvon, mikä ei todellakaan sisällä jotakin sinun määrittelemääsi arvoa? Array `nums` on `5 * 8` tavua pitkä (64-bittisessä järjestelmässä),  joten `nums[0] == 0` ja `nums[4] == 5`. Mutta mitä löytyy vaikkapa arvosta `nums[5]` tai `nums[10]` tai `nums[-4]`?


## Muistiavaruuden suojaaminen

Osoittimien kanssa huomasimme, että voimme hakea tietoa muistiavaruuksista, jotka eivät kuulu muistiavaruuden dataan. Dataa voi myös (yrittää) sijoittaa sinne.

```c
#include <stdio.h>

int main() {
    char title[12];

    printf("What's your title?: ");
    scanf("%s", title);
    printf("Hello, %11s!\n", title);
}
```

Yllä oleva koodi alustaa 12 merkkiä pitkän arrayn. Myöhemmin siitä tulostetaan merkit 0-11. Mutta entäpä jos käyttäjän titteli onkin jokin pitkä? Kokeile ajaa koodi siten, että syötät titteliksi esimerkiksi ==apulaiskaupunginjohtaja== (23 merkkiä). Syntynyt virhe on **buffer overflow**, ja käyttöjärjestelmä voi vastata siihen esimerkiksi virhenimellä segmentation fault tai bus error.

Huomaa, että välilyönti katkaisee `fgets`:n parsimisen, joten käytäthän pitkää yhdyssanaa.

Kokeile tämän jälkeen korvata `scanf` sen turvallisemmalla vastineella `fgets`:

```c
#include <stdio.h>

int main() {
    char title[12];

    printf("What's your title?: ");
    fgets(title, sizeof(title), stdin);
    printf("Hello, %s!\n", title);
}
```

