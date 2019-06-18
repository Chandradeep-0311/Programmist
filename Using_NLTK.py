
# coding: utf-8

# In[7]:


import nltk
#nltk.download('popular')
doc= '''using the previous work to spread search agains the api by keys, use search by mission id key duration label should specify units: Duration(hrs) just like the operator dropdown has it, the inline vehicle edit should have this too the header should dynamically change to show the DCMID next to the title in the details column, we want to display first name last name instead of email(fall back to email only if we cant match it to a user) For multi-modal, we need to add zoom and brightness functionality for LIDAR, to match with the functionality developed for the images. It will use the same sliders, so no GUI is necessary. we observed that when selecting the fail action and then hitting cancel button, it was toggling the whole mission to cancelled state. This button should just close the modal and abort the fail action after creating a mission, there is a new table row added but it is difficult to understand which one this is so we should have a small highlight on this row for a second or 2 that fades away on the row that was added
WO which are created in multi modal are not displaying duration/frames in ADA/A. In DEV, from Laser tag application, selecting on 3D-Other does not create a Work Order'''


# In[8]:


# tokenize doc
tokenized_doc = nltk.word_tokenize(doc)


# In[9]:


tokenized_doc


# In[10]:


tagged_sentences = nltk.pos_tag(tokenized_doc)
ne_chunked_sents = nltk.ne_chunk(tagged_sentences)


# In[11]:


# extract all named entities
named_entities = []
for tagged_tree in ne_chunked_sents:
    if hasattr(tagged_tree, 'label'):
        entity_name = ' '.join(c[0] for c in tagged_tree.leaves()) #
        entity_type = tagged_tree.label() # get NE category
        named_entities.append((entity_name, entity_type))
print(named_entities)


# In[12]:


data= [(['Search','Mission Id','Duration','Operator','Vehicle','DCMID','Title','First name','Last name','Email','Column','Zoom','Brightness','Fail','Cancel','Create','duration','Frames','Created','Laser Tag','3D-Other','Create'],['Action','Value','Field label','Field label','Field label','Value','Popup label','Value','Value','Value','Field','Action','Action','Action','Action','Action','Value','Value','Action','Application','Type','Action'])]



# In[13]:


corpus = []
for (doc, tags) in data:
    doc_tag = []
    for word, tag in zip(doc,tags):
        doc_tag.append((word, tag))
    corpus.append(doc_tag)
print(corpus)


# In[16]:


def doc2features(doc, i):
    word = doc[i][0]
    
    # Features from current word
    features={
        'word.word': word,
    }
    # Features from previous word
    if i > 0:
        prevword = doc[i-1][0]
        features['word.prevword'] = prevword
    else:
        features['BOS'] = True # Special "Beginning of Sequence" tag
        
    # Features from next word
    if i < len(doc)-1:
        nextword = doc[i+1][0]
        features['word.nextword'] = nextword
    else:
        features['EOS'] = True # Special "End of Sequence" tag
    return features
 
def extract_features(doc):
    return [doc2features(doc, i) for i in range(len(doc))]
 
X = [extract_features(doc) for doc in corpus]
print(X)


# In[4]:


def get_labels(doc):
    return [tag for (token,tag) in doc]
y = [get_labels(doc) for doc in corpus]
print(y)


# In[5]:


import sklearn_crfsuite
crf = sklearn_crfsuite.CRF(
    algorithm='lbfgs',
    c1=0.1,
    c2=0.1,
    max_iterations=20,
    all_possible_transitions=False,
)
crf.fit(X, y);


# In[6]:


test = [['Mission Id']]
X_test = extract_features(test)
print(crf.predict_single(X_test))

