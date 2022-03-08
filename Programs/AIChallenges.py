#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Jan 27 14:06:41 2022
List Comprehension
@author: jorgesilveyra
"""
import random
import re

a = [[[x] for y in range(x) if y %2 ==0 ] for x in range(1,100) if x > 10]
print(a)


b = [random.randint(1,4) for x in range(10)]
print(b[:3])

str1 = "Dan is very bored in class today. Why is that Dan?"
str2 = str1[1:9]
print(str2)

str3 = str1.split()
print(str3)

str4 = str1.replace("Dan","Alan")
print(str4)
str5 = str4.replace("bored","late")
print(str5)



numbers = [-4,233,323,-123,213]
numbers2 = [int(random.gauss(5,10)) for x in range(100)]
print(numbers2)


first = [x for x in numbers2 if x > -1]
print(first)

two = [x for x in range(1001) if str(x).find("3") > -1]
print(two)

for i in range(1000):
    if str(i).find("3")!=-1:
        print(i)


three = [x for x in str1.split()]
print(len(three)-1)

three = len(str1.split())
three = str1.count(" ")
print(three)

four = str1.lower().replace("a","")
vowels = ["a","e","i","o","u"]
for i in vowels:
    str1 = str1.replace(i,"")

four=re.sub(["a","e","i","o","u"],"",str1)
    

five = [x for x in str1.split() if len(x) < 4]
