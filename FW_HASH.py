import os
import hashlib
from prettytable import PrettyTable
import datetime


output_data = PrettyTable()
current_dir = "."


def enumerateFilesInDirectory(dir):
	global _HASHIGNORE
	files_list = []
	dirs = [x[0] for x in os.walk(dir)]
	for dir in dirs:
		if dir in _HASHIGNORE:
			pass
	for root, dirs, files in os.walk(dir):
		for file in files:
			file_path = os.path.join(root, file)
			files_list.append(file_path)
	print(files_list)
	return files_list


def readFileContent(file):
	with open(file) as f:
		content = f.read().splitlines()
	for item in content:
		item = ' '.join(item.strip())
	return content


def calculateHashes(file, content):
	#i = 0
	hashed_string = hashlib.sha256(bytes(file, encoding='utf=8')).hexdigest() # first hash should be file`s header
	for string in content:
		b_string = bytes(string, encoding='utf-8')
		hashed_string = hashlib.sha256(b_string+bytes(hashed_string, encoding='utf-8')).hexdigest()
		#output_data.add_row([f"string num.{i}", hashed_string])
		#i += 1
	return hashed_string


def printFilesInDirectory(directory, dirDeep):
	global _HASHIGNORE
	files_list = enumerateFilesInDirectory(directory)
	for item in files_list:
		print(item)
		if os.path.isdir(item):
			printFilesInDirectory(item, dirDeep)
			dirDeep += 1
			print(item)
		else:
			currentFileContent = readFileContent(item)
			calculated_hash = calculateHashes(item, currentFileContent)
			output_data.add_row([item, "calculated_hash"])


_HASHIGNORE = readFileContent(".HASHIGNORE")
print(".HASHIGNORE FILE:", *_HASHIGNORE)

printFilesInDirectory(current_dir, 0)

output_data.title = f"LIST OF CALCULATED CHECKSUMS ({datetime.datetime.now()})"
output_data.field_names = ["FILE", "CHECKSUM (SHA-256)"]

