#!/usr/bin/python

#This scripts performs the basic task  of PEAR (Paired-End reAd mergeR)
#http://sco.h-its.org/exelixis/web/software/pear/doc.html
#But without prerequisites, installations, and so
#It Merges two (pair-end) fastq files (containing raw reads), into one file where reads
#are in consecutive order. Each sequence must be inside ONE LINE.

#For example:

### 1. INPUT FILE (forward reads)  ==> SRR065390_1.fastq <==
#@SRR065390.1 HWUSI-EAS687_61DAJ:8:1:1055:3384 length=100
#TGAANACCTCGAAACTTTTTCAGCGGNNTCNTTNNNNNNNNNNNNNNNNNNNNNNNNNNNNNNNNNNNNNNNNNNNNNNNNNNNNNNNNNNNNNNNNNNN
#+SRR065390.1 HWUSI-EAS687_61DAJ:8:1:1055:3384 length=100
#0000!<:<;:@AAA=@:@@@A@AA@#!!##!##!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
#@SRR065390.2 HWUSI-EAS687_61DAJ:8:1:1055:17846 length=100
#CAGTNAATTTTCGTCGATTTTTCCAANNTTNCGNNNNNNNNNNNNNNNNNNNNNNNNNNNNNNNNNNNNNNNNNNNNNNNNNNNNNNNNNNNNNNNNNNN
#+SRR065390.2 HWUSI-EAS687_61DAJ:8:1:1055:17846 length=100
#0000!8;9;;BBBB@<95?;BABAA#!!##!##!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!


### 2. INPUT FILE (reverse reads)   ==> SRR065390_2.fastq <==
#@SRR065390.1 HWUSI-EAS687_61DAJ:8:1:1055:3384 length=100
#NNNNNNNNNNNNTGAATAAATACTTTTTGCAGATGCTAAAACAATTTCCAAGTAAAAAAATTATNNNNNNNNTNGGCNAGCAGNNGTGAANNNGGNNNAT
#+SRR065390.1 HWUSI-EAS687_61DAJ:8:1:1055:3384 length=100
#!!!!!!!!!!!!####################################################!!!!!!!!#!###!#####!!#####!!!##!!!##
#@SRR065390.2 HWUSI-EAS687_61DAJ:8:1:1055:17846 length=100
#NNNNNNNNNNNNAATGAGCTGAAAAATGTCAAAATTTCGAAAAATTGGCCGGAAAATGACCGAANNNNNNNNNNNNTNGNCGANNATTGANNNNGNNNGN
#+SRR065390.2 HWUSI-EAS687_61DAJ:8:1:1055:17846 length=100
#!!!!!!!!!!!!####################################################!!!!!!!!!!!!#!#!###!!#####!!!!#!!!#!


### 3. Output File
#@SRR065390.1 HWUSI-EAS687_61DAJ:8:1:1055:3384 length=100
#TGAANACCTCGAAACTTTTTCAGCGGNNTCNTTNNNNNNNNNNNNNNNNNNNNNNNNNNNNNNNNNNNNNNNNNNNNNNNNNNNNNNNNNNNNNNNNNNN
#+SRR065390.1 HWUSI-EAS687_61DAJ:8:1:1055:3384 length=100
#0000!<:<;:@AAA=@:@@@A@AA@#!!##!##!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
#@SRR065390.1 HWUSI-EAS687_61DAJ:8:1:1055:3384 length=100
#NNNNNNNNNNNNTGAATAAATACTTTTTGCAGATGCTAAAACAATTTCCAAGTAAAAAAATTATNNNNNNNNTNGGCNAGCAGNNGTGAANNNGGNNNAT
#+SRR065390.1 HWUSI-EAS687_61DAJ:8:1:1055:3384 length=100
#!!!!!!!!!!!!####################################################!!!!!!!!#!###!#####!!#####!!!##!!!##
#@SRR065390.2 HWUSI-EAS687_61DAJ:8:1:1055:17846 length=100
#CAGTNAATTTTCGTCGATTTTTCCAANNTTNCGNNNNNNNNNNNNNNNNNNNNNNNNNNNNNNNNNNNNNNNNNNNNNNNNNNNNNNNNNNNNNNNNNNN
#+SRR065390.2 HWUSI-EAS687_61DAJ:8:1:1055:17846 length=100
#0000!8;9;;BBBB@<95?;BABAA#!!##!##!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
#@SRR065390.2 HWUSI-EAS687_61DAJ:8:1:1055:17846 length=100
#NNNNNNNNNNNNAATGAGCTGAAAAATGTCAAAATTTCGAAAAATTGGCCGGAAAATGACCGAANNNNNNNNNNNNTNGNCGANNATTGANNNNGNNNGN
#+SRR065390.2 HWUSI-EAS687_61DAJ:8:1:1055:17846 length=100
#!!!!!!!!!!!!####################################################!!!!!!!!!!!!#!#!###!!#####!!!!#!!!#!

#It only works for fastq format

from itertools import  izip
import argparse

BUCKET_SIZE = 40000   #just to prevent the costly disk accesses, write only after some size

def _exit(message):
    print message
    exit(1)
    

def check_files(forward, reverse):
    
    with open(forward, "r") as f, open(reverse, "r") as r:
        
        f_firstLine = f.readline()
        r_firstLine = r.readline()
        
        if f_firstLine[0] != '@' or r_firstLine[0] != '@':
            print r_firstLine[0] +' <-- ??'
            _exit('It does not look like fastq format... ')
            
        if f_firstLine.split(' ')[0] != r_firstLine.split(' ')[0]:
            _exit('Reads do not much as pair-end')
          

def merge(forward, reverse, output):
    
    check_files(forward, reverse)
            
    f_bucket = []
    r_bucket = []
    with open(forward, "r") as f, open(reverse, "r") as r, open(output, "w") as w:
        
        w_bucket = []
        for fi, ri in izip(f, r):
            f_bucket.append(fi)
            r_bucket.append(ri)
            if len(f_bucket) == 4:
                w_bucket.extend(f_bucket + r_bucket)
                f_bucket = []
                r_bucket = []
            if len(w_bucket) > BUCKET_SIZE:
                w.write("".join(w_bucket))
                w_bucket = []
        w.write("".join(w_bucket))
    
def main():
    parser = argparse.ArgumentParser(description='coming soon')
    parser.add_argument('-f', '--forward',  help='forward reads')
    parser.add_argument('-r', '--reverse',  help='reverse reads')
    parser.add_argument('-o', '--output',  help='output file')
    args = parser.parse_args()
    
    #assert (args == 4)
    merge(args.forward, args.reverse, args.output)

if __name__ == "__main__":
    main()
