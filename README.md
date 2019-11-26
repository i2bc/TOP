# TOP

**Contacts**

- Christine Pourcel (<christine.pourcel@u-psud.fr>)
- Jean-Philippe Vernadet (<jean-philippe.vernadet@laposte.net>)

The TOP (Transcript Orientation Pipeline) pipeline was initially designed to determine the orientation of CRISPR sequences from transcripts from high throughput sequencing. This pipeline would improve the database [CRISPRCasdb]. However, it could be used to determine the orientation of any sequence of interest.

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
git clone https://github.com/i2bc/TOP.git
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

## Result/Output files

### Structure of the output directory

├── Output
    ├── TaxId_1
    |	├── bbduk_log
    |	|	├── SampleId_1.log
    |	|	├── SampleId_2.log
    |	|	├── SampleId_....log        
    |	├── SampleId_1
    |	|	├──	rnaspades
    |	|	├── aln.sam
    |	|	├── aln_ref.sam
    |	|	├── CRISPR_contigs.fasta
    |	|	├── direction_result.txt
    |	|	├── rseqc_results.txt
    |	|	├── sens_archive.txt
    |	|	├── SampleId_1.csv
    |	|	├── SampleId_1.fq
    |	|	├── SampleId_1.txt
    |	|	├── SampleId_1_bbduk.fq
    |	├── SampleId_2
    |	├── SampleId...
    |	├── genomic.fna
    |	├── genomic.gff
    |	├── Results.csv
    |	├── sequences_list.txt
    |
    ├── TaxId_2
    ├── TaxId...

## Description of result/output files

|  OutputFileName | Description  |
|---|---|
| ```Results.csv```  |  Contains all the results from all SampleID.csv from the TaxId directory. |
| ```SampleId.csv```  |  Contains the final results summary of a sample. Output format is a csv with the following columns: ```Tax ID	Archive's name	Repeat sequence	Number of CRISPR reads in archive	% reads CRISPR in archive	Number of reads in input sens 	% reads in input direction 	Number of reads in reverse input direction 	% reads in reverse input sens	Repeat sens in archive	p-value	% Reads ++ in archive (RseqC)	% Reads +- in archive (RseqC)	Archive direction	Repeat direction
``` |



## Description of scripts and TOP files

|  ScriptName | Description  |
|---|---|
| ```aln.sh```  |  aligns reads of interest with contigs of interest and then filters that do not match. |
|  assembly.csv | Table contains metadatas from RefSeq assemblies.  |
| board.py  |  Builds the final results table. |
| contigs.sh  |Create an empty assemly rnaspades file if rnaspades failed.   |
|  contigs_coverage.py | Filters assembly contigs by coverage rnaspades results.  |
| fai.sh  |  Index contigs of sequences of interest. |
| full_link_fna.awk  | Builds the full link to genome reference file.  |
| full_link_gff.awk  | Builds the full link to the annotation associated with reference genome.  |
|  link.py | Builds link to genome reference file.  |
| orientation.py  | Orientation results of the sequence of interest.  |
| rnaspades.sh  | Launches ```rnaspades.py``` to build contigs of sequence of interest. Creates empty file if there is an empty file in input. |
| RseqC.py  | Filters results from RseqC  |
| rseqc.sh  | Launches ```infer_experiment.py``` from RseqC to orientate archive |
| sequences_list_format.py  | Reformat sequence of interest in input (lower to uppercase ...)  |
| Snakefile  | File input used by ```snakemake```  |
| TOP.yaml  | File used by ```conda``` to build the TOP environment  |

