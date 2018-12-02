# jumo-csv-groupby
Technical exercise for JUMO interviewing process

## Requirements
- Python 3
- Setuptools
- Pip

## Installation
```bash
git clone https://github.com/karischoonbee/jumo-csv-groupby.git
cd jumo-csv-groupby
python setup.py install
```
## Function
```bash
csv --help

Usage: csv [OPTIONS] FILENAME

Options:
  -v, --version                   Print the version.
  -p, --peak                      Show the first 5 rows of the CSV.
  -a, --aggregate-on TEXT         Enter the name of the column to aggregate on
  -t, --aggregation-type [sum|mean|median]
                                  Choose the aggregation function (defaults to
                                  sum)
  -g, --group-by TEXT             Group the aggregation on these columns.
  --help                          Show this message and exit.
```

## Design considerations
- Pandas and similar modules were not allowed
- Uses the built-in Python CSV module for reading files (it felt like np.loadtxt/genfromtxt would be cheating)
- Uses numpy arrays and logical operations on vectors to speed things up considerably.

