#-*- coding:utf-8 -*-
'''
特殊代码
* 代替任意字符
[abc...] 匹配方括号中的任意一个字符
使用方式
如果过滤规则以 / 作为结尾 则表示过滤掉整个文件夹
如果规则不包含路径 则过滤掉所有文件夹里面匹配的文件
如果包含路径 则表示顾虑掉某一个路径下的某个文件
顾虑规则第一字符不能是 /

举例说明
name.txt                过滤所有name.txt的文件
*.txt                   过滤所有后缀为.txt的文件
*.t[axy]t               过滤所有后缀为.tat or .txt or .tyt的文件
public/                 过滤所有文件夹下的文件
public/agc.txt          过滤掉public文件夹下的agc.txt文件

'''
import re
class Filter:
    '''
    过滤器类 通过配置文件里面的配置来过滤哪些文件修改动作可以忽略
    '''
    def __init__(self, match_list):
        for item in match_list:
            if item[0] == '/':
                raise ValueError('unvalide rule -- %s' % item)

