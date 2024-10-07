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
radius = 1
tree = cKDTree(returnData[:, 1:3])
indices = tree.query_ball_point(returnData[:, 1:3], radius)

data_ele = np.empty([len(returnData), 8], dtype=float)
data_ele[:, :4] = returnData[:, :4]
data_ele[:, 4] = returnData[:, 4]
for i in range(len(returnData)):  # 腐蚀
    data_ele[i, 5] = min(data_ele[np.array(indices[i]), 3])
for k in range(len(returnData)):  # 膨胀
    data_ele[k, 6] = max(data_ele[np.array(indices[k]), 5])
data_ele[:, 7] = abs(data_ele[:, 3] - data_ele[:, 6])

thr = 40
correctNum = 0
writefilePosition = open(path + 'results_MOR.txt', "a")
writefilePosition.seek(0)
writefilePosition.truncate()
for j in range(len(returnData)):
    if data_ele[j, 7] > thr:
        predict = 222
    else:
        predict = 111
    if predict - returnData[j, 4] == 0:
        correctNum = correctNum + 1
    writefilePosition.writelines([str(returnData[j, 0]), ', ', str(returnData[j, 1]), ', ', str(returnData[j, 2]),
      ', ', str(returnData[j, 3]), ', ', str(returnData[j, 4]), ', ', str(predict), '\n'])

writefilePosition.close()
accuracy = correctNum/len(returnData)
print('totalNum: '+str(len(returnData))+', correctNum: '+str(correctNum))
print('accuracy: '+str(accuracy))
endtime = datetime.datetime.now()
print((endtime - starttime).seconds)