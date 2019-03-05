QUERY_ALL = {
    "query": {
        "range": {
            "createdAt": {"gte": "01/01/2018","lte": "01/02/2018", "format": "dd/MM/yyyy||dd/MM/yyyy"}
        }
    }
}

QUERY_BY_SOURCE ={
  "query": {
    "bool":
    {
      "must": [
        {
          "term": {
            "metadata.source": "EBAY"
          }
        },

        { "range": {
          "createdAt": {
            "gte": "01/01/2018",
            "lte": "01/02/2018",
            "format": "dd/MM/yyyy||dd/MM/yyyy"
          }
        }
        }
      ]
    }
  }
}
