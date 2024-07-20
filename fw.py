import hashlib
from prettytable import PrettyTable


filename = 'users.sql'
output_data = PrettyTable()

with open(filename) as file:
	content = file.readlines()

output_data.field_names = ["DATA", "HASH"]

i = 0
hashed_string = hashlib.sha256(bytes(filename, encoding='utf=8')).hexdigest()

for string in content:
	b_string = bytes(string, encoding='utf-8')
	hashed_string = hashlib.sha256(b_string+bytes(hashed_string, encoding='utf-8')).hexdigest()
	output_data.add_row([f"string num.{i}", hashed_string])
	i += 1

print(output_data)
