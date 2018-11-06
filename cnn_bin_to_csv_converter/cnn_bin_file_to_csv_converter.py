import glob, struct, random, csv
from tensorflow.core.example import example_pb2

# <s> and </s> are used in the data files to segment the abstracts into sentences. They don't receive vocab ids.
SENTENCE_START = '<s>'
SENTENCE_END = '</s>'

PAD_TOKEN = '[PAD]'  # This has a vocab id, which is used to pad the encoder input, decoder input and target sequence
UNKNOWN_TOKEN = '[UNK]'  # This has a vocab id, which is used to represent out-of-vocabulary words
START_DECODING = '[START]'  # This has a vocab id, which is used at the start of every decoder input sequence
STOP_DECODING = '[STOP]'  # This has a vocab id, which is used at the end of untruncated target sequences


# Note: none of <s>, </s>, [PAD], [UNK], [START], [STOP] should appear in the vocab file.


def example_generator(data_path, single_pass):
    """Generates tf.Examples from data files.

      Binary data format: <length><blob>. <length> represents the byte size
      of <blob>. <blob> is serialized tf.Example proto. The tf.Example contains
      the tokenized article text and summary.

    Args:
      data_path:
        Path to tf.Example data files. Can include wildcards, e.g. if you have several training data chunk files train_001.bin, train_002.bin, etc, then pass data_path=train_* to access them all.
      single_pass:
        Boolean. If True, go through the dataset exactly once, generating examples in the order they appear, then return. Otherwise, generate random examples indefinitely.

    Yields:
      Deserialized tf.Example.
    """
    while True:
        filelist = glob.glob(data_path)  # get the list of datafiles
        assert filelist, ('Error: Empty filelist at %s' % data_path)  # check filelist isn't empty
        if single_pass:
            filelist = sorted(filelist)
        else:
            random.shuffle(filelist)
        for f in filelist:
            reader = open(f, 'rb')
            while True:
                len_bytes = reader.read(8)
                if not len_bytes: break  # finished reading this file
                str_len = struct.unpack('q', len_bytes)[0]
                example_str = struct.unpack('%ds' % str_len, reader.read(str_len))[0]
                yield example_pb2.Example.FromString(example_str)
        if single_pass:
            print "example_generator completed reading all datafiles. No more data."
            break


def abstract2sents(abstract):
    """Splits abstract text from datafile into list of sentences.

    Args:
      abstract: string containing <s> and </s> tags for starts and ends of sentences

    Returns:
      sents: List of sentence strings (no tags)"""
    cur = 0
    sents = []
    while True:
        try:
            start_p = abstract.index(SENTENCE_START, cur)
            end_p = abstract.index(SENTENCE_END, start_p + 1)
            cur = end_p + len(SENTENCE_END)
            sents.append(abstract[start_p + len(SENTENCE_START):end_p])
        except ValueError as e:  # no more sentences
            return sents


def text_generator(example_generator):
    """Generates article and abstract text from tf.Example.

    Args:
      example_generator: a generator of tf.Examples from file. See data.example_generator"""
    while True:
        e = example_generator.next()  # e is a tf.Example
        try:
            article_text = e.features.feature['article'].bytes_list.value[
                0]  # the article text was saved under the key 'article' in the data files
            abstract_text = e.features.feature['abstract'].bytes_list.value[
                0]  # the abstract text was saved under the key 'abstract' in the data files
        except ValueError:
            # tf.logging.error('Failed to get article or abstract from example')
            continue
        else:
            yield (article_text, abstract_text)


def read_bin_files(input_bin_path, output_csv_path,single_pass):
    """Reads data from file and processes into Examples which are then placed into the example queue."""

    input_gen = text_generator(example_generator(input_bin_path, single_pass))

    with open(output_csv_path, mode='w') as output_file:
        output_writer = csv.writer(output_file, delimiter=',', quotechar='"', quoting=csv.QUOTE_MINIMAL)
        while True:
            try:
                (article,
                 abstract) = input_gen.next()  # read the next example from file. article and abstract are both strings.
            except StopIteration:  # if there are no more examples:
                # tf.logging.info("The example generator for this example queue filling thread has exhausted data.")
                if single_pass:
                    # tf.logging.info("single_pass mode is on, so we've finished reading dataset. This thread is stopping.")
                    # self._finished_reading = True
                    break
                else:
                    raise Exception("single_pass mode is off but the example generator is out of data; error.")

            # Use the <s> and </s> tags in abstract to get a list of sentences.
            abstract_sentences = [sent.strip() for sent in abstract2sents(abstract)]
            output_writer.writerow(['. '.join(abstract_sentences), article])


if __name__ == "__main__":
    input_bin_path = '/home/sampanna/Study/BDTS/modified-keras-text-summarization/files/cnn/finished_files/chunked/train_*.bin'
    output_csv_path = 'cnn_summary_dataset.csv'
    read_bin_files(input_bin_path, output_csv_path,True)
