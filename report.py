import queries
import constants
from elasticsearch import Elasticsearch


def get_registers(host, query, size):
    es = Elasticsearch(
        [host],
        retry_on_timeout=True,
        timeout = 30
    )
    registers = es.search(index="shipments", doc_type="shipment", size=size, body=query)
    return registers['hits']['hits']


def is_father(father):
    return isinstance(father, dict) or \
           (isinstance(father, list) and len(father) > 0 and isinstance(father[0], dict))


def get_father(father):
    if isinstance(father, list):
        return father[0]
    else:
        return father


def get_separator(father):
    return ".[]." if isinstance(father, list) else "."


def get_list_keys(element):
    if len(element) > 0:
        father_keys = []
        for key, value in element.items():
            if is_father(value):
                child_keys = get_list_keys(get_father(value))
                father_keys.extend([key + get_separator(value) + child for child in child_keys])
            else:
                father_keys.append(key)
        return father_keys
    else:
        return []


def get_report(registers):
    data = {}
    for doc in registers:
        key = doc['_source']['metadata']['source']
        additional_data = doc['_source']['additionalData']
        if len(additional_data) > 0:
            old_list_additional = data.get(key, set())
            list_keys = get_list_keys(additional_data)
            old_list_additional |= set(list_keys)
            data[key] = old_list_additional
    return data


def print_info_report(registers):
    print('--INFO ----')
    print("%d documents found" % len(registers))

def print_head_report(data):
    print('--HEAD----')
    print(list(data.keys()))


def print_rows_report(data):
    print('--ROWS----')
    for source in data:
        print(source.upper() + " => " + str(len(data[source])))
        print(sorted(data[source]))

def print_report(data):
    print_head_report(data)
    print_rows_report(data)

def print_csv(store):
    max = 0
    for source in store.keys():
        store[source] = list(sorted(store[source]))
        length = len(store[source])
        max = length if length > max else max
        print(source + ";", end="");

    print()
    for i in range(0, max):
        for source in store.keys():
            property = ""
            if (i < len(store[source])):
                property = store[source][i]
            print(property + ";", end="");
        print()

def report(host, query, size):
    report_registers = get_registers(host, query, size)
    report_data = get_report(report_registers)
    print_info_report(report_registers)
    return report_data

def print_report_all():
    size = 120000
    host = constants.HOST_LEMMINGS
    data = report(host, queries.QUERY_ALL, size)
    print_csv(data)

def print_report_by_source():

    #Configuration
    size = 120000
    host = constants.HOST_LEMMINGS

    queries.QUERY_BY_SOURCE['query']['bool']['must'][1]['range']['createdAt']['gte'] = "01/11/2018"
    queries.QUERY_BY_SOURCE['query']['bool']['must'][1]['range']['createdAt']['lte'] = "01/01/2020"

    store = {}

    #BySource
    for source in constants.SOURCES:
        print(source)
        queries.QUERY_BY_SOURCE['query']['bool']['must'][0]['term']['metadata.source'] = source
        data = report(host, queries.QUERY_BY_SOURCE, size)
        if source not in data:
            data[source] = []
        store.update(data)

    print_csv(store)



print_report_by_source()
#print_report_all()