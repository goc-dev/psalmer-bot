# psalmer-bot

*Description*: 
v.1 Telegram bot to provide lyrics and chords of psalms


`.env`
```
PSALMER_BOT_TOKEN="123123123:asdfasdfasdfasdfasdfsadf-defdef"
HYMNAL_HOME_DIR='/workspaces/psalmer-bot/hymnal'
```


How to install ChordPro converter CHO-to-PDF:
https://www.chordpro.org/chordpro/chordpro-install-on-debian/

GitHub Codespace:

```
$ sudo -i
# apt-get update
# apt-get install cpanminus
```

```
$ sudo -i
# cd ~
# mkdir install
# cd install
git clone https://github.com/ChordPro/chordpro
cd chordpro
git checkout dev
perl Makefile.PL
```

```
Checking if your kit is complete...
Looks good
Warning: prerequisite Data::Printer 1.001001 not found.
Warning: prerequisite File::HomeDir 1.004 not found.
Warning: prerequisite File::LoadLines 1.047 not found.
Warning: prerequisite HarfBuzz::Shaper 0.026 not found.
Warning: prerequisite IPC::Run3 0.049 not found.
Warning: prerequisite Image::Info 1.41 not found.
Warning: prerequisite JSON::XS 4.03 not found.
Warning: prerequisite JavaScript::QuickJS 0.18 not found.
Warning: prerequisite LWP::Protocol::https 6.14 not found.
Warning: prerequisite Mozilla::CA 20230801 not found.
Warning: prerequisite Object::Pad 0.818 not found.
Warning: prerequisite PDF::API2 2.045 not found.
Warning: prerequisite String::Interpolate::Named 1.06 not found.
Warning: prerequisite Text::Layout 0.045 not found.
Generating a Unix-style Makefile
Writing Makefile for App::Music::ChordPro
Writing MYMETA.yml and MYMETA.json
```

List missed dependencies:
```
mymeta-requires | cpanm
```

Install packages:
```
cpanm --installdeps .
```

Compile and install:
```
# make
# make install
```

Verify:
```
chordpro -h
```