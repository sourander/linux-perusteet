---
priority: 850
---

# Argumentit

## Käsin parsimalla

Linuxin käytössä sinulle pitäisi olla tullut jo tutuksi, että monille ohjelmille voi syöttää argumentteina, kuten `cat file_a file_b`, jossa argumentteja ovat `file_a` ja `file_b`. C-ohjelmissa argumentit voidaan ottaa vastaan `main`-funktion parametreina. Esimerkiksi:

```c title="argue.c"
#include <stdio.h>

int main(int argc, char *argv[]) {
    printf("Ohjelman nimi: %s\n", argv[0]);
    printf("Argumentteja: %d\n", argc);
    for (int i = 1; i < argc; i++) {
        printf("Argumentti %d: %s\n", i, argv[i]);
    }
    return 0;
}
```

Käännä ohjelma ja kokeile ajaa se eri argumenteilla.

```bash title="Bash"
# Ei argumentteja
$ ./argue

# Yksi argumentti
$ ./argue kissa

# Useampi argumentti
$ ./argue kissa koira "Hello, World"

# Argumentit, joissa suoritetaan erilaista string expansionia
$ ./argue $SHELL $(whoami) $((5+5))
```

!!! question "Kysymys"

    Kokeile ajaa seuraava: 
    
    ```bash title="Bash"
    ./argue kissa koira "Hello, World!"`  # <== Huomaa lisätty huutomerkki! 
    ```
    
    Tämä aiheuttaa ongelmia. Miksi? Miten ne voi kiertää?

## Kirjaston avulla

Argumenttien käsittely on yleinen ongelma, joten (GNU) C:ssä on valmiita kirjastoja, jotka auttavat standardisoimaan argumenttien käsittelyä. Parametrien parmiseen soveltuu `unistd.h`:sta löytyvä funktio `getopt` sekä `getopt_long`. Tyypillinen Linux-käyttäjä odottaa, että optionit voi antaa haluamassaan järjestyksessä, ja annetaan yleensä seuraavanlaisessa formaatissa: 

```bash title="Bash"
myprog \ 
  -v                         `# lyhyt toggle-optio` \
  -a value                   `# lyhyt arvo-optio` \
  --some-long-option==value  `# pitkä arvo-optio` \
  --some-long-toggle         `# pitkä toggle-optio`
```

Tutustu alla olevaan koodiin. Huomaa, että getopt:n kolmas argumentti sisältää kaksoispisteen seuraavien perässä: `n:` ja `w:`. Tämä tarkoittaa, että `n` ja `w` ovat optioita, jotka vaativat arvon. `l` on toggle-optio, joka ei vaadi arvoa. Sillä ei ole perässään kaksoispistettä.

```c title="betterargue.c"
#include <stdio.h>
#include <unistd.h>
#include <stdlib.h>

int main(int argc, char *argv[]) {
    int opt;
    int n = 1;
    int line_numbers = 0;
    char *word = "spam";

    while ((opt = getopt(argc, argv, "n:w:l")) != EOF) {
        switch (opt) {
            case 'n':
                n = atoi(optarg);
                if (n < 1) {
                    fprintf(stderr, "Invalid count: %d\n", n);
                    return 1;
                }
                break;
            case 'w':
                word = optarg;
                break;
            case 'l':
                line_numbers = 1;
                break;
            default:
                fprintf(stderr, "Usage: %s [-l] [-n <count>] [-w <word>]\n", argv[0]);
                return 1;
        }
    }

    for (int i = 0; i < n; i++) {
        if (line_numbers) {
            printf("%d: ", i);
        }
        printf("%s\n", word);
    }

    return 0;
    
}
```

Käännä ja kokeile ajaa seuraavasti:

```bash title="Bash"
# Ei argumentteja
$ ./betterargue

# Pelkkä sana määriteltynä
$ ./betterargue -w kissa

# Pelkkä määrä määriteltynä
$ ./betterargue -n 5

# Molemmat määriteltynä
$ ./betterargue -n 5 -w kissa

# Myös rivinumerot togglettu päälle
$ ./betterargue -n 5 -w kissa -l
```

!!! tip

    Lue aiheesta lisää [The GNU C Library Reference Manual](https://sourceware.org/glibc/manual/latest/html_mono/libc.html#Getopt), mukaan lukien ohje siitä, kuinka käyttää pitkiä optioita kuten `--word` tai `--line-numbers`.