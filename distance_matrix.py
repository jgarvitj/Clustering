from distance import similarity
import pickle
import itertools
from multiprocessing.pool import ThreadPool
import numpy as np
from time import time

temp_file=open('./pkl_files/seq.pkl', 'rb')
seq=pickle.load(temp_file)

count = 0
keys={}

print(len(seq))

for i in seq:
    keys[count]=i
    count=count+1

print(keys)
dist_matrix=np.ones([len(seq),len(seq)])

def dist(i):
    start=time()
    dist_matrix[i[0]][i[1]]=similarity(seq[keys[i[0]]],seq[keys[i[1]]])
    print(time()-start)

keys_pair=list(itertools.product(range(len(seq)), range(len(seq))))
pool=ThreadPool()
pool.map(lambda x: dist(x), keys_pair)

print(dist_matrix)

output=open("./pkl_files/matrix2.pkl",'wb')
pickle.dump(dist_matrix,output)