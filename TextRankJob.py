import csv
import json
import os

def textrankGet(n):
    # read textrank result
    with open('./textrankRes/' + n + '.csv', 'r', newline='', encoding='utf-8') as csvfile:
        reader = csv.reader(csvfile)
        column = [row[0] for row in reader]

    # experiment value top k keyword of 40%/50%/60%
    exp_value = [0.4, 0.5, 0.6]
    keyword = []
        
    # get textrank top k% keyword from csv
    for e in exp_value:
        ind = 0
        temp = []
        for c in column:
            if ind == (200*e):
                break
            temp.append(c)
            ind += 1
        keyword.append(temp)
    
    return keyword


def textrankJob(n):
    # get keyword
    keyword = textrankGet(n)
    # read testdata line by line
    for i in range(1,8):
        with open( n +'dataset' + str(i) +'.csv', 'w', newline='', encoding = 'utf-8') as res:
            writer = csv.writer(res)
            with open('./testData/dataset' + str(i)+ '.txt', 'r', newline='', encoding='utf-8') as txtfile:
                tr = txtfile.readlines()
                flag = True
                for t in tr:
                    if flag is True:
                        article = t
                    else:
                        # store keyword match on article content
                        keywordMatch = []
                        content = t
                        # start match keyword and content
                        for index in keyword:
                            temp = []
                            for k in index:
                                if k in content:
                                    temp.append(k)
                            keywordMatch.append(temp)
                        # write match result to csv
                        writer.writerow([article.strip()])
                        writer.writerow([content.strip()])
                        exp_value = [0.4, 0.5, 0.6]
                        for j in range(3):
                            tempkeyword = []
                            tempkeyword.append(exp_value[j])
                            for k in keywordMatch[j]:
                                tempkeyword.append(k)
                            writer.writerow(tempkeyword)
                        writer.writerow("\n")

                    flag = not flag

        print("----------------------------------------------")