include ../../examples.mk

## samples.csv: sampled snails from survey sites
samples.csv: genomes.json make_samples.py
	python make_samples.py \
	--genomes genomes.json \
	--outfile $@ \
	--params sample_params.json \
	--sites sites.csv \
	--surveys surveys.csv

## genomes.json: synthesized genomes
genomes.json: make_genomes.py
	python make_genomes.py \
	--outfile $@ \
	--params genome_params.json

settings: _settings
