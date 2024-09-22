def camel_split(text):
    """
    Split camel format into underscore format, i.e.:
    MyFunction => my_function
    """

    words = [text[0].lower()]
    n_words = 0

    for i, char in enumerate(text[1:]):
        if char.isupper():
            words.append("")
            n_words += 1

        words[n_words] += char.lower()

    return "_".join(words)