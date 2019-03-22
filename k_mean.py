import pickle
import math
import random

pkl_file = open("pkl_files/matrix1.pkl", 'rb')
distance_matrix = pickle.load(pkl_file)
pkl_file.close()

centroid_list = []
points = {}
def getKindexes(k):
    return random.sample(range(0,310),k)


def formClusters():
    points.clear()
    for i in centroid_list:
        points[i] = [i]
    '''
    takes each point checks if the point is a centroid prints the point and 
    if the point is not centroid then it is assigned to its nearest centroid
    '''
    for i in range(311):
        if i in points.keys():
            continue
        else:
            min = 10000
            for item in centroid_list:
                if min > distance_matrix[i][item]:
                    min = distance_matrix[i][item]
                    tmp = item
            points[tmp].append(i)
    return


def nxtIterations(num):
    if num == 1:
        return
    '''
    calculating centroids of the newly formed clusters
    '''
    #calculating eucladian distance of each point from the rest of the points of the cluster
    tmp = centroid_list.copy()
    centroid_list.clear()
    for i in points:
        l = len(points[i])
        min = 10000
        mini = i
        for item in points[i]:
            sum = 0
            for j in points[i]:
                sum = sum + (distance_matrix[j][item]*distance_matrix[j][item]/l)
            sum = math.sqrt(sum)
            if min > sum:
                min = sum
                mini = item
        centroid_list.append(mini)
    if tmp == centroid_list:
        print("Iteration %d centroids:"% (100-num+2),centroid_list)
        print("local minima found in %d iterations"% (100-num+2))
        return
    print("Iteration %d centroids:"% (100-num+2),centroid_list)
    formClusters()
    nxtIterations(num-1)


if __name__ == "__main__":
    #taking k as input
    k = input("enter k: ")
    k = int(k)
    # getting k index using random function
    centroid_list = getKindexes(k)
    print("Iteration 1 centroids: ",centroid_list)
    formClusters()
    nxtIterations(100)



            

            