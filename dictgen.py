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
    ("d", "д"),
    ("e", "е"),
    ("g", "г"),
    ("i", "и"),
    ("j", "ј"),
    ("k", "к"),
    ("l", "л"),
    ("m", "м"),
    ("n", "н"),
    ("o", "о"),
    ("p", "п"),
    ("r", "р"),
    ("t", "т"),
    ("u", "у"),
    ("w", "ў"),
    ("y", "ү"),
    ("ŋ", "ҥ"),
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

for vowel in ("a", "i", "u", "e", "o"):
    katakana0[unicodedata.normalize("NFC", vowel + "̄")] = vowel + vowel


katakana1 = {}

for vowel in ("a", "i", "u", "e", "o"):
    katakana1[vowel + vowel] = vowel + "ー"


katakana2 = {
    "ka": "カ",
    "ki": "キ",
    "ku": "ク",
    "ke": "ケ",
    "ko": "コ",
    #
    "ga": "ガ",
    "gi": "ギ",
    "gu": "グ",
    "ge": "ゲ",
    "go": "ゴ",
    #
    "ŋa": "カ゚",
    "ŋi": "キ゚",
    "ŋu": "ク゚",
    "ŋe": "ケ゚",
    "ŋo": "コ゚",
    #
    "kxa": "カ̣",
    "kxi": "キ̣",
    "kxu": "ク̣",
    "kxe": "ケ̣",
    "kxo": "コ̣",
    #
    "ta": "タ",
    "ti": "ティ",
    "tu": "トゥ",
    "te": "テ",
    "to": "ト",
    #
    "da": "ダ",
    "di": "ディ",
    "du": "ドゥ",
    "de": "デ",
    "do": "ド",
    #
    "tsa": "ツァ",
    "tsi": "ツィ",
    "tsu": "ツ",
    "tse": "ツェ",
    "tso": "ツォ",
    #
    "tþa": "タ̣",
    "tþi": "テ̣ィ",
    "tþu": "ト̣ゥ",
    "tþe": "テ̣",
    "tþo": "ト̣",
    #
    "na": "ナ",
    "ni": "ニ",
    "nu": "ヌ",
    "ne": "ネ",
    "no": "ノ",
    #
    "pa": "パ",
    "pi": "ピ",
    "pu": "プ",
    "pe": "ペ",
    "po": "ポ",
    #
    "ba": "バ",
    "bi": "ビ",
    "bu": "ブ",
    "be": "ベ",
    "bo": "ボ",
    #
    "pfa": "パ̣",
    "pfi": "ピ̣",
    "pfu": "プ̣",
    "pfe": "ペ̣",
    "pfo": "ポ̣",
    #
    "ma": "マ",
    "mi": "ミ",
    "mu": "ム",
    "me": "メ",
    "mo": "モ",
    #
    "ja": "ヤ",
    "ji": "イ゚",
    "ju": "ユ",
    "je": "エ゚",
    "jo": "ヨ",
    #
    "ra": "ラ",
    "ri": "リ",
    "ru": "ル",
    "re": "レ",
    "ro": "ロ",
    #
    "wa": "ワ",
    "wi": "ヰ",
    "wu": "ウ゚",
    "we": "ヱ",
    "wo": "ヲ",
    #
    "la": "ラ゚",
    "li": "リ゚",
    "lu": "ル゚",
    "le": "レ゚",
    "lo": "ロ゚",
    #
    "a": "ア",
    "i": "イ",
    "u": "ウ",
    "e": "エ",
    "o": "オ",
    #
    "k": "ㇰ",
    "g": "ㇰ゙",
    "ŋ": "ㇰ゚",
    "kx": "ㇰ̣",
    "t": "ㇳ",
    "d": "ㇳ゙",
    "ts": "ッ",
    "tþ": "ㇳ̣",
    "n": "ン",
    "b": "ㇷ゙",
    "p": "ㇷ゚",
    "pf": "ㇷ゚̣",
    "m": "ㇺ",
    "j": "ィ゚",
    "r": "ㇽ",
    "w": "ゥ゚",
    "l": "ㇽ゚",
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
    "b": "ᨅ",
    "d": "ᨉ",
    "g": "ᨁ",
    "j": "ᨐ",
    "k": "ᨀ",
    "l": "ᨒ",
    "m": "ᨆ",
    "n": "ᨊ",
    "p": "ᨄ",
    "r": "ᨑ",
    "t": "ᨈ",
    "ts": "ᨌ",
    "w": "ᨓ",
    "ŋ": "ᨂ",
    "pf": "ᨇ",
    "tþ": "ᨋ",
    "kx": "ᨃ",
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
