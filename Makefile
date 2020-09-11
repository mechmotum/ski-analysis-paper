pdf:
	pdflatex -shell-escape main.tex
	bibtex main.aux
	pdflatex -shell-escape main.tex
	pdflatex -shell-escape main.tex
figures: data/california-2002-surface.csv data/washington-2004-surface.csv src/case_study_figures.py
	python src/case_study_figures.py
clean:
	(rm -rf *.ps *.log *.dvi *.aux *.*% *.lof *.lop *.lot *.toc *.idx *.ilg *.ind *.bbl *.blg *.cpt *.out)
