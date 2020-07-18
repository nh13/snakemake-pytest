[![Language][language-badge]][language-link]
[![Actions Status][action-status-badge]][action-status-link]
[![Code Style][code-style-badge]][code-style-link]
[![Type Checked][type-checking-badge]][type-checking-link]
[![PEP8][pep-8-badge]][pep-8-link]
[![License][license-badge]][license-link]

---

# Snakemake with Pytest example

This demonstrates how to test your [Snakefile][snakemake-link] with [pytest][pytest-link].
Snakemake will be run in `--dryrun` mode to verify that the inputs in the `all` rule can be generated.
It will also make sure there are no syntax errors and run linting (`--lint`).
This is done all programatically (no "shelling out")

## Caveats

This does not support the [checkpoint][snakemake-checkpoint] directive.

This does not support testing on real data and having the rules _actually_ run.
This is something **you should** do.
Set the `dryrun` parameter to `False` in the call to `snakemake.snakemake`.
Make sure that your input files "make sense" given the workflow you are running.
Also make sure any required software is installed or accessible.
For example, a small set of reads in a FASTQ as input over a single exon to test variant calling.
And then make sure `bwa`, `samtools`, and `gatk4` are installed.

## Installation

- [Install conda][conda-link]

- Create the `snakemake-pytest` conda environment

```bash
conda env create --file src/environment.yml
```

- Activate the `snakemake-pytest` conda environment

```bash
conda activate snakemake-pytest
```

- Run the integration tests

```bash
bash ci/check.sh
```

[language-badge]:       http://img.shields.io/badge/language-python-brightgreen.svg
[language-link]:        http://www.python.org/
[action-status-badge]:  https://github.com/nh13/snakemake-pytest/workflows/tests/badge.svg
[action-status-link]:   https://github.com/nh13/snakemake-pytest/actions?query=workflow%3A%22tests%22
[code-style-badge]:     https://img.shields.io/badge/code%20style-black-000000.svg
[code-style-link]:      https://black.readthedocs.io/en/stable/
[type-checking-badge]:  http://www.mypy-lang.org/static/mypy_badge.svg
[type-checking-link]:   http://mypy-lang.org/
[pep-8-badge]:          https://img.shields.io/badge/code%20style-pep8-brightgreen.svg
[pep-8-link]:           https://www.python.org/dev/peps/pep-0008/
[license-badge]:        http://img.shields.io/badge/license-MIT-blue.svg
[license-link]:         https://github.com/fulcrumgenomics/pyfgaws/blob/master/LICENSE
[snakefiles-link]:      https://snakemake.readthedocs.io/en/stable/snakefiles/rules.html
[pytest-link]:          https://docs.pytest.org/en/stable/
[snakemake-checkpoint]: https://snakemake.readthedocs.io/en/stable/snakefiles/rules.html#data-dependent-conditional-execution
[snakemake-link]:       https://snakemake.readthedocs.io/en/stable
[conda-link]:           https://docs.conda.io/projects/conda/en/latest/user-guide/install/
