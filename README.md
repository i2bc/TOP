# TOP

**Contacts**

- Christine Pourcel (<christine.pourcel@u-psud.fr>)
- Jean-Philippe Vernadet (<jean-philippe.vernadet@laposte.net>)

The TOP (Transcript Orientation Pipeline) pipeline was initially designed to determine the orientation of CRISPR sequences from transcripts from high throughput sequencing. However, it could be used to determine the orientation of any sequence of interest.

## Installation

* Conda

```bash
# Get miniconda 
wget https://repo.anaconda.com/miniconda/Miniconda3-latest-Linux-x86_64.sh;
./Miniconda3-latest-Linux-x86_64.sh
```

* TOP environment and scripts
```bash
# Clone or download files
git clone https://github.com/i2bc/b2forensics.git
```

```bash
# Create TOP_env
conda env create -f Scripts/TOP.yaml -n TOP_env
```
## How to use

* Preparation of the required sequences/archives

You must first create a results folder and an archives folder containing a folder for each taxid you want to study. For each taxid folders in results folder, you have to create fasta files named sequences_list.txt containing sequences you are looking for. For each taxid folders in archives folder, put your corresponding archives (fastq.gz files).

Load your TOP environment with conda
```bash
conda activate TOP_env
```

Launch your TOP pipeline

```bash
snakemake
```

## Results/Output


