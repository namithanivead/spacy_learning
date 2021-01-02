import re
doc = nlp("Is there a Servicenow incident for Mail")
list_of_strings = ["Servicenow", "incident", "Mail"]
for s in list_of_strings:
    res = re.search(s,doc.text)
    if res:
        print(s , res.start(), res.end())
