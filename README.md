### ug2cho

`ug2cho` is a tool for downloading leadsheets from
[ultimate-guitar.com](https://ultimate-guitar.com) and converting
them to [ChordPro](https://www.chordpro.org) or plain text.

#### Motivation

UG has a huge number of user-contributed leadsheets, but the website is full of
dark patterns and is quite annoying to use. This problem is largely solved by
the [freetar](https://github.com/kmille/freetar) project. However, it has
recently stopped working well because UG has activated cloudflare client
verification and will deny most requests not coming from a browser.

I also prefer having a local book of song leadsheets. I was initially
maintaining a [fork](https://github.com/dexterlb/freetar) of
[freetar](https://github.com/kmille/freetar) that allows downloading leadsheets
as ChordPro files, but at some point I realised that I don't use the freetar
instance for anything apart from downloading the leadsheet as a `.cho` file.

Thus, I threw this project together.

#### Examples

Download a leadsheet and save it as a `.cho` file:

```
$ ug2cho https://tabs.ultimate-guitar.com/tab/monty-python/always-look-on-the-bright-side-of-life-chords-76791 bright_side.cho
```

Download a leadsheet and save it as a plain-text file:

```
$ ug2cho https://tabs.ultimate-guitar.com/tab/monty-python/always-look-on-the-bright-side-of-life-chords-76791 bright_side.txt
```

Convert a leadsheet from HTML (e.g. you used the browser's Save Page function) to ChordPro:

```
$ ug2cho foo.html foo.cho
```

Force input and output formats:
```
$ ug2cho --in-format=html --out-format=txt html_file out_file
```

Save leadsheet to auto-generated filename

```
$ mkdir songs
$ ug2cho https://tabs.ultimate-guitar.com/tab/monty-python/always-look-on-the-bright-side-of-life-chords-76791 songs
$ ls songs
Monty Python - Always Look On The Bright Side of Life
```

Save to intermediate `ug` format, patch up the leadsheet and then convert it to ChordPro:

```
$ ug2cho <url or HTML file> song.ug
$ vim song.ug   # edit and fix typos in chords, etc
$ ug2cho song.ug song.cho
```
