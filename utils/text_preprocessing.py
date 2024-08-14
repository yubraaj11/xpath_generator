def format_(text):
    words = text.split()

    if len(words) > 1:
        formatted_words = [words[0]] + list(word.capitalize() for word in words[1:])
    else:
        formatted_words = words

    # Join the words back together without spaces
    return ''.join(formatted_words)


def format_text(text):
    words = text.replace('-', "_")
    return words
