import json
import unicodedata
import re


def gendict(
    subdicts=[
        {
            "type": "dict",
            "reverse": False,
            "decomposed": False,
            "caps_insensitive": False,
            "data": {},
        }
    ],
):
    dict = []

    for x in subdicts:
        if x.get("type", "dict") == "dict":
            data = x.get("data")
            primary_dict = {}
            aliases_dict = {}

            for entry in data:
                if data[entry] not in primary_dict.values():
                    primary_dict[entry] = data[entry]
                else:
                    aliases_dict[entry] = data[entry]

            for sub_length in range(
                len(max(data, key=len)),
                len(min(data, key=len)) - 1,
                -1,
            ):
                temp_dict = {}
                aliases_temp_dict = {}
                for item in primary_dict:
                    if len(item) == sub_length:
                        temp_dict[item] = primary_dict[item]
                for item in aliases_dict:
                    if len(item) == sub_length:
                        aliases_temp_dict[item] = aliases_dict[item]
                dict.append(
                    {
                        "type": "dict",
                        "sub_length": sub_length,
                        "reverse": x.get("reverse", False),
                        "decomposed": x.get("decomposed", False),
                        "caps_insensitive": x.get("caps_insensitive", False),
                        "data": temp_dict,
                        "aliases": aliases_temp_dict,
                    }
                )
        elif x.get("type", "dict") == "regex":
            dict.append(
                {
                    "type": "regex",
                    "decomposed": x.get("decomposed", False),
                    "params": x.get("params"),
                    "undo": x.get("undo", None),
                }
            )

    return dict


data = {}

latin0 = {
    "\\AE": "Æ",
    "\\ae": "æ",
    "\\NG": "Ŋ",
    "\\ng": "ŋ",
    "\\TH": "Þ",
    "\\th": "þ",
}

latin1 = {}
for vowel in ("a", "i", "u", "e", "o", "æ", "y"):
    latin1["\=" + vowel] = unicodedata.normalize("NFC", vowel + "̄")
    latin1["\=" + vowel.upper()] = unicodedata.normalize("NFC", vowel.upper() + "̄")

data["Latin"] = gendict([{"data": latin0}, {"data": latin1}])

cyrillic = {
    "pf": "ԥ",
    "Pf": "Ԥ",
    "pF": "ԥ",
    "PF": "Ԥ",
    #
    "ts": "ц",
    "Ts": "Ц",
    "tS": "ц",
    "TS": "Ц",
    #
    "tþ": "ҭ",
    "Tþ": "Ҭ",
    "tÞ": "ҭ",
    "TÞ": "Ҭ",
    #
    "kx": "қ",
    "Kx": "Қ",
    "kX": "қ",
    "KX": "Қ",
}

for a in ("þ", "th"), ("Þ", "Th"), ("þ", "tH"), ("Þ", "TH"):
    for b in list(cyrillic):
        if a[0] in b:
            cyrillic[b.replace(a[0], a[1])] = cyrillic[b]

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

cyrillic["ng"] = "ҥ"
cyrillic["NG"] = "Ҥ"
cyrillic["nG"] = "ҥ"
cyrillic["Ng"] = "Ҥ"

data["Cyrillic"] = gendict(
    [
        {"decomposed": True, "data": cyrillic},
        {
            "type": "regex",
            "params": (
                r"(?i)(н)'(г)",
                r"\1\2",
                "text",
            ),
            "undo": (
                r"(?i)(н)(г)",
                r"\1'\2",
                "text",
            ),
        },
        {
            "type": "regex",
            "params": (
                r"(?i)(т)'(с)",
                r"\1\2",
                "text",
            ),
            "undo": (
                r"(?i)(т)(с)",
                r"\1'\2",
                "text",
            ),
        },
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
    ": ": "：",
    ":": "：",
    ". ": "。",
    ", ": "、",
    "! ": "！",
    "-": "゠",
    "=": "＝",
    "+": "＋",
    "(": "（",
    ")": "）",
    "~": "〜",
}

for a in ("tþ", "tth"), ("ŋ", "ng"):
    for b in list(katakana2):
        if a[0] in b:
            katakana2[b.replace(a[0], a[1])] = katakana2[b]

data["Katakana"] = gendict(
    [
        {"caps_insensitive": True, "data": katakana0},
        {"reverse": True, "caps_insensitive": True, "data": katakana1},
        {
            "type": "regex",
            "params": (
                r"(?i)(a|i|u|e|o|y|æ)((ー){0,})'\1{1}",
                r"\1\2\1",
                "text",
            ),
            "undo": (
                r"(?i)(a|i|u|e|o|y|æ)((ー){0,})\1{1}",
                r"\1\2'\1",
                "text",
            ),
        },
        {"caps_insensitive": True, "data": katakana2},
        {
            "type": "regex",
            "params": (
                r"(ㇰ|ㇰ゙|ㇰ゚|ㇰ̣|ㇲ|ㇲ゙|ㇳ|ㇳ゙|ㇳ̣|ッ゚|ン|ㇴ|ㇷ゚|ㇷ゙|ㇷ゚̣|ㇺ|ィ゚|ㇽ|ㇽ゚|ゥ゚)'(アｪ|イｩ|ア|イ|ウ|エ|オ)",
                r"\1\2",
                "text",
            ),
            "undo": (
                r"(ㇰ|ㇰ゙|ㇰ゚|ㇰ̣|ㇲ|ㇲ゙|ㇳ|ㇳ゙|ㇳ̣|ッ゚|ン|ㇴ|ㇷ゚|ㇷ゙|ㇷ゚̣|ㇺ|ィ゚|ㇽ|ㇽ゚|ゥ゚)(アｪ|イｩ|ア|イ|ウ|エ|オ)",
                r"\1'\2",
                "text",
            ),
        },
        {
            "type": "regex",
            "params": (
                r"(ン|ㇴ)'(ガｪ|ギｩ|ガ|ギ|グ|ゲ|ゴ|ㇰ゙)",
                r"\1\2",
                "text",
            ),
            "undo": (
                r"(ン|ㇴ)(ガｪ|ギｩ|ガ|ギ|グ|ゲ|ゴ|ㇰ゙)",
                r"\1'\2",
                "text",
            ),
        },
        {
            "type": "regex",
            "params": (
                r"(ㇳ)'(サｪ|セｨｩ|サ|セィ|ス|セ|ソ)",
                r"\1\2",
                "text",
            ),
            "undo": (
                r"(ㇳ)(サｪ|セｨｩ|サ|セィ|ス|セ|ソ)",
                r"\1'\2",
                "text",
            ),
        },
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

for a in ("tþ", "tth"), ("ŋ", "ng"):
    for b in list(lontara1):
        if a[0] in b:
            lontara1[b.replace(a[0], a[1])] = lontara1[b]

data["Lontara"] = gendict(
    [
        {"caps_insensitive": True, "data": lontara0},
        {"caps_insensitive": True, "data": lontara1},
        {
            "type": "regex",
            "params": (
                r"(ᨀ̲|ᨁ̲|ᨂ̲|ᨃ̲|ᨄ̲|ᨅ̲|ᨆ̲|ᨇ̲|ᨈ̲|ᨉ̲|ᨊ̲|ᨋ̲|ᨌ̲|ᨐ̲|ᨑ̲|ᨒ̲|ᨓ̲|ᨔ̲)'(ᨕᨗ|ᨕᨘ|ᨕᨙ|ᨕᨚ|ᨕᨛ|ᨕ︠|ᨕ)",
                r"\1\2",
                "text",
            ),
            "undo": (
                r"(ᨀ̲|ᨁ̲|ᨂ̲|ᨃ̲|ᨄ̲|ᨅ̲|ᨆ̲|ᨇ̲|ᨈ̲|ᨉ̲|ᨊ̲|ᨋ̲|ᨌ̲|ᨐ̲|ᨑ̲|ᨒ̲|ᨓ̲|ᨔ̲)(ᨕᨗ|ᨕᨘ|ᨕᨙ|ᨕᨚ|ᨕᨛ|ᨕ︠|ᨕ)",
                r"\1'\2",
                "text",
            ),
        },
        {
            "type": "regex",
            "params": (
                r"(ᨊ̲)'(ᨁ̲|ᨁᨗ|ᨁᨘ|ᨁᨙ|ᨁᨚ|ᨁᨛ|ᨁ︠|ᨁ)",
                r"\1\2",
                "text",
            ),
            "undo": (
                r"(ᨊ̲)(ᨁ̲|ᨁᨗ|ᨁᨘ|ᨁᨙ|ᨁᨚ|ᨁᨛ|ᨁ︠|ᨁ)",
                r"\1'\2",
                "text",
            ),
        },
        {
            "type": "regex",
            "params": (
                r"(ᨈ̲)'(ᨔ̲|ᨔᨗ|ᨔᨘ|ᨔᨙ|ᨔᨚ|ᨔᨛ|ᨔ︠|ᨔ)",
                r"\1\2",
                "text",
            ),
            "undo": (
                r"(ᨈ̲)(ᨁ̲|ᨔ̲|ᨔᨗ|ᨔᨘ|ᨔᨙ|ᨔᨚ|ᨔᨛ|ᨔ︠|ᨔ)",
                r"\1'\2",
                "text",
            ),
        },
    ]
)


out = json.dumps(data, sort_keys=True, indent=4)
f = open("dict.json", "w")
f.write(out)
f.close()
