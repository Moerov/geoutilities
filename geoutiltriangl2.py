__author__ = 'moerov'

import os
import sys
from geopy.geocoders import GoogleV3
from geopy.distance import vincenty
from geopy.point import Point
from math import sqrt, pow, ceil
from random import randint
from sys import stdout

def is_in_triangle(vertices, point):
	#Return true if point is inside the triangle
	p1 = vertices[0]
	p2 = vertices[1]
	p3 = vertices[2]

	alpha = ((p2[1] - p3[1])*(point[0] - p3[0]) + 
		(p3[0] - p2[0])*(point[1] -p3[1])) / ((p2[1] - p3[1])*(p1[0] - p3[0]) + 
		(p3[0] - p2[0])*(p1[1] - p3[1]))

	beta = ((p3[1] - p1[1])*(point[0] - p3[0]) + 
		(p1[0] - p3[0])*(point[1] -p3[1])) / ((p2[1] - p3[1])*(p1[0] - p3[0]) + 
		(p3[0] - p2[0])*(p1[1] - p3[1]))

	gamma = 1 - alpha - beta
	#print alpha, beta, gamma
	return (alpha > 0 and beta > 0 and gamma > 0)

def is_in_area(begin, end, point):
  
  latitude = point[0]
  longitude = point[1]

  if end[0] < latitude < begin[0] and begin[1] < longitude < end[1]:
    return True

  return False

def create_bounding_box(box_length):
	"""Given the coordinate of the center and the length of the box returns
	two cordinates of the rectangle box (left_top, right_bottom)"""
	
	coordinate = GoogleV3().geocode("Beijing, Peking, China")[1]
	d = vincenty()

	begin = d.destination(coordinate, 315, sqrt(2 * pow(box_length/2, 2)))
	end = d.destination(coordinate, 135, sqrt(2 * pow(box_length/2, 2)))

	return begin, end

def create_partitioned_bounding_box(box_length, partition_length):
	
	bounding_box = create_bounding_box(box_length)
	partition_height = partition_length * sqrt(3) / 2

	partitions_row_count = int(ceil(box_length/partition_height))
	partitions_column_count = int(ceil(box_length/partition_length))
	
	partitions = []
	distance_calculator = vincenty()
	left_bound = distance_calculator.destination(bounding_box[0], 
			270, partition_length/2)
	for i in range(partitions_row_count):
		row_start = distance_calculator.destination(left_bound, 180, 
			(i+1) * partition_height)
		row_partitions = []
		for j in range(partitions_column_count):
			bottom_partition_1 = distance_calculator.destination(row_start, 90, 
									j*partition_length)
			bottom_partition_2 = distance_calculator.destination(bottom_partition_1, 90, 
									partition_length)
			bottom_partition_3 = distance_calculator.destination(bottom_partition_1, 30, 
									partition_length)
			top_partition_1 = bottom_partition_2
			top_partition_2 = distance_calculator.destination(top_partition_1, 30, 
									partition_length)
			top_partition_3 = bottom_partition_3
			row_partitions.append((bottom_partition_1, 
				bottom_partition_2, bottom_partition_3))
			row_partitions.append((top_partition_1, 
				top_partition_2, top_partition_3))
		partitions.append(row_partitions)

	return partitions


def create_grid(box_length, partition_length, file_name):
	"""Generate partitions and write them into the file"""
	partitions = []
	partition_ids = []
	partitions_raw = create_partitioned_bounding_box(box_length, partition_length)
	for partition_row in partitions_raw:
		for partition in partition_row:
			partition_id = None

			while True:
				partition_id = randint(0, pow(2, 24))
				if not partition_id in partition_ids:
					partition_ids.append(partition_id)
					break
			partitions.append((partition[0], partition[1], partition[2], partition_id))

	partition_height = partition_length * sqrt(3) / 2
	partitions_file = open(file_name, 'w')
	partitions_file.write("%s;%s;%s;%s\n" % ("box_length", "partition_length",
	 "column_count", "row_count"))
	partitions_file.write("%.2f;%.2f;%d;%d\n" % (box_length, partition_length,
                                             2*int(ceil(box_length/partition_length)),
                                             int(ceil(box_length/partition_height))))
	partitions_file.write("%s;%s;" % ("first_point_lat",
									"first_point_lon"))
	partitions_file.write("%s;%s;" % ("second_point_lat",
									"second_point_lon"))
	partitions_file.write("%s;%s;" % ("third_point_lat",
									"third_point_lon"))
	partitions_file.write("%s\n" % "id")
	for partition in partitions:
		partitions_file.write("%f;%f;" % (partition[0][0], partition[0][1]))
		partitions_file.write("%f;%f;" % (partition[1][0], partition[1][1]))
		partitions_file.write("%f;%f;" % (partition[2][0], partition[2][1]))
		partitions_file.write("%s\n" % partition[3])
	partitions_file.flush()
	partitions_file.close()

def load_grid(partitions_file_path):
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

				first_point = Point(partition_values[0], partition_values[1])
				second_point = Point(partition_values[2], partition_values[3])
				third_point = Point(partition_values[4], partition_values[5])
				id = int(partition_values[6])

				partition_row.append((first_point, second_point, third_point, id))
			else:
				return None
		partitions.append(partition_row)
	return partitions

def find_partition_to_point(partitions, point):
	partition_found = False
	partition_row_index = 0
	partition_column_index = 0
	partition_id = 0

	for row_index in range(len(partitions)):
		partition_row = partitions[row_index]
		row_bottom = partition_row[0][0]
		row_top = partition_row[0][2]
		
		if (row_bottom[0] < point[0] < row_top[0]):
			for column_index in range(len(partition_row)):
				partition = partition_row[column_index]
				if is_in_triangle(partition[:3], point):
					partition_found = True
					partition_row_index = row_index
					partition_column_index = column_index
					partition_id = partition[3]
					break
		if partition_found:
			break
	return partition_row_index, partition_column_index, partition_id

def find_meetings_by_partition_on_day(geolife_folder, partitions, day, 
									  month=3, interval=5, condition=2):
	coordinates_in_region_by_time = {}

	userdirs = os.listdir(geolife_folder)

	for userdir in userdirs:
		user_day_file_name = os.path.join(geolife_folder, userdir, 
								'2009-%02d-%02d.trajectories' % (month, day))
		
		if not os.path.isfile(user_day_file_name):
			continue

		user_day_file = open(user_day_file_name)
		user_day_data = user_day_file.readlines()

		for line in user_day_data:
			data = line.split(',')
			location = Point(float(data[0]), float(data[1]))
			time = data[6].split(':')
			hour = time[0]
			minute = int(time[1]) - (int(time[1]) % interval)

			timestamp = '%s:%02d' % (hour, minute)

			if timestamp not in coordinates_in_region_by_time:
				coordinates_in_region_by_time[timestamp] = []
				#print 'hit!'
			coordinates_in_region_by_time[timestamp].append(
				(userdir, find_partition_to_point(partitions, location)))
	return coordinates_in_region_by_time