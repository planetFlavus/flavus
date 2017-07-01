
# dictionary

DICTIONARY=dictionary/texicon.tex
YMLDICT=dictionary/lexicon.yml

# latex guide

LATEXMKOPT=-xelatex
CONTINUOUS=-pvc

MAIN=guide/flavus
SOURCES=$(MAIN).tex Makefile font/flavangeometric.otf $(DICTIONARY)






# targets

all: $(MAIN).pdf $(DICTIONARY)

$(DICTIONARY): $(YMLDICT) dictionary/dictionary.py
	python dictionary/dictionary.py

.refresh:
	touch .refresh

$(MAIN).pdf: $(MAIN).tex .refresh $(SOURCES)
	cd guide; latexmk $(LATEXMKOPT) $(CONTINUOUS) flavus

clean:
	cd guide; latexmk -C flavus
	cd guide; rm -f $(MAIN).pdfsync 
	cd guide; rm -rf *~ *.tmp 
	cd guide; rm -f *.bbl *.blg *.aux *.end *.fls *.log *.out *.fdb_latexmk
	rm -f dictionary/texicon.tex

once:
	cd guide; latexmk $(LATEXMKOPT) flavus

.PHONY: clean force once all

.PRECIOUS: $(MAIN).pdf
