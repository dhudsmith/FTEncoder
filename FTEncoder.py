import fasttext as ft
from typing import Callable
import pandas as pd

class FTEncoder(object):
    """
    Represents an embedding model wrapper based in the fastText learning models to ease workflow loops
    Meant for working on the Clemson Palmetto Cluster but should work anywhere.

    Methods:
        -fit
            -Fits a model to given data.  Supervised or unsupervised depending on whether target outputs are given
        -get_encoding
            -Get a single encoding from a trained model
        -get_all_encodings
            -Get all encodings from a trained model of an entire Series of text instances
        -save_model
            -Saves the underlying fastText model so it can be loaded later
        -load_model
            -Loads a saved fastText model into the underlying fastText model of the object instance

    """
    def __init__(self,
                 data_dir: str = './',
                 preprocessor: Callable[[str], str] = None,
                 training_file: str = None,
                 inspection_file: str = None,
                 model: str = None):
        self.save_dir = data_dir
        self.preprocessor = preprocessor
        self.training_file_name = "unsupervised_training_data_for_fasttext.txt" if not training_file else None
        self.inspection_file_name = "unsupervised_training_data_for_inspection.csv" if not inspection_file else None

        # if a model path is provided, then load it
        if model:
            self.model: ft.FastText = ft.load_model(model)
        else:
            self.model: ft.FastText = None

    def fit(self, text_series: pd.Series, **kwargs):
        """
        Fits the underlying fastText model to the given text input and optional target outputs
        
        Parameters:
            :param text_series: A pandas Series of text inputs to train an unsupervised model or supervised model
            :param kwargs: The keyword arguments to pass onto the fastText training method
        """

        # preprocess the text
        text_series_processed = self.preprocess_series(text_series)
        text_series_processed.name = 'preprocessed_text'

        # save for use by fasttext
        text_series_processed.to_csv(self.save_dir + self.training_file_name, index=False, header=False)

        # save for inspection
        pd.concat([text_series, text_series_processed], axis=1).\
            to_csv(self.save_dir + self.inspection_file_name, index=False)

        self.model = ft.train_unsupervised(self.save_dir + self.training_file_name, **kwargs)

    def preprocess_series(self, text_series: pd.Series) -> pd.Series:
        # if the user supplied a preprocessor then condition the text
        if self.preprocessor:
            def safe_preproc(txt):
                try:
                    assert type(txt) == str
                    return self.preprocessor(txt)
                except:
                    print("Input text was not of str type. Returning original input: %s." % str(txt))
                    return txt

            return text_series.apply(safe_preproc)
        # otherwise return the input text
        else:
            return text_series

    def get_encoding(self, text: str):
        """
        Generate encodings from a document string
        """
        # preprocess the text
        text = self.preprocessor(text)

        # get the encoding
        encoding = self.model.get_sentence_vector(text)

        return text, encoding

    def get_encodings_for_series(self, text_series: pd.Series):
        """
        Generate encodings for all document strings in a pandas series
        """
        all_encodings = pd.DataFrame(text_series.
                                     apply(lambda x: pd.Series(self.get_encoding(x))).
                                     values.
                                     tolist())

        # return preprocessed text as first column and encodings as all others
        preprcessed_text = all_encodings[0]
        preprcessed_text.name = 'preprocessed_text'
        encodings = pd.DataFrame(all_encodings[1].tolist())
        encodings.columns = ['v'+str(x).zfill(3) for x in range(len(encodings.columns))]

        return pd.concat([preprcessed_text, encodings], axis=1)

def training_and_using_model():
    # prepare the data
    df = pd.read_csv("TestData/all_tweets_filtered_final.csv", encoding='UTF-8')
    txt = df.text

    # create a preprocessor
    from Preproc import Preproc
    prep = Preproc()

    # create the fasttext encoder model
    enc = FTEncoder(preprocessor=prep.preprocess_text, data_dir='TestData/')

    # train the encoder
    enc.fit(txt)

    # save it for later
    enc.model.save_model('Models/test_model.bin')

    # get an encoding
    print(enc.get_encoding("The blue bat hit the red ball"))

    # get a series of encodings
    text_ser = pd.Series(["The steel ball struck the glass table and it shattered",
                          "The glass table was struck by the steel ball and it shattered",
                          "The glass table, struck by the steel ball, shattered."])
    print(enc.get_encodings_for_series(text_ser))

def loading_and_using_model():
    # prepare the data

    # create a preprocessor
    from Preproc import Preproc
    prep = Preproc()

    # create the fasttext encoder model
    enc = FTEncoder(preprocessor=prep.preprocess_text,
                    data_dir='TestData/',
                    model='Models/test_model.bin')

    # get an encoding
    print(enc.get_encoding("The blue bat hit the red ball"))

    # get a series of encodings as a datafrmae
    text_ser = pd.Series(["The steel ball struck the glass table and it shattered",
                          "The glass table was struck by the steel ball and it shattered",
                          "The glass table, struck by the steel ball, shattered."])
    print(enc.get_encodings_for_series(text_ser))


if __name__=="__main__":
    from line_profiler import LineProfiler
    from Preproc import Preproc

    # setup line profiling
    profiler = LineProfiler()
    profiler.add_function(Preproc.preprocess_text)
    test_func = profiler(loading_and_using_model)

    # call the test function and print profiling results
    test_func()
    profiler.print_stats()

