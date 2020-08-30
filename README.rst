Build the paper
===============

::

   $ make

Generate figures
================

To generate the figures, create a conda environment for this project::

   $ conda env create -f /path/to/ski-jump-analysis-paper/environment.yml

Activate the enivronment::

   $ conda activate ski-analysis-paper

Install the development version of skijumpdesign (for now)::

   (ski-analysis-paper)$ git clone https://gitlab.com/moorepants/skijumpdesign.git
   (ski-analysis-paper)$ cd skijumpdesign
   (ski-analysis-paper)$ python setup.py develop

And run the Python script to generate the figures::

   (ski-analysis-paper)$ python /path/to/ski-jump-analysis-paper/src/case_study_figures.py

References
==========

This Zotero collection is being used to generated the bib file:

https://www.zotero.org/groups/966974/mechmotum/collections/D3MHJZ2G

The Better BibTex Zotero plugin is used to generate the bib file and the
citation keys using [Auth][Year]:

https://github.com/retorquere/zotero-better-bibtex
