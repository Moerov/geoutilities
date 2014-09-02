__author__ = 'moerov'

import sys
import os
import shutil
import glob
import geoutilities

def filter_by_week(geolife_old_folder, geolife_new_folder):
  
  #Store absolute paths
  path_to_old_folder = os.path.join(os.path.curdir, 
  									geolife_old_folder)
  path_to_new_folder = os.path.join(os.path.curdir, 
  									geolife_new_folder)

  #If filtered_by_week folder already exists remove it
  if os.path.exists(path_to_new_folder):
        os.rmdir(path_to_new_folder)
  os.mkdir(geolife_new_folder)
  print 'Starting filter by week: 01.03.2009 - 07.03.2009'

  userdirs = os.listdir(path_to_old_folder)
  userdirssize = len(userdirs)
  x = 1.0

  count = 0
  for user in userdirs:
  	 
    progress = float((x / userdirssize) * 100)

    #sys.stdout.write("\rProgress: %6.2f%%" % progress)
    #sys.stdout.flush()
    x += 1.0
    
    files = glob.glob(os.path.join(path_to_old_folder, user, '2009-03-0[1-7].trajectories'))
    count+=len(files)  
    if files:
     # print '\n'.join(files)
     for file in files:
       new_path = os.path.join(geolife_new_folder, user)
       
       if not os.path.exists(new_path): 
        os.mkdir(new_path)
       shutil.copy(file, new_path)

  print "Number of trajectories within the time period = ", count

def filter_by_area(begin, end, geolife_folder):

  trajectories_out_of_area = []

  userdirs = os.listdir(geolife_folder)

  for user in userdirs:
    trajectories = os.listdir(os.path.join(geolife_folder, user))

    for trajectory_path in trajectories:
      is_out_of_area = False
      abs_path_trajectory = os.path.join(geolife_folder, user, trajectory_path)
      trajectory = open(abs_path_trajectory)
      points = trajectory.readlines()
      for point in points:
        first_coord = float(point.split(',')[0])
        second_coord = float(point.split(',')[1])
        coordinates = []
        coordinates.append(first_coord)
        coordinates.append(second_coord)
        if not geoutilities.is_in_area(begin, end, coordinates):
          is_out_of_area = True
          break
      if is_out_of_area:
        trajectories_out_of_area.append(abs_path_trajectory)

  
  print '\n'.join(trajectories_out_of_area)
  print len(trajectories_out_of_area)

  for traj in trajectories_out_of_area:
    os.remove(traj)

def test_all_points_in_area(begin, end):
  all_points = []
  geolife_folder = './geolife_data_1.3/filtered_by_week'
  userdirs = os.listdir(geolife_folder)
  for user in userdirs:
    trajectories = os.listdir(os.path.join(geolife_folder, user))
    for traj in trajectories:
      abs_path_trajectory = os.path.join(geolife_folder, user, traj)
      trajectory = open(abs_path_trajectory)
      all_points.extend(trajectory.readlines())

  for point in all_points:
    first_coord = float(point.split(',')[0])
    second_coord = float(point.split(',')[1])
    coordinates = []
    coordinates.append(first_coord)
    coordinates.append(second_coord)
    if not geoutilities.is_in_area(begin, end, coordinates):
      print 'fuck'
      return False
  return True


if __name__ == "__main__":

  #filter_by_week ('./geolife_data_1.3/filtered', './geolife_data_1.3/filtered_by_week')
  #geoutilities.test()

  begin, end = geoutilities.create_bounding_box(100)
  filter_by_area(begin, end, './geolife_data_1.3/filtered_by_week')

