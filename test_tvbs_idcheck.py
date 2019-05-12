# -*- coding: utf-8 -*-
"""
Created on Fri Apr 26 13:31:22 2019

@author: Student
"""
import json;
# 全部結束後產生沒有配對到 type的文章ID列表
id_Check = [];
# 697844 為已確認無法匹配到type的文章 id
for i in range(697844, 1116259, 1):
    with open("C:/news_tvbs/tvbs_type_dic.json", "r") as reader:
        jf = json.loads(reader.read());
        if str(i) in jf:
            print('.',end='');
        else:
            id_Check.append(i);
            print(i);
            