import numpy as np
# import pclpy
# from pclpy import pcl
# import pcl
import MyFileOperator
from sklearn.neighbors import NearestNeighbors
from scipy.spatial import cKDTree
import math
import sympy as sp
from scipy.optimize import fsolve
import datetime

starttime = datetime.datetime.now()
print(starttime)
def line_sphere_intersection(line_origin, line_direction, sphere_center, sphere_radius):
    def equation(t):
        x = line_origin[0] + line_direction[0] * t
        y = line_origin[1] + line_direction[1] * t
        z = line_origin[2] + line_direction[2] * t
        return (x - sphere_center[0])**2 + (y - sphere_center[1])**2 + (z - sphere_center[2])**2 - sphere_radius**2

    # Initial guesses for fsolve
    initial_guesses = [-1.0, 1.0]

    # Use fsolve to find intersection points numerically
    t_values = []
    for guess in initial_guesses:
        try:
            t_root = fsolve(equation, guess)[0]
            t_values.append(t_root)
        except:
            pass

    # Calculate intersection points
    intersection_points = []
    for i in range(len(t_values)):
        t = t_values[i]
        intersection_points.append([line_origin[0] + line_direction[0] * t, line_origin[1] + line_direction[1] * t,
                                    line_origin[2] + line_direction[2] * t])
    intersection_points = np.array(intersection_points)
    return intersection_points


path = '../0Data/Vancouver_BCIT/5SHDR/'
path_r = path+'03_raw_cut.txt'
returnData = MyFileOperator.read_file_5(path_r)
returnData = returnData[:, :]

# radius = 2
# tree = cKDTree(returnData[:, 1:4])
# indices = tree.query_ball_point(returnData[:, 1:4], radius)
# max_len = 0
# for i in range(len(indices)):
#     if len(indices[i]) > max_len:
#         max_len = len(indices[i])
#         max_id = i
# center_point = returnData[max_id, :]

# max_id = 2196590
max_id = 10000
sphere_center_array = []
sphere_center_array.append(returnData[max_id, 1:4])
sphere_center = sphere_center_array[0]
sphere_radius = 3
tree = cKDTree(returnData[:, 1:4])
indices_valid = tree.query_ball_point(sphere_center, sphere_radius)
# valid_points_id = returnData[indices, 0]
# data_delete = np.delete(returnData, indices, axis=0)

line_origin = sphere_center
line_direction_array = np.array([[0,0,1], [0,1,0], [1,0,0], [1,1,1], [1,-1,1], [1,1,-1], [1,-1,-1]])
# line_direction_array = np.array([[0,0,1], [0,1,0], [1,0,0]])
while 1:
    sphere_center_new = []
    for i in range(len(sphere_center_array)):
        sphere_center = sphere_center_array[i]
        line_origin = sphere_center
        for j in range(len(line_direction_array)):
            line_direction = line_direction_array[j, :]
            intersection_points = line_sphere_intersection(line_origin, line_direction, sphere_center, sphere_radius)
            for k in range(len(intersection_points)):
                # tree = cKDTree(data_delete[:, 1:4])
                indices = tree.query_ball_point(intersection_points[k, :], sphere_radius)
                # diff_set = list(set(a).difference(set(b)))  # a中有而b中没有的
                diff_set = list(set(indices).difference(set(indices_valid)))
                if len(diff_set) > 0:
                    indices_valid = np.hstack((indices_valid, diff_set))
                    sphere_center_new.append(intersection_points[k, :])
                # if len(indices) > 0:
                #     valid_points_id = np.hstack((valid_points_id, returnData[indices, 0]))
                #     # data_delete = np.delete(data_delete, indices, axis=0)
                #     sphere_center_new.append(intersection_points[k, :])
    if len(sphere_center_new) != 0:
        sphere_center_array = sphere_center_new
    else:
        break
# valid_points_id = list(set(valid_points_id))
indices_valid = sorted(indices_valid)
valid_points = returnData[indices_valid, :]
correctNum = 0
validNum = 0
TP = 0
FN = 0
FP = 0
TN = 0
writefilePosition = open(path + '03_results_SHDR_rawMethod.txt', "a")
writefilePosition.seek(0)
writefilePosition.truncate()
for j in range(len(returnData)):
    if j == indices_valid[validNum]:
        if returnData[j, 4] == 111:
            TN = TN + 1
            correctNum = correctNum + 1
        else:
            FN = FN + 1
        writefilePosition.writelines([str(returnData[j, 0]), ', ', str(returnData[j, 1]), ', ', str(returnData[j, 2]),
          ', ', str(returnData[j, 3]), ', ', str(returnData[j, 4]), ', ', str(111), '\n'])
        validNum = validNum + 1

    else:
        if returnData[j, 4] == 222:
            TP = TP + 1
            correctNum = correctNum + 1
        else:
            FP = FP + 1
        writefilePosition.writelines([str(returnData[j, 0]), ', ', str(returnData[j, 1]), ', ', str(returnData[j, 2]),
          ', ', str(returnData[j, 3]), ', ', str(returnData[j, 4]), ', ', str(222), '\n'])

writefilePosition.close()
accuracy = correctNum/len(returnData)
print('totalNum: '+str(len(returnData))+', correctNum: '+str(correctNum))
print('accuracy: '+str(accuracy))
print('TP: '+str(TP))
print('FN: '+str(FN))
print('FP: '+str(FP))
print('TN: '+str(TN))
endtime = datetime.datetime.now()
print((endtime - starttime).seconds)
a = 1










### my low computational cost version, but it is wrong
## for the point cloud with clustered noisy points
# path = '../0Data/Vancouver_BCIT/'
# path_r = path+'0Raw/03_LDR090717_235159_1.txt'
# correctNum = 0
# TP = 0
# FN = 0
# FP = 0
# TN = 0
# writefilePosition = open(path + '5SHDR/03_LDR090717_235159_1.txt', "a")
# writefilePosition.seek(0)
# writefilePosition.truncate()
#
# returnData = MyFileOperator.read_file_5(path_r)
# height = 64
# cluster_noise = returnData[np.where(returnData[:, 3] > height)]
# cluster_noise_indices = np.where(returnData[:, 3] > height)
# for i in range(len(cluster_noise)):
#     if cluster_noise[i, 4] == 222:
#         TP = TP + 1
#         correctNum = correctNum + 1
#     else:
#         FP = FP + 1
#     writefilePosition.writelines([str(returnData[i, 0]), ', ', str(returnData[i, 1]), ', ', str(returnData[i, 2]),
#       ', ', str(returnData[i, 3]), ', ', str(returnData[i, 4]), ', ', str(222), '\n'])
#
#
# data = np.delete(returnData, cluster_noise_indices, axis=0)
# sphere_radius = 1
# tree = cKDTree(data[:, 1:4])
# indices = tree.query_ball_point(data[:, 1:4], sphere_radius)
# for j in range(len(data)):
#     if len(indices[j]) == 0:
#         if data[j, 4] == 222:
#             TP = TP + 1
#             correctNum = correctNum + 1
#         else:
#             FP = FP + 1
#         writefilePosition.writelines([str(data[j, 0]), ', ', str(data[j, 1]), ', ', str(data[j, 2]),
#           ', ', str(data[j, 3]), ', ', str(data[j, 4]), ', ', str(222), '\n'])
#     else:
#         if data[j, 4] == 111:
#             TN = TN + 1
#             correctNum = correctNum + 1
#         else:
#             FN = FN + 1
#         writefilePosition.writelines([str(data[j, 0]), ', ', str(data[j, 1]), ', ', str(data[j, 2]),
#           ', ', str(data[j, 3]), ', ', str(data[j, 4]), ', ', str(111), '\n'])
#
# writefilePosition.close()
# accuracy = correctNum/len(returnData)
# print('totalNum: '+str(len(returnData))+', correctNum: '+str(correctNum))
# print('accuracy: '+str(accuracy))
# print('TP: '+str(TP))
# print('FN: '+str(FN))
# print('FP: '+str(FP))
# print('TN: '+str(TN))
#
#
# a = 1


# # for the point cloud without clustered noisy points
# path = '../0Data/Vancouver_BCIT/'
# path_r = path+'0Raw/06_LDR090718_000445_1.txt'
# correctNum = 0
# TP = 0
# FN = 0
# FP = 0
# TN = 0
# writefilePosition = open(path + '5SHDR/06_LDR090718_000445_1.txt', "a")
# writefilePosition.seek(0)
# writefilePosition.truncate()
# returnData = MyFileOperator.read_file_5(path_r)
# sphere_radius = 3
# tree = cKDTree(returnData[:, 1:4])
# indices = tree.query_ball_point(returnData[:, 1:4], sphere_radius)
# for j in range(len(returnData)):
#     if len(indices[j]) == 0:
#         if returnData[j, 4] == 222:
#             TP = TP + 1
#             correctNum = correctNum + 1
#         else:
#             FP = FP + 1
#         writefilePosition.writelines([str(returnData[j, 0]), ', ', str(returnData[j, 1]), ', ', str(returnData[j, 2]),
#           ', ', str(returnData[j, 3]), ', ', str(returnData[j, 4]), ', ', str(222), '\n'])
#     else:
#         if returnData[j, 4] == 111:
#             TN = TN + 1
#             correctNum = correctNum + 1
#         else:
#             FN = FN + 1
#         writefilePosition.writelines([str(returnData[j, 0]), ', ', str(returnData[j, 1]), ', ', str(returnData[j, 2]),
#           ', ', str(returnData[j, 3]), ', ', str(returnData[j, 4]), ', ', str(111), '\n'])
#
# writefilePosition.close()
# accuracy = correctNum/len(returnData)
# print('totalNum: '+str(len(returnData))+', correctNum: '+str(correctNum))
# print('accuracy: '+str(accuracy))
# print('TP: '+str(TP))
# print('FN: '+str(FN))
# print('FP: '+str(FP))
# print('TN: '+str(TN))
#
# a = 1


