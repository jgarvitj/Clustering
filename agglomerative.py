import pickle
from distance import *
import itertools


pkl_file=open("../pkl_files/seq.pkl","rb")
seq=pickle.load(pkl_file)
pkl_file.close()

pkl_file=open("../pkl_files/distance.pkl","rb")
dist=pickle.load(pkl_file)
pkl_file.close()

hash_table = {}

count=0

for i in seq:
	if seq[i] not in hash_table:
		hash_table[seq[i]]=count
		count=count+1

# dist = [[0, 0.71, 5.66, 3.61, 4.24, 3.20], [0.71, 0, 4.95, 2.92, 3.54, 2.50], [5.66, 4.95, 0, 2.24, 3.54, 2.50], [3.61, 2.92, 2.24, 0, 1, 0.5], [4.24, 3.54, 1.41, 1, 0, 1.12], [3.20, 2.5, 2.5, 0.5, 1.12, 0]]
# print(dist)

prev_clusters = {}

count = 1

for i in seq:
	l = []
	l.append(seq[i])
	prev_clusters[count] = l
	count = count+1

# print(prev_clusters)

def form_clusters(prev_clusters):
	new_clusters = {}
	count = 0
	vis = [0]*320
	
	a = 0
	b = 0
	mini = 100000
	# print(len(prev_clusters))
	for i in prev_clusters:
		# print(i)
		for j in prev_clusters[i]:
			# print(hash_table[j])
			if vis[hash_table[j]]==0:
				for k in prev_clusters:
					for w in prev_clusters[k]:
						if vis[hash_table[w]]==0 and (dist[hash_table[j]][hash_table[w]] < mini) and i!=k and j!=w:
							mini = dist[hash_table[j]][hash_table[w]]
							a = i
							b = k
							# print(a, b, dist[hash_table[j]][hash_table[w]], mini, hash_table[j], hash_table[w])
	# print(dist)

	l = []
	flag1 = 0
	flag2 = 0
	# print(a, b)
	if a!=b:
		for j in prev_clusters[a]:
			if vis[hash_table[j]] == 0:
				vis[hash_table[j]] = 1
				l.append(j)
				flag1 = 1
				# print(l)
		for k in prev_clusters[b]:
			if vis[hash_table[k]] == 0:
				vis[hash_table[k]] = 1
				l.append(k)
				flag2 = 1
				# print(l)
		if flag1==1 & flag2==1:
			new_clusters[count] = l
			count = count+1
		# print(l)

	for i in prev_clusters:
		l = []
		flag = 0
		for j in prev_clusters[i]:
			# print(j, vis[j])
			if vis[hash_table[j]]==0:
				vis[hash_table[j]] = 1
				l.append(j)
				flag = 1
				# print("yaya")
		if flag==1:
			new_clusters[count] = l
			count = count+1
	# print(new_clusters)
	# print(l)
	return new_clusters


new_clusters = form_clusters(prev_clusters)
print(new_clusters)
# print(hash_table)
count = 1
print(count, len(new_clusters))

while len(new_clusters)!=1:
	prev_clusters = new_clusters
	new_clusters = form_clusters(prev_clusters)
	# print(new_clusters)
	print(count, len(new_clusters))
	count = count+1

print(new_clusters)
output=open("../pkl_files/agglo.pkl",'wb')
pickle.dump(new_clusters,output)
output.close()


