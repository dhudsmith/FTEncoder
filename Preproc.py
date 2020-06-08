import re

class Preproc(object):
    def __init__(self,
                 is_lower: bool = True,
                 is_expand_contractions: bool = True,
                 is_remove_utf8: bool = True,
                 is_tokenize_hashtag: bool = True,
                 is_tokenize_mention: bool = True,
                 is_tokenize_misc: bool = True,
                 is_remove_slashes_and_brackets: bool = True,
                 is_pad_punct_ws: bool = True,
                 is_remove_punct: bool = True,
                 is_remove_stopwords: bool = True):
        self.is_lower = is_lower
        self.is_expand_contractions = is_expand_contractions
        self.is_remove_utf8 = is_remove_utf8
        self.is_tokenize_hashtag = is_tokenize_hashtag
        self.is_tokenize_mention = is_tokenize_mention
        self.is_tokenize_misc = is_tokenize_misc
        self.is_remove_slashes_and_brackets = is_remove_slashes_and_brackets
        self.is_pad_punct_ws = is_pad_punct_ws
        self.is_remove_punct = is_remove_punct
        self.is_remove_stopwords = is_remove_stopwords





    # Combined processing function
    def preprocess_text(self, txt):
        txt = (txt.lower() if self.is_lower else txt)
        txt = (Preproc.convert_contractions(txt) if self.is_expand_contractions else txt)
        txt = (Preproc.remove_utf8(txt) if self.is_remove_utf8 else txt)
        txt = (Preproc.tokenize_hashtags(txt) if self.is_tokenize_hashtag else txt)
        txt = (Preproc.tokenize_mentions(txt) if self.is_tokenize_mention else txt)
        txt = (Preproc.tokenize_misc(txt) if self.is_tokenize_misc else txt)
        txt = (Preproc.remove_slashes_and_brackets(txt) if self.is_remove_slashes_and_brackets else txt)
        txt = (Preproc.pad_punct_ws(txt) if self.is_pad_punct_ws else txt)
        txt = (Preproc.remove_punct(txt) if self.is_remove_punct else txt)
        txt = (Preproc.remove_stopwords(txt) if self.is_remove_stopwords else txt)

        return txt

    # precompile regex search strings
    re_hashtag = re.compile('[#]+[A-Za-z-_]+[A-Za-z0-9-_]')
    re_mention = re.compile('[@]+[A-Za-z0-9-_]+')
    re_percent = re.compile('(\d+(\.\d+)?%)')
    re_currency = re.compile('[\$]{1}[\d,]+\.?\d{0,2}')
    re_numbers = re.compile(r'\b\d+(?:,\d+)?\b')

    # contraction expansions
    contractions = {
        "ain't": "is not",
        "aren't": "are not",
        "can't": "cannot",
        "cant": "cannot",
        "can't've": "cannot have",
        "'cause": "because",
        "could've": "could have",
        "couldn't": "could not",
        "couldn't've": "could not have",
        "didn't": "did not",
        "doesn't": "does not",
        "don't": "do not",
        "hadn't": "had not",
        "hadn't've": "had not have",
        "hasn't": "has not",
        "haven't": "have not",
        "he'd": "he would",
        "he'd've": "he would have",
        "he'll": "he will",
        "he'll've": "he will have",
        "he's": "he is",
        "how'd": "how did",
        "how'd'y": "how do you",
        "how'll": "how will",
        "how's": "how is",
        "I'd": "I would",
        "I'd've": "I would have",
        "I'll": "I will",
        "I'll've": "I will have",
        "I'm": "I am",
        "I've": "I have",
        "isn't": "is not",
        "it'd": "it would",
        "it'd've": "it would have",
        "it'll": "it will",
        "it'll've": "it will have",
        "it's": "it is",
        "let's": "let us",
        "ma'am": "madam",
        "mayn't": "may not",
        "might've": "might have",
        "mightn't": "might not",
        "mightn't've": "might not have",
        "must've": "must have",
        "mustn't": "must not",
        "mustn't've": "must not have",
        "needn't": "need not",
        "needn't've": "need not have",
        "o'clock": "of the clock",
        "oughtn't": "ought not",
        "oughtn't've": "ought not have",
        "shan't": "shall not",
        "sha'n't": "shall not",
        "shan't've": "shall not have",
        "she'd": "she would",
        "she'd've": "she would have",
        "she'll": "she will",
        "she'll've": "she will have",
        "she's": "she is",
        "should've": "should have",
        "shouldn't": "should not",
        "shouldn't've": "should not have",
        "so've": "so have",
        "so's": "so is",
        "that'd": "that would",
        "that'd've": "that would have",
        "that's": "that is",
        "there'd": "there would",
        "there'd've": "there would have",
        "there's": "there is",
        "they'd": "they would",
        "they'd've": "they would have",
        "they'll": "tthey will",
        "they'll've": "they will have",
        "they're": "they are",
        "they've": "they have",
        "to've": "to have",
        "wasn't": "was not",
        "we'd": "we would",
        "we'd've": "we would have",
        "we'll": "we will",
        "we'll've": "we will have",
        "we're": "we are",
        "we've": "we have",
        "weren't": "were not",
        "what'll": "what will",
        "what'll've": "what will have",
        "what're": "what are",
        "what's": "what is",
        "what've": "what have",
        "when's": "when is",
        "when've": "when have",
        "where'd": "where did",
        "where's": "where is",
        "where've": "where have",
        "who'll": "who will",
        "who'll've": "who will have",
        "who's": "who is",
        "who've": "who have",
        "why's": "why is",
        "why've": "why have",
        "will've": "will have",
        "won't": "will not",
        "won't've": "will not have",
        "would've": "would have",
        "wouldn't": "would not",
        "wouldn't've": "would not have",
        "y'all": "you all",
        "y'all'd": "you all would",
        "y'all'd've": "you all would have",
        "y'all're": "you all are",
        "y'all've": "you all have",
        "yall": "you all",
        "yall'd": "you all would",
        "yall'd've": "you all would have",
        "yall're": "you all are",
        "yall've": "you all have",
        "you'd": "you would",
        "you'd've": "you would have",
        "you'll": "you will",
        "you'll've": "you will have",
        "you're": "you are",
        "you've": "you have"
    }

    nltk_stopwords = {"i", "me", "my", "myself", "we", "our", "ours", "ourselves", "you", "your", "yours", "yourself",
                      "yourselves", "he", "him", "his", "himself", "she", "her", "hers", "herself", "it", "its", "itself",
                      "they", "them", "their", "theirs", "themselves", "what", "which", "who", "whom", "this", "that",
                      "these", "those", "am", "is", "are", "was", "were", "be", "been", "being", "have", "has", "had",
                      "having", "do", "does", "did", "doing", "a", "an", "the", "and", "but", "if", "or", "because", "as",
                      "until", "while", "of", "at", "by", "for", "with", "about", "against", "between", "into", "through",
                      "during", "before", "after", "above", "below", "to", "from", "up", "down", "in", "out", "on", "off",
                      "over", "under", "again", "further", "then", "once", "here", "there", "when", "where", "why", "how",
                      "all", "any", "both", "each", "few", "more", "most", "other", "some", "such", "only", "own", "same",
                      "so", "than", "too", "very", "s", "t", "can", "will", "just", "don", "should", "now"}

    # convert common contractions
    @staticmethod
    def convert_contractions(txt):
        new_txt = []
        for tok in txt.split():
            if tok in Preproc.contractions.keys():  # replace contractions
                tok = Preproc.contractions[tok]
            new_txt.append(tok)

        return " ".join(new_txt)

    # Remove stray utf8
    @staticmethod
    def remove_utf8(txt):
        patt = r'\\x[a-zA-Z0-9]{2}'
        txt = re.sub(patt, ' ', txt)

        return txt

    # Remove all slashes
    @staticmethod
    def remove_slashes_and_brackets(txt):
        patt = r'[\\|\/\]\[]'
        txt = re.sub(patt, ' ', txt)

        return txt

    # tokenize misc symbols
    @staticmethod
    def tokenize_misc(txt):
        txt = re.sub(r'\.\.\.', ' <ellipsis> ', txt)
        txt = re.sub(Preproc.re_percent, '<percent>', txt)
        txt = re.sub(Preproc.re_currency, ' <usd> ', txt)
        txt = re.sub(Preproc.re_numbers, ' <number> ', txt)
        return txt

    # tokenize hashtags
    @staticmethod
    def tokenize_hashtags(txt):
        txt = Preproc.re_hashtag.sub("<hashtag>", txt)
        return txt

    # tokenize mentions
    @staticmethod
    def tokenize_mentions(txt):
        txt = Preproc.re_mention.sub("<mention>", txt)
        return txt

    # Surround punct. w/ whitespace
    @staticmethod
    def pad_punct_ws(txt):
        punct = '([$.,!?()@#\/:\[\]\'\";-])'
        txt = re.sub(punct, r' \1 ', txt)
        txt = re.sub('\s{2,}', ' ', txt)

        return txt.strip()

    # Remove punctuation
    @staticmethod
    def remove_punct(txt):
        punct = '([$.,!?()@#\/:\[\]\'\";-])'
        txt = re.sub(punct, ' ', txt)
        return txt.strip()

    # remove stopwords
    @staticmethod
    def remove_stopwords(txt):
        txt = " ".join([x for x in txt.split() if x not in Preproc.nltk_stopwords])

        return txt

def test(file_path: str):

    txt = "Alberta sent me $50 over PayPal @AlbertaRocks! #FreeMoney!!!"
    prep = Preproc()

    print(txt)
    print(prep.preprocess_text(txt))

if __name__=='__main__':
    from line_profiler import LineProfiler

    # setup line profiling
    profiler = LineProfiler()
    profiler.add_function(Preproc.preprocess_text)
    test_func = profiler(test)

    # call the test function and print profiling results
    data_path = "TestData/all_tweets_filtered_final.csv"
    test_func(data_path)
    profiler.print_stats()
