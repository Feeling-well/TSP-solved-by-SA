# Main functions: To solve TSP problems, the code is translated from c++.

# Reference website: https://mp.weixin.qqq.com/s?_biz=MzIyNzg5MTQ5Mg=&mid=2247484213&idx=1&sn=1e7c4e8df11d4b98dd753bb1ef116f83&chksm = e85b037edf2c8a686d9546ed5bccc852c9af6b32d1eb1b1c868959c331f9a7898d7895f5c8 & scene = 21# wechat_redirect

# How to develop the algorithm and how to choose the path

# Reference website 1: https://blog.csdn.net/on2way/article/details/40216517

# Reference website 2: https://blog.csdn.net/zhangzhengyi03539/article/details/46673545

import matplotlib.pyplot as plt
import sys
import math
import numpy as np

# Initial parameter definition
T = 50000.0  # initial temperature
T_end = 1e-8 #Iterative precision
q = 0.98  # Annealing coefficient
L = 100  # The number of iterations per temperature, i.e. chain length


city = np.array ([[1304, 2312], [3639, 1315], [4177, 2244], [3712, 1399],
                  [3488, 1535], [3326, 1556], [3238, 1229], [4196, 1004],
                  [4312, 790], [4386, 570], [3007, 1970], [2562, 1756],
                  [2788, 1491], [2381, 1676], [1332, 695],
                  [3715, 1678], [3918, 2179], [4061, 2370],
                  [3780, 2212], [3676, 2578], [4029, 2838],
                  [4263, 2931], [3429, 1908], [3507, 2367],
                  [3394, 2643], [3439, 3201], [2935, 3240],
                  [3140, 3550], [2545, 2357], [2778, 2826],
                  [2370, 2975]])
num = city.shape[0]


# Dismat [i] [j] matrix represents the distance from J to i;
def getdistmat(city):
    num = city.shape[0]
    distmat = np.zeros ((num, num))
    for i in range (num):
        for j in range (i, num):
            distmat[i][j] = distmat[j][i] = np.linalg.norm (city[i] - city[j])
    return distmat



# Calculate the distance between two cities
def distance(i, j):
    x1 = city[i][0]
    y1 = city[i][1]
    x2 = city[j][0]
    y2 = city[j][1]
    dis = ((x1 - x2) ** 2 + (y1 - y2) ** 2) ** 0.5
    return dis


# Calculate the path length from 1 node to the end node
def pathlen():
    path = 0
    for i in range (0, num - 1):
        dis = distance (i, (i + 1))
        path += dis
    path += distance (0, num - 1)
    return path


distmat = getdistmat (city)
# New results
solutionnew = np.arange (num)
valuenew = np.max

# Current results
solutioncurrent = solutionnew.copy ()
valuecurrent = sys.maxsize

# Optimal result
solutionbest = solutionnew.copy ()
valuebest = sys.maxsize

result = []  # Record the best results in iterations
count = 0
while T > T_end:
    for i in np.arange (L):
        count += 1
        # The following two and three commutations are two perturbation modes for generating new solutions.
        # # There are two main ways to generate new solutions based on probability: two-exchange and three-exchange.
        # # Secondary switching is to select two cities to exchange directly in TSP loop
        # # Three exchanges are to select three points in the TSP loop, loc1, loc2, loc3, and then exchange the cities between loc1 and LoC2 directly with the cities of corresponding length before loc3.
        if np.random.rand () > 0.5:  # Two exchange
            # np.random.rand()产生[0, 1)区间的均匀随机数
            while True:  # Generate two different random numbers
                loc1 = np.int (np.ceil (np.random.rand () * (num - 1)))  # intRectify and ensure exchange
                loc2 = np.int (np.ceil (np.random.rand () * (num - 1)))  # ceil Upward rounding, num-1 guarantees that random values do not maximize
                if loc1 != loc2:
                    break
            solutionnew[loc1], solutionnew[loc2] = solutionnew[loc2], solutionnew[loc1]
        else:  # Three exchange
            while True:
                loc1 = np.int (np.ceil (np.random.rand () * (num - 1)))
                loc2 = np.int (np.ceil (np.random.rand () * (num - 1)))
                loc3 = np.int (np.ceil (np.random.rand () * (num - 1)))
                if ((loc1 != loc2) & (loc2 != loc3) & (loc1 != loc3)):
                    break
            # The following three judgment statements make loc1<loc2<loc3
            if loc1 > loc2:
                loc1, loc2 = loc2, loc1
            if loc2 > loc3:
                loc2, loc3 = loc3, loc2
            if loc1 > loc2:
                loc1, loc2 = loc2, loc1

            # The following three lines insert data from the [loc1, loc2] interval after loc3
            tmplist = solutionnew[loc1:loc2].copy ()
            solutionnew[loc1:loc3 - loc2 + 1 + loc1] = solutionnew[loc2:loc3 + 1].copy ()
            solutionnew[loc3 - loc2 + 1 + loc1:loc3 + 1] = tmplist.copy ()
        valuenew = 0
        # Finding the Path Length
        for i in range (num - 1):
            valuenew += distmat[solutionnew[i]][solutionnew[i + 1]]
        valuenew += distmat[solutionnew[0]][solutionnew[num - 1]]  # Head and end length


        if valuenew < valuecurrent:  # Is the new solution better than the current one?
            valuecurrent = valuenew
            solutioncurrent = solutionnew.copy ()
            if valuenew < valuebest:  # Whether the new solution is superior to the optimal solution
                valuebest = valuenew
                solutionbest = solutionnew.copy ()
        else:
            df = valuenew - valuecurrent
            r = np.random.rand ()  # Generating uniform random numbers in [0,1] intervals
            if math.exp (-df / T) > r:# Whether Metropolis criterion is satisfied
                valuecurrent = valuenew
                solutioncurrent = solutionnew.copy ()
            else:  # Unacceptable solution
                solutionnew = solutioncurrent.copy ()
    T *= q
    result.append (valuebest)
    print (T)


ax1 = plt.subplot(2,1,1)
ax1 = plt.plot (np.array (result))
# print (np.array (result))
ax1 = plt.ylabel ("valuebest")
ax1 = plt.xlabel ("t")
ax2 = plt.subplot(2,1,2)
x = city[:, 0]
y = city[:, 1]
for i in (0,30) :
    x[i] = x[solutionbest[i]]
    y[i] = x[solutionbest[i]]
ax2 = plt.plot(x,y,c='b', marker='x', alpha=1)
plt.show()

print ("The most appropriate path is：" ,solutionbest)
print ("Shortest distance:", valuebest)
print ("Trial frequency:", count)