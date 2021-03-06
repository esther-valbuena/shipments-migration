import config

from elasticsearch import Elasticsearch

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


def get_registers(query):
    es = Elasticsearch(
        [config.DEFAULT_HOST],
        retry_on_timeout=True,
        timeout = config.DEFAULT_TIMEOUT
    )
    registers = {}
    try:
        result = es.search(index="shipments", doc_type="shipment", size=config.DEFAULT_SIZE, body=query)
        registers = result['hits']['hits']
    except:
        print('Query fail')

    return registers



def get_list_keys(element):
    if len(element) > 0:
        father_keys = []
        for key, value in element.items():
            if is_father(value): #node dictionary or list
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
        key = config.get_key(doc)
        values = config.get_value(doc)
        if  (values is not None) and (len(values) > 0):
            old_list_values = data.get(key, set())
            list_keys = get_list_keys(values)
            old_list_values |= set(list_keys)
            data[key] = old_list_values
    return data


def generate_report(query):
    report_registers = get_registers(query)
    report_data = get_report(report_registers)
    return report_data







