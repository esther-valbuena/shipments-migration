SOURCES = ["ebay_inbound", "PRO","COM", "amazon_inbound", "API", "module_prestashop", "module_woocommerce", "EBAY", "epages_strato_inbound", "csv_inbound", "epages_1and1eu_inbound", "catawiki_inbound", "epages_epages_inbound", "prestashop_inbound", "mirakl_eprice_inbound", "epages_arsys_inbound", "mirakl_pernod_ricard_inbound", "wizishop_inbound", "epages_hosteurope_inbound", "module_zencart", "RiderUnik.com", "Otakubox", "mirakl_creavea_inbound", "source_inbound", "eutradepoint.com", "epages_sage_inbound", "merkatea", "module_magento", "woocommerce_inbound", "module_citizenkid", "PHP API TEST", "prestasop", "ebay", "eutradepoint_inbound", "prestashop_module"]

HOST_LEMMINGS = "http://elasticsearch-9200.service.consul:27777/"
HOST_LOCAL = "http://elasticsearch-9200.service.consul:9200/"


def get_key(doc):
    #return doc['_source']['metadata']['source']
    return doc['_source']['currency']

def get_value(doc):
    return doc['_source']
    #return doc['_source']['price']
    #return doc['_source']['additionalData']


DEFAULT_TIMEOUT = 60
DEFAULT_SIZE = 1500000
DEFAULT_HOST = HOST_LEMMINGS
DEFAULT_PATH = "/Users/valbuena/Documents/"
