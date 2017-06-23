from util.geo_distance import great_circle_distance
import numpy as np


def g_lcss(t0, t1,eps):

    n0 = len(t0)
    n1 = len(t1)
    # An (m+1) times (n+1) matrix
    C = [[0] * (n1+1) for _ in range(n0+1)]
    for i in range(1, n0+1):
        for j in range(1, n1+1):
            if great_circle_distance(t0[i-1,0],t0[i-1,1],t1[j-1,0],t1[j-1,1])<eps:
                C[i][j] = C[i-1][j-1] + 1
            else:
                C[i][j] = max(C[i][j-1], C[i-1][j])
    lcss = 1-float(C[n0][n1])/min([n0,n1])
    return lcss


def g_edr(t0, t1,eps):
    n0 = len(t0)
    n1 = len(t1)
    # An (m+1) times (n+1) matrix
    C = [[0] * (n1+1) for _ in range(n0+1)]
    for i in range(1, n0+1):
        for j in range(1, n1+1):
            if great_circle_distance(t0[i-1][0],t0[i-1][1],t1[j-1][0],t1[j-1][1])<eps:
                subcost = 0
            else:
                subcost = 1
            C[i][j] = min(C[i][j-1]+1, C[i-1][j]+1,C[i-1][j-1]+subcost)
    edr = float(C[n0][n1])/max([n0,n1])
    return edr


def g_dtw(t0,t1):

    n0 = len(t0)
    n1 = len(t1)
    C=np.zeros((n0+1,n1+1))
    C[1:,0]=float('inf')
    C[0,1:]=float('inf')
    for i in np.arange(n0)+1:
        for j in np.arange(n1)+1:
            C[i,j]=great_circle_distance(t0[i-1][0],t0[i-1][1],t1[j-1][0],t1[j-1][1]) +\
                   min(C[i,j-1],C[i-1,j-1],C[i-1,j])
    dtw = C[n0,n1]
    return dtw

