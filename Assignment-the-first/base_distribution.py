#!/usr/bin/env python

import numpy as np
import bioinfo
import argparse
import gzip

def get_args():
    parser = argparse.ArgumentParser()
    parser.add_argument("-f", "--filename", help="Input filename", required=True)
    parser.add_argument("-o", "--outfile", help="output file name", type=str)
    parser.add_argument("-l", "--length", help="length of sequence", type=int)
    return parser.parse_args()

args=get_args()
f=args.filename
o=args.outfile
l=args.length

def init_list(lst: list, l, value: float=0.0) -> list:
    '''This function takes an empty list and will populate it with
    the value passed in "value". If no value is passed, initializes list
    with 101 values of 0.0.'''
    for ZEROS in range(l):
        lst.append(value)
    return lst
my_list: list = []
my_list = init_list(my_list, l, 0.0)

def populate_list(f: str) -> tuple[list, int]:
    """Creates an ongoing sum of Phred scores from the file."""
    lst=[]
    my_list=init_list(lst, l, 0.0)
    num_lines=0

    with gzip.open(f, "rt") as fastq:
        for line in fastq:
            num_lines=num_lines+1
            line = line.strip('\n')
            if num_lines%4 == 0:
                for index,letter in enumerate(line):
                    score = bioinfo.convert_phred(letter)
                    my_list[index] += score

                    #emptylist is no longer empty, it's filled with the ongoing sums of each phred score                
    return my_list, num_lines

my_list, num_lines = populate_list(f)

print('#of base pairs\tMean Quality Score')
for i,thing in enumerate(my_list): 
    averagescore= thing/(num_lines/4)
    my_list[i]=averagescore
    print(f'{i}\t{averagescore}')

import matplotlib.pyplot as plt
plt.bar(range(l), my_list)
plt.xlabel('Number of Base Pairs')
plt.ylabel('Mean Quality Score')
plt.title('Mean Quality Score of '+ o)
plt.savefig(o+".png")
