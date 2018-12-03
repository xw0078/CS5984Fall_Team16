# ETD Chapter Summarization  
 
## Abstract

Team 16 in the fall 2018 course "CS 4984/5984 Big Data Text Summarization," in partnership with the University Libraries and the Digital Library Research Laboratory, prepared a corpus of electronic theses and dissertations (ETDs) for students to study natural language processing with the power of state-of-the-art deep learning technology. The ETD corpus is made up of 13,071 doctoral dissertations and 17,890 master theses downloaded from the University Libraries’ VTechWorks system. This particular study is designed to explore big data summarization for ETDs, which is a relatively under-explored area. The result of the project will help to address the difficulty of information extraction from ETD documents, the potential of transfer learning on automatic summarization of ETD chapters, and the quality of state-of-the-art deep learning summarization technologies when applied to the ETD corpus.

The goal of this project is to generate chapter level abstractive summaries for an ETD collection through deep learning. Major challenges of the project include accurately extracting well-formatted chapter text from PDF files, and the lack of labeled data for supervised deep learning models. For PDF processing, we compare two state of the art scholarly PDF data extraction tools, Grobid and Science-Parse, which generate structured documents from which we can further extract metadata and chapter level text. For the second challenge, we perform transfer learning by training supervised learning models on a labeled dataset of Wikipedia articles related to the ETD collection. Our experimental models include Sequence-to-Sequence and Pointer Generator summarization models. Besides supervised models, we also experiment with an unsupervised reinforcement model, Fast Abstractive Summarization-RL.

The general pipeline for our experiments consists of the following steps: PDF data processing and chapter extraction, collecting a training data set of Wikipedia articles, manually creating human generated gold standard summaries for testing and validation, building deep learning models for chapter summarization, evaluating and tuning the models based on results, and then iteratively refining the whole process.


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
 
### Where to Get Data

#### VTechWorks ETD collection

The majority of the ETDs housed in VTechWorks, the Virginia Tech
institutional repository maintained by the University Libraries, are
open access and can be viewed and downloaded free of charge.

  - ETDs: Virginia Tech Electronic Theses and Dissertations:  
    <http://hdl.handle.net/10919/5534>

  - Masters Theses:  
    <http://hdl.handle.net/10919/9291>

  - Doctoral Dissertations:  
    <http://hdl.handle.net/10919/11041>

#### Wikipedia Dump

Wikimedia foundation does regular Wikipedia Database backup dumps in
different format. In our experiment, we use the latest pages and
articles backup. Please find "enwiki-latest-pages-articles.xml.bz2" file
from the link to latest English Wiki database backups. The data is in
XML format and the schema can be found through Wikimedia dump XML
schema. Notice that the XML schema defines the complete structure for
all Wiki dumps, different version of backups may share a subset of the
whole schema.

Links to official resources:

  - Official Wikimedia Downloads Documentation:  
    <https://dumps.wikimedia.org/>

  - Latest English Wiki Database Backups:  
    <https://dumps.wikimedia.org/enwiki/latest/>

  - Wikimedia dump XML schema:  
    <https://www.mediawiki.org/xml/export-0.10.xsd>

##### Gensim Wiki Parser

We use Gensim scripts for extracting plain text out of a raw Wikipedia
dump. Use the following command to parse
"enwiki-latest-pages-articles.xml.bz2":

``` bash
    python -m gensim.scripts.segment_wiki -f enwiki-latest-pages-articles.xml.bz2 -o enwiki-latest.json.gz}
```

Command arguments:

  - `-h` show this help message and exit

  - `-f` path to Wiki dump (read-only).

  - `-o` path to output file (stdout if not specified). If ends in .gz
    or .bz2, the output file will be automatically compressed
    (recommended\!).

  - `-w` number of parallel workers for multi-core systems. Default: 7.

  - `-m` ignore articles with fewer characters than this (article
    stubs). Default: 200.

Official Documentation:  
<https://radimrehurek.com/gensim/scripts/segment_wiki.html>
 
#### CNN-Dailymail Dataset

CNN-Dailymail dataset is the original dataset used for our different
deep learning summarizing models.

Links to official resources:

  - Official Github:  
    <https://github.com/abisee/cnn-dailymail>

On the Github page, you will learn how to download and process the
original original CNN-Dailymail data. You will also learn how to use the
processed data directly.

In our experiments, we use the processed data provided by the official
Github page. Our code for processing Wikipedia data into binary format
also refers the code in this repository.

### Grobid

Links to official resources:

  - Official Github:  
    <https://github.com/kermitt2/grobid>

  - Official Documentation:  
    <https://grobid.readthedocs.io/en/latest/References/>

  - Release we use:  
    []()

  - Latest Release:  
    <https://github.com/kermitt2/grobid/releases/>

#### Installation and Usage

There are various of ways to use Grobid: run locally as an application;
run locally as a service; run locally through JAVA interface etc. Here,
we use the JAR file to run Grobid through JAVA interface. Please refer
official documentation for other usage.

  - Get the latest JAR release from “Latest Release” link

  - Clone the latest Github repo

  - Use following command to parse your PDF
    data:
    
    ``` bash
        java -Xmx4G -jar  /path/to/grobid-core-0.5.2-SNAPSHOT-onejar.jar -ignoreAssets -r -gH /path/to/github/grobid/grobid-home -dIn /input/directory/ -dOut /output/directory/ -exe processFullText
    ```

Command arguments explanation:

  - `-gH` path to grobid-home directory

  - `-dIn` path to the directory of input PDF files

  - `-dOut` path to the output directory (if omitted the current
    directory)

  - `-ignoreAssets` do not extract and save the PDF assets (bitmaps,
    vector graphics), by default the assets are extracted and saved

  - `-r` recursive processing of files in the sub-directories (by
    default not recursive)

For other details, please check following manual page:  
<https://grobid.readthedocs.io/en/latest/Grobid-batch/>

### ScienceParse

#### Installation and Usage

There are three different ways to get started with Science Parse. Each
has its own document:

  - Server: This contains the SP server. It’s useful for PDF parsing as
    a service. It’s also probably the easiest way to get going. 

  - CLI: This contains the command line interface to SP. That’s most
    useful for batch processing. 

  - Core: This contains SP as a library. It has all the extraction code,
    plus training and evaluation. Both server and CLI use this to do the
    actual work. 

Alternatively, you can run the docker image:

``` bash
    docker run -p 8080:8080 --rm allenai/scienceparse:2.0.1
``` 
 
We used the ‘cli’ version of science parse. Following are the steps to
 get it running:
 
   - Download SBT
     
     ``` bash
         wget https://piccolo.link/sbt-1.2.4.zip
     ```
 
   - Unzip it
     
     ``` bash
         unzip sbt-1.2.4.zip
     ```
 
   - Setup the path:
     
     ``` bash
         export PATH=$PATH:~/sbt/bin
         
     ```
 
   - In Cascades, load the JDK module:
     
     ``` bash
         module load jdk/1.8.0u172
     ```
 
   - Clone the Science Parse github repository
     
     ``` bash
         git clone https://github.com/allenai/science-parse.git
     ```
 
   - Change the directory to the cloned repository
     
     ``` bash
         cd science-parse
     ```
 
   - Start the build of the fat jar using SBT:
     
     ``` bash
         sbt cli/assembly
     ```
 
   - After the build is complete, change the directory to the built jar
     file
     
     ``` bash
         cd cli/target/scala-2.11
     ```
 
   - Create a test PDF file to download the pre-trained models:
     
     ``` bash
         touch test.pdf
     ```
 
   - Trigger the parser for the first time using this test pdf file. It
     is ideal to get 6 GB of memory to load the pre-trained
     models:
     
     ``` bash
         java -Xmx6g -jar science-parse-cli-assembly-2.0.2-SNAPSHOT.jar test.pdf || true
     ```
 
   - Removing the temporary
     
     ``` bash
         rm test.pdf
     ```
 
   - Setup complete.
 
Use the following command to parse a single PDF
file:

``` bash
java -Xmx6g -jar /path/to/science-parse-cli-assembly-2.0.2-SNAPSHOT.jar input.pdf
```

Use the following command to parse multiple PDF
files:

``` bash
java -Xmx6g -jar /path/to/scala-2.11/science-parse-cli-assembly-2.0.2-SNAPSHOT.jar <path_to_the_folder_with_PDFs> -o <output_directory_path>
```

Use the following command to know more
options:

``` bash
java -Xmx6g -jar /path/to/scala-2.11/science-parse-cli-assembly-2.0.2-SNAPSHOT.jar --help
```

### Pointer-Summarizer

Point-summarizer is the PyTorch implementation of pointer-generator.  
Links to official resources:

  - Official Github:  
    <https://github.com/atulkum/pointer_summarizer>

#### Installation and Usage

1.  Clone the code from offical Github

2.  Set up environment for the program  
    Option 1: Set up following environment in your preferred way:
    
      - Python 2.7
    
      - PyTorch 3.0
    
      - Tenserflow 1.10
    
    Option 2: Create environment from our provided Conda YML file
    \[1\]  

3.  Find `config.py` file in `data_util` directory

4.  Configure parameters in `config.py`  
    `train_data_path`: training data path  
    `eval_data_path`: evaluation data path  
    `decode_data_path`: decode data path  
    `vocab_path`: vocabulary file path  
    `log_root`: output and log path

5.  Run the program through following scripts:  
    `start_train.sh`: run training  
    `start_eval.sh`: run evaluation, provide model path as argument  
    `start_decode.sh`: run decoding, provide model path as argument

Note:

  - For "`config.py not found`" error, add following code to according
    file:
    
    ``` python
        import sys
        sys.path.append('/path/to/pointer-summarizer')
    ```

<!-- end list -->

1.  <https://github.com/xw0078/CS5984Fall_Team16/tree/master/conda_yml> 

### Seq2Seq Model

Links to official resources:

  - Official Github:  
    <https://github.com/zwc12/Summarization>

  - Official Documentation:  
    <https://github.com/zwc12/Summarization/blob/master/README.md>

This model implements a simple sequence-to-sequence model with an
Attentional Recurrent Neural Network (RNN) encoder-decoder. 

#### Installation

This model can be used by cloning the latest code from the GitHub
repository mentioned above. Once the code has been cloned, the model
needs to be trained and then testing can be done by making use of the
trained model. 
 
### Fast Abstractive Summarization-RL

The Github link\[1\] to the project provides a detailed information
about the setup.

#### Prerequisites

1.  Create a conda environment and install the following dependencies:
    
      - Gensim
    
      - tensorboardX
    
      - Cytoolz
    
      - Pyrouge

2.  If you are working on Cascades, install the PyTorch Linux binaries
    compiled with CUDA 9.0\[2\]

3.  Clone the project from Github

#### Execution

1.  You can directly decode the pretrained model available in the
    repository or preprocess the CNN/Dailymail dataset by following the
    steps outlined\[3\]

2.  To train your model on the Wikipedia corpus, preprocess the dataset
    by running our code\[4\]

3.  Train a word2vec word embedding by running the following script:
    
    ``` python
        python train_word2vec.py --dim=300 --path=[word2vecPath]
    ```
    
    where dim parameter denotes the dimensionality (default value is
    128) and path denotes the path to save the word2vec model.

4.  Make the pseudo-labels by running the command:
    
    ``` python
        python make_extraction_labels.py
    ```
    
    This will create labels in the training and validation dataset and
    add the arrays *score* and *extracted* to them.

5.  Train the *abstractor* and *extractor* using ML
    objectives:
    
    ``` python
        python train_abstractor.py --path=[path/toSave/abstractor/model] --w2v=[path/to/word2vec.bin]
    ```

6.  Train the RL
    model
    
    ``` python
         python train_full_rl.py --path=[path/to/save/model] --abs_dir=[path/to/abstractor/model] --ext_dir=[path/to/extractor/model]
    ```

7.  Decode the model by
    running:
    
    ``` python
         python decode_full_model.py --path=[path/to/save/decoded/files] --model_dir=[path/to/pretrainedRL] --beam= 5 --test
    ```

<!-- end list -->

1.  <https://github.com/ChenRocks/fast_abs_rl>

2.  <https://pytorch.org/get-started/previous-versions/##pytorch-linux-binaries-compiled-with-cuda-90>

3.  [
    https://github.com/ChenRocks/cnn-dailymail](%20https://github.com/ChenRocks/cnn-dailymail)

4.  <https://github.com/namanahuja/CS5984Fall_Team16/tree/master/FastRL_PreProcessWikiData>
 
 
## Credits
 
Naman Ahuja ([@namanahuja](https://github.com/namanahuja))  
Ritesh Bansal ([@Riteshbansal](https://github.com/Riteshbansal))  
Bill Ingram ([@waingram](https://github.com/waingram))  
Palakh Jude ([@palakhjude](https://github.com/palakhjude))  
Sampanna Kahu ([@sampannakahu](https://github.com/sampannakahu))  
Xinyue Wang ([@xw0078](https://github.com/xw0078))  
