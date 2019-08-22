import argparse
import csv
import os
from rpy2.robjects import r

def replace_str_index(text, index=0, replacement=''):
    return text[:index] + replacement + text[index + 1:]


def complement(kmer):  # return kmer's reverse complementary sequence
    reverse = ""
    rev_l = ""
    for letter in kmer[::-1]:
        if letter == "A":
            rev_l = "T"
        elif letter == "T":
            rev_l = "A"
        elif letter == "C":
            rev_l = "G"
        elif letter == "G":
            rev_l = "C"
        elif letter == "\n":
            rev_l = ""
        reverse += rev_l
    return reverse


def dr_list(dr="", k=0):  # return list of DR's kmer with one mismatch
    list = []
    i = 0
    while i + k < len(dr) + 1:
        kmer = dr[i:k + i]
        if kmer not in list:
            list.append(kmer)
        pos = 0
        while pos < k:  # create kmer with one mismatch at each position of the kmer
            kmer1 = replace_str_index(kmer, pos, "A")
            if kmer1 not in list:
                list.append(kmer1)
            kmer1 = replace_str_index(kmer, pos, "C")
            if kmer1 not in list:
                list.append(kmer1)
            kmer1 = replace_str_index(kmer, pos, "G")
            if kmer1 not in list:
                list.append(kmer1)
            kmer1 = replace_str_index(kmer, pos, "T")
            if kmer1 not in list:
                list.append(kmer1)
            pos += 1
        i += 1
    return list


def proportion_sens(files, list_k, list_r):  # proportion of reads in direct orientation and in antisense.
    # list_k= list of kmers in direct sens ; list_r list of reverse kmers

    forward = 0  # variable "forward" to count the number of reads in forward sens
    reverse = 0  # variable "reverse" to count the number of reads in reverse sens

    in_list_k = set(list_k)
    in_list_r = set(list_r)
    not_duplicate_kmers = in_list_r - in_list_k
    list_all_kmers = list_k + list(not_duplicate_kmers)  # list that contains all kmers and their reverse

    with open(files, "r") as read:
        lignes = [ligne for i, ligne in enumerate(read.readlines()) if i % 4 == 1]  # list of all read sequences from
        # the file
        for ligne in lignes:  # for each read
            match_read = 0
            i = 0
            while i < len(list_all_kmers) and match_read == 0:  # match_read is a variable to stop looking at kmer if
                # one kmer has already match in read
                # if kmer in read is in list_k then +1 for forward
                # if kmer in read is in list_r then +1 for reverse
                if list_all_kmers[i] in ligne:
                    if list_all_kmers[i] in list_k and match_read == 0:
                        forward += 1
                        match_read = 1
                    if list_all_kmers[i] in list_r and match_read == 0:
                        reverse += 1
                        match_read = 1
                i += 1
        if forward + reverse > 0:  # to give proportion of read in forward and in reverse
            pforward = round(forward / (reverse + forward) * 100.0, 3)
            preverse = round(reverse / (reverse + forward) * 100.0, 3)
        else:
            pforward = 0
            preverse = 0
        return pforward, forward, preverse, reverse


def bbduk(file_log):  # to retrieve the number of reads in the archive
    with open(file_log, 'r') as log:
        lines = log.readlines()
        for line in lines:
            if "Input:" in line:
                words_line = line.split("\t")
                words_nbreads = words_line[1].split(" ")
                nbreads = int(words_nbreads[0])
                return nbreads


parser = argparse.ArgumentParser()
parser.add_argument('reads_file', help="input reads file")
parser.add_argument('DRs_file', help="input repeat sequences file")
parser.add_argument('k', type=int, help="input kmer size used in BBDuk")
parser.add_argument('bbduk_log', help="input BBDuk_log file")
parser.add_argument('output_file', help="define the path and the name file")
args = parser.parse_args()

reads_file = args.reads_file
DRs_file = args.DRs_file
k = args.k
bbduk_log = args.bbduk_log
output = args.output_file

archive = os.path.basename(reads_file)  # retrieve archive name
taxon = os.path.dirname(DRs_file)  # retrieve tax_id
path = os.path.dirname(reads_file)  # retrieve path where fq file is

readstotaux = bbduk(bbduk_log)

if not os.path.exists(output):  # if board isn't already created then create it with this header
    with open(output, 'w') as board:
        board = csv.writer(board, delimiter='\t')
        board.writerow(("Tax ID", "Archive's name", "Repeat sequence", "Number of CRISPR reads in archive",
                        "% reads CRISPR in archive", "Number of reads in input sens ", "% reads in input direction ",
                        "Number of reads in reverse input direction ", "% reads in reverse input sens",
                        "Repeat sens in archive","p-value"))

with open(DRs_file, "r") as read:
    Drs_list = [DR for i, DR in enumerate(read.readlines()) if i % 2 == 1]  # list that contains all Drs from the file
    for DR in Drs_list:
        kmer_list = dr_list(DR, k)
        reverse_DR = complement(DR)
        reverse_list = dr_list(reverse_DR, k)
        pforward, forward, preverse, reverse = proportion_sens(reads_file, kmer_list, reverse_list)

        pCRISPRreads = round((forward + reverse) / readstotaux * 100.0, 3)  # percentage of CRISPR reads found

        if pforward > 65:
            sens = "+"
        elif pforward < 35:
            sens = "-"
        elif 65 >= pforward >= 35:
            sens = "unstranded"
        if pforward == 0 and preverse == 0:
            sens = "ND"

        if forward+reverse > 0:
            r.assign('forward', forward)  # assign forward and reverse as a variable R called forward and reverse
            r.assign('reverse', reverse)
            var=r('df = binom.test(x=forward,n=forward+reverse,p=0.5)$p.value')  # binomial test in R
            list_var = list(var)  # retrieve the p-value of binomial test into a list
            pvalue=list_var[0]
        else:
            pvalue="ND"

        with open(path + "/" + os.path.splitext(archive)[0] + ".txt", "w") as txt:  # keep results in a txt file
            txt.write("Reads' number having repeat in input's direction : " + str(forward) + "\t%: " + str(
                pforward) + "\nReads' number having repeat in reverse input direction: " + str(reverse) + "\t%: " + str(
                preverse))

        with open(output, 'a') as board:  # Put results in a csv file
            board = csv.writer(board, delimiter='\t')
            board.writerow((os.path.basename(taxon), os.path.splitext(archive)[0], DR.rstrip('\n'),
                            str(forward + reverse), str(pCRISPRreads) + '%', forward, str(pforward) + '%', reverse,
                            str(preverse) + '%', sens, str(pvalue)))
