import numpy as np

consonants = [
        "k",
        "p",
        "b",
        "t",
        "d",
        "tt",
        "dd",
        "dh",
        "s",
        "sh",
        "f",
        "r",
        "g",
        "m",
        "n",
        "ng",
        "rd",
        "rt",
        "rb",
        "kt",
        "ttf",
        "ttl",
        "ttk",
        "ttng",
        "zg",
        "rk",
        "rg",
        "rm",
        "gm",
        "dhl",
        "sl",
        "shl",
        ]

vowels = ["a","y","e","o"]

for i in range(100):
    start_vowel = np.random.choice([0,1], p=[0.8,0.2])
    number_units = int(round(np.random.exponential(4)))
    
    number_units = max(2,number_units)

    word = ""

    for n in range(number_units):
        if n%2 == 0:
            if (n != 0) or (not start_vowel):
                consonant_index = len(consonants)
                while consonant_index >= len(consonants):
                    consonant_index = np.random.zipf(1.01)
                word += consonants[consonant_index]
        else:
            word += np.random.choice(vowels)

    print word
            
