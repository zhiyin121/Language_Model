# text = "Mr. Smith's parents couldn't communicate, so they divorced? \
#        Mr. Smith's parents couldn't communicate, so they divorced."
# text = "'Tis very like: he'abc hath the failing sickness."


def tokenize(text):
    from nltk.tokenize import RegexpTokenizer
    tokenizer = RegexpTokenizer(r'\w+|\$[\d\.]+|\S+')
    tokens = tokenizer.tokenize(text)
    return tokens


def detokenize(tokens):
    import re
    while None in tokens:
        tokens.remove(None)

    tokens = ' '.join(tokens)

    p = re.compile(r'(\sn\'t)|(\s\'s)')
    for match in p.finditer(tokens):
        a = match.group()
        b = a[1:]
        tokens = tokens.replace(a, b)

    # tokens = tokens.capitalize()

    # p = re.compile('(\s\.\s)|(\s\?\s)|(\s\!\s)|(\s\,\s)|(\s\"\s)')
    # for match in p.finditer(tokens):
        # s = match.start()
        # a = tokens[s+3:]
        # b = tokens[s+3:].capitalize()
        # tokens = tokens.replace(a, b)
    tokens = tokens.replace(' ?', '?')
    tokens = tokens.replace(' !', '!')
    tokens = tokens.replace(' .', '.')
    tokens = tokens.replace(' ,', ',')
    tokens = tokens.replace(' "', '"')
    tokens = tokens.replace(" 'd", "'d")
    tokens = tokens.replace(" 'll", "'ll")
    tokens = tokens.replace(" 's", "'s")
    tokens = tokens.replace(' ;', ';')
    tokens = tokens.replace(' :', ':')

    return tokens

# print (tokenize(text))
# print (detokenize(tokenize(text)))
