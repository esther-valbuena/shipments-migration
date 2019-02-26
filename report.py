import queries
import config
from elasticsearch import Elasticsearch


def get_registers(host, query):
    es = Elasticsearch(
        [host]
    )
    registers = es.search(index="shipments", doc_type="shipment", size=1, body=query)
    return registers['hits']['hits']


def is_father_value(father):
    return isinstance(father, dict) or \
           (isinstance(father, list) and len(father) > 0 and isinstance(father[0], dict))


def get_father_element(father):
    if isinstance(father, list):
        return father[0]
    else:
        return father


def get_father_separator(father):
    if isinstance(father, list):
        return "@"
    else:
        return "."


def get_list_keys(element):
    if len(element) > 0:
        father_keys = []
        for key, value in element.items():
            if isinstance(value, dict):
                child_keys = get_list_keys(value)
                father_keys.extend([key + "." + child for child in child_keys])
            # elif isinstance(value, list):
            #     child_keys = get_list_keys(value[0])
            #     father_keys.extend([key + "@" + child for child in child_keys])
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
            print(get_list_keys(additional_data))
            old_list_additional = data.get(key.upper(), set())
            old_list_additional |= set(additional_data.keys())
            data[key.upper()] = old_list_additional
    return data


def print_info_report(registers):
    print('------')
    print("%d documents found" % len(registers))
    print('------')


def print_head_report(data):
    print('------')
    print("TOTAL SOURCE =>" + str(len(data)))
    print(list(data.keys()))
    print(data)
    print('------')


def print_rows_report(data):
    for source in data:
        print(source + " => " + str(len(data[source])))
        print(sorted(data[source]))


def main():
    report_registers = get_registers(config.HOST_LEMMINGS, queries.QUERY_ALL)
    report_data = get_report(report_registers)
    print_info_report(report_registers)
    print_head_report(report_data)
    print_rows_report(report_data)


main()
