from flask import Flask, request
import requests 
import numpy as np
import json
from nltk.stem import PorterStemmer
from scipy.sparse import lil_matrix, csc_matrix
import sys

if len(sys.argv) == 1:
    npzfile = np.load("sparse_matrix_csc.npz")
    data = npzfile['data']
    indices = npzfile['indices']
    indptr = npzfile['indptr']
    shape = tuple(npzfile['shape'])
    sparse_matrix_csc = csc_matrix((data, indices, indptr), shape = shape)
else:
    #if sys.argv[1] not in [100, ]
    U = np.load("U"+sys.argv[1]+".npy")
    s = np.load("s"+sys.argv[1]+".npy")
    V = np.load("V"+sys.argv[1]+".npy")

app = Flask(__name__)

portet = PorterStemmer()





with open("empty_bag_of_words.txt", 'r') as file:
    empty_bag_of_words = json.loads(file.read())
with open("set_of_words.txt", 'r') as file:
    set_of_words = set(json.loads(file.read()))
with open("documents_index_map.txt", 'r') as file:
    documents_index_map = json.loads(file.read())

def fetch_prompt(prompt):
    prompt_vector = lil_matrix((1,len(empty_bag_of_words)), dtype=np.float64)
    prompt_bag_of_words = {key : 0 for key in empty_bag_of_words.keys()}
    for word in prompt.split():
        stemmed_word = portet.stem(word)
        if stemmed_word in set_of_words:
            prompt_bag_of_words[stemmed_word] += 1
    column_norm = 0
    column_idx = []
    for index, word in enumerate(empty_bag_of_words):
        if prompt_bag_of_words[word] != 0:
            prompt_vector[0,index] = prompt_bag_of_words[word] 

            column_norm += prompt_vector[0,index]**2
            column_idx.append(index)
    column_norm = np.sqrt(column_norm)
    for i in column_idx:
        prompt_vector[0,i] /= column_norm    
    if len(sys.argv) == 1:
        qA = prompt_vector@sparse_matrix_csc
    else:
        s_diag = np.diag(s)
        qA = ((prompt_vector@U)@s_diag)@V
    resultMap = {}
    if len(sys.argv) == 1:
        index_element_tuples = sorted(zip(qA.indices,qA.data), key = lambda x: x[1], reverse=True)
    else:
        indices = np.argsort(qA[0,:])[::-1]
        print(qA.shape)
        index_element_tuples = [[index, qA[0,index]] for index in indices]
    seen = []
    unique_tuples = []

    for tup in index_element_tuples:
        flag = True
        for x in seen:
            if x-tup[1]<10**-9:
                flag = False
        if(flag):
            unique_tuples.append(tup)
            seen.append(tup[1])
        if len(unique_tuples) == 10:
            break
    for index,value in unique_tuples[0:10]:
        #print(index, value)
        resultMap[documents_index_map[str(index)]] = value
    
    resultMap = [[k, v] for k,v in sorted(resultMap.items(), key=lambda x:x[1], reverse=True)]
    data = {
        "data" : resultMap
    }
    
    return json.dumps(data)

@app.route("/members")
def members():
    return {"members": ["Member1", "Member2", "Member3"]}

@app.route("/prompt", methods=["GET", "POST"])
def prompt():
    fetched_prompt = fetch_prompt(request.json.get('text'))
    if fetched_prompt:
        return fetched_prompt
    else:
        return "Failed to fetch prompt"

if __name__ == "__main__":
    
    app.run(debug=True)
    