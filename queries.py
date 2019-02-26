QUERY_ALL = {
    "query": {
        "range": {
            "createdAt": {"gte": "01/01/2019","lte": "01/01/2020", "format": "dd/MM/yyyy||dd/MM/yyyy"}
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
            "metadata.source": "COM"
          }
        },

        { "range": {
          "createdAt": {
            "gte": "01/01/2019",
            "lte": "01/01/2020",
            "format": "dd/MM/yyyy||dd/MM/yyyy"
          }
        }
        }
      ]
    }
  }
}