from chatbot import Chat, register_call
import wikipedia
import os
import warnings
import spacy
from spacy.pipeline import EntityRecognizer
warnings.filterwarnings("ignore")


@register_call("whoIs")
def who_is(session, query):
    try:
        return wikipedia.summary(query)
    except Exception:
        for new_query in wikipedia.search(query):
            try:
                return wikipedia.summary(new_query)
            except Exception:
                pass
    return "I don't know about "+query

nlp_ner = spacy.load('/Users/namithav/demo_chatbot/ner')
nlp_en = spacy.load('en_core_web_sm')
assert nlp_en.vocab != nlp_ner.vocab
assert nlp_en.vocab.vectors.to_bytes() == nlp_ner.vocab.vectors.to_bytes()
ner_new = EntityRecognizer(nlp_en.vocab)
ner_new.from_bytes(nlp_ner.get_pipe("ner").to_bytes(exclude=["vocab"]))
nlp_en.add_pipe(ner_new, name="ner_new")
assert nlp_en.vocab == ner_new.vocab

@register_call("process_text")
def process_text(session, query):
    try:
        doc = nlp_en(query)
        for ent in doc.ents:
            if ent.label_ == "SERVICENOW":
                service_now(query)
        #return query
    except Exception:
        return False
    return "I don't know about "+query

def service_now(text):
    print("inside snow fn")
    #return text
    doc = nlp_en(text)
    for ent in doc.ents:
        print(ent.text, ent.label_)
    return text



first_question = "Hi, how are you?"
chat = Chat(os.path.join(os.path.dirname(os.path.abspath(__file__)), "Example.template"))
chat.converse(first_question)
