INSERT INTO classes VALUES
(
    'Kuviokellunta',
    'Kuviokellunta on kaikenikäisillä sopiva harrastus, jossa kellutaan ihanasti veden varassa muodostaen kauniita rymäkuvioita. Tässä lajissa eivät taatustikaan nivelet kärsi.'
),
(
    'Brasilialainen Zouk',
    'Brasilialainen Zouk on paritanssi joka kehittyi 1990-luvulla Lambada nimisestä Brasilialaisesta tanssista. Zoukin nimi tulee Zouk-musiikista, jonka tahtiin lajia alunperin tanssittiin. Nykyään Zouk-tanssin musiikkirepertuaari on kuitenkin huomattavasti laajentunut, ja sitä tanssitaan muun muassa myös R''n''B, hip hop ja pop -musiikkiin.'
),
(
    'Kriketti',
    'Kriketti on Englannissa alkunsa saanut mailapallopeli. Siinä kaksi 11-henkistä joukkuetta ottaa mittaa toisistaan ja tavoitteena on tehdä enemmän juoksuja kuin vastustajajoukkue. Kriketin arvioidaan olevan maailman toiseksi suosituin laji, jalkapallon jälkeen.'
);

INSERT INTO members(fname, lname, email) VALUES
(
    'Aku',
    'Ankka',
    'aku.ankka@kwak.fi'
),
(
    'James',
    'Bobond',
    '008@mi.six'
),
(
    'Iida',
    'Ihmetyyppi',
    'i.iida@tehoposti.fi'
);

INSERT INTO users VALUES
(
    'admin',
    -- keepsecret
    'scrypt:32768:8:1$86mF34EX3sbXBncp$636277adce3450fe7aaebd122feaac76db04d4558d52ebf47c501158f275533903e9652871fec69a0d91796d6c37f8e246ac7c635f9c41818fbfc79289fd87aa',
    TRUE,
    NULL
),
(
    'aku964',
    -- oispajoperjantai
    'scrypt:32768:8:1$DjyRPGGPhbhGmavr$7341ddce37b3b48d7e406d6078971bef95c7b69645d7732db2b96486c8a9f071cf99e629aed6aa2aeb140fec33567340450bd967f7ed69aa5b38a636dfb9a771',
    FALSE,
    1
),
(
    'smartboyXZ',
    -- foobar
    'scrypt:32768:8:1$1UnADmG2IjoIN0Y5$48a5ec54738af7df0a11431151098f257c2103777cc5b3f6ec8be6d72b8a27be1de6a6993846f0f860408c6c737495f4454c2ec94c86c0daaa73fbf74eb8040b',
    FALSE,
    2
),
(
    'IidaLOL',
    -- oleniidahehe
    'scrypt:32768:8:1$043MOIodhm6Hnh6m$1839deb4ba8555cbafa9b87f1c9e3c0832169a22e242b7cb891a88db7fb8d4c5d94839546bcde94d7cb4898cb73623fcf2a288af73990dfe925061c1de1416ab',
    FALSE,
    3
);

INSERT INTO comments(classname, username, comment) VALUES
(
    'Kuviokellunta',
    'aku964',
    'paras kurssi ikinä 🔥🔥'
),
(
    'Brasilialainen Zouk',
    'IidaLOL',
    'liian vaikeet, en jaksa'
),
(
    'Kriketti',
    'smartboyXZ',
    'i don''t understand this weird finnish language... can somebody translate?'
);
