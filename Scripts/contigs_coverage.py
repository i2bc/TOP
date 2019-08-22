import argparse


def complement(kmer):  # complementary reverse function
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


parser = argparse.ArgumentParser()
parser.add_argument('DRs_file', help="input repeat sequences file")
parser.add_argument('contigs_file', help="input rnaspade's transcripts file")
parser.add_argument('output_file', help="define the path and the name file")
args = parser.parse_args()

DRs_file = args.DRs_file
contigs_file = args.contigs_file
output = args.output_file

contigs = []
contig = ""
headers = []
reverse_list = []

with open(contigs_file, "r") as contigs_f:  # contigs list take as value all contigs from contigs_file
    # and headers list take as values all headers from contigs_file
    lines = contigs_f.readlines()
    for line in lines:
        if ">" in line:
            headers.append(line)
            contigs.append(contig)
            contig = ""
        else:
            contig = contig + line.strip()
    contigs.append(contig)

contigs.pop(0)  # delete first element from this list because it isn't a contig

with open(DRs_file, "r") as DRs_f:  # Drs list take as values all repeats from Drs_file
    Drs = [DR for i, DR in enumerate(DRs_f.readlines()) if i % 2 == 1]
    Drs_list = [Dr.strip() for Dr in Drs]

for dr in Drs_list:
    reverse_list.append(complement(dr))  # reverse_liste take as values complementary reverse of
    # all repeat from Drs list
    all_drs = Drs_list + reverse_list  # all_drs list composed of repeats and their complementary reverse sequence

open(output, 'a').close()  # create empty file

for i in range(0, len(contigs)):
    words = headers[i].split("_")
    if float(words[5]) > 1:  # if assembly coverage > 1
        a = 0
        while a < len(all_drs):
            if all_drs[a] in contigs[i]:
                # if repeat is in contig of contigs list, write contig in a new file and check for next contigs.
                with open(output, "a") as new_contigs:
                    print(headers[i])
                    new_contigs.write(headers[i] + contigs[i] + '\n')
                    a = len(all_drs)
            else:  # if not, check if others repeats from all_drs list are in this contig
                a = a + 1




