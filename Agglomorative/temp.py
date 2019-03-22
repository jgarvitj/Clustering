import pickle
from distance import *
import itertools

main = [[0 for x in range(10)] for y in range(10)] 
hash_table = {}

count=1

seq = {}
seq[1] = "A"
seq[2] = "B"
seq[3] = "C"
seq[4] = "D"
seq[5] = "E"
seq[6] = "F"

for i in seq:
	hash_table[i]=seq[i]
print(hash_table)



def distance_matrix(seq):
	clusters = {}
	count = 0
	dist = [[0 for x in range(len(seq)+1)] for y in range(len(seq)+1)]
	for i in seq:
		l = []
		sim = {}
		for j in seq:
			if i!=j:
				# print(i)
				dist[i][j] = similarity(seq[i], seq[j])
		return dist

def clust_dist():
	

main = distance_matrix(seq)
dist = main

def min_dist(dist):
	mini = 100
	a = 0
	b = 0
	for i in range():
		for j in range():
			if mini > dist[i][j]:
				mini = dist[i][j]
				a = i
				b = j
	return mini, a, b

def form_clusters():
	mini, a, b = min_dist(dist)
	print(a)
	print(b)
	l = []
	l.append(a)
	l.append(b)
	clusters[count] = l
	del seq[a]
	if a!=b:
		del seq[b]
form_clusters()

# dist = distance_matrix(seq)
# print(dist)

prev_clusters = {}

count = 1

for i in hash_table:
	l = []
	l.append(i)
	prev_clusters[count] = l
	count = count+1

