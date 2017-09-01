##Created at 08/02/2017 by Yubin Xie, MSKCC
##Modified at #### by ***
## This script is to find the starting points in the binary images and find the shortest path between them (the starting point only have 1 connection instead of 2)
import itertools
import math
from scipy import misc
from scipy.sparse.dok import dok_matrix
from scipy.sparse.csgraph import dijkstra
import operator
from operator import sub, add
import numpy as np
from matplotlib import pyplot as plt
from PIL import Image
import itertools
InputFolder = "../Output/Selected_Tissue2/"
TissueID = "495400_0"   #"Segmentated_Thinned423690_2" "path" Segmentated_Thinned495400_1.png Segmentated_Label495400_1.bmp
def main(Array):
    try:
        # Load the image
        img = Array
        SourceList=[]
        for i in range(0,img.shape[0]-1):
            for j in range(0,img.shape[1]-1):
                if img[i,j]>=1:
                    img[i,j]=1

        for i in range(1,img.shape[0]-2):
            for j in range(1,img.shape[1]-2):
                if img[i,j]==0:
                    continue
                sourse=None
                NearValue=0
                CornerValue=0
                NearValueList=[]
                CornerValueList=[]
                NearPosition = [(-1,0),(0,-1),(0,1),(1,0),]
                CornerPosition = [(-1,1),(1,1),(-1,-1),(1,-1)]
                for direction in range(4):
                    NearValue=NearValue+img[tupleadd((i,j),NearPosition[direction])]
                    NearValueList.append(img[tupleadd((i,j),NearPosition[direction])])
                    CornerValue=CornerValue+img[tupleadd((i,j),CornerPosition[direction])]
                    CornerValueList.append(img[tupleadd((i,j),CornerPosition[direction])])
                if NearValue + CornerValue==1:
                    sourse = (i,j)
                if NearValue==1 and CornerValue==1:
                    NearDirection=NearPosition[NearValueList.index(1)]
                    CornerDirection=CornerPosition[CornerValueList.index(1)]
                    if (NearDirection[0]==CornerDirection[0]) or (NearDirection[1]==CornerDirection[1]):
                        sourse = (i,j)
                if sourse!=None:
                    if sourse not in SourceList:
                        SourceList.append(sourse)
        print len(SourceList), " single points are found in the image", SourceList
        adjacency = dok_matrix((img.shape[0] * img.shape[1],img.shape[0] * img.shape[1]), dtype=bool)
        directions = list(itertools.product([0, 1, -1], [0, 1, -1]))
        for i in range(1, img.shape[0] - 1):
            for j in range(1, img.shape[1] - 1):
                if not img[i, j]:
                    continue
                for y_diff, x_diff in directions:
                    if img[i + y_diff, j + x_diff]:
                        adjacency[to_index(i, j),
                            to_index(i + y_diff, j + x_diff)] = True
        Distance=[]
        Combination = [(p1,p2) for p1 in range(len(SourceList)) for p2 in range(p1+1,len(SourceList))]
        for p1,p2 in Combination:
            p1 = to_index(SourceList[p1][0],SourceList[p1][1])
            p2 = to_index(SourceList[p2][0],SourceList[p2][1])
            dist_matrix = dijkstra(adjacency, directed=False,unweighted=True,indices=[p1],limit=1000)
            Distance.append( dist_matrix[0,p2] )



    #Distance = [dist_matrix[to_index(SourceList[p1][0],SourceList[p1][1]),to_index(SourceList[p2][0],SourceList[p2][1])] for p1 in range(len(SourceList)) for p2 in range(p1+1,len(SourceList))]
        Start_End= Combination[Distance.index(max(Distance))]        
        return
    except Exception, e:
        print e
        pass


if __name__ == '__main__':
  main(Array)
