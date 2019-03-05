## Requisites

- Pynthon 3.7
- Elasticsearch library (https://elasticsearch-py.readthedocs.io/en/master/index.html)

`sudo pip install elasticsearch
`
##Info

Get shipment information by source in csv files.
There is two queries: 
- all : get documents from ELS in one query
- bySource : get documents from ELS in several queries, once by source

##Configuration

Open ssh tunnel

`````
ssh -vN -p 22822 packdev@lemmingsteamqa-bastion01.packitos.com -L 27777:elasticsearch-9200.service.consul:9200

`````

Configuration to connect to ELS 
````
DEFAULT_TIMEOUT = 30            #read timeout to ELS
DEFAULT_SIZE = 100              #number of documents to get
DEFAULT_HOST = HOST_LEMMINGS    #ELS host
````

Configuratio about csv
````
DEFAULT_PATH = "/Users/valbuena/Documents/" #path where csv files are created
````

Configuration about which field you want to use to filter 
``````
def get_key(doc):
    #return doc['_source']['metadata']['source']
    return doc['_source']['currency']
``````
Configuration about which fields you want to get 
``````
def get_value(doc):
    # doc['_source']['price']
    return doc['_source']['additionalData']
``````

## Run

Execute file : print.py

