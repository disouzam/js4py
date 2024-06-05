---
template: slides
title: "The Server"
tagline: "Where our data comes from."
abstract: >
    FIXME
syllabus:
-   FIXME
---

[%issue 2 %]

[%fixme "describe Flask data server" %]

[%fixme "describe command-line UI" %]

---

## Data

-   Parameters
    -   `params/assay_params.json`:
    -   `params/genome_params.json`:
    -   `params/sample_params.json`:
    -   `params/site_params.csv`: locations of sample sites
    -   `params/survey_params.csv`: dates and sites of field surveys
-   Generated Data
    -   `data/assay_data.json`: genomic assays
    -   `data/genome_data.json`: synthetic genomes
    -   `data/sample_data.csv`: genomes found in surveys
    -   `data/designs/*.csv`: plate designs
    -   `data/readings/*.csv`: plate readings
    -   `data/lab.db`: SQLite database of the above
