# ETD Chapter Summarization  
 
TODO: **add abstract**

## Contents

This repository is made up of several Python scripts and Jupyter notebooks organized in separate
directories.

  - training data scripts – Scripts for managing and manipulating the
    training corpus
    
      - `clean_wiki_text.py` – Take out the wiki markup and only leave
        clean sentences.
    
      - `doc2vec_similarity.ipynb` – Use doc2vec to find similar
        wikipedia articles from ETD chapters
    
      - `doc2vec_train_wiki_model.py` – Train doc2vec on Wikipedia dump
        and save models
    
      - `sentence_tokenization.py` – Extract sentences from
        Grobid-generated TEI XML
    
      - `wiki_summary_segmentation.py` – Extract Wikipedia article
        summary given the page\_name by hitting the Wikipedia API.

  - pipeline – Training data pipeline: scripts for extracting chapters
    from TEI, comparing and gathering similar Wikipedia articles,
    cleaning article text, and generating `bin` files for training
    
      - `grobid_paragraph_extraction.py` – Parse and transform GROBID
        TEI into JSON containing title, chapters, and paragraphs
    
      - `Wiki_ETD_Similarity_Extraction.ipynb` – Use doc2vec models to
        find Wikipedia articles similar to our corpus of ETDs
    
      - `WikiJson_to_PGM_Bin.ipynb` – Convert Wikipedia article JSON
        into PGM bin files

  - science parse
    
      - `setup_science_parse.sh` – Single script to completely set-up
        science-parse on remote server (with dependencies)

  - CNN bin to CSV – convert bin files to human-readable CSV
    
      - `cnn_bin_file_to_csv_converter.py` – convert the CNN dailymail
        dataset bin files into a simple CSV file which can also be fed
        to other networks

## Usage
 
TODO: Write some instructions for how to use the software
 
## Credits
 
Naman Ahuja ([@namanahuja](https://github.com/namanahuja))  
Ritesh Bansal ([@Riteshbansal](https://github.com/Riteshbansal))  
Bill Ingram ([@waingram](https://github.com/waingram))  
Palakh Jude ([@palakhjude](https://github.com/palakhjude))  
Sampanna Kahu ([@sampannakahu](https://github.com/sampannakahu))  
Xinyue Wang ([@xw0078](https://github.com/xw0078))  