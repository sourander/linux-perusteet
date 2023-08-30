TODO

## Merkkijonot

```
$ echo 'Onko $USER täällä?'     #
Onko $USER täällä?

$ echo "Onko $USER täällä?"     #
Onko opettaja täällä?

$ echo "Tänään on: $(date -I)"  # Command substitution
Tänään on: 2023-12-31

$ echo "Sormia on: $((5 + 5))"  # Arithmetic substitution
Sormia on: 10

$ echo Liian \                  # Line continuation
> pitkä lause \
> yhdelle riville
Liian pitkä lause yhdelle riville

echo Elämän tarkoitus: \        # Parameter expansion
> ${MEANING_OF_LIFE:-42}  
42

$ echo $'c\nb\na'               # ANSI-C Quoting (1)
c
b
a
```

1. Yksittäisten lainausmerkkien välissä oleva, dollareiden edeltävä merkkijono, voi sisältää poistumismerkillä (kenoviiva, `\`)   alkavia taikasanoja, joista dekoodataan myöhemmin haluttu merkki. Yleisesti tarpeellisin on rivinvaihto eli `\n`. Lue lisää: [Bash Reference Manual (gnu.org)](https://www.gnu.org/savannah-checkouts/gnu/bash/manual/bash.html#ANSI_002dC-Quoting)