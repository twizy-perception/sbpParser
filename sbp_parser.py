# Copyright 2018 Filip Karlsson

# Script that decodes GNSS and IMU data from binary files
# of the format defined by Swift Binary Protocol and writes
# data to comma separated textfiles.



from struct import *
import os
import glob
import matplotlib.pyplot as plt; plt.rcdefaults()
import numpy as np
import matplotlib.pyplot as plt

preamble = b'\x55'

# Path to binery .sbp files
path = '0002/'

# Functions
def readNextMsg(binary_file):
	# Preamble (1 byte)
	pre = binary_file.read(1)

	if pre == preamble:
		#print("Preamble OK")
		pass
	else:
		print("Preamble failure.")
		return -1

	# Msg type (2 bytes)
	msg_type = binary_file.read(2)
	#print(str(msg_type))

	# Sender (2 bytes)
	msg_sender = binary_file.read(2)

	# Lenght (1 byte)
	msg_lenght = int.from_bytes(binary_file.read(1), byteorder='big')
	# Payload (N bytes)
	msg_payload = binary_file.read(msg_lenght)

	fun, filename = MSG_TYPE.get(msg_type, (do_nothing, ""))
	fun(msg_payload, filename)
	#print(msg_payload)
	# CRC (2 bytes)
	msg_crc = binary_file.read(2)

	return 1



def MSG_POS_LLH(msg_payload, filename):
	with open(filename, 'a') as file:	
		tow = unpack('I', msg_payload[0:4])[0]
		lat = unpack('d', msg_payload[4:12])[0]
		lon = unpack('d', msg_payload[12:20])[0]
		height = unpack('d', msg_payload[20:28])[0]
		h_acc = unpack('H', msg_payload[28:30])[0]
		v_acc = unpack('H', msg_payload[30:32])[0]
		n_sats = unpack('B', msg_payload[32:33])[0]
		flags  = unpack('B', msg_payload[33:34])[0]
		
		file.write(str(tow) + "," + str(lat) + "," + str(lon) + "," + str(height) + "," + str(flags) + "," + str(h_acc) + "," + str(v_acc) + ","+ "\n")



def MSG_IMU_RAW(msg_payload, file):
	with open(file, 'a') as file_imu:	
		tow = unpack('I', msg_payload[0:4])[0]
		tow_f = unpack('B', msg_payload[4:5])[0]
		acc_x = unpack('h', msg_payload[5:7])[0]
		acc_y = unpack('h', msg_payload[7:9])[0]
		acc_z = unpack('h', msg_payload[9:11])[0]
		gyr_x = unpack('h', msg_payload[11:13])[0]
		gyr_y = unpack('h', msg_payload[13:15])[0]
		gyr_z = unpack('h', msg_payload[15:17])[0]

		out = str(tow) + "," + str(tow_f) + "," + str(acc_x) + "," + str(acc_y) + "," + str(acc_z) + "," + str(gyr_x) +"," + str(gyr_y) +"," + str(gyr_z) + "\n"
		file_imu.write(out)


def MSG_MAG_RAW(msg_payload, file):
	with open(file, 'a') as file_mag:	
		tow = unpack('I', msg_payload[0:4])[0]
		tow_f = unpack('B', msg_payload[4:5])[0]
		mag_x = unpack('h', msg_payload[5:7])[0]
		mag_y = unpack('h', msg_payload[7:9])[0]
		mag_z = unpack('h', msg_payload[9:11])[0]

		out = str(tow) + "," + str(tow_f) + "," + str(mag_x) + "," + str(mag_y) + "," + str(mag_z) + "\n"
		file_mag.write(out)


def do_nothing(msg_payload, file):
	pass



colors = {0:'r', 1:'y', 2:'b', 3:'k', 4:'g', 5:'c'}
MSG_TYPE = {b'\x0A\x02':(MSG_POS_LLH, path + 'pos_llh.txt'), b'\x00\x09':(MSG_IMU_RAW, path +'imu_raw.txt'), b'\x02\x09':(MSG_MAG_RAW, path +'mag_raw.txt')}


filelist = glob.glob(os.path.join(path, '*.sbp'))

for infile in sorted(filelist): 
  	#do some fancy stuff
	print(str(infile))
	
	with open(infile, "rb") as binary_file:
		data = binary_file.read()
		binary_file.seek(0)
	
		while readNextMsg(binary_file) == 1:
	   		pass















	





