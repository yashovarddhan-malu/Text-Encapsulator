import spacy
from spacy.lang.en.stop_words import STOP_WORDS
from string import punctuation
from heapq import nlargest

stopwords = list(STOP_WORDS)
nlp = spacy.load('en_core_web_sm')
punctuation += '\n'

def summarizer(text, n):
    no_sentences = int(n)
    doc = nlp(text)
   
    word_frequencies = {}  # Dictionary
    for word in doc: # Calculating Word Frequency
        if word.text.lower() not in stopwords:
            if word.text.lower() not in punctuation:
                if word.text not in word_frequencies.keys():
                    word_frequencies[word.text] = 1
                else:
                    word_frequencies[word.text] += 1

    max_frequency = max(word_frequencies.values())

    for word in word_frequencies.keys():
        word_frequencies[word] = word_frequencies[word]/max_frequency  # Weight w.r.t max frequency

    sentence_list = [sentence for sentence in doc.sents]

    sentence_scores = {} 
    for sent in sentence_list:
        for word in sent:
            if word.text.lower() in word_frequencies.keys():
                if len(sent.text.split(' ')) < 30:
                    if sent not in sentence_scores.keys():
                        sentence_scores[sent] = word_frequencies[word.text.lower()] # Adding word frequency to calculate sentence score
                    else:
                        sentence_scores[sent] += word_frequencies[word.text.lower()]

    summary = nlargest(no_sentences, sentence_scores, key = sentence_scores.get)
    final_sentences = [word.text for word in summary]
    summary = ''.join(final_sentences)

    return summary