import queries
import config
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

def print_csv(store, name):
    time_name = time.strftime("%Y%m%d-%H%M%S")
    file = open(config.DEFAULT_PATH + 'shipment-' + name + '-' + time_name + '.csv', 'w')
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
    data = generate_report(queries.QUERY_ALL)
    print_csv(data, 'all')


def print_report_by_source():

    store = {}
    queries.QUERY_BY_SOURCE['query']['bool']['must'][1]['range']['createdAt']['gte'] = "01/11/2018"
    queries.QUERY_BY_SOURCE['query']['bool']['must'][1]['range']['createdAt']['lte'] = "01/01/2020"

    #BySource
    for source in config.SOURCES:
        print(source)
        queries.QUERY_BY_SOURCE['query']['bool']['must'][0]['term']['metadata.source'] = source
        data = generate_report(queries.QUERY_BY_SOURCE)
        if source not in data:
            data[source] = []
        store.update(data)

    print_csv(store, 'by_source')

print_report_by_source()
print_report_all()