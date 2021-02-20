import unicodedata


def preCommon(text):
    # 	text = unicodedata.normalize('NFC', unicodedata.normalize('NFD', text))
    text = text.replace("ng", "ŋ")
    return text


def postCommon(text):
    text = unicodedata.normalize("NFC", unicodedata.normalize("NFD", text))
    text = text.replace("\\", "")
    return text


def convert(text, dictionary):

    for subdict in dictionary:
        data, to_reverse, caps_insensitive = (
            subdict.get("data", {}),
            subdict.get("reverse", False),
            subdict.get("caps_insensitive", False),
        )
        sub_length = subdict.get("sub_length", len(max(data, key=len)))

        # Decompose and recompose everything in the text
        text = unicodedata.normalize("NFC", unicodedata.normalize("NFD", text))
        if subdict.get("decomposed"):
            text = unicodedata.normalize("NFD", text)

        index = 0
        print(sub_length)
        while index <= len(text) - sub_length:

            if to_reverse:
                sub_string = text[len(text) - index - sub_length : len(text) - index]
            else:
                sub_string = text[index : index + sub_length]
            print(sub_string)
            key = sub_string

            if caps_insensitive:
                key = key.lower()

            if key in data:
                input_text = text
                replace_from = sub_string

                replace_to = data.get(key)

                if to_reverse:
                    input_text = input_text[::-1]
                    replace_from = replace_from[::-1]
                    replace_to = replace_to[::-1]

                text = input_text.replace(replace_from, replace_to, 1)

                if to_reverse:
                    text = text[::-1]
            print(text)
            index += 1

    return unicodedata.normalize("NFC", text)
