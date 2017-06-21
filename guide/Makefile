LATEXMKOPT=-xelatex
CONTINUOUS=-pvc

MAIN=flavus
SOURCES=$(MAIN).tex Makefile ../font/flavangeometric.otf

all: $(MAIN).pdf

.refresh:
	touch .refresh

$(MAIN).pdf: $(MAIN).tex .refresh $(SOURCES)
	latexmk $(LATEXMKOPT) $(CONTINUOUS)

clean:
	latexmk -C $(MAIN) 
	rm -f $(MAIN).pdfsync 
	rm -rf *~ *.tmp 
	rm -f *.bbl *.blg *.aux *.end *.fls *.log *.out *.fdb_latexmk

once:
	latexmk $(LATEXMKOPT) $(MAIN)

.PHONY: clean force once all
