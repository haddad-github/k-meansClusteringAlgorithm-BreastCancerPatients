import random
import math
import statistics

#fonction de mettre un .txt en une liste
def readFile(filename):
	contenu = open(filename, "r")
	lecture = contenu.read()
	lecture2 = lecture.split()

	return lecture2

subtype = readFile("patient_subtype.txt")

#initiation des variables
basal = 0
luma = 0
lumb = 0
her2 = 0
normal = 0

#calcul du nombre de patient par sous-types
for type in subtype:
  if type == 'Basal':
    basal += 1
  elif type == "LumA":
    luma += 1
  elif type == "LumB":
    lumb += 1
  elif type == "Her2":
    her2 += 1
  elif type == "Normal":
    normal += 1
print('DONNEES THEORIQUES')  
print("Basal:", basal)
print("LumA:", luma)
print("LumB:", lumb)
print("Her2:", her2)
print("Normal:", normal)
print("Total patients:", basal+luma+lumb+her2+normal)


#fonction de faire une liste avec chaque lignes d'un .txt dans un liste
def parseRNA(filename):
  #ouverture du .txt
  content = open(filename, "r")
  lignes = content.readlines()
  #initier la variable
  RNA = []
  #sortir chaque ligne dans une liste de liste
  for ligne in lignes:
    ligne = ligne.strip()
    ligneSplit = ligne.split(" ")
    ligneSplit = [float(i) for i in ligneSplit]
    RNA.append(ligneSplit)
  
  return RNA

X = parseRNA("patient_expression.txt")

#Initiation des variables pour le kmean
k = 5
N = len(X)
f = len(X[0])
max_ite=1000

####################### KMEAN ###########################

#Initialiser clusters
def initClusters(k, N, X):

    clusters = {}  #dictonnaire
    for i in range(k): #nombre de clusters
        clusters[i] = []  #assigner clefs clusters (0,1,2..)

    for x in X:  #pour sous-ensemble dans ensemble de points
        clusters[random.randrange(0, k)] += [x] #[clusterk][point]

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

    #calcul de la moyenne pour chaque features de chaque cluster
    for i in range(k):
        for n in range(len(clusters[i])):
            for j in range(f):
                tmp = [clusters[i][n][j]]
                centroids[i][j] += tmp

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
    f = len(X[0])  #nombre de features

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

print('Nombre de genes par patient:',len(kmeans[0][0][0]), "\n")
print('DONNEES ITEREES')
print('Cluster1:',len(kmeans[0][0]))
print('Cluster2:',len(kmeans[0][1]))
print('Cluster3:',len(kmeans[0][2]))
print('Cluster4:',len(kmeans[0][3]))
print('Cluster5:',len(kmeans[0][4]))
