import argparse
import csv
import os


def orientation(direction, archive_direction):  # Final orientation of sequences
    if direction == "+" and archive_direction == "-":
        orient = "-"
    elif direction == "+" and archive_direction == "+":
        orient = "+"
    elif direction == "-" and archive_direction == "-":
        orient = "+"
    elif direction == "-" and archive_direction == "+":
        orient = "-"
    else:
        orient = "ND"
    return orient


parser = argparse.ArgumentParser()
parser.add_argument('rseqc_results_file', help="input rseqc results file from Python script")
parser.add_argument('csv_board', help="input csv board of percentages CRISPR reads ")
parser.add_argument('archive_name', help="input archive name")
parser.add_argument('path', help="path of the output")
args = parser.parse_args()

rseqc = args.rseqc_results_file
board = args.csv_board
archive_name = args.archive_name
path = args.path

# retrieve percentage of reads for archive orientation from rseqc results file
with open(rseqc, 'r') as rseqc_results:
    sens = rseqc_results.readline().strip()
    words_sens = sens.split("\t")
    sens_archive = words_sens[1]
    percent_sens1 = words_sens[3]
    percent_sens2 = words_sens[5]

# if Results.csv file doesn't already exist then create it with the header.
if not os.path.exists(path + "/Results.csv"):
    with open(path + "/Results.csv", 'w') as tab_f:
        tab_final = csv.writer(tab_f, delimiter='\t')
        tab_final.writerow(("Tax ID", "Archive's name", "Repeat sequence", "Number of CRISPR reads in archive",
                            "% reads CRISPR in archive", "Number of reads in input sens ",
                            "% reads in input direction ",
                            "Number of reads in reverse input direction ", "% reads in reverse input sens",
                            "Repeat sens in archive","p-value", "% Reads ++ in archive (RseqC)", "% Reads +- in archive (RseqC)",
                            "Archive direction", "Repeat direction"))

# Results.csv will take the data from the board of percentages CRISPR reads
# adding RseqC percentages and the orientation of the studied sequences.
# creation of a txt file with results
with open(board, 'r') as tab:
    CRISPR_tab = csv.reader(tab, delimiter='\t')
    for column in CRISPR_tab:
        if archive_name == column[1]:
            nb_reads = int(column[3])
            sens_reads = column[9]
            repeat = column[2]
            ori = orientation(sens_reads, sens_archive)
            with open(path + "/" + archive_name + "/direction_result.txt", "a") as results:
                results.write(repeat + ": \nNumber of CRISPR reads : " + str(
                    nb_reads) + "\n" + "Repeat direction : " + ori + "\n \n")
            with open(path + "/Results.csv", 'a') as tabout:
                final_board = csv.writer(tabout, delimiter='\t')
                result = column + [str(percent_sens1) + '%'] + [str(percent_sens2) + '%'] + [sens_archive] + [ori]
                final_board.writerow(result)
