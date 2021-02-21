import unicodedata
import re

url_regex = re.compile(
    r"((about|ftp(s)?|filesystem|git|ssh|http(s)?):(\/\/)?)?(www\.)?[-a-zA-Z0-9@:%._\+~#=]{1,256}\.[a-zA-Z0-9()]{1,6}\b([-a-zA-Z0-9()@:%_\+.~#?&//=]*)\s?"
)


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
        while index <= len(text) - sub_length:

            if to_reverse:
                sub_string = text[len(text) - index - sub_length : len(text) - index]
            else:
                sub_string = text[index : index + sub_length]
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
            index += 1

    return unicodedata.normalize("NFC", text)


def url_separate(text):
    working_text = text
    results = []
    if url_regex.search(text) is not None:
        while url_regex.search(working_text) is not None:
            partitions = working_text.partition(url_regex.search(working_text).group(0))
            results.append(partitions[0])
            results.append(partitions[1])
            working_text = partitions[2]
        else:
            results.append(working_text)
        return results
    else:
        return [text]
