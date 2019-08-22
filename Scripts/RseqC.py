import argparse
import os

parser = argparse.ArgumentParser()
parser.add_argument('rseqc_log', help="input RseqC log")
args = parser.parse_args()

file_log = args.rseqc_log

name = os.path.basename(file_log)
path = os.path.dirname(file_log)

with open(file_log, 'r') as log:
    if os.stat(file_log).st_size == 0 :
        fes=0
        fea=0
        controle = "ND"
        with open(path + "/sens_archive.txt", "w") as result:
            result.write("Sens archive:\t" + controle + "\tReads percentage ++ in archive (rseqC) :\t" + str(
                fes) + "\tReads percentage reads +- in archive (rseqC) : \t" + str(
                fea))
    else :
        lines = [line.strip() for line in log]  # retrieve information of rseqc results

        words_failed = lines[3].split(" ")
        ff = float(words_failed[6])  # ff = proportion of reads failed to determine

        words_explainedsens = lines[4].split(" ")
        words_explainedantisens = lines[5].split(" ")
        fes = float(words_explainedsens[6])  # fes = proportion of reads explained by ++,--
        fea = float(words_explainedantisens[6])  # fea = proportion of reads explained by +-, -+
        ft = fes + fea

        # calculate percentage of reads taking for account only fes and fea
        # if % > 65% then the archive is stranded +
        # if % < 35% then the archive is stranded -
        # if 35 <= % <= 65 then the archive is unstranded

        if fes / ft > 0.65:
            controle = "+"
        elif fes / ft < 0.35:
            controle = "-"
        else:
            controle = 'unstranded'

        with open(path + "/sens_archive.txt", "w") as result:
            result.write("Sens archive:\t" + controle + "\tReads percentage ++ in archive (rseqC) :\t" + str(
                round(fes / ft * 100.0, 3)) + "\tReads percentage reads +- in archive (rseqC) : \t" + str(
                round(fea / ft * 100.0, 3)))
