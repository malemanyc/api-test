# API

This API is intended to be used to parse sentences and extract and classify names from them.

The **POST** method will allow you to post an input sentence and you will get an **output in json format** with all names found and their classification.

## Usage

An input example could be the following:

* **curl -H "Content-Type: application/raw" -X POST -d "President Xi Jinping warned of the epidemic escalating outside the epicentre of Hubei province as more people travel and crowds gather across China." http://127.0.0.1:5000**




The output of the previous command is:

[

  {

    "entity": "place", 

    "name": "Hubei", 

    "position": 12

  }, 

  {

    "entity": "place", 

    "name": "China'", 

    "position": 22

  }, 

  {

    "entity": "person", 

    "name": "Xi Jinping", 

    "position": 1

  }

]

