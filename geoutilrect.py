__author__ = 'moerov'

import os
import sys
from geopy.geocoders import GoogleV3
from geopy.distance import vincenty
from geopy.point import Point
from math import sqrt, pow, ceil, degrees, atan
from random import randint
from sys import stdout

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

def create_partinioned_bounding_box(box_length, partition_length, partition_width):
	
	"""Calculate the partitions' coordinate"""
	bounding_box = create_bounding_box(box_length)

	partitions_row_count = int(ceil(float(box_length) / float(partition_width)))
	print partitions_row_count
	partitions_column_count = int(box_length / partition_length)
	print partitions_column_count
	partitions = []

	distance_calculator = vincenty()

	for i in range(partitions_row_count):
		row_partitions = []
		row_start = distance_calculator.destination(bounding_box[0], 180, i *
			partition_width)
		for j in range(partitions_column_count):
			partition_start = distance_calculator.destination(row_start, 90, j * 
				partition_length)
			angle = 90 + degrees(atan(float(partition_width)/float(partition_length)))
			#print angle
			partition_end = distance_calculator.destination(partition_start, angle, 
				sqrt(pow(partition_length, 2)+pow(partition_width, 2)))
			row_partitions.append((partition_start, partition_end))
		partitions.append(row_partitions)
	return partitions

def create_grid(box_length, partition_length, partition_width, file_name):
	
	"""Generate partitions and write them into the file"""
	partitions = []
	partition_ids = []
	partitions_raw = create_partinioned_bounding_box(box_length, partition_length, partition_width)

	for partition_row in partitions_raw:
		for partition in partition_row:
			partition_id = None

			while True:
				partition_id = randint(0, pow(2, 24))
				if not partition_id in partition_ids:
					break
			partitions.append((partition[0], partition[1], partition_id))
	
	partitions_file = open(file_name, 'w')
	partitions_file.write("%s;%s;%s;%s;%s\n" % ("box_length", "partition_length",
	 "partition_width", "column_count", "row_count"))
	partitions_file.write("%.2f;%.2f;%.2f;%d;%d\n" % (box_length, partition_length,
                                             partition_width,
                                             int(ceil(float(box_length)/float(partition_length))),
                                             int(ceil(float(box_length)/float(partition_width)))))
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

def load_grid(partitions_file_path):
	"""Load the partition definitions from file"""

	partitions_file = open(partitions_file_path)

	partitions_file.readline()
	partitions_headers = partitions_file.readline()

	headers = partitions_headers.split(';')
	column_count = int(headers[3].strip())
	row_count = int(headers[4].strip())

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
		partitions.append(partition_row)
	return partitions

def find_partition_to_point(partitions, point):
	"""Get the partition of a given coordinate"""

	partition_found = False
	partition_row_index = 0
	partition_column_index = 0
	partition_id = -42

	for row_index in range(len(partitions)):
		partition_row = partitions[row_index]
		partition_row_start = partition_row[0][0]
		partition_row_end = partition_row[-1][1]

		if is_in_area(partition_row_start, 
					  partition_row_end,
					  point):
			for column_index in range(len(partition_row)):
				partition = partition_row[column_index]
				partition_start = partition[0]
				partition_end = partition[1]
				if is_in_area(partition_start, partition_end, point):
					partition_found = True
					partition_row_index = row_index
					partition_column_index = column_index
					partition_id = partition[2]
					break
		if partition_found:
			break
	return partition_id

def find_meetings_by_partition_on_day(geolife_folder, partitions, day, month=3, 
									  interval=5):
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
