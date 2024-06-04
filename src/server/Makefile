include ../../examples.mk

## all: make all datasets
all: assay_data.json genome_data.json sample_data.csv

## assays: generate assay files
assay_data.json: make_assays.py assay_params.json
	python $< \
	--outfile $@ \
	--params assay_params.json

## sample_data.csv: sampled snails from survey sites
sample_data.csv: make_samples.py genome_data.json sample_params.json site_params.csv survey_params.csv
	python $< \
	--genomes genome_data.json \
	--outfile $@ \
	--params sample_params.json \
	--sites site_params.csv \
	--surveys survey_params.csv

## genome_data.json: synthesized genomes
genome_data.json: make_genomes.py genome_params.json
	python $< \
	--outfile $@ \
	--params genome_params.json

settings: _settings
