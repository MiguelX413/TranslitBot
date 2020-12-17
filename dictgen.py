import json


def gendict(
    main,
    revmain=False,
    preproc=False,
    revpreproc=False,
    postproc=False,
    revpostproc=False,
    demacron=False,
    decomposed=False,
    tolowercase=False,
):
    dict = {}
    if main:
        dict["main"] = {
            "min": len(min(main, key=len)),
            "max": len(max(main, key=len)),
            "rev": revmain,
            "data": main,
        }
    if preproc:
        dict["preproc"] = {
            "min": len(min(preproc, key=len)),
            "max": len(max(preproc, key=len)),
            "rev": revpreproc,
            "data": preproc,
        }
    if postproc:
        dict["postproc"] = {
            "min": len(min(postproc, key=len)),
            "max": len(max(postproc, key=len)),
            "rev": revpostproc,
            "data": postproc,
        }
    dict["demacron"] = demacron
    dict["decomposed"] = decomposed
    dict["tolowercase"] = tolowercase
    return dict


data = {}
cyrillic = {
    "Pf": "Ԥ",
    "pF": "ԥ",
    "PF": "Ԥ",
    "pf": "ԥ",
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

data["Cyrillic"] = gendict(cyrillic, decomposed=True)


katakanaPre = {}

for Kvowel in ("a", "i", "u", "e", "o"):
    katakanaPre[Kvowel + Kvowel] = Kvowel + "ー"


katakanaMain = {
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
    "k": "ㇰ",
    "g": "ㇰ゙",
    "ŋ": "ㇰ゚",
    "kx": "ㇰㇷ",
    "t": "ㇳ",
    "d": "ㇳ゙",
    "tþ": "ㇳ゚",
    "n": "ン",
    "b": "ㇷ゙",
    "p": "ㇷ゚",
    "pf": "ㇷ゚ㇷ",
    "m": "ㇺ",
    "r": "ㇽ",
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
    katakanaMain,
    revmain=False,
    preproc=katakanaPre,
    revpreproc=True,
    demacron=True,
    tolowercase=True,
)


# Lontara Dict Generator
lontara = {",": "᨞", ".": "᨟"}
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
lontaraAttachments = {"": "̲", "a": "", "i": "ᨗ", "u": "ᨘ", "e": "ᨙ", "o": "ᨚ", "æ": "ᨛ"}

for x in lontaraConsonants:
    for y in lontaraAttachments:
        lontara[x + y] = lontaraConsonants[x] + lontaraAttachments[y]

del lontara[""]

data["Lontara"] = gendict(lontara, False, demacron=True, tolowercase=True)

out = json.dumps(data, sort_keys=True, indent=4)
f = open("dict.json", "w")
f.write(out)
f.close()
