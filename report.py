import queries
import config
from elasticsearch import Elasticsearch

def getRegisters(host, query):
    es = Elasticsearch(
        [host]
    )
    registers = es.search(index="shipments", doc_type="shipment", size=10000, body=query)
    return registers['hits']['hits']


def getReport (registers):

    data = {}
    for doc in registers:
        key = doc['_source']['metadata']['source']
        additionalData = doc['_source']['additionalData']
        if (len(additionalData) > 0):
            oldListAdditional = data.get(key.upper(), set())
            oldListAdditional |= set(additionalData.keys())
            data[key.upper()] = oldListAdditional
    return data

def printInfoReport(registers):
    print('------')
    print("%d documents found" % len(registers))
    print('------')

def printHeadReport (data):
    print('------')
    print ("TOTAL SOURCE =>" + str(len(data)))
    print(list(data.keys()))
    print(data)
    print('------')

def printRowsReport(data):
    for source in data:
        print (source + " => " + str(len(data[source])))
        print(sorted(data[source]))

def main():
    registersReport = getRegisters(config.HOST_LEMMINGS, queries.QUERY_ALL)
    dataReport = getReport(registersReport)
    printInfoReport(registersReport)
    printHeadReport(dataReport)
    printRowsReport(dataReport)


main()
