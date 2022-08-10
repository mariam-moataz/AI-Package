# coding: utf-8

# In[1]:

import numpy as np
from sklearn.cluster import DBSCAN
from sklearn.datasets import make_blobs
from sklearn.preprocessing import StandardScaler

# In[2]:

# for making density data
centers = [[1, 1], [-1, -1], [1, -1]]
X, labels_true = make_blobs(n_samples=1500, centers=centers, cluster_std=0.4, random_state=0)
X = StandardScaler().fit_transform(X)

# In[3]:

visited = [False for i in range(X.shape[0])]
labels = [-1 for i in range(X.shape[0])]


# In[4]:

def MyDBSCAN(D, eps, MinPts):
    """
    Cluster the dataset `D` using the DBSCAN algorithm.

    MyDBSCAN takes a dataset `D` (a list of vectors), a threshold distance
    `eps`, and a required number of points `MinPts`.

    It will return a list of cluster labels. The label -1 means noise, and then
    the clusters are numbered starting from 1.
    """
    # This list will hold the final cluster assignment for each point in D.
    # There are two reserved values:
    #    -1 - Indicates a noise point
    #     0 - Means the point hasn't been considered yet.
    # Initially all labels are 0.

    C = 0

    for i in range(D.shape[0]):

        if visited[i] is False:

            visited[i] = True

            sphere_points = regionQuery(D, D[i], eps)  # indexes

            if len(sphere_points) >= MinPts:
                C += 1

                growCluster(D, i, sphere_points, C, eps, MinPts)

    return labels


# In[5]:

def growCluster(D, P, NeighborPts, C, eps, MinPts):
    """
    Grow a new cluster with label `C` from the seed point `P`.

    This function searches through the dataset to find all points that belong
    to this new cluster. When this function returns, cluster `C` is complete.

    Parameters:
      `D`      - The dataset (a list of vectors)
      `labels` - List storing the cluster labels for all dataset points
      `P`      - Index of the seed point for this new cluster
      `NeighborPts` - All of the neighbors of `P`
      `C`      - The label for this new cluster.
      `eps`    - Threshold distance
      `MinPts` - Minimum required number of neighbors
    """

    labels[P] = C

    for j in NeighborPts:

        if visited[j] is False:

            visited[j] = True

            expanded_sphere_points = regionQuery(D, D[j], eps)  # indexes

            if len(expanded_sphere_points) >= MinPts:
                NeighborPts += expanded_sphere_points

            if labels[j] == -1:
                labels[j] = C

    pass


# In[6]:

def regionQuery(D, P, eps):
    """
    Find all points in dataset `D` within distance `eps` of point `P`.

    This function calculates the distance between a point P and every other
    point in the dataset, and then returns only those points which are within a
    threshold distance `eps`.
    """
    region_points = []

    for i in range(D.shape[0]):

        distance = np.sqrt(pow((P[0]) - (D[i][0]), 2) + pow((P[1]) - (D[i][1]), 2))

        if distance <= eps:
            region_points.append(i)

    return region_points


# In[7]:

my_labels = MyDBSCAN(X, eps=0.3, MinPts=10)
print(my_labels)

# In[8]:

# built in DBSCAN Function
db = DBSCAN(eps=0.3, min_samples=10).fit(X)
skl_labels = db.labels_
print(skl_labels)

# In[9]:

# Scikit learn uses -1 to for NOISE, and starts cluster labeling at 0. I start
# numbering at 1, so increment the skl cluster numbers by 1.
for i in range(0, len(skl_labels)):
    if not skl_labels[i] == -1:
        skl_labels[i] += 1

print(skl_labels)

# In[10]:

num_disagree = 0
# ---------------------------------
# compare built in and custom made dbsan function
# Go through each label and make sure they match (print the labels if they
# don't)
for i in range(0, len(skl_labels)):
    if not skl_labels[i] == my_labels[i]:
        print('Scikit learn:', skl_labels[i], 'mine:', my_labels[i])
        num_disagree += 1

if num_disagree == 0:
    print('PASS - All labels match!')
else:
    print('FAIL -', num_disagree, 'labels don\'t match.')

# In[ ]:



