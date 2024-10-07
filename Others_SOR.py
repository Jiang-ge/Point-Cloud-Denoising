import numpy as np
# import pclpy
# from pclpy import pcl
# import pcl
import MyFileOperator
from sklearn.neighbors import NearestNeighbors
from scipy.spatial import cKDTree
import math
import datetime
'''
# python-pcl
def do_statistical_outlier_filtering(pcl_data,mean_k,tresh):
    # :param pcl_data: point could data subscriber
    # :param mean_k:  number of neighboring points to analyze for any given point
    # :param tresh:   Any point with a mean distance larger than global will be considered outlier
    # :return: Statistical outlier filtered point cloud data
    # eg) cloud = do_statistical_outlier_filtering(cloud,10,0.001)
    # : https://github.com/fouliex/RoboticPerception
    
    outlier_filter = pcl_data.make_statistical_outlier_filter()
    outlier_filter.set_mean_k(mean_k)
    outlier_filter.set_std_dev_mul_thresh(tresh)
    return outlier_filter.filter()



path = '../0Data/Vancouver_BCIT/'
path_r = path+'LDR090717_233955_1_addLabel_test.txt'
returnData = MyFileOperator.read_file_10(path_r)
# returnData = returnData[:1000, 1:4]
file_name = 'LDR090717_233955_1_addLabel_test'
txt2pcd.txt2pcd(returnData, path, file_name)

points = pcl.load(path+'LDR090717_233955_1_addLabel_test.pcd')
for i in range(points.size):
    print(points[i][0])
    print(points[i][1])
    print(points[i][2])
# points.from_file(path+'LDR090717_233955_1_addLabel_test.pcd')
cloud = do_statistical_outlier_filtering(points, 10, 0.001)
        # number of neighboring points of 10
        # standard deviation threshold of 0.001
'''

starttime = datetime.datetime.now()
path = '../0Data/Ontario/'
path_r = path+'L3_200x40x15deg_400_C2_r.txt'
returnData = MyFileOperator.read_file_5(path_r)
neighborNum = 6
nbrs = NearestNeighbors(n_neighbors=neighborNum, algorithm='kd_tree').fit(returnData[:, 1:4])
distances, indices = nbrs.kneighbors(returnData[:, 1:4])
mean = sum(map(sum, distances)) / (len(returnData)*6)
std = math.sqrt(sum(map(sum, (distances-mean) ** 2)) / (len(returnData)*6))

correctNum = 0
writefilePosition = open(path + 'results_SOR.txt', "a")
writefilePosition.seek(0)
writefilePosition.truncate()
for j in range(len(returnData)):
    dis_mean = sum(distances[j]) / neighborNum
    if dis_mean > (mean + std) or dis_mean < (mean - std):
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