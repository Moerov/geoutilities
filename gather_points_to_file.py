__author__ = 'moerov'

import os
from sys import stdout
import glob

def write_points_to_file(geolife_folder, file_name):
	points_file = open(file_name, 'w')
	points_file.write("%s;%s;%s;%s\n" %('color', 'symbol', 'latitude', 'longitude'))
	userdirs = os.listdir(geolife_folder)
	for userdir in userdirs:
		trajectories = glob.glob(os.path.join(geolife_folder, userdir, '*.trajectories'))
		if trajectories:
			for trajectory in trajectories:
				trajectory_data = open(trajectory)
				traj_points = trajectory_data.readlines()
				for point in traj_points:
					latitude = float(point.split(',')[0])
					longitude = float(point.split(',')[1])
					points_file.write("%s;%s;%f;%f\n" %('red', 'googlemini', latitude, longitude))

if __name__ == "__main__":
	write_points_to_file('./geolife_data_1.3/filtered_by_week', 'allpoints.csv')