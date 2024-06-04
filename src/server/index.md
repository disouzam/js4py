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

-   `site_params.csv`: locations of sample sites
-   `survey_params.csv`: dates and sites of field surveys
-   `genome_data.json`: synthetic genomes
-   `sample_data.csv`: genomes found in surveys
    -   `staff`: lab staff
    -   `experiments`: which experiments have been done
    -   `performed`: who did which experiments
    -   `plates`: which plates were used in which experiments
    -   `invalidated`: which plates have been invalidated
-   `assay_data.json`: genomic assays
-   `designs/*.csv`: plate designs
-   `readings/*.csv`: plate readings
-   `lab.db`: SQLite database of the above
