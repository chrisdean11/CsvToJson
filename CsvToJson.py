#!/usr/bin/python3
import os
import sys
import glob

# Returns the indent to the first non-empty string, where the number of commas is the value of the indent
def getIndent(line):
	ind = 0
	for str in line:
		if (str.strip() == ''):
			ind = ind + 1
		else:
			return ind
	return -1

# Returns the number of non-empty values on this line of csv. Assumes there are no empty strings in-between.
def count(line):
	count = 0
	for str in line:
		if (str.strip() != ''):
			count = count + 1
	return count

# Returns whitespace to indent the output file
def indent(num):
	result = "  "
	for i in range(num):
		result += "  "
	return result

# True if the string is a float, false if not
def isANumber(str):
    try:
        float(str)
        return True
    except:
        return False

# Returns a valid json value as a string: boolean, number, quoted value, or null
def getValAtColumn(line, indent):
	str = line[indent]
	if(isANumber(str)):
		return str
	elif(str.lower() == 'true' or str.lower() == 'false' or str.lower() == 'null'):
		return str.lower()
	else:
		return "\"" + line[indent] + "\""

def stripComma(res):
	# Special case of last character 
	if res[-1] == ',':
		return res[:-1]
	for i in range(1, len(res)):
		# If the last line was the end of an object, it won't have a comma at the end
		if res[-i] == '}':
			return res
		if res[-i] == ',':
			return res[:-i] + res[-i+1:]

def main():
	with open (sys.argv[1]) as file:
		res = "{\n"
		ind = 0

		while (True):
			line = file.readline().rstrip('\n')
			if not line or line.strip() == '':
				break
			line = line.split(',')
			lineIndent = getIndent(line)

			# End of an object
			if (lineIndent < ind):
				ind = ind - 1
				res = stripComma(res)
				res += indent(ind) + "},\n"

			# Beginning of new object
			if (count(line) == 1):
				res += indent(ind) + getValAtColumn(line, lineIndent) + " : \n" + indent(ind) + "{\n"
				ind = ind + 1

			# Key-Value pair
			elif (count(line) == 2):
				res += indent(ind) + "\"" + line[lineIndent] + "\" : " + getValAtColumn(line, lineIndent + 1) + ",\n"

			# Array
			elif (count(line) > 2):
				res += indent(ind) + "\"" + line[lineIndent] + "\" : ["
				for i in range(lineIndent + 1, lineIndent + count(line)):
					res += getValAtColumn(line, i) 
					if i != lineIndent + count(line) - 1: 
						res += ", "
				res += "],\n"

			# 
			else:
				break

		# Get rid of last comma added
		res = stripComma(res)
		res += "}"
		print (res)

		# Write to file
		base = os.path.basename(sys.argv[1])
		filename = os.path.splitext(base)[0] + '.json'
		print(filename)
		resFile = open(filename, "w")
		resFile.write(res)
		resFile.close()

if __name__ == "__main__":
	print('executing CsvToJson')
	main()
