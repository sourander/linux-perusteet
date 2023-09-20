Jotta levyjä voisi käyttää käyttöjärjestelmässä, täytyy niillä olla osio tai useampi (eng. partition). Osiointiin voi käyttää ohjelmaa `parted` tai `fdisk`. Ensimmäisestä löytyy myös GUI-versio nimellä `gparted`. Osiot tallennetaan **kyseisellä levyllä** olevaan osiointitaulukkoon (eng. partitioning table), joka on (ainakin loogisen osoitteen puolesta) levyn alussa, eli HDD:n tapauksessa sen voi kuvitella olevan pyörivän kiekon ulkolaidalla. SSD:n tapauksessa pyörivää kiekkoa ei ole, mutta loogiset osoitteet löytyvät silti. Varsinaiset partitiot eli ohjelmien tallentama data tallennetaan kiekon (tai median) alueille, joita ei ole varattu GPT:n käyttöön.

Olemassa olevat osiot voi listata seuraavalla komennolla:

```bash
$ sudo parted -l
Model: QEMU QEMU HARDDISK (scsi)                                          
Disk /dev/sda: 10,7GB
Sector size (logical/physical): 512B/512B
Partition Table: unknown
Disk Flags: 

Error: /dev/sdb: unrecognised disk label
Model: QEMU QEMU HARDDISK (scsi)                                          
Disk /dev/sdb: 10,7GB
Sector size (logical/physical): 512B/512B
Partition Table: unknown
Disk Flags: 

Model: Virtio Block Device (virtblk)
Disk /dev/vda: 68,7GB
Sector size (logical/physical): 512B/512B
Partition Table: gpt
Disk Flags: 

Number  Start   End     Size    File system  Name                  Flags
 1      1049kB  538MB   537MB   fat16        EFI System Partition  boot, esp
 2      538MB   68,7GB  68,2GB  ext4
```

Huomaa yllä olevasta tulosteesta, että kummallakaan SCSI-levyllä (sda, sdb) ei ole osiointitaulukkoa olemassa. Sen sijaan Ubuntu Installerin luoma levy on partitioitu GPT-taulukon avulla. Osiointitaulukkoja on kahta sorttia: vanhempi **MBP** ja uudempi **GPT**. Nämä tulevat sanoista Master Boot Record sekä GUID Partition Table. MBP kannattaa uusissa koneissa jättää kokonaisuudessaan historiaan ja käyttää sen uudempaa, UEFI-yhteensopivaa vastinetta eli GPT:tä.

Yllä mainittu GUID (eli siis GPT-lyhenteen ensimmäinen kirjain) tulee sanoista Globally Unique Identifier, joka näytetään käyttäjälle tyypillisesti heksadesimaalina, joka on eritelty muutamaan katkoviivalla eriteltyyn ryppääseen, joissa kussakin on seuraava määrä digittejä: `<8-4-4-4-12>`. Alla näkyy nykyisten osioiden GUID:t:

```bash
$ sudo blkid /dev/vda
/dev/vda: PTUUID="b617623d-318a-4180-b190-04037556de27" PTTYPE="gpt"

$ sudo blkid /dev/sda
# Ei tulostu mitään
```



## Yksi osio uudelle levylle

!!! warning
    Ethän tee näitä harjoitteita koneella, jossa on pieninkään riski menettää dataa. Nämä harjoitukset tulisi tehdä sinun itsesi hostaamalla virtuaalikoneella, jolle ei ole tallennettu mitään arvokasta.

Kokeillaan osioida yllä mainittu levy `sda`, luoda sille file system, ja mountata levy johonkin, missä sitä voidaan käyttää. Aivan ensimmäiseksi on hyvä varmistaa, että levyä ei ole jo mountattu johonkin. Tässä tapauksessa on vähän mahdotonta, kun levyllä ei ole edes osioida joita mountata, mutta tilanne voi olla toinen, mikäli sinulla on fyysinen kone, ja sen kiintolevyillä on entuudestaan jotakin sisältöä.

```bash
$ mount | grep sda # Tuloste on arvatenkin tyhjä
```

Käynnistetään partitiointiohjelma.

```bash
$ sudo parted /dev/sda
GNU Parted 3.4
Using /dev/sda
Welcome to GNU Parted! Type 'help' to view a list of commands.
```

Tämä käynnistää interaktiivisen ohjelman, joten `$`-merkkiä ei jatkossa ole enää prompt:n alussa, vaan promtia ylläpitää parted. Tämän tunnistaa `(parted)`-tekstistä promptin alussa. Kuten aina, tarkista help ensin, jos ohjelmasta sellainen löytyy. Koko manuaali lyötyy [GNU:n sivuilta](https://www.gnu.org/software/parted/manual/parted.html).

```txt
(parted) help
  align-check TYPE N                       check partition N for TYPE(min|opt) alignment
  help [COMMAND]                           print general help, or help on COMMAND
  mklabel,mktable LABEL-TYPE               create a new disklabel (partition table)
  mkpart PART-TYPE [FS-TYPE] START END     make a partition
  ...
```

Ajetaan seuraavat komennot. Risuaidalla alkavat kommentit eivät kuulu komentoihin.

```bash
(parted) mklabel gpt # kommentti (1)

(parted) print       # (2)
Model: QEMU QEMU HARDDISK (scsi)
Disk /dev/sda: 10,7GB
Sector size (logical/physical): 512B/512B
Partition Table: gpt
Disk Flags: 

Number  Start  End  Size  File system  Name  Flags

(parted) mkpart       # (3)
Partition name?  []? mydata
File system type?  [ext2]? ext4 # (4)
Start? 0%             # (5)
End? 100%

(parted) print
Model: QEMU QEMU HARDDISK (scsi)
Disk /dev/sda: 10,7GB
Sector size (logical/physical): 512B/512B
Partition Table: gpt
Disk Flags:

Number  Start   End     Size    File system  Name    Flags
 1      1049kB  10,7GB  10,7GB  ext4         mydata

(parted) quit          # (6)
Information: You may need to update /etc/fstab.
```

1. Luodaan osiointitaulu tai ylikirjoitetaan sellainen.
2. Tulostetaan tähän asti luodut osiot. Huomaa, että `parted` luo kaiken heti käskyn tapahtuessa eikä vasta komennosta poistuessa. Kaikki muutokset ovat siis välittömästi voimassa.
3. Luodaan osio. Tämä käynnistää interaktiiviset kyselyt tulevan osion tiedoista.
4. Tämä komento ei vielä luo file systemiä, mutta varmistaa osion yhteensopivuuden sen file systemin kanssa, jonka siihen aiot myöhemmin luoda.
5. Levytila on helpointa täyttää prosentteina. Luku `0%` on sama kuin kirjoittaisit luvun `1`.
6. Muutoksia ei tarvitse erikseen tallentaa. Poistu ohjelmasta quit-komennolla.

Nyt jos tarkistat `parted -l` komennolla, mitä osioita sinulla on, niin huomaat että levylle on ilmestynyt sekä partition table että yksi osio. Osion `File system` on yhä tyhjä.

```bash
$ sudo parted -l
Model: QEMU QEMU HARDDISK (scsi)
Disk /dev/sda: 10,7GB
Sector size (logical/physical): 512B/512B
Partition Table: unknown
Disk Flags:

Number  Start   End     Size    File system  Name    Flags
 1      1049kB  10,7GB  10,7GB               mydata

# Muiden levyjen output poistettu
```



## Tiedostojärjestelmän luonti

Linuxista löytyy komento `mkfs`, mutta sen man pages sanoo: `This mkfs frontend is deprecated in favour of filesystem specific mkfs.<type> utils.` Emmehän siis käydä vanhentunutta komentoa, vaan tuoreempaa. Konepellin alla tämä kutsuu `mke2fs`-ohjelmaa.

```bash
$ sudo mkfs.ext4 -L MyData /dev/sda1
mke2fs 1.46.5 (30-Dec-2021)
Discarding device blocks: done                            
Creating filesystem with 2620928 4k blocks and 655360 inodes
Filesystem UUID: 2923e1e0-d42a-42d0-a702-abf4d814dd43
...
```



## Osion mounttaus

```bash
# Luo kansio mihin osio mountataan
$ sudo mkdir /mnt/mydata

# Salli itsellesi pääsy tavalla tai toisella. 
# Uusi group olisi hyvä käytäntö, tämä on nopea käytäntö.
$ sudo chown opettaja:opettaja /mnt/mydata

# Mount
$ sudo mount /dev/sda1 /mnt/mydata

# Tarkista
$ mount | grep sda
/dev/sda1 on /mnt/mydata type ext4 (rw,relatime)
```



## Osion mounttaus bootissa

Yksi pieni ongelma on vielä jäljellä. Nykyisellään levyä ei mountata buutin yhteydessä mihinkään, joten joutuisit aina ajamaan käsin `sudo mount ...`-komennon. Tätä varten meidän tarvitsee lisätä kyseinen osio `fstab`-tiedostoon. Luethan ohjekirjan ennen fstab-tiedostoon kajoamista! Ubuntun fstab ohjeet löytyvät esimerkiksi verkkoversiona [Ubuntun manpagesista](https://manpages.ubuntu.com/manpages/jammy/man5/fstab.5.html) tai vanhalla tutulla `man`-komennolla.

```bash
# Tarkista osion UUID. Ei siis levyn vaan osion (sda1)
$ sudo blkdid /dev/sda1
/dev/sda1: LABEL="MyData" UUID="2923e1e0-d42a-42d0-a702-abf4d814dd43" BLOCK_SIZE="4096" TYPE="ext4" PARTLABEL="mydata" PARTUUID="d860c8fb-13ba-4ee0-a3a7-d234d7585ec3"
```

Lisää rivi fstabiin. Alla näkyy`/etc/fstab`-tiedostota vain muutama rivi. Loput on leikattu pois luettavuuden parantamisen takia:

```bash
# <file system> <mount point>   <type>  <options>       <dump>  <pass>
# / was on /dev/vda2 during installation
UUID=a094efbe-85e7-4ca3-ad32-fd590709b753 /               ext4    errors=remount-ro 0       1
UUID=2923e1e0-d42a-42d0-a702-abf4d814dd43 /mnt/mydata     ext4    defaults          0       2
```

Jatkossa, kun käynnistät koneen, kernel mounttaa bootin yhteydessä levyn sille määrättyyn paikkaan File System Hierarchyssä. Mikäli haluat tutkia siihen kohdistuneita operaatioita, tutki kernel ring bufferia komennolla:

```bash
$ sudo dmesg | grep sda
[    3.476610] sd 0:0:0:0: [sda] Attached SCSI disk
[    4.092008] EXT4-fs (sda1): mounted filesystem 2923e1e0-d42a-42d0-a702-abf4d814dd43 with ordered data mode. Quota mode: none.
```

Uusi partitio on näkyvillä muun muassa lsblk komennon outputissa:

```bash
$ lsblk -e 7
NAME   MAJ:MIN RM  SIZE RO TYPE MOUNTPOINTS
sda      8:0    0   10G  0 disk 
└─sda1   8:1    0   10G  0 part /mnt/mydata
sdb      8:16   0   10G  0 disk 
sr0     11:0    1 1024M  0 rom  
vda    252:0    0   64G  0 disk 
├─vda1 252:1    0  512M  0 part /boot/efi
└─vda2 252:2    0 63,5G  0 part /
```



## Osion poisto

TODO
