# Import the necessary libraries
from nltk.stem import PorterStemmer
ps = PorterStemmer()

# Read the content of the text file
convo1text = open("conversation1.txt", "r").readlines()

# Create a new variable with clean and non-empty sentences
newConvo = []
for sent in convo1text:
    sent = sent.strip("\n")
    if not sent is '':
        newConvo.append(sent)
    
convo1text = newConvo

# Use ':' to extract speaker name and use as prefix for subsequent sentences
for index,sent in enumerate(convo1text):
    if sent.count(':') > 0:
        previousSpeaker = sent.split(':')[0]
    if sent.count(':') == 0:
        convo1text[index] = previousSpeaker + ':' + sent

# Structure conversation pairs such that each pair consists of the speaker name and their corresponding sentence        
conversation1 = []
for sent in convo1text:
    convo = sent.split(':')
    if len(convo) > 2:
        convo[1] += ('-').join(convo[2:])
    convo = convo[:2]
    convo[1] = convo[1].strip()
    if not convo[1] is '':
        conversation1.append([c for c in convo])

# Read all contractions from json file and store in a variable
import json
with open("contractions.json", "r") as read_file:
    data = json.load(read_file)
    
contractions = data['contractions']

# Process each sentence
import re
processedConversation = []
for speaker, dialog in conversation1:
    for (key, val) in contractions.items():
        dialog = dialog.lower()   # Convert text to lowercase
        dialog = dialog.replace(key, val)   # Replace contractions
        dialog = re.sub(r"([\w/'+$\s-]+|[^\w/'+$\s-]+)\s*", r"\1 ", dialog)   # Perform reg-ex based text preprocessing
        dialog = ' ' + dialog + ' '   # Add spaces at the beginning and end of the sentence
        dialog = re.sub(' +', ' ',dialog)   # Replace multiple spaces with a single space
        
    processedConversation.append([speaker, dialog])

# Identify where someone used a word stemming from 'summar' such as summary/summarize/summarization and process the accumulated text using spaCy
import spacy

spacy.cli.download("en_core_web_sm")
nlp = spacy.load("en_core_web_sm")

summary = ''
summarySpeaker = None
for speaker, dialog in processedConversation:
    if summarySpeaker is None:
        doc = nlp(dialog)
        for token in doc:
            if ps.stem(token.lemma_) == 'summar':
                summarySpeaker = speaker
    else:
        if speaker == summarySpeaker:
            summary = summary + dialog
        else:
            summarySpeaker = None

doc = nlp(summary)

# Use the NLTK library to remove stopwords, punctuation, and single character words
import nltk

from nltk.corpus import stopwords
from string import punctuation

stopwords = set(stopwords.words('english') + list(punctuation) + list(' '))
word_sent = [word.text for word in doc if word.text not in stopwords]

# Join the words into a sentence
sentence = ' '.join(word_sent)

# Print the sentence
print(sentence)