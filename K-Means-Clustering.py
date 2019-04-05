import numpy as np
import random
import hashlib
import matplotlib.pyplot as plt


#........................................................ 
# This code generates a class for data point where a
# data point is a (1,150) vector. 
#........................................................
class DataPoint():
	def __init__(self,c):
		self.c=c


#........................................................ 
# This code generates a class for a Cluster with the
# cluster object specifying the centroid for the cluster
# and an array of data points. The methods perform 
# operations on clusters.
#........................................................
class Cluster():


	def __init__(self,cent,dpArr,hash=None):
		self.cent=cent
		self.dpArr=dpArr
		self.hash=hash
	#........................................................ 
	# This function calculates the 'eucleidian distance' or 
	# L2-norm between the cluster centroid and data point
	#........................................................
	def dist(self,point):
		cent=self.cent
		# cent=np.array(cent)
		# point=np.array(point)
		ret= np.linalg.norm(cent-point)
		return ret

	#........................................................ 
	# This function calculates total sum of squares dist 
	# between each data-point in a cluster and its centroid 
	#........................................................
	def ssq(self):
		cent=self.cent
		dpArr=self.dpArr
		# cent=np.array(cent)
		# point=np.array(point)
		ret=0
		for i in dpArr:
			ret= ret + np.linalg.norm(cent-i)
		return ret

	#........................................................ 
	# This function prints data points in a cluster
	#........................................................
	def printClust(self):
		dpArr=self.dpArr
		for i in dpArr:
			print(i.val)
		print('.......')
	#........................................................ 
	# This function calculates the mean value of the data 
	# points in the cluster and assigns the value to the 
	# cluster object as its centroid. 
	#........................................................

	def calcCent(self):
		dpArr=self.dpArr
		dpArr=np.array(dpArr)
		cent=np.mean(dpArr, axis=0)
		self.cent=cent
		s=str(dpArr)
		hash=int(hashlib.sha256(s.encode('utf-8')).hexdigest(), 16)% 10**8
		self.hash=hash


#........................................................ 
# This function generates the random row numbers in 
# data point space to initialize the initial cluster 
# centers. 'num' specifies the number of clusters k
#........................................................
def genRandClusterCent(num):
	ret=[]
	for i in range(num):
		ret.append(random.randint(0,150))
	return ret

#........................................................ 
# This function generates the required input array 
# as specified by the question 
#........................................................

def genInput():
	# Initialize a zeros(150*150) array
	a=np.zeros([150,150])

	# Code to generate block diagonal array
	a[0:150,0:150]=0.3
	a[0:50,0:50]=0.7
	a[50:100,50:100]=0.7
	a[100:150,100:150]=0.7

	# Generate a random (150*150) array N
	b=np.random.rand(150,150)

	sh=np.shape(a)

	c=np.zeros([150,150])

	# Create data points array by applying conditions
	for i in range(sh[0]):
		for j in range(sh[1]):
			if b[i][j]>a[i][j]:
				c[i][j]=1
			else:
				c[i][j]=0

	
	# randomly permute the data point array rows
	np.random.shuffle(c)
	
	
	return c
#........................................................ 
# This function generates the required input array 
# as specified by the question 
#........................................................
def initialize(matrix):
	# print(matrix)
	ret=[]
	sh=np.shape(matrix)
	for i in range(sh[0]):
		
		x=DataPoint(matrix[i])
		ret.append(x)

	return ret

#........................................................ 
# MAIN CODE STARTS HERE 
#........................................................

# GENERATE DATA SPACE
matrix=(genInput())

# INITIALIZE AN ARRAY OF DATAPOINT OBJECTS
dataSpace=initialize(matrix)

# <................IMPORTANT...........................>
# In first case the number of clusters K=3

start_clus_centroid=genRandClusterCent(3)

# Initialize cluster array of 3 with their random 
# centroid values and empty data point array

clus_centroid=[]

for i in start_clus_centroid:
	x=Cluster(dataSpace[i].c,[],None)
	clus_centroid.append(x)
	


# Main k-means algorithm code starts here
while 1:

	# For comparing cluster datapoints array I am using hash value of 
	# the datapoint array of clusters in string form. The code below 
	# initializes a list of hash strings corresponding to each cluster
	hashCentroidList=[]
	for i in clus_centroid:
	
		hashCentroidList.append(i.hash)

	# Step 1: Assign each data point to closest cluster based on dist
	# from cluster centroid

	for i in dataSpace:
		minArr=[]
		for j in clus_centroid:
			# Calculate distance between cluster centroid and 
			# data point
			minArr.append(j.dist(i.c))

		# Get index of closest cluster
		ind=minArr.index(min(minArr))

		# Assign data point to closest cluster
		clus_centroid[ind].dpArr.append(i.c)

	# Step 2: Calculate mean of data point values and assign the mean 
	# value to cluster centroid

	for i in clus_centroid:
		i.calcCent()

	check=True

	# The following code compares the hash values of previous cluster 
	# datapoint array with latest. If they are same the K-means algorithm 
	# loop stops and returns the resultant clustering  

	for x in range(len(hashCentroidList)):
		# print(hashCentroidList[x])
		# print(clus_centroid[x].hash)
		if hashCentroidList[x]!=clus_centroid[x].hash:
			check=False
			break

	if check==True:
		break




f=open('k3clustering.txt','w+')

for i in range(len(clus_centroid)):
	f.write('....................................................................................................')
	f.write('\n')
	f.write('Cluster '+str(i+1))
	f.write('\n')
	for j in clus_centroid[i].dpArr:
		f.write(str(j))
		f.write('\n')


f.close()	

# <......................IMPORTANT...........................>
# In second case the number of clusters varies from k=2 to 10
yaxis=[]
xaxis=[]

for num in range(2,11):


	start_clus_centroid=genRandClusterCent(num)

	# Initialize cluster array of 'num' values with their random 
	# centroid values and empty data point array

	clus_centroid=[]

	for i in start_clus_centroid:
		x=Cluster(dataSpace[i].c,[],None)
		clus_centroid.append(x)
		


	# Main k-means algorithm code starts here
	while 1:

		# For comparing cluster datapoints array I am using hash value of 
		# the datapoint array of clusters in string form. The code below 
		# initializes a list of hash strings corresponding to each cluster
		hashCentroidList=[]
		for i in clus_centroid:
		
			hashCentroidList.append(i.hash)

		# Step 1: Assign each data point to closest cluster based on dist
		# from cluster centroid

		for i in dataSpace:
			minArr=[]
			for j in clus_centroid:
				# Calculate distance between cluster centroid and 
				# data point
				minArr.append(j.dist(i.c))

			# Get index of closest cluster
			ind=minArr.index(min(minArr))

			# Assign data point to closest cluster
			clus_centroid[ind].dpArr.append(i.c)

		# Step 2: Calculate mean of data point values and assign the mean 
		# value to cluster centroid

		for i in clus_centroid:
			i.calcCent()

		check=True

		# The following code compares the hash values of previous cluster 
		# datapoint array with latest. If they are same the K-means algorithm 
		# loop stops and returns the resultant clustering  

		for x in range(len(hashCentroidList)):
			# print(hashCentroidList[x])
			# print(clus_centroid[x].hash)
			if hashCentroidList[x]!=clus_centroid[x].hash:
				check=False
				break

		if check==True:
			break


	sm=0

	# Code below calculates the sum of squared dist between each cluster 
	# centroid and its respective data points 
	for i in clus_centroid:
		sm=sm+i.ssq()
	
	xaxis.append(num)
	yaxis.append(sm)

# Following code generates the plot of the K-values in x axis with 
# sum of square dist in y axis

plt.plot(xaxis, yaxis, 'ro')
plt.axis([1, 11, min(yaxis)-1000,max(yaxis)+1000])
plt.show()





