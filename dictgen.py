import json
import unicodedata


def gendict(
    subdicts=[
        {"reverse": False, "decomposed": False, "caps_insensitive": False, "data": {}}
    ],
):
    dict = []

    for x in subdicts:
        data = x.get("data")
        for sub_length in range(
            len(max(data, key=len)),
            len(min(data, key=len)) - 1,
            -1,
        ):
            tempdict = {}
            for item in data:
                if len(item) == sub_length:
                    tempdict[item] = data[item]

            dict.append(
                {
                    "sub_length": sub_length,
                    "reverse": x.get("reverse", False),
                    "decomposed": x.get("decomposed", False),
                    "caps_insensitive": x.get("caps_insensitive", False),
                    "data": tempdict,
                }
            )
    return dict


data = {}
cyrillic = {
    "Pf": "Ԥ",
    "pF": "ԥ",
    "PF": "Ԥ",
    "pf": "ԥ",
    #
    "Ts": "Ц",
    "tS": "ц",
    "TS": "Ц",
    "ts": "ц",
    #
    "Tþ": "Ҭ",
    "tÞ": "ҭ",
    "TÞ": "Ҭ",
    "tþ": "ҭ",
    #
    "Kx": "Қ",
    "kX": "қ",
    "KX": "Қ",
    "kx": "қ",
}

cyrillicpairs = [
    ("a", "а"),
    ("æ", "ӕ"),
    ("b", "б"),
    ("g", "г"),
    ("d", "д"),
    ("e", "е"),
    ("z", "з"),
    ("i", "и"),
    ("j", "ј"),
    ("k", "к"),
    ("l", "л"),
    ("m", "м"),
    ("n", "н"),
    ("ŋ", "ҥ"),
    ("o", "о"),
    ("p", "п"),
    ("r", "р"),
    ("s", "с"),
    ("t", "т"),
    ("u", "у"),
    ("w", "ў"),
    ("y", "ү"),
]

for x in cyrillicpairs:
    cyrillic[x[0].lower()] = x[1].lower()
    cyrillic[x[0].upper()] = x[1].upper()

data["Cyrillic"] = gendict(
    [
        {"decomposed": True, "data": cyrillic},
    ]
)

katakana0 = {}

for vowel in ("a", "i", "u", "e", "o", "æ", "y"):
    katakana0[unicodedata.normalize("NFC", vowel + "̄")] = vowel + vowel


katakana1 = {}

for vowel in ("a", "i", "u", "e", "o", "æ", "y"):
    katakana1[vowel + vowel] = vowel + "ー"


katakana2 = {
    "a": "ア",
    "i": "イ",
    "u": "ウ",
    "e": "エ",
    "o": "オ",
    "æ": "アｪ",
    "y": "イｩ",
    #
    "ka": "カ",
    "ki": "キ",
    "ku": "ク",
    "ke": "ケ",
    "ko": "コ",
    "kæ": "カｪ",
    "ky": "キｩ",
    #
    "ga": "ガ",
    "gi": "ギ",
    "gu": "グ",
    "ge": "ゲ",
    "go": "ゴ",
    "gæ": "ガｪ",
    "gy": "ギｩ",
    #
    "ŋa": "カ゚",
    "ŋi": "キ゚",
    "ŋu": "ク゚",
    "ŋe": "ケ゚",
    "ŋo": "コ゚",
    "ŋæ": "カ゚ｪ",
    "ŋy": "キ゚ｩ",
    #
    "kxa": "カ̣",
    "kxi": "キ̣",
    "kxu": "ク̣",
    "kxe": "ケ̣",
    "kxo": "コ̣",
    "kxæ": "カ̣ｪ",
    "kxy": "キ̣ｩ",
    #
    "sa": "サ",
    "si": "セィ",
    "su": "ス",
    "se": "セ",
    "so": "ソ",
    "sæ": "サｪ",
    "sy": "セｨｩ",
    #
    "za": "ザ",
    "zi": "ゼィ",
    "zu": "ズ",
    "ze": "ゼ",
    "zo": "ゾ",
    "zæ": "ザｪ",
    "zy": "ゼｨｩ",
    #
    "ta": "タ",
    "ti": "ティ",
    "tu": "トゥ",
    "te": "テ",
    "to": "ト",
    "tæ": "タｪ",
    "ty": "テｨｩ",
    #
    "da": "ダ",
    "di": "ディ",
    "du": "ドゥ",
    "de": "デ",
    "do": "ド",
    "dæ": "ダｪ",
    "dy": "デｨｩ",
    #
    "tþa": "タ̣",
    "tþi": "テ̣ィ",
    "tþu": "ト̣ゥ",
    "tþe": "テ̣",
    "tþo": "ト̣",
    "tþæ": "タ̣ｪ",
    "tþy": "テ̣ｨｩ",
    #
    "tsa": "ツァ",
    "tsi": "ツィ",
    "tsu": "ツ",
    "tse": "ツェ",
    "tso": "ツォ",
    "tsæ": "ツｧｪ",
    "tsy": "ツｨｩ",
    #
    "na": "ナ",
    "ni": "ニ",
    "nu": "ヌ",
    "ne": "ネ",
    "no": "ノ",
    "næ": "ナｪ",
    "ny": "ニｩ",
    #
    "pa": "パ",
    "pi": "ピ",
    "pu": "プ",
    "pe": "ペ",
    "po": "ポ",
    "pæ": "パｪ",
    "py": "ピｩ",
    #
    "ba": "バ",
    "bi": "ビ",
    "bu": "ブ",
    "be": "ベ",
    "bo": "ボ",
    "bæ": "バｪ",
    "by": "ビｩ",
    #
    "pfa": "パ̣",
    "pfi": "ピ̣",
    "pfu": "プ̣",
    "pfe": "ペ̣",
    "pfo": "ポ̣",
    "pfæ": "パ̣ｪ",
    "pfy": "ピｩ̣",
    #
    "ma": "マ",
    "mi": "ミ",
    "mu": "ム",
    "me": "メ",
    "mo": "モ",
    "mæ": "マｪ",
    "my": "ミｩ",
    #
    "ja": "ヤ",
    "ji": "イ゚",
    "ju": "ユ",
    "je": "エ゚",
    "jo": "ヨ",
    "jæ": "ヤｪ",
    "jy": "イ゚ｩ",
    #
    "ra": "ラ",
    "ri": "リ",
    "ru": "ル",
    "re": "レ",
    "ro": "ロ",
    "ræ": "ラｪ",
    "ry": "リｩ",
    #
    "la": "ラ゚",
    "li": "リ゚",
    "lu": "ル゚",
    "le": "レ゚",
    "lo": "ロ゚",
    "læ": "ラ゚ｪ",
    "ly": "リ゚ｩ",
    #
    "wa": "ワ",
    "wi": "ヰ",
    "wu": "ウ゚",
    "we": "ヱ",
    "wo": "ヲ",
    "wæ": "ワｪ",
    "wy": "ヰｩ",
    #
    "k": "ㇰ",
    "g": "ㇰ゙",
    "ŋ": "ㇰ゚",
    "kx": "ㇰ̣",
    "s": "ㇲ",
    "z": "ㇲ゙",
    "t": "ㇳ",
    "d": "ㇳ゙",
    "tþ": "ㇳ̣",
    "ts": "ッ゚",
    "n": "ン",
    "p": "ㇷ゚",
    "b": "ㇷ゙",
    "pf": "ㇷ゚̣",
    "m": "ㇺ",
    "j": "ィ゚",
    "r": "ㇽ",
    "l": "ㇽ゚",
    "w": "ゥ゚",
    #
    " ": "・",
    ".": "。",
    ",": "、",
    "!": "！",
    ". ": "。",
    ", ": "、",
    "! ": "！",
    "-": "―",
    "+": "＋",
    "(": "（",
    ")": "）",
    "~": "〜",
}

data["Katakana"] = gendict(
    [
        {"caps_insensitive": True, "data": katakana0},
        {"reverse": True, "caps_insensitive": True, "data": katakana1},
        {"caps_insensitive": True, "data": katakana2},
    ]
)

# Lontara Dict Generator

lontara0 = {}

for vowel in ("a", "i", "u", "e", "o", "y", "æ"):
    lontara0[unicodedata.normalize("NFC", vowel + "̄")] = vowel + vowel

lontara1 = {",": "᨞", ".": "᨟"}
lontaraConsonants = {
    "k": "ᨀ",
    "g": "ᨁ",
    "ŋ": "ᨂ",
    "kx": "ᨃ",
    "p": "ᨄ",
    "b": "ᨅ",
    "m": "ᨆ",
    "pf": "ᨇ",
    "t": "ᨈ",
    "d": "ᨉ",
    "n": "ᨊ",
    "tþ": "ᨋ",
    "ts": "ᨌ",
    "j": "ᨐ",
    "r": "ᨑ",
    "l": "ᨒ",
    "w": "ᨓ",
    "s": "ᨔ",
    "": "ᨕ",
}
lontaraAttachments = {
    "": "̲",
    "a": "",
    "i": "ᨗ",
    "u": "ᨘ",
    "e": "ᨙ",
    "o": "ᨚ",
    "æ": "ᨛ",
    "y": "︠",
}

for x in lontaraConsonants:
    for y in lontaraAttachments:
        if x != "" or y != "":
            lontara1[x + y] = lontaraConsonants[x] + lontaraAttachments[y]

data["Lontara"] = gendict(
    [
        {"caps_insensitive": True, "data": lontara0},
        {"caps_insensitive": True, "data": lontara1},
    ]
)

out = json.dumps(data, sort_keys=True, indent=4)
f = open("dict.json", "w")
f.write(out)
f.close()
