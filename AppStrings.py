default_settings = {"max timer copy": 30000, "max password size": 20}
info_labels = {"info_symb": "ciao", "info_word": "aòlalala"}

def set_language(language):
    if language == 0:
        cboxes_labels = {"lowchar": "Lowercases [a-z]", "numchar": "Numbers [0-9]", "upchars": "Uppercases [A-Z]",
                         "symbchars": "ASCII Symbols"}
    elif language == 1:
        cboxes_labels = {"lowchar": "Minuscole [a-z]", "numchar": "Numeri [0-9]", "upchars": "Maiuscole [A-Z]",
                         "symbchars": "Simboli ASCII"}
    return cboxes_labels