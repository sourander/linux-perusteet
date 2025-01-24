---
priority: 840
---

# Standardivirrat

### Syöte kuin syöte

Käytimme [Yleistä](yleista.md)-materiaalissa Zorro-peliä, jolle syötimme näppäimistöä käyttäen syötteen, kuten "Z" ja "3". Huomaa, että syöte on syötettä, tuli se näppäimistöltä tai tiedostosta. Tutustutaan tähän konseptiin hieman:

```bash title="Bash"
# Kokeile syöttää pelkkä Z. Minkä arvon "n" sai?
$ echo "Z" > zorro_input.txt
$ cat zorro_input.txt | ./zorro

# Lisää tiedostoon myös numero ja kokeile uusiksi
$ echo "3" >> zorro_input.txt
$ cat zorro_input.txt | ./zorro

# P.S. Varmista, että ymmärrät, mitä zorro_input.txt tiedosto sisältää
#      ja mitä cat tulostaa.
$ cat zorro_input.txt
```

!!! tip

    Kokeile putkituksen lisäksi myös syötteen ohjaamista tiedostosta käyttäen `<`-merkkiä.

    ```bash title="Bash"
    $ ./zorro < zorro_input.txt
    ```

### Syötteen hakeminen stdin:stä 

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

```bash title="Bash"
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

## Standard erroriin kirjoittaminen

Funktio `printf` kirjoittaa aina standard outputiin. Jos haluat kirjoittaa johonkin muualle, kuten standard erroriin tai jopa tiedostoon, voit käyttää `fprintf`-funktiota.


```c title="errors.c"
#include <stdio.h>

int main() {
    fprintf(stdout, "Olen matkalla Standard Outtiin\n");
    fprintf(stderr, "Olen matkalla Standard Erroriin.\n");
    return 1;
}
```

??? question "Kysymys"

    Myös `fputs`-funktio toimii! Kuinka käyttäisit fputs-funktiota fprintf:n tilalla? Huomaa:

    * puts ja fputs ovat eri funktioita.
    * printf ja fprintf ovat eri funktioita.


Nyt voimme harjoitella syötteen ohjaamista ja virheilmoitusten käsittelyä. Tutki, mitä seuraavat tulostavat ja minne:

```bash title="Bash"
# Komento 1
$ ./errors

# Komento 2
./errors > /dev/null

# Komento 3
./errors 2> /dev/null

# Komento 4
./errors > /dev/null 2>&1
```

!!!tip

    Jos et ole varma, mitä `/dev/null`:iin päätyy, kokeile korvata se vaikkapa tiedostolla `output.log`.