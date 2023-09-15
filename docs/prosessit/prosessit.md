Linuxin kerneli luo jokaiselle käynnistetylle ohjelmalle oman prosessin, ja jokaisella prosessilla on oma tunniste (PID, Process ID). Käyttämäsi shell, kuten GNU bash, on yksi monista ohjelmista, jonka voi käynnistää, ja siten se saa oman PID:n. Ympäristömuuttuja `$0` sisältää ohjelman nimen, kun taas `$$` sisältää ohjelman PID:n. Tutki alla olevaa koodia ajatuksella:

```bash
Last login: Fri Sep 15 09:10:36 on ttys005
$ echo $0
-zsh        # Tämän käyttäjän login shell ei olekaan bash vaan zsh

$ echo $$
18039       # Kyseisen shell-instanssin PID on tämä

$ bash
$ echo $0
bash        # Bash-komento käynnisti bash-prosessin nykyisessä terminaalissa

$echo $$
18196       # Tämän bash shell -instanssin PID on eri kuin zsh:n

$ pstree 18039
-+= 18039 opettaja -zsh
 \-+= 18196 opettaja bash
   \-+= 18546 opettaja pstree 18039
     \--- 18547 root ps -axwwo user,pid,ppid,pgid,command

$ echo $$
18196       # Bash shell -instanssin PID on yhä sama kuin aiemmin

$ exit
$ echo $$
18039       # Myös Z Shellin PID on pysynyt samana.
```

Yllä ajettu pstree paljastaa, että Z Shelli on parent process käynnistämällemme GNU Bash prosessille. Juuri ajettu `pstree`-komento sen sijaan on tämän prosessin child. Komento `pstree` on sisäisesti käynnistänyt prosessin `ps`. Kun näiden ohjelmien suorittaminen loppui, terminaaliin tuli takaisin aiemmin ajamamme `bash`-ohjelman prompt. PID:t `pstree (18039)` sekä `ps (18547)` ovat terminoituja, koska niiden suoritus on jo loppunut.

Kokeillaan ajaa sama komento, minkä pstree ajoi sisäisesti. Jos haluat hieman lyhentää command-sarakkeen sisältöä, korvaa `command`-sana argumentista sanalla `comm`.

```bash
# Aja täysin sama komento
$ sudo ps -axwwo user,pid,ppid,pgid,command
root                 1     0     1 /sbin/launchd
root                88     1    88 /usr/libexec/logd
root                89     1    89 /usr/libexec/smd
...
```

Tutustu `ps`-komentoon `man`:n tai netistä löytyvien esimerkkien avulla. Selvitä muun muassa, mitä alla olevat komennot tekevät. Huomaa, että komento tukee kolmenlaista syntaksia optioneille: UNIX, BSD ja GNU. Jos kokeilet samaa komentoa macOS:lla, huomaat, että vain osa samoista optioneista toimii edes sinne päin samalla tavalla.

```bash
# Mitä tämä tekee?
$ ps -u $(whoami) | grep python

# Entä tämä?
$ ps -o ppid= -p 1

# Mites tämä?
$ ps -x -o pid,user,%mem,%cpu,comm
```



## Prosessori- ja muistinkäytön seuranta

Windowsista tutun tehtävienhallinnan (task manager) tai macOS:stä tutun Activity Monitorin kaltaiset tiedot saa shellissä esiin komennolla `top`. Kyseinen komento näyttää järjestetyn eli sortatun listan järjestelmän prosesseista. Sorttaukseen käytettyä saraketta voi vaihtaa parametreillä tai pikanäppäimillä.

```bash
$ top -o mem   # Järjestä muistinkäytön mukaan laskevasti
```



Tutustu komentoon `man`-komennon avulla.

Tutki myös, löytyykö käyttämästäsi työpöytäympäristöstäsi (esim. GNOME) vastaava graafinen sovellus kuten System Monitor.



## Jumiutuneiden ohjelmien tappaminen

Mikäli jokin ohjelma on auttamattomasti jumissa, voit viime kädessä tappaa sen aina `kill -9 pid`-komennolla. Option `-9` on signaalille `KILL` annettu numero. Kaikki kill-signaalit ja niiden numerot ovat alla:

| #    | Signaali | Selitys                                                      |
| ---- | -------- | ------------------------------------------------------------ |
| 1    | HUP      | Hang up. Aikoinaan tällä lyötiin "luuri korvaan" modeemissa. Nykyisin tällä voidaan esimerkiksi pakottaa daemon lataamaan konfiguraatiotiedostot uusiksi. |
| 2    | INT      | Interrupt. Sama kuin ++ctrl+c++. Ohjelmaa pyydetään sulkeutumaan nätisti. |
| 3    | QUIT     | Quit. Ohjelmaa pyydetään sulkeutumaan ja kirjoittamaan core dump. |
| 6    | ABRT     | Abort. Ohjelmaa pyydetään sulkeutumaan ja kirjoittamaan core dump. |
| 9    | KILL     | Kill. Ohjelmalta ei pyydetä mitään eikä ohjelma täten voi jättää tätä tekemättä. Kernel lopettaa prosessin ajon ja poistaa sen muistista. |
| 14   | ALRM     | Alarm.                                                       |
| 15   | TERM     | Terminate. Komennon `kill` default. Ohjelmaa pyydetään sulkemaan itsensä. |

Tyypillisesti `kill`-komentoa ei pitäisi tarvita laisinkaan. Jos sitä kuitenkin tarvitsee, kokeile ensin `TERM`:n avulla eli `kill pid`. Mikäli ohjelma ei näytä sammutan, aja perään `KILL`. Alla esimerkki:

```bash
# Luo prosessi, joka nukkuu 24h
$ sleep $((60 * 60 * 24))

###############################################
# Avaa toinen pseudo- tai virtuaaliterminaali #
###############################################

$ ps
PID   TTY           TIME CMD
26967 ttys008    0:01.32 /bin/zsh
29527 ttys008    0:00.00 sleep 86400    # <= Tämä
...

$ kill -TERM 29527

###########################################
# Mene takaisin ensimmäiseen terminaaliin #
# #########################################

[1]    29527 terminated  sleep $((60 * 60 * 24))
```



## Tausta-ajo

Ohjelmia voi ajaa myös taustalla päättämällä komentiriviin `&`-merkkiin. Ohjelma siirtyy tausta-ajoon myös siten, että etualalla ajettavan ohjelman kohdalla painetaan ++ctrl+z++ (`SIGTSTP`). Tosin tämä pysäyttää ohjelman ajon. Ohjelman saa takaisin etualalle komennolla `fg`, tai `fg %n`, jossa `n` on se hakasuluissa näytetty numero eli `JOB_SPEC`, joka on useimmiten `[1]`. Vaihtoehtoisesti ohjelman voi laittaa käyntiin ++ctrl+z++ painamisen jälkeen komennolla `bg %n`, jossa `n` on yhä `JOB_SPEC`

```bash
$ sleep $((60 * 60 * 24)) &
$ sleep $((60 * 60 * 24)) &
$ sleep $((60 * 60 * 24)) &
$ sleep $((60 * 60 * 24)) &

$ jobs -l   # -l listaa myös PID:t
[1]    71338 running    sleep $((60 * 60 * 24))
[2]    71344 running    sleep $((60 * 60 * 24))
[3]  - 71350 running    sleep $((60 * 60 * 24))
[4]  + 71435 running    sleep $((60 * 60 * 24))

$ kill %4  # JOB_SPEC-numeroon voi viitata %n:llä
[4]  + 71435 terminated  sleep $((60 * 60 * 24))

$ jobs
[1]    running    sleep $((60 * 60 * 24))
[2]  - running    sleep $((60 * 60 * 24))
[3]  + running    sleep $((60 * 60 * 24))
```

Huomaa, että jos nyt loggaat ulos tai suljet shellin (`exit`), niin kyseiset prosessit päättyvät välittömästi. Tuoreimman jobin rivillä on `+`-merkki, joka viittaa siihen, että ilman parametrejä annettu komento (kuten `fg`) viittaa kyseiseen jobiin.

```bash
$ fg
[3]  - 71350 running    sleep $((60 * 60 * 24))

# PAINA CTRL + Z
[3]  + 71350 suspended  sleep $((60 * 60 * 24))

$ bg %3
[3]  - 71350 continued  sleep $((60 * 60 * 24))

$ jobs
[1]    running    sleep $((60 * 60 * 24))
[2]  - running    sleep $((60 * 60 * 24))
[3]  + running    sleep $((60 * 60 * 24))

$ kill %1 %2 %3
[1]    71338 terminated  sleep $((60 * 60 * 24))
[3]  + 71350 terminated  sleep $((60 * 60 * 24))
[2]  + 71344 terminated  sleep $((60 * 60 * 24))
```

Jos on tarve ajaa ohjelma siten, että se ei sammu terminaalin sulkeutumisen yhteydessä tai logoutin yhteydessä, niin komento `nohup` on avuksi. Ajetaan vanha tuttu `sleep` uusiksi, mutta ohjataan stdout bittiavaruuteen ja stderr tiedostoon `errors.log`. 

```bash
$ nohup sleep $((60 * 60 * 24)) > /dev/null 2> errors.log &
[1] 71645

$ jobs
[1]  + running    nohup sleep $((60 * 60 * 24)) > /dev/null 2> errors.log

#######################################
# Uudelleenkäynnistä pseudoterminaali #
#######################################

$ jobs
# Ei tulosta mitään

$ ps 71645
PID     TT  STAT      TIME COMMAND
71645   ??  SN     0:00.01 sleep 86400

$ kill 71645
$ rm errors.log
```



## Avoimien tiedostojen etsiminen

Mikäli haluat saada tietää, mikä ohjelmaa lukee tai kirjoittaa paraikaa johonkin tiedostoon, tähän auttaa komento `lsof`. FD-kentässä olevat numerot viittaavat "Descriptor ID":hen, joista 0 on standard input, 1 on standard output ja 2 on standard error. Numeroa 2 suuremmat ovat ohjelmien itsensä avaamia uusia descriptoreita (esimerkiksi `open()`-funktion puolesta.)

```bash
$ echo "Miau" > kissa.txt
$ tail -f kissa.txt &
[1] 71967
Miau

$ jobs
[1]  + running    tail -f kissa.txt

$ lsof | grep kissa.txt
tail      71967  janisou1  3r  /Users/opettaja/kissa.txt # Lyhennetty

$ echo "MIAW" > kissa.tx
MIAW   # Huomaathan, että bg ei estä ohjelmaa tulostamasta stdouttia tty:iin

$ kill %1
$ rm kissa.txt
```
