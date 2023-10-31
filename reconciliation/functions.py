# !pip install requests
import requests

#!pip install SPARQLWrapper

from SPARQLWrapper import SPARQLWrapper, JSON
import ssl

#!pip install fuzzywuzzy
import difflib
# !pip install python-Levenshtein
# !pip install thefuzz
from fuzzywuzzy import fuzz
from fuzzywuzzy import process
# from thefuzz import fuzz
# from thefuzz import process
import json
import csv
import time #





def sparql_query_setting(query, endpoint):# set the endpoint 
    sparql = SPARQLWrapper(endpoint)
    # set the query
    sparql.setQuery(query)
    # set the returned format
    sparql.setReturnFormat(JSON)
    # get the results
    results = sparql.query().convert()
    return results



def wikidata_reconciliation(r, endpoint, q_class=None): # specify the class of which the individual should be instance of
# r = json results of the get request 
  # double check if the entity belongs to the right class
  if 'search' in r and len(r['search']) >= 1:
      if q_class: # if a class is given, it checkes if the wikidata entity belongs to the correct class. 
        query_string = """ASK {<"""+r['search'][0]['concepturi']+"""> wdt:P31 wd:"""+q_class+""". }"""
        res = sparql_query_setting(query_string, endpoint)
        # print("\nRES", query, query_string, res)
        if res["boolean"] == True: # add a timeout

          return [ r['search'][0]['concepturi'] , 'class_match']
        else:
          return [ r['search'][0]['concepturi'] , 'no_class_match']
      else:
        return [ r['search'][0]['concepturi'] , 'no_class_given']
  else:
      return 'not matched'

# having a dictionary containing q terms, query wd for asking its related terms in external vocabulary, as specified by the query.
def alignments_through_wd(dictionary, query, variable_list, endpoint, url_string): 
  all_items = dictionary.items() # ordered dict of tuples
  for item in all_items: # tuple with key-value pairs
    if type(item[1]) == list: 
      for el in item[1]: # item[1]
        if el.startswith("http://www.wikidata.org/entity/"): # in this way, we also filter automatically also the " rec" keys
          print(el, item[0])
          cleaned_el = el.replace("\"","")
          final_query = query.replace("toBeReplaced", cleaned_el)
          res = sparql_query_setting(final_query, endpoint)
          for result in res["results"]["bindings"]:
            for var in variable_list: 
              aligned = url_string+result[var]["value"]
              print(aligned)
              if aligned not in dictionary[item[0]]: 
                dictionary[item[0]].append(aligned)
  return(dictionary)
    
# function already present in the main script - remove/add terms from a dictionary
def remove_add_terms(dictionary, pair_list, instruction_string): # dictionary to be updated, list containing tuples with key-link to be removed
  for pair in pair_list: # pair[0] = name, pair[1] = value
   # print(pair)
    if instruction_string == "remove": 
      if pair[1] in dictionary[pair[0]]:
        dictionary[pair[0]].remove(pair[1])
    elif instruction_string == "add": 
      # if dictionary[pair[0]][0].startswith("http://icondataset.org/") and len(dictionary[pair[0]]) == 1: # we double check that the term is really without an alignment
      if len(dictionary[pair[0]]) <=1:
        dictionary[pair[0]] = [pair[1]]
  return dictionary

# mean of the fuzzywuzzy parameters for word similarity
def fuzz_ratio_mean(name, term):
  ratio1 = fuzz.ratio(name, term)
  ratio2 = fuzz.partial_ratio(name, term)
  ratio3 = fuzz.token_sort_ratio(name, term)
  ratio4 = fuzz.WRatio(name, term)
  mean = (ratio1+ratio2+ratio3+ratio4)/4
  return mean

# open dictionaries stored in json
def open_json(json_file): 
  with open(json_file, mode='r', encoding="utf-8") as jsonfile:
    dictName = json.load(jsonfile)
    return dictName

# save a dictionary in json
def store_in_json(file_name, dictName): 
  with open(file_name, mode='w', encoding="utf-8") as jsonfile:
    json.dump(dictName, jsonfile)


# stop words and others removal. After this passage: ready to reconcile

def rumor_removal(dictionary):
  for item in dictionary.items(): 
    if type(item[1]) == list: 
      for i in range(len(item[1])- 1, -1, -1): # len - 1 = last postition; start -1 = 0; move of -1
        if item[1][i].startswith("http") is False:
          del item[1][i]
  return(dictionary)

# store in csv

def store_csv(file_name, first_line, list_of_lists): 
    with open(file_name, mode='w', newline='', encoding='UTF-8') as my_file:
        file = csv.writer(my_file, delimiter=',', quotechar='"', quoting=csv.QUOTE_ALL)
        file.writerow(first_line) 
        for l in list_of_lists: 
            file.writerow(l) 
    return(file_name)

# store in csv
# input: list of tuples, where tup[0] is the name and tup[1] is the reconciled link
# store in a json where the first column is the name and the second column is a concat of all the values having that key, with " @ " as separator
def from_tup_to_csv(list_of_tup, file_name, first_line): 
    list_of_lists = []
    tot_dict = {}
    for tup in list_of_tup: 
        if tup[0] not in tot_dict: 
            tot_dict[tup[0]] = []
        tot_dict[tup[0]].append(tup[1])

    for item in tot_dict.items(): 
        list_of_lists.append([item[0], ' @ '.join(item[1])])
        
    with open(file_name, mode='w', newline='') as my_file:
        file = csv.writer(my_file, delimiter=',', quotechar='"', quoting=csv.QUOTE_ALL)
        file.writerow(first_line) 
        for l in list_of_lists: 
            file.writerow(l) 
    return(file_name) 

import csv

# from dict to csv: 
def store_dict_in_csv(file_name, first_line, dictionary):
    list_of_lists = []
    for tup in dictionary.items(): 
        if tup[0].endswith(" rec"): 
            col1 = tup[0].replace(" rec", "")
            if type(tup[1])== list:
                col2 = ' @ '.join(tup[1])
            else: 
                col2 = tup[1]
            list_of_lists.append([col1, col2])
    final = store_csv(file_name, first_line, list_of_lists)
    return final



# filtering

def filter_values(my_list):
    "query that iterate over a list, print the item and allows to input if the value is selected"
    yes = []
    no = []
    for i in my_list:
        confirm = input('Do you like this value?'+ str(i) + '(y/n):')
    if confirm == 'y':
          yes.append(i)
    else:
          no.append(i)
    return yes

def see_candidate(candidate_list): 
    "takes as input a list with the description of the candidate and allows a choice between yes and no" 
    confirm = input('Do you like this value?'+ str(candidate_list) + '(y/n):')
    return confirm