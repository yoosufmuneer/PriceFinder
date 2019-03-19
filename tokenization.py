from nltk.tokenize import word_tokenize, sent_tokenize
from nltk.tag import pos_tag

paragraph = input("Enter a description: ")

sentence = sent_tokenize(paragraph)
#tokens = word_tokenize(paragraph)
#tagging = pos_tag(tokens)

data = []
for sent in sentence:
    data = data + pos_tag(word_tokenize(sent))

for word in data:
    if 'JJ' or 'JJS' in word[1]:
        print(word)

#print(sentence)
#print(tokens)
#print(tagging)

