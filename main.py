import spacy
from string import punctuation
from spacy.lang.en.stop_words import STOP_WORDS

nlp = spacy.load('en_core_web_sm')
stopwords = list(STOP_WORDS)
from heapq import nlargest

def tokenizer(text):
  doc = nlp(text)
  tokens = [token.text for token in doc]
  return doc,tokens


def wordfreq(doc):
  word_freq = {}
  import re

  for word in doc:
    if word.text.lower() not in stopwords and word.text.lower() not in punctuation:
      if word.text not in word_freq.keys():
        word_freq[word.text]=1
      else:
        word_freq[word.text]+=1

  del word_freq['\n\n']
  del word_freq['\n']
  max_freq = max(word_freq.values())
  for word in word_freq.keys():
    word_freq[word] = word_freq[word]/max_freq
  return word_freq

def sent_tokenizer(doc,word_freq):
  sent_tokens = [sent for sent in doc.sents]
  sent_scores = {}

  for sent in sent_tokens:
    for word in sent:
      if word.text in word_freq.keys():
        if sent not in sent_scores.keys():
          sent_scores[sent]=word_freq[word.text]
        else:
          sent_scores[sent]+=word_freq[word.text]
  return sent_scores

def summarizer(text):
  doc, tokens = tokenizer(text)
  word_freq = wordfreq(doc)
  sent_scores  = sent_tokenizer(doc,word_freq)
  select_len = int(len(sent_scores.keys())*0.3)
  summary = nlargest(select_len, sent_scores, key = sent_scores.get)
  final_summary = [word.text for word in summary]
  final_summary = " ".join(final_summary)
  print(final_summary)