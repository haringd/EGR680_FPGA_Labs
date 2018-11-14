# -*- coding: utf-8 -*-
"""
Created on Thu Nov  1 18:53:04 2018

@author: schwa
"""

out=open("output.txt", 'w')
f=open("input.txt",'r')
for lines in f:
    out.write(str(float(lines))+'\n')
out.close()
f.close()