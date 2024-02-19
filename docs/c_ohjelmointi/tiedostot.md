Standardikirjasto sisältää funktioita, jotka ovat tarpeellisia tiedostojen käsittelemiseksi. Alla äärimmäisen pelkistetty esimerkki, jossa luetaan tiedosto read-only tilassa ja suljetaan se.

```c
#include <stdio.h>

int main() {
    FILE *file;
    file = fopen("tiedosto.txt", "r");
    // Tässä välissä voisit tehdä jotakin tiedoston datalla.
    fclose(file);
    return 0;
}
```

Olet aiemmin käyttänyt `fprintf` ja `fputs` funktioita virtaan (`stdout`, `stderr`) kirjoittamiseen. Mikäli kokeilet mouse-overia IDE:ssä jomman kumman funktion päällä, huomaat, että kumpikin haluaa parametrin `FILE *`-tyyppisestä muuttujasta. Voit sijoittaa tähän myös FILE-osoittimen, joka on avattu tiedostoon. Tämä mahdollistaa tiedostosta lukemisen ja tiedostoon kirjoittamisen.

## Muista sulkea
 
Muista aina sulkea tiedosto, kun olet valmis käyttämään sitä. Tämä vapauttaa resurssit ja mahdollistaa muiden ohjelmien käyttää sitä. Voit kokeilla tiedoston jättämistä auki ja ohjelman tappamista ennenaikaisesti sleep:n avulla.


```c title="noclose.c"
#include <stdio.h>
#include <unistd.h> // <== for sleep

int main() {
    FILE *file;
    file = fopen("tiedosto.txt", "w");
    fputs("I am a line!\n", file);  // <== fputs ei lisää newlinea automaattisesti
    // sleep for 10 minutes
    sleep(600);
    return 0;
}
```

Aja tämä:

```bash
# Aja taustalla
$ ./noclose &

# Tarkista, että tiedosto on auki
$ lsof tiedosto.txt

# Katso, onko tiedostossa oikeasti mitään
$ cat tiedosto.txt

# Tapa ohjelma
$ kill %1

# Tarkista, sulkiko käyttöjärjestelmä tiedoston
$ lsof tiedosto.txt

# Tarkista, onko tiedostosa vieläkään mitään
$ cat tiedosto.txt
```

## Esimerkki: Datan lukeminen ja kirjoittaminen

Alla koodi, joka lukee dataa rivi riviltä yhdestä tiedostosta ja kirjoittaa ne toiseen. Toisin sanoen se suorittaa tiedoston kopioinnin.

```c title="copyer.c"
#include <stdio.h>

#define MAX_LINE_LENGTH 256

int main(int argc, char *argv[]) {
    // Check if the correct number of arguments is provided
    if (argc != 3) {
        printf("Usage: %s <filename_src> <filename_dst>\n", argv[0]);
        return 1;
    }

    // Open the source file in read-only mode
    FILE *src_file = fopen(argv[1], "r");
    if (src_file == NULL) {
        fprintf(stderr, "Failed to open %s\n", argv[1]);
        return 1;
    }

    // Open the destination file in write mode
    FILE *dst_file = fopen(argv[2], "w");
    if (dst_file == NULL) {
        fprintf(stderr, "Failed to open %s\n", argv[2]);
        fclose(src_file);
        return 1;
    }

    // Read lines from source file and write them to destination file
    char line[MAX_LINE_LENGTH];
    while (fgets(line, sizeof(line), src_file) != NULL) {
        fputs(line, dst_file);
    }

    // Close the files
    fclose(src_file);
    fclose(dst_file);

    printf("File copied successfully.\n");

    return 0;
}
```

Käännä ja aja ohjelma seuraavasti:

```bash
# Kopioi ja katso mitä sisältää
$ echo "Kissa" > src.txt
$ ./copyer src.txt dest.txt
$ cat dest.txt

# Lisää rivi ja toista
$ echo "Koira" >> src.txt
$ ./copyer src.txt dest.txt
$ cat dest.txt
```
