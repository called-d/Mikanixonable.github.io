import json
import glob
import os
import codecs
from PIL import Image
# import pandas as pd
import csv

deskPath = "./Mikanixonable.github.io/"
jsonPath = deskPath + 'json/illusts5.json'

def makeCSV(filename,nums):
    illustRange = (min(int(nums)), max(int(nums)))
    csvPath = deskPath + "./json/" + filename
    with open(csvPath, "w", newline="") as f:
        writer = csv.writer(f, delimiter="\t", quotechar='"', quoting=csv.QUOTE_MINIMAL)
        for i in range(illustRange[0],illustRange[1]+1):
            writer.writerow([i, []])

def csv2dic(filename):
    csv_file_path = deskPath + filename
    dateDic = {}
    with open(csv_file_path, 'r', encoding='utf-8') as csvfile:
        reader = csv.reader(csvfile, delimiter='\t')
        for row in reader:
            dateDic[row[0]] = row[1]

    return dateDic

#実行
def main():
    nums = [os.path.splitext(os.path.basename(png))[0] for png in glob.glob(deskPath + "illusts/*.png")]
    
    #減少分更新
    for illust in illusts:
        if illust["num"] not in nums:
            del illust
    #増加分更新
    for num in nums:
        if num not in dicNums:
            illusts.append({
                "num":num
                           })
    #基本情報の追加
    for illust in illusts:
        imgPath = deskPath + "illusts/" + illust["num"] + ".png"
        img = Image.open(imgPath)
       
        illust["width"] = img.width
        illust["height"] = img.height
        illust["size"] = os.path.getsize(imgPath)

    #csv insert
    dateDic = csv2dic('json/date.csv')
    tagDic = csv2dic("json/tag.csv")
    for illust in illusts:
        n = illust["num"]
        illust["date"] = dateDic[n]
        illust["tags"] = tagDic[n]
    
    #特定の要素削除
    # for illust in illusts:
    #     delKey = "byte"
    #     try :
    #         del illust[delKey]
    #     except KeyError :
    #         print('存在しないキーです')

    # #csv make
    # makeCSV("tag2.csv",nums)


if os.path.isfile(jsonPath):
    f = codecs.open(jsonPath, "r", "utf-8")
    illusts = json.load(f)
    dicNums = [illust.get('num') for illust in illusts]
    f.close()
else:
    illusts = []
    dicNums = []

main()

f = codecs.open(jsonPath, "w", "utf-8")
json.dump(illusts, f, indent = 2, ensure_ascii=False)
f.close()
