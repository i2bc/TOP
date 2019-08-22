import argparse

parser = argparse.ArgumentParser()
parser.add_argument('DRs_file', help="input repeat sequences file")
args = parser.parse_args()

drs_file = args.DRs_file

headers = []
Drs = []
seq = ""

with open(drs_file, "r") as drs_f:  # Drs list take as value all sequences from Drs_file and headers list take as
    # value all headers from Drs_file
    lines = drs_f.readlines()
    for line in lines:
        if ">" in line:
            headers.append(line)
            Drs.append(seq.upper())
            seq = ""
        else:
            seq = seq + line.strip()
    Drs.append(seq.upper())

Drs.pop(0)  # delete first element from this list because it isn't a sequence
with open(drs_file, "w") as drs_f:
    for i in range(len(Drs)):
        drs_f.write(headers[i] + Drs[i] + "\n")
