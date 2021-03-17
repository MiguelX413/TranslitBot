import unicodedata
import re


def convert(text, dictionary):
    for subdict in dictionary:
        if subdict.get("type", "dict") == "dict":
            data, aliases, to_reverse, caps_insensitive = (
                subdict.get("data", {}),
                subdict.get("aliases", {}),
                subdict.get("reverse", False),
                subdict.get("caps_insensitive", False),
            )
            if len(data) > 0:
                sub_length = subdict.get("sub_length", len(max(data, key=len)))
            elif len(aliases) > 0:
                sub_length = subdict.get("sub_length", len(max(aliases, key=len)))
            else:
                sub_length = 1

            # Decompose and recompose everything in the text
            text = unicodedata.normalize("NFC", unicodedata.normalize("NFD", text))
            if subdict.get("decomposed"):
                text = unicodedata.normalize("NFD", text)

            index = 0
            while index <= len(text) - sub_length:

                if to_reverse:
                    sub_string = text[
                        len(text) - index - sub_length : len(text) - index
                    ]
                else:
                    sub_string = text[index : index + sub_length]
                key = sub_string

                if caps_insensitive:
                    key = key.lower()

                if key in data or key in aliases:
                    input_text = text
                    replace_from = sub_string

                    replace_to = data.get(key, aliases.get(key))

                    if to_reverse:
                        input_text = input_text[::-1]
                        replace_from = replace_from[::-1]
                        replace_to = replace_to[::-1]

                    text = input_text.replace(replace_from, replace_to, 1)

                    if to_reverse:
                        text = text[::-1]
                index += 1
        elif subdict.get("type", "dict") == "regex":
            params = subdict.get("params", None)
            if params is not None:
                working_text = unicodedata.normalize("NFC", text)

                if subdict.get("decomposed"):
                    working_text = unicodedata.normalize("NFD", working_text)
                if subdict.get("repeat", False):
                    while re.search(params["pattern"], working_text) is not None:
                        working_text = re.sub(string=working_text, **params)
                else:
                    working_text = re.sub(string=working_text, **params)
                text = working_text
        else:
            print('Unknown subdict type "' + str(subdict.get("type", "")) + '"')
    return unicodedata.normalize("NFC", text)
