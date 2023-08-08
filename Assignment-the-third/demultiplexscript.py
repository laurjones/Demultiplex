#!/usr/bin/env python

# import numpy as np
import argparse
import gzip

def get_args():
    parser = argparse.ArgumentParser()
    parser.add_argument("-f1", "--filename1", help="Input filename1", required=True)
    parser.add_argument("-f2", "--filename2", help="Input filename2", required=True)
    parser.add_argument("-f3", "--filename3", help="Input filename3", required=True)
    parser.add_argument("-f4", "--filename4", help="Input filename4", required=True)
    return parser.parse_args()

args=get_args()
f1=args.filename1
f2=args.filename2
f3=args.filename3
f4=args.filename4

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

known_dict={"GTAGCGTA":0,"AACAGCGA":0,"CTCTGGAT":0,"CACTTCAC":0,"CGATCGAT":0,"GATCAAGG":0,"TAGCCATG":0,"CGGTAATC":0,"TACCGGAT":0,"CTAGCTCA":0,"GCTACTCT":0,"ACGATCAG":0,"TATGGCAC":0,"TGTTCCGT":0,"GTCCTAAG":0,"TCGACAAG":0,"TCTTCGAC":0,"ATCATGCG":0,"ATCGTGGT":0,"TCGAGAGT":0,"TCGGATTC":0,"GATCTTGC":0,"AGAGTCCA":0,"AGGATAGC":0}
instances_dict={"matched":0, "hopped":0, "unknown":0}
possibleindexpairs_dict={}

unknownR1=open("unknown_R1.fq", "w")
unknownR4=open("unknown_R2.fq", "w")
matchedR1=open("matched_R1.fq", "w")
matchedR4=open("matched_R2.fq", "w")
hoppedR1=open("hopped_R1.fq", "w")
hoppedR4=open("hopped_R2.fq", "w")

with open (f1,"r") as fh1, open (f2,"r") as fh2, open (f3,"r") as fh3, open (f4,"r") as fh4:
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
 
        index1=record_r2[1]
        index3=reverse_compliment_function(record_r3[1])
        
        new_key=(index1 +'-'+index3)

        if "N" in record_r2[1] or "N" in index3:
            instances_dict["unknown"]+=1
            unknownR1.write(record_r1[0]+'\n'+record_r1[1]+'\n'+record_r1[2]+'\n'+record_r1[3]+'\n') 
            unknownR4.write(record_r4[0]+'\n'+record_r4[1]+'\n'+record_r4[2]+'\n'+record_r4[3]+'\n')
        elif index1 not in known_dict or index3 not in known_dict:
            instances_dict["unknown"]+=1
            unknownR1.write(record_r1[0]+'\n'+record_r1[1]+'\n'+record_r1[2]+'\n'+record_r1[3]+'\n') 
            unknownR4.write(record_r4[0]+'\n'+record_r4[1]+'\n'+record_r4[2]+'\n'+record_r4[3]+'\n')
        elif index1 in known_dict and index1==index3:
            instances_dict["matched"]+=1
            matchedR1.write(record_r1[0]+'\n'+record_r1[1]+'\n'+record_r1[2]+'\n'+record_r1[3]+'\n') 
            matchedR4.write(record_r4[0]+'\n'+record_r4[1]+'\n'+record_r4[2]+'\n'+record_r4[3]+'\n')
            if new_key in possibleindexpairs_dict:
                possibleindexpairs_dict[new_key]+=1
            else:
                possibleindexpairs_dict[new_key]=1
        elif index1 in known_dict and index3 in known_dict and index1!=index3:
            instances_dict["hopped"]+=1
            hoppedR1.write(record_r1[0]+'\n'+record_r1[1]+'\n'+record_r1[2]+'\n'+record_r1[3]+'\n')
            hoppedR4.write(record_r4[0]+'\n'+record_r4[1]+'\n'+record_r4[2]+'\n'+record_r4[3]+'\n')
            if new_key in possibleindexpairs_dict:
                possibleindexpairs_dict[new_key]+=1
            else:
                possibleindexpairs_dict[new_key]=1
print(possibleindexpairs_dict)
#print(instances_dict)

unknownR1.close()
unknownR4.close()
matchedR1.close()
matchedR4.close()
hoppedR1.close()
hoppedR4.close()


