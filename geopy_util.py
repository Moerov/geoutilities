__author__ = 'moerov'

import os
import sys
from geopy.geocoders import GoogleV3
from geopy.distance import vincenty
from math import sqrt, pow
from random import randint
from sys import stdout


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

	#print x_coordinates
	#print x_coordinates[-1]
	#print y_coordinates
	#print y_coordinates[-1]

def create_bounding_box(box_length):
	"""Given the coordinate of the center and the length of the box returns
	two cordinates of the rectangle box (left_top, right_bottom)"""

	coordinate = GoogleV3().geocode("Beijing, Peking, China")[1]
	d = vincenty()

	begin = d.destination(coordinate, 315, sqrt(2 * pow(box_length/2, 2)))
	end = d.destination(coordinate, 135, sqrt(2 * pow(box_length/2, 2)))

	return begin, end

def create_partinioned_bounding_box(box_length, partition_length):
	
	"""Calculate the partitions' coordinate"""
	bounding_box = create_bounding_box(box_length)

	partitions_row_count = int(box_length / partition_length)
	
	partitions = []

	distance_calculator = vincenty()

	for i in range(partitions_row_count):
		row_partitions = []
		row_start = distance_calculator.destination(bounding_box[0], 180, i *
			partition_length)
		for j in range(partitions_row_count):
			partition_start = distance_calculator.destination(row_start, 90, j * 
				partition_length)
			partition_end = distance_calculator.destination(partition_start, 135, 
				sqrt(2*pow(partition_length, 2)))
			row_partitions.append((partition_start, partition_end))

			
			'''stdout.write('%f, %f\n' % (partition_start[0], partition_start[1]))
			stdout.write('%f, %f\n' % (partition_end[0], partition_end[1]))
			stdout.flush()'''
		partitions.append(row_partitions)
	"""for row in partitions:
		for partition in row:
			stdout.write('%f, %f\n' % (partition[0][0], partition[1][1]))"""
	return partitions

def create_quadratic_grid(box_length, partition_length, file_name):
	
	"""Generate partitions and write them into the file"""
	partitions = []
	partition_ids = []
	partitions_raw = create_partinioned_bounding_box(box_length, partition_length)

	#print partitions_raw

	for partition_row in partitions_raw:
		for partition in partition_row:
			partition_id = None

			while True:
				partition_id = randint(0, pow(2, 32))
				if not partition_id in partition_ids:
					break
			partitions.append((partition[0], partition[1], partition_id))
	
	partitions_file = open(file_name, 'w')
	partitions_file.write("%s;%s;%s;%s\n" % ("box_length", "partition_length",
	 "column_count", "row_count"))
	partitions_file.write("%.2f;%.2f;%d;%d\n" % (box_length, partition_length,
                                             box_length / partition_length,
                                             box_length / partition_length))
	partitions_file.write("%s;%s;" % ("partition_start_lat",
									"partition_start_lon"))
	partitions_file.write("%s;%s;" % ("partition_end_lat",
									"partition_end_lon"))
	partitions_file.write("%s\n" % "id")
	for partition in partitions:
		partitions_file.write("%f;%f;" % (partition[0][0], partition[0][1]))
		partitions_file.write("%f;%f;" % (partition[1][0], partition[1][1]))
		partitions_file.write("%s\n" % partition[2])
	
	partitions_file.flush()
	partitions_file.close()

def load_quadratic_partition(partitions_file_path):
	"""Load the partition definitions from file"""

	partitions_file = open(partitions_file_path)

	partitions_file.readline()
	partitions_headers = partitions_file.readline()

	headers = partitions_headers.split(';')
	column_count = int(headers[2].strip())
	row_count = int(headers[3].strip())

	partitions_file.readline()
	partitions = []

	for _ in range(row_count):
		partition_row = []
		for _ in range(column_count):

			partition_line = partitions_file.readline().strip()

			if not partition_line == '':
				partition_values = partition_line.split(';')

				start = Point(partition_values[0], partition_values[1])
				end = Point(partition_values[2], partition_values[3])
				id = int(partition_values[4])

				partition_row.append((start, end, id))
			else:
				return None
		paritions.append(partition_row)
	return partitions

if __name__ == "__main__":
	#create_partinioned_bounding_box(center_coordinate, 100, 20)
	create_quadratic_grid(100, 20, './partitions/partitions.20.csv')
