#!/usr/bin/env python
# -*- coding: utf-8 -*-

import yaml
import re
import os,sys

os.chdir(os.path.dirname(sys.argv[0]))

def pronunciate(word):

    if len(word.split()) > 1:
        return " ".join( map(pronunciate, word.split()))

    vocalic_raw = r"a|e|o|1|y|\\s\{r\}|\\s{\l\}|\\s\{m}\}|\\s\{n\}|W|i"
    vocalic = r"(" + vocalic_raw + r")"
    vocalic_not = r"(?!" + vocalic_raw + r")"

    groupI = r"(m|p|b|t|t:|d|d:|f|n|t)"
    groupII = r"(k|g|r|s|S|\b|^)"
    groupIII = r"(N)"

    subs = [
            ("y","1"),                  # base ytta
            ("ng","N"),                 # ng
            ("1([rmn])"+vocalic_not,r"\s{\1}"),     # syllabisation
            ("sh","S"),                 # sh
            ("tt","t:"),                # gem t
            ("dd","d:"),                # gem d
            ("dh","D"),                 # dh
            ("N"+vocalic,r"N\~{\1}"),    # nasalization
            ("l([^ae1yo])", r"\s{l}\1"), # ??????
            (r"l\b",r"\s{l}"),          # final l syllabic
            (r"D\b",r"D:"),              # final dh geminated
            (vocalic + "D" + vocalic, r"\1D:\2"), # medial dh geminated

            # ytta robordam
            (groupI +   "1" + groupI, r"\1i\2"),
            (groupII +  "1" + groupI, r"\1ij\2"),
            (groupIII + "1" + groupI, r"\1Wj\2"),
            (groupI + "1" + groupII, r"\1j1\2"),
            (groupIII + "1" + groupIII, r"\1W\2"),
            (groupI + "1" + groupIII, r"\1jW\2"),
            (groupII + "1" + groupIII, r"\1jW\2"),
            (groupIII + "1" + groupIII, r"\1W\2"),

            # flap
            (vocalic + "r" + vocalic, r"\1R\2"),

            # palatalization

            (r"k(e|i|j)",r"c\1"),
            (r"n(e|i|j)",r"ɲ\1")

            ]


    subs_final = [
            ("ɲ",r"\\textltailn ")
            ]

    word = word.lower()

    for key,value in subs:
        word = re.sub(key,value, word)


    syllables = [match for match in re.finditer(r"(a|e|o|\\s\{r\}|\\s\{l\}|1)",word)]

    if len(syllables) > 1:
        last = syllables[-1]
        penultimate = syllables[-2]

        stress = -2

        if last.group(0) == "a":
            stress = -1

        if r":" in word[penultimate.start() : last.start()]:
            stress = -2

        if r":" in word[last.start():]:
            stress = -1

        if syllables[stress].group(0) == "e":
            word = list(word)
            word[syllables[stress].start()] = "E"
            word = "".join(word)
        if syllables[stress].group(0) == "o":
            word = list(word)
            word[syllables[stress].start()] = "O"
            word = "".join(word)

        word = word[:syllables[stress].start()]+"\""+word[syllables[stress].start():]

    else:
        word = re.sub("e","E",word)
        word = re.sub("o","O",word)

    for key,value in subs_final:
        word = re.sub(key,value,word)


    return word


data = yaml.load(open("lexicon.yml"))


alphabetical = sorted(data)

print "Total number of lemmas: %d"%len(alphabetical)


# fix phrase refs

for phrase in alphabetical:
    if "refs" in data[phrase]:
        for word in data[phrase]["refs"]:
            if word in data:
                try:
                    data[word]["phrases"].append(phrase)
                except KeyError:
                    data[word]["phrases"] = [phrase]



#print data

tex = ""

for word in alphabetical:
    tex += r"\textbf{"+word+r"}"
    try:
        translation = data[word]["tr"]
    except KeyError:
        translation = "NO TRANSLATION"

    try:
        part_of_speech = data[word]["part"]
    except KeyError:
        part_of_speech = None


    tex += r" \fliv{"+word+r"}"

    tex += r" \apa{"+pronunciate(word)+r"}"


    tex += r" "

    if part_of_speech:
        tex += r"\emph{" + part_of_speech +r"}"

    tex += r" \textperiodcentered "

    if not isinstance(translation, basestring):
        translation_text = ""
        for i in range(len(translation)):
            translation_text += "%d. "%(i+1) + r""+translation[i]+ r" "
    else:
        translation_text = r""+translation+r""

    tex += translation_text 


    if "note" in  data[word]:
        tex += r" | " + data[word]["note"]


    if "lit" in data[word]:
        tex += r" (lit. \emph{"+data[word]["lit"] + r"})"

    if "phrases" in data[word]:
        tex += r", see also \textbf{" + r"}, \textbf{".join(data[word]["phrases"])+r"}"


    tex += r"\\"

#    tex += r"\\ \vspace{7pt}"

outfile = open("texicon.tex",'w')
outfile.write(tex)
