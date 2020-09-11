Get the paper source and set up the software
============================================

Make a directory somewhere to work in and navigate there::

   $ mkdir ski-paper
   $ cd ski-paper

Clone the paper and the skijumpdesign repositories::

   $ git clone git@gitlab.com:mechmotum/ski-jump-analysis-paper.git
   $ git clone git@gitlab.com:moorepants/skijumpdesign.git

Create a conda environment for this project::

   $ conda env create -f ski-jump-analysis-paper/environment.yml

Activate the environment::

   $ conda activate ski-analysis-paper

Install the development version of skijumpdesign::

   (ski-analysis-paper)$ cd skijumpdesign
   (ski-analysis-paper)$ pip install --no-dependencies -e .
   (ski-analysis-paper)$ cd -

Build the paper
===============

Navigate into the paper directory::

   (ski-analysis-paper)$ cd ski-jump-analysis-paper

Run the Python script to generate the figures::

   (ski-analysis-paper)$ python src/case_study_figures.py

Build the paper::

   (ski-analysis-paper)$ make

References
==========

This Zotero collection is being used to generated the bib file:

https://www.zotero.org/groups/966974/mechmotum/collections/D3MHJZ2G

The Better BibTex Zotero plugin is used to generate the bib file and the
citation keys using [Auth][Year]:

https://github.com/retorquere/zotero-better-bibtex
