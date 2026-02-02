# dataset-prep

This python package provides utilities for prepping datasets for publication,
building on the [Frictionless data](https://frictionlessdata.io/) framework
and [corresponding python package](https://framework.frictionlessdata.io/).

This package is currently in alpha status and provides a script for generating field-level
information from a frictionless datapackage file for inclusion in a dataset readme (plain text)
or accompanying data dictionary (CSV). The script assumes you have already created a
[datapackage](https://datapackage.org/) to describe your dataset.

[![PyPI - Version](https://img.shields.io/pypi/v/dataset-prep)](https://pypi.org/project/dataset-prep/)
[![Apache 2 License](https://img.shields.io/badge/license-Apache%20License%202.0-blue)](#license)

## Basic Usage

Install the package from python using your preferred method (`pip` or `uv`):

```console
pip install dataset-prep
```

Run the `dataset-readme-info` script with a path to your datapackage file. The data files
referenced in the datapackage must be present at the path specified.

> [!NOTE]
> We highly recommend running `frictionless validate` on your datapackage to
> ensure your dataset and your datapackage agree on the structure of your data!

To generate a plain-text list of fields with the descriptions in the datapackage file:

```console
dataset-readme-info my-dataset/datapackage.json
```

The script will output text content to the console, which can be copied and pasted
into the readme for your dataset.

To generate a CSV data dictionary with field information (description, type, name)
for each resource described in the datapackage file, specify the path where
the file should be generated:

```console
dataset-readme-info my-dataset/datapackage.json --data-dictionary my-dataset/datadictionary.csv
```

Use the `-h` or `--help` option for script usage.

### Examples

The dataset-readme-info script is generalized from one that was used to help prepare datasets from
the [Shakespeare and Company Project](https://shakespeareandco.princeton.edu/) for publication.

The 2.0 version of the data published in 2025 includes a CSV data dictionary:

> Koeser, Rebecca Sutton & Kotin, Joshua. (2025). Shakespeare and Company Project Datasets [Data set]. Version 2. Princeton University. [https://doi.org/10.34770/kf6c-b079](https://doi.org/10.34770/kf6c-b079)

The 1.2 version of the data published in 2022 includes field details in the README:

> Kotin, Joshua, Koeser, Rebecca Sutton, et al. (2022). Shakespeare and Company Project Dataset: Lending Library Members, Books, Events [Data set]. Version 1.2. Princeton University. [https://doi.org/10.34770/dtqa-2981](https://doi.org/10.34770/dtqa-2981)

## License

This project is licensed under the [Apache 2.0 License](LICENSE).

(c)2025 Trustees of Princeton University. Permission granted for non-commercial
distribution online under a standard Open Source license.
