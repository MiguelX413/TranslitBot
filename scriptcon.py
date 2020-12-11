import unicodedata


def preCommon(text):
    # 	text = unicodedata.normalize('NFC', unicodedata.normalize('NFD', text))
    text = text.replace("ng", "ŋ")
    return text


def postCommon(text):
    text = unicodedata.normalize("NFC", unicodedata.normalize("NFD", text))
    text = text.replace("\\", "")
    return text


def convert(text, dictionary, vowels=("a", "i", "u", "e", "o", "æ", "y")):
    # Decompose and recompose everything in the text
    text = unicodedata.normalize("NFC", unicodedata.normalize("NFD", text))
    # Convert double bowels to
    if dictionary.get("demacron"):
        for vowel in vowels:
            text = text.replace(
                unicodedata.normalize("NFC", vowel + "̄"), (vowel + vowel)
            )
            text = text.replace(
                unicodedata.normalize("NFC", vowel + "̄").upper(),
                (vowel + vowel).upper(),
            )

    if dictionary.get("decomposed"):
        text = unicodedata.normalize("NFD", text)

    if dictionary.get("tolowercase"):
        text = text.lower()

    for step in ("preproc", "main", "postproc"):
        if dictionary.get(step):
            if dictionary[step].get("rev") == False:
                for size in range(
                    dictionary[step].get("max", len(max(dictionary[step], key=len))),
                    dictionary[step].get("min", len(min(dictionary[step], key=len)))
                    - 1,
                    -1,
                ):
                    index = 0
                    while index <= len(text) - size:
                        # print(text)
                        # print(len(text))
                        # print(text[index : index + size])
                        text = text.replace(
                            text[index : index + size],
                            dictionary[step]["data"].get(
                                text[index : index + size], text[index : index + size]
                            ),
                            1,
                        )
                        index = index + 1

            else:
                for size in range(
                    dictionary[step].get("max", len(max(dictionary[step], key=len))),
                    dictionary[step].get("min", len(min(dictionary[step], key=len)))
                    - 1,
                    -1,
                ):
                    index = 0
                    while len(text) - index - size >= 0:
                        # print(text)
                        # print(len(text))
                        # print(text[index : index + size])
                        text = text[::-1].replace(
                            text[len(text) - index - size : len(text) - index][::-1],
                            dictionary[step]["data"].get(
                                text[len(text) - index - size : len(text) - index],
                                text[len(text) - index - size : len(text) - index],
                            )[::-1],
                            1,
                        )[::-1]
                        index = index + 1
    return unicodedata.normalize("NFC", text)
