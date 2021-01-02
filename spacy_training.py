from __future__ import unicode_literals, print_function
import plac
import random
from pathlib import Path
import spacy
from tqdm import tqdm

# training data
TRAIN_DATA = [
              ("Is there a Servicenow incident for Mail", {"entities": [(11, 22, "TOOLS"), (22,30, "TARGET"),(35,39, "PROPERTY")]}),
              ("Get all the incident that impacted Mail between yesterday and today", {"entities": [(12,20, "TARGET"),(35,39, "PROPERTY")]}),
              ("Please ping the yamas graph for alert", {"entities": [(16, 21, "TOOLS"),(22,27, "TOOLS"),(32,37, "ALERT")]})
            ]

model = None
output_dir=Path("/Users/namithav/demo_chatbot/ner")
n_iter=100

#load the model

if model is not None:
    nlp = spacy.load(model)
    print("Loaded model '%s'" % model)
else:
    nlp = spacy.blank('en')
    print("Created blank 'en' model")

#set up the pipeline

if 'ner' not in nlp.pipe_names:
    ner = nlp.create_pipe('ner')
    nlp.add_pipe(ner, last=True)
else:
    ner = nlp.get_pipe('ner')

for _, annotations in TRAIN_DATA:
    for ent in annotations.get('entities'):
        ner.add_label(ent[2])

other_pipes = [pipe for pipe in nlp.pipe_names if pipe != 'ner']
with nlp.disable_pipes(*other_pipes):  # only train NER
    optimizer = nlp.begin_training()
    for itn in range(n_iter):
        random.shuffle(TRAIN_DATA)
        losses = {}
        for text, annotations in tqdm(TRAIN_DATA):
            nlp.update(
                [text],
                [annotations],
                drop=0.5,
                sgd=optimizer,
                losses=losses)
        print(losses)
for text, _ in TRAIN_DATA:
    doc = nlp(text)
    print('Entities', [(ent.text, ent.label_) for ent in doc.ents])
