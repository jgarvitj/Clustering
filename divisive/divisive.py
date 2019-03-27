import numpy as np
from scipy.cluster.hierarchy import dendrogram
import pickle
import matplotlib.pyplot as plt

#Distance Matrix
pkl_file = open("../pkl_files/matrix.pkl","rb")
distance_matrix = pickle.load(pkl_file)

temp_file=open('./pkl_files/seq.pkl', 'rb')
seq=pickle.load(temp_file)
import time
start = time.time()
count1 = 0
keys={}

#Hash_Table used for clusters
for i in seq:
    keys[count1]=i
    count1=count1+1

clusters={}

max_clusters=distance_matrix.shape[0]

#Intial Cluster i.e. One cluster which contains all the points
clusters[2*max_clusters-2]=list(range(max_clusters))

#Linkage Matrix Intialization
link=np.zeros([max_clusters-1, 4])


def enddivisive():
    if len(clusters) >= max_clusters:
        return True
    return False

'''
Function used to calculate the cluster which has maximum diameter and split index i.e. the index for which
cluster will be splitted. 
'''
def max_distance(cluster_number):
    #Makes a dictionary of every cluster_diamter 
    cluster_diameters={k:(len(v)<1)*(-1)+(len(v)>1)*np.max(distance_matrix[np.ix_(v,v)]) for k,v in clusters.items()}
    max_index=max(cluster_diameters, key=cluster_diameters.get)
    #Makes a dictionary of avg distance of that point in every cluster to calculate split index
    avg_within_cluster_distances={pt:(np.sum(distance_matrix[np.ix_(clusters[max_index], [pt])])/(len(clusters[max_index])-1)) for pt in clusters[max_index]}
    split_index=max(avg_within_cluster_distances, key=avg_within_cluster_distances.get)
    cluster_number=cluster_number+1
    return max_index,split_index,cluster_number

#Termination Condition for divisive
def terminate():
    for j in clusters:
        if len(clusters[j]) > 1:
            return 1
    return 0

#Insertion into linkage matrix for dendogram
def make_linkage_function(cluster_1, cluster_2, dist, len_cluster_2):
    link[max_clusters-cluster_number-1, 0]=cluster_2
    link[max_clusters-cluster_number-1, 1]=cluster_1
    link[max_clusters-cluster_number-1, 2]=dist
    link[max_clusters-cluster_number-1, 3]=len_cluster_2

'''
Function:
Input: 
Cluster_Index: Index to be splitted
Split_Index: Index on which cluster will be splitted
Max_Val: Index for linkage matrix
Cluster_Number: Number of Iteration for diana
Output:
Updates the cluster dictionary with splitted clusters and deletes the previous ones.
'''
def divide(cluster_index,split_index,max_val,cluster_number):
    #Makes a list of new Cluster and Old Cluster
    new_cluster=[split_index]
    clusters[cluster_index].remove(split_index)
    old_cluster=clusters[cluster_index]
    
    #Removes the cluster_index to be splitted
    del clusters[cluster_index]

    #Rearranging of cluster elements which are not splitted
    old_dist={pt:np.mean(distance_matrix[np.ix_(old_cluster,[pt])]) for pt in old_cluster }
    split_dist={}
    for p in old_cluster:
        split_dist[p]=distance_matrix[p,split_index]
    
    #Makes a dictionary to calculate the diiference between split_index and for every element remaining in clusters
    difference={}
    for p in old_cluster:
        difference[p]=old_dist[p]-split_dist[p]
    
    #Rearranges the cluster dictionary
    for pt in old_cluster:
        if difference[pt]>0 and len(old_cluster)>1:
            new_cluster.append(pt)
            old_cluster.remove(pt)
    #Dist b/w two clusters, value which need to added in linkage matrix
    dist_bw_clusters=np.max(distance_matrix[np.ix_(old_cluster, new_cluster)])
    
    #Updates cluster dictionary
    if len(old_cluster)==1:
        clusters[old_cluster[0]]=old_cluster
        orig_cluster_key=old_cluster[0]
    else:
        max_val-=1
        clusters[max_val]=old_cluster
        orig_cluster_key=max_val

    if len(new_cluster)==1:
        clusters[new_cluster[0]]=new_cluster
        new_cluster_key=new_cluster[0]
    else:
        max_val-=1
        clusters[max_val]=new_cluster
        new_cluster_key=max_val

    make_linkage_function(new_cluster_key, orig_cluster_key, dist_bw_clusters, len(new_cluster)+len(old_cluster))
    return max_val
    
max_index=2*max_clusters-2
count = 0
cluster_number=0

#Diana
while terminate():
    cluster_index,split_index,cluster_number=max_distance(cluster_number)
    max_index=divide(cluster_index,split_index,max_index,cluster_number)
    count=count+1
print(time.time()-start)

#Dendogram Plotting
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
