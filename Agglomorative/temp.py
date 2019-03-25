import pickle
from distance import *
from scipy.cluster.hierarchy import dendrogram
import matplotlib.pyplot as plt

pkl_file=open("../pkl_files/seq.pkl","rb")
seq=pickle.load(pkl_file)
pkl_file.close()

pkl_file=open("../pkl_files/distance.pkl","rb")
dist=pickle.load(pkl_file)
pkl_file.close()

hash_table = {}

max_clusters=dist.shape[0]
link = np.zeros([max_clusters-1, 4])

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

def cluster_dist(cl1, cl2, type):
	val = 0
	if type == "min":
		val = 10000
		for i in cl1:
			for j in cl2:
				if (dist[hash_table[i]][hash_table[j]] < val):
					print(val, dist[hash_table[i]][hash_table[j]])
					val = dist[hash_table[i]][hash_table[j]]
					
	if type == "max":
		for i in cl1:
			for j in cl2:
				# print(hash_table[i], hash_table[j])
				if (dist[hash_table[i]][hash_table[j]] > val):
					# print(val, dist[hash_table[i]][hash_table[j]], len(cl1))
					val = dist[hash_table[i]][hash_table[j]]

	if type == "centroid":
    	for i in cl1:
			for j in cl2:
                val+=dist[hash_table[i]][hash_table[j]]
                length = len(cl1)*len(cl2)
        val = val/length
	# print(val)
	return val


def make_linkage_function(cluster_1, cluster_2, dist, len_cluster_2):
    link[max_clusters-cluster_number-2, 0]=cluster_2
    link[max_clusters-cluster_number-2, 1]=cluster_1
    link[max_clusters-cluster_number-2, 2]=dist
    link[max_clusters-cluster_number-2, 3]=len_cluster_2

def form_clusters(prev_clusters, cluster_number):
	new_clusters = {}
	count = 0
	vis = [0]*320
	
	a = 0
	b = 0
	mini = 1000
	# print(len(prev_clusters))
	for i in prev_clusters:
		# print(len(prev_clusters), len(prev_clusters[i]))
		for j in prev_clusters:
			cl1 = prev_clusters[i]
			cl2 = prev_clusters[j]
			# print(i, j)
			# print(len(prev_clusters), len(prev_clusters[i]))
			
			if i!=j and (cluster_dist(cl1, cl2, "max")<mini):
				# print(cluster_dist(cl1, cl2, "min"), mini)
				mini = cluster_dist(cl1, cl2, "max")
				a = i
				b = j
				
		
				
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
			new_clusters[a] = l
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
			new_clusters[i] = l
			count = count+1
	
	if len(new_clusters)!=len(prev_clusters):
		make_linkage_function(a, b, mini, len(new_clusters))
		# cluster_number = cluster_number+1
	print(cluster_number, len(new_clusters), "yaya")
	# print(l)
	return new_clusters

cluster_number = 0
new_clusters = form_clusters(prev_clusters, cluster_number)
cluster_number = cluster_number+1
# print(new_clusters)
# print(hash_table)
count = 1
# print(count, len(new_clusters))

while len(new_clusters)!=10:
	prev_clusters = new_clusters
	new_clusters = form_clusters(prev_clusters, cluster_number)
	# print(new_clusters)
	# print(count, len(new_clusters))
	count = count + 1
	cluster_number = cluster_number+1


# print(new_clusters)
for i in new_clusters:
	print(i, (new_clusters[i]))
output=open("../pkl_files/temp.pkl",'wb')
pickle.dump(link,output)
output.close()

					