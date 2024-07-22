import os
import hashlib
from prettytable import PrettyTable
import datetime


output_data = PrettyTable()
current_dir = "."


def enumerateFilesInDirectory(dir, ign_file):
	files_list = []

	for root, dirs, files in os.walk(dir):
		dirs[:] = [d for d in dirs if d not in ign_file]
		files = [f for f in files if f not in ign_file]
		#files_list.append((root, dirs, files))
		for file in files:
			path = os.path.relpath(os.path.join(root, file), start=dir)
			if not any(item in path for item in ign_file):
				files_list.append(path)
	return files_list


def readFileContent(file):
	with open(file) as f:
		content = f.read().splitlines()
	for item in content:
		item = ' '.join(item.strip())
	return content


def calculateHashes(file, content):
	#i = 0
	hashed_string = hashlib.sha256(bytes(file, encoding='utf-8')).hexdigest() # first hash should be file`s header
	for string in content:
		b_string = bytes(string, encoding='utf-8')
		hashed_string = hashlib.sha256(b_string+bytes(hashed_string, encoding='utf-8')).hexdigest()
		#output_data.add_row([f"string num.{i}", hashed_string])
		#i += 1
	return hashed_string


def printFilesInDirectory(directory):
	files_list = enumerateFilesInDirectory(directory, _HASHIGNORE)
	for file in files_list:
		print(file)
		currentFileContent = readFileContent(file)
		calculated_hash = calculateHashes(file, currentFileContent)
		output_data.add_row([file, "calculated_hash"])


_HASHIGNORE = readFileContent(".HASHIGNORE")

printFilesInDirectory(current_dir)

output_data.title = f"LIST OF CALCULATED CHECKSUMS ({datetime.datetime.now()})"
output_data.field_names = ["FILE", "CHECKSUM (SHA-256)"]

