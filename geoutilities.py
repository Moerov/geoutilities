__author__ = 'moerov'

import os
import sys
from geopy.geocoders import GoogleV3
from geopy.distance import vincenty
from geopy.point import Point
from math import sqrt, pow
from random import randint
from sys import stdout


def test():
	print 'It works!'

def is_in_area(begin, end, point):
  
  latitude = point[0]
  longitude = point[1]

  if end[0] < latitude < begin[0] and begin[1] < longitude < end[1]:
    return True

  return False

def get_list_of_x_coordinates(path_to_file):
	x_coordinates = []
	file = open(path_to_file)
	points = file.readlines()
	for point in points:
		x_coordinates.append(float(point.split(',')[0]))
	#print x_coordinates
	return x_coordinates

def get_list_of_y_coordinates(path_to_file):
	y_coordinates = []
	file = open(path_to_file)
	points = file.readlines()
	for point in points:
		y_coordinates.append(float(point.split(',')[1]))
	#print y_coordinates
	return y_coordinates

def get_coordinates_of_area(geolife_folder):
	#Get list of all users
	userdirs = os.listdir(geolife_folder)
	
	x_coordinates = []
	y_coordinates = []

	for userdir in userdirs:
		trajectories = os.listdir(os.path.join(geolife_folder, userdir))
		for trajectory in trajectories:
			x_coordinates.extend(get_list_of_x_coordinates(
				os.path.join(geolife_folder, userdir, trajectory)))
			y_coordinates.extend(get_list_of_y_coordinates(
				os.path.join(geolife_folder, userdir, trajectory)))

	x_coordinates.sort()
	y_coordinates.sort()


def create_bounding_box(box_length):
	"""Given the coordinate of the center and the length of the box returns
	two cordinates of the rectangle box (left_top, right_bottom)"""
	
	coordinate = GoogleV3().geocode("Beijing, Peking, China")[1]
	d = vincenty()

	begin = d.destination(coordinate, 315, sqrt(2 * pow(box_length/2, 2)))
	end = d.destination(coordinate, 135, sqrt(2 * pow(box_length/2, 2)))

	return begin, end


if __name__ == "__main__":
	pass
	#create_partinioned_bounding_box(center_coordinate, 100, 20)
	#create_quadratic_grid(100, 20, './partitions/partitions.quad.20.csv')
	#find_meetings_by_partition_on_day('./geolife_data_1.3/filtered_by_week', 2, 3)
	partitions = create_partinioned_bounding_box_circ(100, 11.2838)
	create_grid_of_circles(100, 11.2838, './partitions/partitions.circ.20.csv')
	
