#doc = nlp("""\Calabria, known in antiquity as Bruttium (US: /ˈbrʊtiəm, ˈbrʌt-/),[7][8] is an administrative region of Italy. Located in the south of the Italian Peninsula, separated from Sicily by the Strait of Messina. As of 2019, the region has a population of around 2,000,000 people. The capital city of Calabria is Catanzaro. The Regional Council of Calabria is based at the Palazzo Campanella in the city of Reggio Calabria. The region is bordered to the north by the Basilicata Region, to the west by the Tyrrhenian Sea, and to the east by the Ionian Sea. The Strait of Messina separates it from the island of Sicily. The region covers 15,080 km2 (5,822 sq mi) and has a population of just under 2 million. The demonym of Calabria is calabrese in Italian and Calabrian in English. In antiquity the name Calabria referred, not as in modern times to the toe, but to the heel tip of Italy, from Tarentum southwards,[9] a region nowadays known as Salento. The region is generally known as the "toe" of the "boot" of Italy and is a long and narrow peninsula which stretches from north to south for 248 km (154 mi), with a maximum width of 110 km (68 mi). Some 42% of Calabria's area, corresponding to 15,080 km2, is mountainous, 49% is hilly, while plains occupy only 9% of the region's territory. It is surrounded by the Ionian and Tyrrhenian seas. It is separated from Sicily by the Strait of Messina, where the narrowest point between Capo Peloro in Sicily and Punta Pezzo in Calabria is only 3.2 km (2 mi). Three mountain ranges are present: Pollino, La Sila and Aspromonte, each with its own flora and fauna. The Pollino Mountains in the north of the region are rugged and form a natural barrier separating Calabria from the rest of Italy. Parts of the area are heavily wooded, while others are vast, wind-swept plateaus with little vegetation. These mountains are home to a rare Bosnian Pine variety and are included in the Pollino National Park, which is the largest national park in Italy, covering 1,925.65 square kilometres. La Sila, which has been referred to as the "Great Wood of Italy",[16][17][18] is a vast mountainous plateau about 1,200 metres (3,900 feet) above sea level and stretches for nearly 2,000 square kilometres (770 square miles) along the central part of Calabria. The highest point is Botte Donato, which reaches 1,928 metres (6,325 feet). The area boasts numerous lakes and dense coniferous forests. La Sila also has some of the tallest trees in Italy which are called the "Giants of the Sila" and can reach up to 40 metres (130 feet) in height.[19][20][21] The Sila National Park is also known to have the purest air in Europe.[22] The Aspromonte massif forms the southernmost tip of the Italian peninsula bordered by the sea on three sides. This unique mountainous structure reaches its highest point at Montalto, at 1,995 metres (6,545 feet), and is full of wide, man-made terraces that slope down towards the sea. Most of the lower terrain in Calabria has been agricultural for centuries, and exhibits indigenous scrubland as well as introduced plants such as the prickly pear cactus. The lowest slopes are rich in vineyards and orchards of citrus fruit, including the Diamante citron. Further up, olives and chestnut trees appear while in the higher regions there are often dense forests of oak, pine, beech and fir trees The region is generally known as the "toe" of the "boot" of Italy and is a long and narrow peninsula which stretches from north to south for 248 km (154 mi), with a maximum width of 110 km (68 mi). Some 42% of Calabria's area, corresponding to 15,080 km2, is mountainous, 49% is hilly, while plains occupy only 9% of the region's territory. It is surrounded by the Ionian and Tyrrhenian seas. It is separated from Sicily by the Strait of Messina, where the narrowest point between Capo Peloro in Sicily and Punta Pezzo in Calabria is only 3.2 km (2 mi). Three mountain ranges are present: Pollino, La Sila and Aspromonte, each with its own flora and fauna. The Pollino Mountains in the north of the region are rugged and form a natural barrier separating Calabria from the rest of Italy. Parts of the area are heavily wooded, while others are vast, wind-swept plateaus with little vegetation. These mountains are home to a rare Bosnian Pine variety and are included in the Pollino National Park, which is the largest national park in Italy, covering 1,925.65 square kilometres. La Sila, which has been referred to as the "Great Wood of Italy",[16][17][18] is a vast mountainous plateau about 1,200 metres (3,900 feet) above sea level and stretches for nearly 2,000 square kilometres (770 square miles) along the central part of Calabria. The highest point is Botte Donato, which reaches 1,928 metres (6,325 feet). The area boasts numerous lakes and dense coniferous forests. La Sila also has some of the tallest trees in Italy which are called the "Giants of the Sila" and can reach up to 40 metres (130 feet) in height.[19][20][21] The Sila National Park is also known to have the purest air in Europe.[22] The Aspromonte massif forms the southernmost tip of the Italian peninsula bordered by the sea on three sides. This unique mountainous structure reaches its highest point at Montalto, at 1,995 metres (6,545 feet), and is full of wide, man-made terraces that slope down towards the sea.Most of the lower terrain in Calabria has been agricultural for centuries, and exhibits indigenous scrubland as well as introduced plants such as the prickly pear cactus. The lowest slopes are rich in vineyards and orchards of citrus fruit, including the Diamante citron. Further up, olives and chestnut trees appear while in the higher regions there are often dense forests of oak, pine, beech and fir trees.""")
#region Imports
import logging

import azure.functions as func

#from shared_code import commonHelper

import jsonschema
from jsonschema import validate
import base64
import os
import json
import spacy
from spacy import displacy 
import pandas as pd
import geopy 
import matplotlib.pyplot as plt
from geopy.extra.rate_limiter import RateLimiter
#endregion Imports

#region Vars

inputSchema = {
    "type": "object",
    "properties": {
        "base64Value": {"type": "string"}
    },
    "required": [
        "base64Value"
    ]
}

#endregion Vars

#region Custom Methods

# Validates a json based on a schema
def validateJson(jsonData, myschema):
    try:
        validate(instance=jsonData, schema=myschema)
    except jsonschema.exceptions.ValidationError as err:
        #print(str(err))
        return False
    return True

# Validates that input is in fact base64 encoded
def isBase64(sb):
    try:
        if isinstance(sb, str):
            # If there's any unicode here, an exception will be thrown and the function will return false
            sb_bytes = bytes(sb, 'ascii')
        elif isinstance(sb, bytes):
            sb_bytes = sb
        else:
            return False
        return base64.b64encode(base64.b64decode(sb_bytes)) == sb_bytes
    except Exception:
        return False

def performNER(input_text):
    try:
        #initiate model
        msg = 'Environment: ' + os.environ["AZURE_FUNCTIONS_ENVIRONMENT"].lower()
        logging.info(msg)
        if os.environ["AZURE_FUNCTIONS_ENVIRONMENT"] != "Development":
            nlp = spacy.load(os.environ["SPACY_PATH"])
        else:
            nlp = spacy.load('xx_ent_wiki_sm')
            #nlp = spacy.load('/home/isi/jon/projects/python/nlp2/nlproj2/xx_ent_wiki_sm')
        
        doc = nlp(input_text)
        
        locations = []
        locations.extend([[ent.text, ent.start, ent.end] for ent in doc.ents if ent.label_ in ['LOC']])

        df = pd.DataFrame(locations, columns=['Location', 'start','end'])

        df.drop_duplicates(subset='Location', keep='first', inplace=True)
        df.sort_values("Location", inplace = True)

        locator = geopy.geocoders.Nominatim(user_agent="geoparser")
        geocode = RateLimiter(locator.geocode, min_delay_seconds=1)

        # Geocode locations, assigning to new field
        df["address"] = df["Location"].apply(geocode)

        df['coordinates'] = df['address'].apply(lambda loc: tuple(loc.point) if loc else None)
        df[['latitude', 'longitude', 'altitude']] = pd.DataFrame(df['coordinates'].tolist(), index=df.index)
        df.latitude.isnull().sum()
        df = df[pd.notnull(df["latitude"])]
        
        #out = df.to_json(orient='records')[1:-1].replace('},{', '} {')
        dfJSON = df.to_json(orient='records')
        parsed = json.loads(dfJSON)
        out = json.dumps(parsed, indent=4)

        return out

    except Exception as e:
        logging.error(str(e))
        return None

#end Custom Methods

def main(req: func.HttpRequest) -> func.HttpResponse:
    try:
        logging.info('Python HTTP trigger function processed a request.')

        msg = 'Environment: ' + os.environ["AZURE_FUNCTIONS_ENVIRONMENT"].lower()
        logging.info(msg)

        # Input validation
        try:
            req_body = req.get_json()
        except ValueError:
            res = json.dumps({'error': 'Wrong input. Expecting schema: ' + ''.join(json.dumps(inputSchema))})
            return func.HttpResponse(res, status_code=400)
        else:
            isValid = validateJson(req_body, inputSchema)
            if not isValid:
                res = json.dumps({'error': 'Wrong input. Expecting schema: ' + ''.join(json.dumps(inputSchema))})
                return func.HttpResponse(res, status_code=400)

        base64Value = req_body.get('base64Value')

        if not isBase64(base64Value):
            #Will assume incoming vaue is text then...
            plainText = base64Value

        else:
            plainText = str(base64.b64decode(base64Value), "utf-8")

        res = performNER(plainText)

        return func.HttpResponse(res, status_code=200)


    except Exception as e:
        return func.HttpResponse(json.dumps({'error1': str(e)}), status_code=500)

