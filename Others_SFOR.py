import numpy as np
# import pclpy
# from pclpy import pcl
# import pcl
import MyFileOperator
from sklearn.neighbors import NearestNeighbors
from scipy.spatial import cKDTree
import math
import datetime

starttime = datetime.datetime.now()

path = '../0Data/Ontario/'
path_r = path+'L3_200x40x15deg_400_C2_r.txt'
returnData = MyFileOperator.read_file_5(path_r)
radius = 2
tree = cKDTree(returnData[:, 1:4])
indices = tree.query_ball_point(returnData[:, 1:4], radius)

correctNum = 0
writefilePosition = open(path + 'results_SFOR.txt', "a")
writefilePosition.seek(0)
writefilePosition.truncate()
for j in range(len(returnData)):
    if len(indices[j]) < 2:
        predict = 222
    else:
        predict = 111
    if returnData[j, 4] - predict == 0:
        correctNum = correctNum + 1
    writefilePosition.writelines([str(returnData[j, 0]), ', ', str(returnData[j, 1]), ', ', str(returnData[j, 2]),
      ', ', str(returnData[j, 3]), ', ', str(returnData[j, 4]), ', ', str(predict), '\n'])

writefilePosition.close()
accuracy = correctNum/len(returnData)
print('totalNum: '+str(len(returnData))+', correctNum: '+str(correctNum))
print('accuracy: '+str(accuracy))
endtime = datetime.datetime.now()
print((endtime - starttime).seconds)