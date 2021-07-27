import re
import sys


def open_file_and_get_columns(name):
	count = 0
	with open(name, encoding='utf-8') as file:
		column_names = file.readline().strip().split(',')
		dict1 = dict(zip(column_names, [[] for _ in range(len(column_names))]))
		desribtion = [i.strip().split(',') for i in file.readlines()]
		for key in dict1:
			for i in desribtion:
				dict1[key].append(i[count])
			count += 1
	return dict1


def maximun(args):
	nums = [len(i) for i in args]
	for i in range(1, len(nums)):
		if nums[i - 1] == nums[i]:
			continue
		else:
			return False
	return True


def max_length():
	if maximun(columns[i]):
		return len(columns[i][0])
	max1 = len(max(columns[i], key=len))
	return max1 + max1 * 0.25


def check_model(models):
	# demo_patterns ver 1.0
	pattern_email = r'[\w\.]+@[\w]+\.[\w]+'
	pattern_boolean = r'[True|False]'
	pattern_url = r'([https|http|ftp]+)://([\w\.]+)'
	pattern_date = r'[\d{2}\.\d{2}+\.\d{4} | \d{4}\-\d{2}\-\d{2} | \d{2}\/\d{2}+\/\d{4}]'
	# IntegerField()
	if all([i.replace('-', '').isdigit() for i in models]):
		for i in models:
			if int(i) < 0:
				return 'IntegerField()'
		return 'PositiveIntegerField()'
	# EmailField()
	elif all([re.match(pattern_email, i) for i in models]):
		return f'EmailField()'
	# BooleanField()
	elif all([re.match(pattern_boolean, i.title()) for i in models]):
		return f'BooleanField()'
	# URLField()
	elif all([re.match(pattern_url, i) for i in models]):
		return f'URLField()'
	elif all([re.match(pattern_date, i) for i in models]):
		return f'DateField()'
	# default CharField()
	else:
		return f'CharField(max_length = {max_length()})'


name = sys.argv[1]
columns = open_file_and_get_columns(name)

with open('file.py', 'w') as f:
	class_name = ''.join([i.title() for i in name[:-4].split('_')])
	f.write(f'from django.db import models\n\n\n')
	f.write(f'class {class_name}(models.Model):\n\t')
	for i in columns:
		f.write(f'{i} = models.{check_model(columns[i])}\n\t')
