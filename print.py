import queries
import constants
import time
from report import generate_report


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
    time_name = time.strftime("%Y%m%d-%H%M%S")
    file = open('/Users/valbuena/Documents/shipment-'+ time_name + '.csv', 'w')
    max = 0
    for source in store.keys():
        store[source] = list(sorted(store[source]))
        length = len(store[source])
        max = length if length > max else max
        file.write(source + ";")

    file.write("\n")
    for i in range(0, max):
        for source in store.keys():
            property = ""
            if (i < len(store[source])):
                property = store[source][i]
            file.write(property + ";")
        file.write("\n")

    file.close()


def print_report_all():
    size = 100
    host = constants.HOST_LEMMINGS
    data = generate_report(host, queries.QUERY_ALL, size)
    print_csv(data)


def print_report_by_source():

    #Configuration
    size = 100
    host = constants.HOST_LEMMINGS

    queries.QUERY_BY_SOURCE['query']['bool']['must'][1]['range']['createdAt']['gte'] = "01/11/2018"
    queries.QUERY_BY_SOURCE['query']['bool']['must'][1]['range']['createdAt']['lte'] = "01/01/2020"

    store = {}

    #BySource
    for source in constants.SOURCES:
        print(source)
        queries.QUERY_BY_SOURCE['query']['bool']['must'][0]['term']['metadata.source'] = source
        data = generate_report(host, queries.QUERY_BY_SOURCE, size)
        if source not in data:
            data[source] = []
        store.update(data)

    print_csv(store)

#print_report_by_source()
print_report_all()