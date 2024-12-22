def single_root_words(root_word, *other_words):
    same_words = []
    some_words = []
    for word in other_words:
        some_words.append(word)
        if root_word.lower() in (item.lower() for item in some_words):
            same_words.append(word)

    return same_words

print(single_root_words('classic', 'rock', 'pop', 'folk', 'classic', 'Classical', 'ClassicaL'))