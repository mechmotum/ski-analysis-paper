FIRST_DIFF_TAG = before-tech-note

pdf: main.pdf sup.pdf
main.pdf: main.tex references.bib figures/salvini-v-snoqualmie.pdf figures/vine-v-bear-valley.pdf
	pdflatex -shell-escape main.tex
	bibtex main.aux
	pdflatex -shell-escape main.tex
	pdflatex -shell-escape main.tex
sup.pdf: sup.tex references.bib
	pdflatex -shell-escape sup.tex
	bibtex sup.aux
	pdflatex -shell-escape sup.tex
	pdflatex -shell-escape sup.tex
trackchanges:
	git checkout $(FIRST_DIFF_TAG)
	cp main.tex $(FIRST_DIFF_TAG).tex
	git checkout master
	latexdiff $(FIRST_DIFF_TAG).tex main.tex > diff-master_$(FIRST_DIFF_TAG).tex
	rm $(FIRST_DIFF_TAG).tex
	pdflatex -shell-escape -interaction nonstopmode -halt-on-error -file-line-error diff-master_$(FIRST_DIFF_TAG).tex
	bibtex diff-master_$(FIRST_DIFF_TAG).aux
	pdflatex -shell-escape -interaction nonstopmode -halt-on-error -file-line-error diff-master_$(FIRST_DIFF_TAG).tex
	pdflatex -shell-escape -interaction nonstopmode -halt-on-error -file-line-error diff-master_$(FIRST_DIFF_TAG).tex
figures/salvini-v-snoqualmie.pdf figures/vine-v-bear-valley.pdf: data/california-2002-surface.csv data/washington-2004-surface.csv src/case_study_figures.py
	python src/case_study_figures.py
clean:
	(rm -rf *.ps *.log *.dvi *.aux *.*% *.lof *.lop *.lot *.toc *.idx *.ilg *.ind *.bbl *.blg *.cpt *.out)
