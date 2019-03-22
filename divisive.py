import numpy as np
from scipy.cluster.hierarchy import dendrogram
import pickle
import matplotlib.pyplot as plt
pkl_file = open("./pkl_files/matrix1.pkl","rb")
distance_matrix = pickle.load(pkl_file)

temp_file=open('./pkl_files/seq.pkl', 'rb')
seq=pickle.load(temp_file)

count1 = 0
keys={}

for i in seq:
    keys[count1]=i
    count1=count1+1

clusters={}
max_clusters=distance_matrix.shape[0]

clusters[2*max_clusters-2]=list(range(max_clusters))

link=np.zeros([max_clusters-1, 4])


def enddivisive():
    if len(clusters) >= max_clusters:
        return True
    return False

def max_distance(cluster_number):
    cluster_diameters={k:(len(v)<1)*(-1)+(len(v)>1)*np.max(distance_matrix[np.ix_(v,v)]) for k,v in clusters.items()}
    max_index=max(cluster_diameters, key=cluster_diameters.get)
    avg_within_cluster_distances={pt:(np.sum(distance_matrix[np.ix_(clusters[max_index], [pt])])/(len(clusters[max_index])-1)) for pt in clusters[max_index]}
    split_index=max(avg_within_cluster_distances, key=avg_within_cluster_distances.get)
    cluster_number=cluster_number+1
    return max_index,split_index,cluster_number

def terminate():
    for j in clusters:
        if len(clusters[j]) > 1:
            return 1
    return 0

def make_linkage_function(cluster_1, cluster_2, dist, len_cluster_2):
    link[max_clusters-cluster_number-1, 0]=cluster_2
    link[max_clusters-cluster_number-1, 1]=cluster_1
    link[max_clusters-cluster_number-1, 2]=dist
    link[max_clusters-cluster_number-1, 3]=len_cluster_2


def divide(cluster_index,split_index,max_val,cluster_number):
    new_cluster=[split_index]
    clusters[cluster_index].remove(split_index)
    old_cluster=clusters[cluster_index]

    del clusters[cluster_index]

    old_dist={pt:np.mean(distance_matrix[np.ix_(old_cluster,[pt])]) for pt in old_cluster }
    split_dist={}
    for p in old_cluster:
        split_dist[p]=distance_matrix[p,split_index]

    difference={}
    for p in old_cluster:
        difference[p]=old_dist[p]-split_dist[p]
    
    for pt in old_cluster:
        if difference[pt]>0 and len(old_cluster)>1:
            new_cluster.append(pt)
            old_cluster.remove(pt)
    
    dist_bw_clusters=np.max(distance_matrix[np.ix_(old_cluster, new_cluster)])
    
    if len(old_cluster)==1:
        clusters[old_cluster[0]]=old_cluster
        orig_cluster_key=old_cluster[0]
    else:
        # print("old",old_cluster,max_val)
        max_val-=1
        clusters[max_val]=old_cluster
        orig_cluster_key=max_val

    if len(new_cluster)==1:
        clusters[new_cluster[0]]=new_cluster
        new_cluster_key=new_cluster[0]
    else:
        # print("new",old_cluster,max_val)
        max_val-=1
        clusters[max_val]=new_cluster
        new_cluster_key=max_val

    make_linkage_function(new_cluster_key, orig_cluster_key, dist_bw_clusters, len(new_cluster)+len(old_cluster))
    return max_val
    
max_index=2*max_clusters-2
count = 0
cluster_number=0
while terminate():
    cluster_index,split_index,cluster_number=max_distance(cluster_number)
    max_index=divide(cluster_index,split_index,max_index,cluster_number)
    count=count+1
fig=plt.figure(figsize=(20, 8))
plt.title("Dendrogram - Divisive Clustering")
labels=['temp']*len(keys)
for idx,label in keys.items():
    labels[idx]=label
labels=np.array(labels)
dendrogram(link, orientation='top', labels=labels)
fig.savefig('dendrogram_divisive.png')
print("Clustering Completed")
plt.show()
