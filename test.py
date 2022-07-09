from py_edamam import Edamam
from dotenv import load_dotenv
import os
import pprint

load_dotenv()
API_Token = os.getenv("API_TOKEN")
API_ID = os.getenv("API_ID")

e = Edamam(recipes_appid=API_ID, recipes_appkey=API_Token)
recipes = e.search_recipe("onion and chicken")
pprint.pprint(recipes)
pretty_dict_str = pprint.pformat(recipes)
with open("data.txt", "w") as q:
    q.write(pretty_dict_str)

"""

with open("data.txt", "w") as q:
    for a in recipes["hits"]:
        for i in a["recipe"]:
            for key, val in i.items():
                q.write(str(key) + ": " + str(val) + "\n")
    q.close()
"""


print("DONE")
print()
print("DONE")
