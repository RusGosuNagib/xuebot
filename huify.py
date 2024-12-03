import re

# Гласные и их замены
vowel_replacements = {
    'а': 'я',
    'о': 'е',
    'у': 'ю',
    'ы': 'и',
    'е': 'е',
    'я': 'я',
    'ю': 'ю',
    'и': 'и',
    'э': 'е',
}

prefix_to_skip_re = re.compile(r"^[бвгджзйклмнпрстфхцчшщьъ]+")
only_dashes_re = re.compile(r"^-*$")
huified_prefix = "ху"

def huify_word(word):
    word = word.lower()
    if word.startswith("ху"):  # Уже хуефицированное
        return word
    if only_dashes_re.match(word):  # Только тире
        return word
    postfix = prefix_to_skip_re.sub("", word)
    if len(postfix) < 2:  # Если слишком короткое
        return word

    # Проверяем первую гласную
    for i, char in enumerate(postfix):
        if char in vowel_replacements:
            return "ху" + vowel_replacements[char] + postfix[i + 1:]
    return "ху" + word

def huify(text):
    words = text.split()
    result = []
    for word in words:
        result.append(huify_word(word))
    return " ".join(result)