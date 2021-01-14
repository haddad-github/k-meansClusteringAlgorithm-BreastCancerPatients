import random
import math
import statistics
import matplotlib.pyplot as plt

#k = clusters; N = nombre points; f = features; max_ite = nombre iterations
k = 3
N = 200
f = 2
max_ite = 100

#Generer des donnees synthetiques
def generateData(N, k):

    #donnees (liste de tuples)
    G = []

    #constantes pour distanciation 
    cx = [random.randrange(0, k) for i in range(k)]
    cy = [random.randrange(0, k) for i in range(k)]

    #points (x,y)
    for i in range(k):
        x = []
        y = []

    for n in range(N):
        x += [random.random() + cx[i]]
        y += [random.random() + cy[i]]

    #mettre coordonnees dans G (donnees)
    for b in x:
        G += [(b, y[x.index(b)])]

    #plot donnees
    plt.plot(x, y, "o")
    plt.show()

    return G

X = generateData(N, k)

#Initialiser clusters
def initClusters(k, N, X):

    clusters = {}  #dictionnaire
    for i in range(k):  #nombre de clusters
        clusters[i] = []  #assigner clefs clusters (0,1,2,..)

    for x in X:  #pour sous-ensemble dans ensemble de points
        clusters[random.randrange(0, k)] += [x]  #[clusterk][point]

    return clusters

clusters = initClusters(k, N, X)

#Mise-a-jours des centroides
def updateCentroids(clusters, k, f):
    #dictionnaire qui calcule les moyennes de chaques features
    centroids = {}
    for i in range(k):
        centroids[i] = {}
    for i in range(k):
        for j in range(f):
            centroids[i][j] = []
    
    #exemple de fonctionnement: 
    #centroids[0] = cluster 0
    #centroids[0][0] = x
    #centroids[0][1] = y

    #dictionnaire qui va contenir les centroides en liste par rapport à leur cluster
    Centroids = {}
    for i in range(k):
        Centroids[i] = []

    #creation de liste pour chaque feature pour chaque cluster
    for i in range(k):
        for n in range(len(clusters[i])):
            for j in range(f):
                tmp = [clusters[i][n][j]]
                centroids[i][j] += tmp
    #calcul de la moyenne de chaque features
    for i in range(k):
        for j in range(f):
            centroids[i][j] = [statistics.mean(centroids[i][j])]

    #convertir les dictionaires de features en une liste par clusters
    for i in range(k):
        for j in range(f):
            for l in range(1):
                Centroids[i] += [centroids[i][j][l]]

    return Centroids

cent = updateCentroids(clusters, k, f)

#Calcul de la distance eucledienne
def euclideanDistance(cent, X):
    tmp = []

    for i in range(len(cent)):
        tmp += [((cent[i] - X[i])**2)]

    ED = sum(tmp)

    return math.sqrt(ED)

dist = euclideanDistance(cent[1], X[1])

#Assigner points aux clusters
def assignCluster(cent, X, k):

    #clusters
    assign = {}
    for i in range(k):
        assign[i] = []

    #calcul distance point et centroid
    for x in range(len(X)):
        distance = []
        for c in range(k):
            distance += [euclideanDistance(cent[c], X[x])]

        assign[distance.index(min(distance))] += [X[x]]

    return assign

assign = assignCluster(cent, X, k)

#Algorithme kmeans
def kmeans(max_ite, k, data):
    #initialiser variables
    data = X
    N = len(X)  #nombre points = longueur data generee
    f = len(X[0])  #feature = len du tuple (x,y) = 2; (x,y,z) = 3

    #initialiser clusters
    init = initClusters(k, N, X)
    cent = updateCentroids(init, k, f)

    #iteration
    i = 0
    while i != max_ite:
        clust = assignCluster(cent, X, k)
        cent = updateCentroids(clust, k, f)

        i += 1
    return clust, cent

kmeans = kmeans(max_ite, k, X)


#plot Clusters sans centroides

def plotClusters():
    #cluster1
    x0 = []
    y0 = []
    #cluster2
    x1 = []
    y1 = []
    #cluster3
    x2 = []
    y2 = []

    #creation d'une liste des features du cluster 1
    for i in range(len(kmeans[0][0])):
        x0 += [kmeans[0][0][i][0]]
        y0 += [kmeans[0][0][i][1]]
    #creation d'une liste des features du cluster 2
    for i in range(len(kmeans[0][1])):
        x1 += [kmeans[0][1][i][0]]
        y1 += [kmeans[0][1][i][1]]
     #creation d'une liste des features du cluster 3
    for i in range(len(kmeans[0][2])):
        x2 += [kmeans[0][2][i][0]]
        y2 += [kmeans[0][2][i][1]]

    plt.plot(x0, y0, "o", color="red")
    plt.plot(x1, y1, "o", color="blue")
    plt.plot(x2, y2, "o", color="green")
    
    plt.show()

plotClusters()

#plot clusters avec Centroids
def plotCentroids():
    #clusters1
    x0 = []
    y0 = []
    #clusters2
    x1 = []
    y1 = []
    #clusters3
    x2 = []
    y2 = []
    #centroides
    cent0x = [kmeans[1][0][0]]
    cent0y = [kmeans[1][0][1]]
    cent1x = [kmeans[1][1][0]]
    cent1y = [kmeans[1][1][1]]
    cent2x = [kmeans[1][2][0]]
    cent2y = [kmeans[1][2][1]]

    #creation d'une liste des features du cluster 1
    for i in range(len(kmeans[0][0])):
        x0 += [kmeans[0][0][i][0]]
        y0 += [kmeans[0][0][i][1]]
    #creation d'une liste des features du cluster 2
    for i in range(len(kmeans[0][1])):
        x1 += [kmeans[0][1][i][0]]
        y1 += [kmeans[0][1][i][1]]
     #creation d'une liste des features du cluster 3
    for i in range(len(kmeans[0][2])):
        x2 += [kmeans[0][2][i][0]]
        y2 += [kmeans[0][2][i][1]]

    plt.plot(x0, y0, "o", color="red")
    plt.plot(x1, y1, "o", color="blue")
    plt.plot(x2, y2, "o", color="green")
    plt.plot(cent0x, cent0y, "*", markersize=10, color="crimson")
    plt.plot(cent1x, cent1y, "*", markersize=10, color="cyan")
    plt.plot(cent2x, cent2y, "*", markersize=10, color="lime")

    plt.show()


plotCentroids()
