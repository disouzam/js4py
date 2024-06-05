include ../../examples.mk

## serve: run server
serve: data/lab.db
	python server.py data/lab.db

## datasets: make all datasets
datasets: data/lab.db data/designs/.touch data/readings/.touch

data/lab.db: bin/make_db.py data/assay_data.json data/sample_data.csv data/genome_data.json
	@mkdir -p data
	python $< \
	--dbfile $@ \
	--assays data/assay_data.json \
	--samples data/sample_data.csv \
	--sites params/site_params.csv \
	--surveys params/survey_params.csv

## plates: generate plate files
plates: data/designs/.touch data/readings/.touch

data/designs/.touch data/readings/.touch: bin/make_plates.py data/assay_data.json
	@mkdir -p data/designs data/readings
	rm -f data/designs/*.csv data/readings/*.csv
	python $< \
	--assays data/assay_data.json \
	--designs data/designs \
	--params params/assay_params.json \
	--readings data/readings
	touch data/designs/.touch data/readings/.touch

## assays: generate assay files
data/assay_data.json: bin/make_assays.py params/assay_params.json data/genome_data.json data/sample_data.csv
	@mkdir -p data
	python $< \
	--genomes data/genome_data.json \
	--outfile $@ \
	--params params/assay_params.json \
	--samples data/sample_data.csv

## sample_data.csv: sampled snails from survey sites
data/sample_data.csv: bin/make_samples.py data/genome_data.json params/sample_params.json params/site_params.csv params/survey_params.csv
	@mkdir -p data
	python $< \
	--genomes data/genome_data.json \
	--outfile $@ \
	--params params/sample_params.json \
	--sites params/site_params.csv \
	--surveys params/survey_params.csv

## genome_data.json: synthesized genomes
data/genome_data.json: bin/make_genomes.py params/genome_params.json
	@mkdir -p data
	python $< \
	--outfile $@ \
	--params params/genome_params.json

clean: _clean
	@rm -rf data designs readings

settings: _settings
