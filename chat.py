from chatbot import Chat, register_call
import os
import warnings
import spacy
from spacy.pipeline import EntityRecognizer
warnings.filterwarnings("ignore")

nlp = spacy.load('en_core_web_sm')

@register_call("process_text")
def process_text(session, query):
    try:
        doc = nlp(query)
        lemma_doc = nlp(" ".join([token.lemma_ for token in doc]))
        date_str = "Today"
        for ent in doc.ents:
            if ent.label_ == "DATE":
                date_str = ent.text

        snow_keywords = ["servicenow", "snow", "incident", "outage"]
        snow_status = ["open", "create", "resolve", "close", "closed"]
        count = False
        state = "open"
        snow = False
        for token in lemma_doc:
            if token.pos_ == "ADJ":
                if token.text == "many":
                    count = True
            if token.text in snow_status:
                    state = token.text
            if token.pos_ == "NOUN" and token.text in snow_keywords:
                snow = True
                
        if snow:
            return service_now(date_str, state, count)
        else:
            return "I don't know about " + query
    except Exception:
        return "Internal error, please retry"

def service_now(date_str, state, count):
    if state == "close":
        state = "closed"
    date_str = date_str.title()
    snow_base = "https://vzbuilders.service-now.com/incident_list.do?sysparm_query="
    snow_state_urls = {
        "open": "stateIN1%2C-1%2C2&sysparm_first_row=1",
        "resolve": "resolved_atON{}@javascript:gs.beginningOf{}()@javascript:gs.endOf{}()",
        "create": "sys_created_onON{}@javascript:gs.beginningOf{}()@javascript:gs.endOf{}()",
        "closed": "closed_atON{}@javascript:gs.beginningOf{}()@javascript:gs.endOf{}()",
        "property": "%5Eu_responsible_property.name={}%5EORcmdb_ci.name={}"
    }
    #print(date_str, state, count)
    url = snow_base + snow_state_urls[state].format(date_str, date_str, date_str)
    return url

first_question = "Hi, how are you?"
chat = Chat(os.path.join(os.path.dirname(os.path.abspath(__file__)), "Example.template"))
chat.converse(first_question)
