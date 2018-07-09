# -*- coding: UTF-8 -*-

import os
import requests
import json
import re
import math
import operator
import csv
import jieba

def segmentation_one(content):

	stopword = [
		'！', '~', '。', '：', '@', '、', '∼', '，',
		'阿', '喔', '啦', '啊', '了', '的',
		'推', '要', '真', '了', '和', '是',
		'就', '你', '妳', '他', '她', '才', '且', 
		'都','而','及','與','著','或',
		'一個', '沒有', '是否',
		'我們','你們','妳們','他們','她們', '哈哈哈', '啊啊啊']
	for word in stopword:
		content = content.replace(word, " ")

	seg_list = list(jieba.cut(content, cut_all = False))
	return seg_list




def tf_idf():
	tf_result = {}
	with open('tf_idf.csv', 'r') as csvfile:
		red = csv.reader(csvfile, delimiter=',')
		for k, v in red:
			if float(v) > 0:
				tf_result[k] = v
	return tf_result


def get_summary(content, tf_idf):

	contentSegment = re.split('，|。', content)

	segmentScoreList = []
	for i in range(len(contentSegment)):
		score = 0
		total = 0
		seg_list = segmentation_one(contentSegment[i])

		for seg in seg_list:
			try:
				score += float(tf_idf[seg])
				total += 1
			except KeyError:
				pass

		if total != 0:
			segmentScoreList.append({
				'segment' : contentSegment[i],
				'score' : score / total
			})

	scoreList = sorted(segmentScoreList, key=lambda k: k['score'], reverse=True)
	
	goals = []
	i = 0
	for s in scoreList:
		if len(s['segment']) > 10:
			goals.append(s['segment'])
			i += 1
			if i == 5:
				break

	#0-1300字 10句話，1301-1950字 15句話，1951-2600 20句話，2601-3250 25句話，3251-Max 30句話
	length = [0,1301,1951,2601,3251,1000000000000000000000]
	limit = [10,15,20,25,30]
	
	for lower,upper,c in zip(length,length[1:],limit):
		if lower <= len(content) < upper:
			limit = c
			break
	
	result = []
	flag = 0
	for i in range(len(contentSegment)):
		if contentSegment[i] in goals:
			try:
				if flag < limit:
					flag += 1
					result.append(contentSegment[i])
			except:
				pass
	return '，'.join(result) + "。"


def main():

	tf_idf_res = tf_idf()

	for i in range(2,3):
		with open('./testData/dataset' + str(i)+ '.txt', 'r') as txtfile:
			tr = txtfile.readlines()
			flag = True
			for t in tr:
				if flag is True:
					article = t
					for a in article:
						if '。' == a:
							print(i)
					# else:
					summary = get_summary(article, tf_idf_res)
					#print(summary)
				
				flag = not flag

if __name__ == '__main__':
	main()
