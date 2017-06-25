import yaml
import re
import os,sys

os.chdir(os.path.dirname(sys.argv[0]))

def pronunciate(word):
    subs = [
            ("y","1"),
            ("1r",r"\s{r}"),
            ("ng","N"),
            ("sh","S"),
            ("tt","t:"),
            ("dd","d:"),
            ("dh","D"),
            ("N([ae1yo])",r"N\~\1"),
            ("l([^ae1yo])", r"\s{l}\1"),
            (r"l\b",r"\s{l}"),
            (r"D\b",r"D:")
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

    return word


data = yaml.load(open("lexicon.yml"))

#print data

alphabetical = sorted(data)

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
    tex += r"\\"

#    tex += r"\\ \vspace{7pt}"

outfile = open("texicon.tex",'w')
outfile.write(tex)
