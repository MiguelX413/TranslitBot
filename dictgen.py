import json


def gentable(dictionary):
    return {
        "min": len(min(dictionary, key=len)),
        "max": len(max(dictionary, key=len)),
        "dict": dictionary,
    }


cyrillic = {}

cyrillicpairs = [
    ("a", "а"),
    ("æ", "ӕ"),
    ("b", "б"),
    ("d", "д"),
    ("e", "е"),
    ("g", "г"),
    ("i", "и"),
    ("k", "к"),
    ("l", "л"),
    ("m", "м"),
    ("n", "н"),
    ("o", "о"),
    ("p", "п"),
    ("r", "р"),
    ("t", "т"),
    ("u", "у"),
    ("y", "ү"),
    ("ŋ", "ҥ"),
]

for x in cyrillicpairs:
    cyrillic[x[0].lower()] = x[1].lower()
    cyrillic[x[0].upper()] = x[1].upper()

cyrillic["Pf"] = "Ԥ"
cyrillic["pF"] = "ԥ"
cyrillic["PF"] = "Ԥ"
cyrillic["pf"] = "ԥ"
#
cyrillic["Tþ"] = "Ҭ"
cyrillic["tÞ"] = "ҭ"
cyrillic["TÞ"] = "Ҭ"
cyrillic["tþ"] = "ҭ"
#
cyrillic["Kx"] = "Қ"
cyrillic["kX"] = "қ"
cyrillic["KX"] = "Қ"
cyrillic["kx"] = "қ"


katakana = {
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
    "kxa": "カㇵ",
    "kxi": "キㇶ",
    "kxu": "クㇷ",
    "kxe": "ケㇸ",
    "kxo": "コㇹ",
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
    "tþa": "タ゚",
    "tþi": "テ゚ィ",
    "tþu": "ト゚ゥ",
    "tþe": "テ゚",
    "tþo": "ト゚",
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
    "pfa": "パㇵ",
    "pfi": "ピㇶ",
    "pfu": "プㇷ",
    "pfe": "ペㇸ",
    "pfo": "ポㇹ",
    #
    "ma": "マ",
    "mi": "ミ",
    "mu": "ム",
    "me": "メ",
    "mo": "モ",
    #
    "ra": "ラ",
    "ri": "リ",
    "ru": "ル",
    "re": "レ",
    "ro": "ロ",
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
    "b": "ㇷ゙",
    "d": "ㇳ゙",
    "g": "ㇰ゙",
    "k": "ㇰ",
    "l": "ㇽ゚",
    "m": "ㇺ",
    "n": "ン",
    "p": "ㇷ゚",
    "r": "ㇽ",
    "t": "ㇳ",
    "ŋ": "ㇰ゚",
    "kx": "ㇰㇷ",
    "pf": "ㇷ゚ㇷ",
    #
    " ": "・",
    ".": "。",
    ",": "、",
    "!": "！",
}


# Lontara Dict Generator
lontara = {}
lontaraConsonants = {
    "b": "ᨅ",
    "d": "ᨉ",
    "g": "ᨁ",
    "k": "ᨀ",
    "l": "ᨒ",
    "m": "ᨆ",
    "n": "ᨊ",
    "p": "ᨄ",
    "r": "ᨑ",
    "t": "ᨈ",
    "ŋ": "ᨂ",
    "pf": "ᨓ",
    "tþ": "ᨔ",
    "kx": "ᨖ",
    "": "ᨕ",
}
lontaraAttachments = {"": "̲", "a": "", "i": "ᨗ", "u": "ᨘ", "e": "ᨙ", "o": "ᨚ"}

for x in lontaraConsonants:
    for y in lontaraAttachments:
        lontara[x + y] = lontaraConsonants[x] + lontaraAttachments[y]

del lontara[""]

data = {}

data["Lontara"] = gentable(lontara)
data["Katakana"] = gentable(katakana)
data["Cyrillic"] = gentable(cyrillic)

out = json.dumps(data, sort_keys=True, indent=4)
f = open("dict.json", "w")
f.write(out)
f.close()
