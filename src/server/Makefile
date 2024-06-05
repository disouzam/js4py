include ../../examples.mk

## serve: run server
serve: lab.db
	python server.py lab.db

## data: make all datasets
data: lab.db

lab.db: make_db.py designs/.touch readings/.touch assay_data.json genome_data.json sample_data.csv
	python $< \
	--dbfile $@ \
	--assays assay_data.json \
	--samples sample_data.csv \
	--sites site_params.csv \
	--surveys survey_params.csv

## plates: generate plate files
plates: designs/.touch readings/.touch

designs/.touch readings/.touch: make_plates.py assay_data.json
	mkdir -p designs readings
	rm -f designs/*.csv readings/*.csv
	python $< \
	--assays assay_data.json \
	--designs designs \
	--params assay_params.json \
	--readings readings
	touch designs/.touch readings/.touch

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
