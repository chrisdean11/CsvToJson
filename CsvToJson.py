#!/usr/bin/python3
import os
import glob

# Returns the indent to the first non-empty string, where the number of commas is the value of the indent
def getIndent(line):
	ind = 0
	for str in line:
		if (str.strip() == str) ind++
		else return ind
	return -1

# Returns the number of non-empty values on this line of csv. Assumes there are no empty strings in-between.
def count(line):
	count = 0
	for str in line:
		if (str.strip() != str):
			count++
	return count

# Returns whitespace to indent the output file
def indent(num):
	result = ""
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
	elif(str.tolower() == 'true' || str.tolower() == 'false' || str.tolower() == 'null'):
		return str.tolower()
	else:
		return "\"" + line[indent] "\""

def main():
	with open ('./file') as f:
		res = "{\n"
		ind = 0

		while (True):
			line = file.readline().split(',')

			# End of an object
			if (getIndent(line) < ind):
				ind--
				res += indent(ind) + "}\n"

			# Beginning of new object
			if (count(line) == 1):
				res += "\"" + getValAtColumn(line, getIndent(line)) + "\" : {\n"
				ind++

			# Key-Value pair
			elif (count(line) == 2):
				res += "\"" + line[getIndent(line)] + "\" : " + getValAtColumn(line, getIndent(line) + 1) + ",\n"

			# Array
			elif (count(line) > 2):
				res += "\"" + line[getIndent(line)] + "\" : ["
				for 
				res += "]\n"

			# Blank line at end or error
			else:


if __name__ == "__main__":
	print('executing CsvToJson')
	main()
