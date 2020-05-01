# How about a making a word-association graph from an input text? 
# It shows the nouns (red) in the text connected to the adjectives (yellow)
# and the verbs (blue). The node sizes are proportional to their degree. 
# It is 49 lines if you don’t count the import statements ;)
import nltk
#nltk.download('punkt')
#nltk.download('averaged_perceptron_tagger')
import pandas as pd
import numpy as np
import networkx as nx
import matplotlib.pyplot as plt

def word_association_graph(text, k=0.4, font_size=24):
    nouns_in_text = []
    is_noun = lambda pos: pos[:2] == 'NN'
    for sent in text.split('.')[:-1]:   
        tokenized = nltk.word_tokenize(sent)
        nouns=[word for (word, pos) in nltk.pos_tag(tokenized) if is_noun(pos)]
        nouns_in_text.append(' '.join([word for word in nouns if not (word=='' or len(word)==1)]))
    nouns_list = []
    for sent in nouns_in_text:
        temp = sent.split(' ')
        for word in temp:
            if word not in nouns_list:
                nouns_list.append(word)
    df = pd.DataFrame(np.zeros(shape=(len(nouns_list),2)), columns=['Nouns', 'Verbs & Adjectives'])
    df['Nouns'] = nouns_list
    is_adjective_or_verb = lambda pos: pos[:2]=='JJ' or pos[:2]=='VB'
    for sent in text.split('.'):
        for noun in nouns_list:
            if noun in sent:
                tokenized = nltk.word_tokenize(sent)
                adjectives_or_verbs = [word for (word, pos) in nltk.pos_tag(tokenized) if is_adjective_or_verb(pos)]
                ind = df[df['Nouns']==noun].index[0]
                df['Verbs & Adjectives'][ind]=adjectives_or_verbs
    fig = plt.figure(figsize=(30,30))
    G = nx.Graph()
    color_map=[]
    for i in range(len(df)):
        G.add_node(df['Nouns'][i])
        color_map.append('blue')
        for word in df['Verbs & Adjectives'][i]:
            G.add_edges_from([(df['Nouns'][i], word)])
    pos = nx.spring_layout(G, k)
    d = nx.degree(G)
    node_sizes = []
    for i in d:
        _, value = i
        node_sizes.append(value)
    color_list = []
    for i in G.nodes:
        if len(i)>0:
            value = nltk.pos_tag([i])[0][1]
        if (value=='NN' or value=='NNP' or value=='NNS'):
            color_list.append('red')
        elif value=='JJ':
            color_list.append('yellow')
        else:
            color_list.append('blue')
    nx.draw(G, pos, node_size=[(v+1)*200 for v in node_sizes], with_labels=True, node_color=color_list, font_size=font_size)
    plt.show()

import re

#text = "Wikipedia was launched on January 15, 2001, by Jimmy Wales and Larry Sanger.[10] Sanger coined its name,[11][12] as a portmanteau of wiki[notes 3] and 'encyclopedia'. Initially an English-language encyclopedia, versions in other languages were quickly developed. With 5,748,461 articles,[notes 4] the English Wikipedia is the largest of the more than 290 Wikipedia encyclopedias. Overall, Wikipedia comprises more than 40 million articles in 301 different languages[14] and by February 2014 it had reached 18 billion page views and nearly 500 million unique visitors per month.[15] In 2005, Nature published a peer review comparing 42 science articles from Encyclopadia Britannica and Wikipedia and found that Wikipedia's level of accuracy approached that of Britannica.[16] Time magazine stated that the open-door policy of allowing anyone to edit had made Wikipedia the biggest and possibly the best encyclopedia in the world and it was testament to the vision of Jimmy Wales.[17] Wikipedia has been criticized for exhibiting systemic bias, for presenting a mixture of 'truths, half truths, and some falsehoods',[18] and for being subject to manipulation and spin in controversial topics.[19] In 2017, Facebook announced that it would help readers detect fake news by suitable links to Wikipedia articles. YouTube announced a similar plan in 2018." 

#text = "If the manner in which I began the previous chapter on the Wind seemed too much like fantastical writing and the showful throwing off of fulsome sobriquets to The Great Progenitor much like newlyweds are showered confetti, then the facts need to be repeated again. I reemphasize: Mother Earth is alive in every way, in every bit of her manifestations—from the animate to the seemingly volition-lacking inanimate. And in none is it more apparent than in the Wind and its numerous effects on far-ranging seemingly disparate phenomena.\nOn the coasts of South Africa, there is a phenomenon that occurs once a year that baffles everyone lucky enough to observe it. To the mouth agape Observer’s eye, no spectacle ever recorded has quite demonstrated the Ocean’s immensity, power and productivity much like this. This is the sardine run of southern Africa. It occurs—vicariously as pertains to this author’s point of view—from May to July. Billions of sardines a’congregating in one spot—who knows what they are up to? And what they bring in their wake! Dolphins, sharks, several large gamefish, whales of all sorts, numerous birds, even humans get in on the action. And what it culminates in! You haven’t seen a feeding frenzy quite like this. What triggers and starts this whole process off? And why only at a certain particular time of the year?\nThe wind system off of the southern African coast has created a dominating ocean current known as the Agulhas Current. That whole general area of the current is called the Agulhas Bank. The Agulhas Bank is a natural boundary between ocean currents from the Atlantic Ocean, Indian Ocean, and Southern Ocean, resulting in one of the most turbulent waters of the world oceans. Let’s hear the experts on it:\n"

#text = "If the manner in which I began the previous chapter on the Wind seemed too much like fantastical writing and the showful throwing off of fulsome sobriquets to The Great Progenitor much like newlyweds are showered confetti, then the facts need to be repeated again. I reemphasize: Mother Earth is alive in every way, in every bit of her manifestations—from the animate to the seemingly volition-lacking inanimate."

text = "Hello, Nuertey is bored, and unsurprisingly, he is quite dangerous when bored."

text = re.sub("[\[].*?[\]]", "", text) ## Remove brackets and anything inside it (to remove the citations)
# You can do more cleaning (like lemmatization, stemming, stopword removal, etc if you want)
 
word_association_graph(text)

print(text)
print()
