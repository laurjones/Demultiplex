#!/usr/bin/env python

import argparse
import gzip

#implementing argparse
def get_args():
    parser = argparse.ArgumentParser()
    parser.add_argument("-f1", "--filename1", help="Input filename1", required=True)
    parser.add_argument("-f2", "--filename2", help="Input filename2", required=True)
    parser.add_argument("-f3", "--filename3", help="Input filename3", required=True)
    parser.add_argument("-f4", "--filename4", help="Input filename4", required=True)
    parser.add_argument("-i", "--indexes", help="Input indexfilename", required=True)
    return parser.parse_args()

args=get_args()
f1=args.filename1
f2=args.filename2
f3=args.filename3
f4=args.filename4
i=args.indexes

my_dict = {"A":"T","T":"A","G":"C","C":"G","N":"N"}
def reverse_compliment_function(DNA:str) -> str:
    '''A function that reverse compliments barcodes.'''
    new_seq = ""
    for base in DNA:
        new_seq += my_dict[base]
    return (new_seq[::-1])

def readfour(fh):
    '''Function to read through four lines and returns all lines in record as a tuple'''
    header=fh.readline().strip()
    seq=fh.readline().strip()
    plus=fh.readline().strip()
    qual=fh.readline().strip()
    return header,seq,plus,qual

#dictionaries used
instances_dict={"matched":0, "hopped":0, "unknown":0}
possibleindexpairs_dict={}
indexes_dict={}

#populating index dictionary with indexes(key) and filehandles(value)
with open (i , "r") as fh:
    for line in fh:
        indexes=line.strip().split('\t')[4]
        indexes_dict[indexes]=[open(indexes+"R1.fq", "w"),open(indexes+"R2.fq", "w")]

#opening unknown and hopped files
unknownR1=open("unknown_R1.fq", "w")
unknownR4=open("unknown_R2.fq", "w")
hoppedR1=open("hopped_R1.fq", "w")
hoppedR4=open("hopped_R2.fq", "w")

with gzip.open (f1,"rt") as fh1, gzip.open (f2,"rt") as fh2, gzip.open (f3,"rt") as fh3, gzip.open (f4,"rt") as fh4:
    while True:
        record_r1 = readfour(fh1)
        #print(record_r1)
        if record_r1 == ("","","",""):
            break #breaks when reaches end of the file where there are no more tuples
        record_r2 = readfour(fh2)
        record_r3 = readfour(fh3)
        record_r4 = readfour(fh4)
        new_header = record_r1[0]+" "+record_r2[1]+"-"+reverse_compliment_function(record_r3[1])
        #print(record_r2)
 
        index1=record_r2[1] #had already been reverse complimented, so we didn't need to do it again
        index3=reverse_compliment_function(record_r3[1])
        
        new_key=(index1+'-'+index3)

        if "N" in record_r2[1] or "N" in index3: #puts all indexes with unknown nucleotide into unknown file
            instances_dict["unknown"]+=1 #increments each time there is an unknown index
            unknownR1.write(record_r1[0]+'\n'+record_r1[1]+'\n'+record_r1[2]+'\n'+record_r1[3]+'\n') 
            unknownR4.write(record_r4[0]+'\n'+record_r4[1]+'\n'+record_r4[2]+'\n'+record_r4[3]+'\n')
        elif index1 not in indexes_dict or index3 not in indexes_dict: #puts all indexes not in the known index into unkown file
            instances_dict["unknown"]+=1 #increments each time there is an unknown index
            unknownR1.write(record_r1[0]+'\n'+record_r1[1]+'\n'+record_r1[2]+'\n'+record_r1[3]+'\n') 
            unknownR4.write(record_r4[0]+'\n'+record_r4[1]+'\n'+record_r4[2]+'\n'+record_r4[3]+'\n')
        elif index1 in indexes_dict and index1==index3: #puts all matched indexes into appropriate file
            instances_dict["matched"]+=1 #increments each time there is a matched index 
            indexes_dict[index1][0].write(record_r1[0]+'\n'+record_r1[1]+'\n'+record_r1[2]+'\n'+record_r1[3]+'\n') 
            indexes_dict[index1][1].write(record_r4[0]+'\n'+record_r4[1]+'\n'+record_r4[2]+'\n'+record_r4[3]+'\n')
            if new_key in possibleindexpairs_dict: #increments each time a new index occurs
                possibleindexpairs_dict[new_key]+=1
            else:
                possibleindexpairs_dict[new_key]=1
        elif index1 in indexes_dict and index3 in indexes_dict and index1!=index3: #puts all hopped indexes into appropriate file
            instances_dict["hopped"]+=1 #increments each time there is a hopped index
            hoppedR1.write(record_r1[0]+'\n'+record_r1[1]+'\n'+record_r1[2]+'\n'+record_r1[3]+'\n')
            hoppedR4.write(record_r4[0]+'\n'+record_r4[1]+'\n'+record_r4[2]+'\n'+record_r4[3]+'\n')
            if new_key in possibleindexpairs_dict: #increments each time a new index occurs
                possibleindexpairs_dict[new_key]+=1
            else:
                possibleindexpairs_dict[new_key]=1
        else:
            print("WARNING! Unexpected result!", record_r1) #fun Leslie trick to see if something funky is happening in output

print("index combination\tnumber of occurences") #formatting the output for both dictionaries as a string with a header where needed
for key in possibleindexpairs_dict:
    print(key,possibleindexpairs_dict[key], sep='\t')
print()
for key in instances_dict:
    print(key,instances_dict[key], sep='\t')


unknownR1.close() #closing all unknown and hopped files
unknownR4.close()
hoppedR1.close()
hoppedR4.close()

for key in indexes_dict: #closing all indexed files
    indexes_dict[key][0].close()
    indexes_dict[key][1].close()

