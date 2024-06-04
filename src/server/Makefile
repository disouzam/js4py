include ../../examples.mk

## samples.csv: sampled snails from survey sites
samples.csv: genomes.csv synthesize_samples.py
	python synthesize_samples.py \
	--genomes genomes.csv \
	--mutant 10.0 \
	--normal 1.0 \
	--outfile $@ \
	--sites sites.csv \
	--seed 1791128 \
	--surveys surveys.csv

## genomes.csv: synthesized genomes
genomes.csv: synthesize_genomes.py
	python synthesize_genomes.py \
	--outfile $@ \
	--length 40 \
	--num_genomes 100 \
	--num_snp 5 \
	--prob_other 0.01 \
	--seed 102938

settings: _settings
