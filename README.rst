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

Updating the References
=======================

This Zotero collection is being used to generated the bib file:

https://www.zotero.org/groups/966974/mechmotum/collections/D3MHJZ2G

The Better BibTex Zotero plugin is used to generate the bib file and the
citation keys using [Auth][Year]:

https://github.com/retorquere/zotero-better-bibtex

Setup
-----

1. Install Zotero.
2. Install the Zotero connector for your web browser:
   https://www.zotero.org/download/connectors
3. Open Zotero (application on your computer).
4. Setup syncing in the Zotero preferences by providing your zotero username
   and password (create an account if needed and inform Jason of your
   username).
5. Install the zotero-better-bibtex plugin by following these directions:
   https://retorque.re/zotero-better-bibtex/installation/
6. Restart Zotero
7. In the Zotero menu open the Edit>Preferences and click the "Better BibTex"
   button. Change the citation key format to ``[auth][year]`` and close the
   preferences window.
8. Select the "Ski Jump EFH Analysis" folder.
9. Highlight (select) all the items in the folder and right click. Select the
   Better BibTeX > Refresh BibTeX key to set all the citekeys to the new
   format.

Adding new references
---------------------

1. Open Zotero and select the "Ski Jump EFH Analysis" folder in the left
   column.
2. Open your web browser and navigate to a journal article web page.
3. Press the "Save to Zotero" button in the upper right (just to right of url
   bar). The article (and pdf) should show up in Zotero.

See these instructions if more info is needed:
https://www.zotero.org/support/adding_items_to_zotero

Updating the .bib file on Overleaf
----------------------------------

1. In Zotero, right click the "Ski Jump EFH Analysis" folder and select "Export
   collection".
2. Set the Format to "Better BibTeX" and press "OK".
3. Save the ``.bib`` file somewhere as ``references.bib``.
4. In Overleaf, remove the ``references.bib`` file and upload your new one.
   Optionally, you can open the file on your computer, copy all the text and
   paste over all the text in the bib file on Overleaf.

Build the paper
===============

Navigate into the paper directory::

   (ski-analysis-paper)$ cd ski-jump-analysis-paper

Run the Python script to generate the figures::

   (ski-analysis-paper)$ python src/case_study_figures.py

Build the paper::

   (ski-analysis-paper)$ make
