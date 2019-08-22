import argparse
import csv

parser = argparse.ArgumentParser()
parser.add_argument('tax_ID', help="input a tax ID")
parser.add_argument('file_genome', help="input the csv with reference genome and their associated ID")
parser.add_argument('path', help="output path")
args = parser.parse_args()

id = args.tax_ID
file_genome = args.file_genome
path = args.path

link1 = ""
link2 = ""
link3 = ""
link4 = ""

with open(file_genome, "r") as gen_file:
    genome = csv.reader(gen_file, delimiter='\t')
    for column in genome:  # retrieve one genome for the taxID (specie)
        if len(column) > 1 and column[6] == id:
            if (column[4] == 'reference genome' or column[4] == 'representative genome') and column[11] == 'Complete ' \
                    'Genome' and link1 == "":
                link1 = column[19]
            elif (column[4] == 'reference genome' or column[4] == 'representative genome') and column[11] != 'Complete'\
                    ' Genome' and link2 == "":
                link2 = column[19]
            elif (column[4] != 'reference genome' and column[4] != 'representative genome') and column[11] == \
                    'Complete Genome' and link3 == "":
                link3 = column[19]
            else:
                link4 = column[19]

if link1 == "" and link2 == "" and link3 == "" and link4 == "":  # if no match with a specie taxID
    with open(file_genome, "r") as gen_file:
        genome = csv.reader(gen_file, delimiter='\t')
        for column in genome:  # retrieve one genome for the taxID (strain)
            if len(column) > 1 and column[5] == id:
                if (column[4] == 'reference genome' or column[4] == 'representative genome') and column[11] == \
                        'Complete Genome' and link1 == "":
                    link1 = column[19]
                elif (column[4] == 'reference genome' or column[4] == 'representative genome') and column[11] != \
                        'Complete Genome' and link2 == "":
                    link2 = column[19]
                elif (column[4] != 'reference genome' and column[4] != 'representative genome') and column[11] == \
                        'Complete Genome' and link3 == "":
                    link3 = column[19]
                else:
                    link4 = column[19]


with open(path+"/link.txt", "w") as linkf:  # Priority : link1 > link2 > link3 > link4. Keep the best one in a txt file

    if link1 != "":
        linkf.write(link1)
    elif link2 != "":
        linkf.write(link2)
    elif link3 != "":
        linkf.write(link3)
    elif link4 != "":
        linkf.write(link4)
