import pickle
import numpy as np
from scipy.cluster.hierarchy import dendrogram,is_valid_linkage
import matplotlib.pyplot as plt
import time

start=time.time()
pkl_file=open("../pkl_files/seq.pkl","rb")
seq=pickle.load(pkl_file)
pkl_file.close()

count1=0
keys={}

for i in seq:
    keys[count1]=i
    count1=count1+1

pkl_file=open("../pkl_files/matrix.pkl","rb")
dist=pickle.load(pkl_file)
pkl_file.close()

max_clusters=dist.shape[0]
link = np.zeros([max_clusters-1, 4])


prev_clusters = {}

count = 0

#first set of clusters containing one element each.
for i in seq:
	prev_clusters[count] = [count]
	count = count+1


def cluster_dist(cl1, cl2, type):
	'''find distance between two clusters based on
		single linkage, complete linkage, and centroid method.
	'''
	val = 0
	if type == "min":
		val = 10000
		for i in cl1:
			for j in cl2:
				if (dist[i][j] < val):
					val = dist[i][j]
					
	if type == "max":
		for i in cl1:
			for j in cl2:
				if (dist[i][j] > val):
					val = dist[i][j]

	if type == "centroid":
		for i in cl1:
			for j in cl2:
				val+=dist[i][j]
		length = len(cl1)*len(cl2)
		val = val/length
	return val

#linkage function to form dendogram
def make_linkage_function(cluster_1, cluster_2, dist, len_cluster_2):
    link[cluster_number, 0]=cluster_2
    link[cluster_number, 1]=cluster_1
    link[cluster_number, 2]=dist
    link[cluster_number, 3]=len_cluster_2

def form_clusters(prev_clusters, cluster_number,max_index):
	'''
	Merge two from n clusters with closest distance to form n-1 clusters
	'''
	count = 0
	vis = [0]*320

	merge_index_1 = 0
	merge_index_2 = 0
	mini = 10000
	
	#find clusters with min distance in between
	for i in prev_clusters:
		for j in prev_clusters:
			cl1 = prev_clusters[i]
			cl2 = prev_clusters[j]
			if i!=j and (cluster_dist(cl1, cl2, "min")<mini):
				mini = cluster_dist(cl1, cl2, "min")
				merge_index_1 = i
				merge_index_2 = j

	l = []
	flag1 = 0
	flag2 = 0
	

	#merge clusters with min distance
	if merge_index_1!=merge_index_2:
		for j in prev_clusters[merge_index_1]:
			if vis[j] == 0:
				vis[j] = 1
				l.append(j)
				flag1 = 1
				
		for k in prev_clusters[merge_index_2]:
			if vis[k] == 0:
				vis[k] = 1
				l.append(k)
				flag2 = 1
				
		if flag1==1 & flag2==1:
			prev_clusters[max_index] = l
			max_index=max_index+1
			count = count+1

	x=len(prev_clusters[merge_index_1])+len(prev_clusters[merge_index_2])	

	#delete already merged clusters from original cluster set
	del prev_clusters[merge_index_1]
	del prev_clusters[merge_index_2]	

	

	make_linkage_function(merge_index_1, merge_index_2, mini, x)
	
	return prev_clusters,max_index

cluster_number = 0
max_index=311
count =0

while len(prev_clusters)!=1:
	prev_clusters,max_index = form_clusters(prev_clusters, cluster_number,max_index)
	count = count + 1
	cluster_number = cluster_number+1

stop=time.time()

print(stop-start)
output=open("../pkl_files/temp.pkl",'wb')
pickle.dump(link,output)
output.close()
print(link[0])
fig=plt.figure(figsize=(16, 9))
plt.title("Dendrogram - Agglomerative Clustering")
labels=['temp']*len(keys)
for idx,label in keys.items():
    labels[idx]=label
labels=np.array(labels)
dendrogram(link, orientation='top', labels=labels)
fig.savefig('dendrogram_divisive.png')
print("Clustering Completed")
plt.show()
					
