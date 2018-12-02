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
$ csv --help
 
Usage: csv [OPTIONS] FILENAME

Options:
  -o, --output PATH               Output CSV path
  -v, --version                   Print the version.
  -p, --peak                      Show the first 5 rows of the CSV.
  -a, --aggregate-on TEXT         Enter the column to aggregate on
  -t, --aggregation-type [sum|mean|median]
                                  Choose the aggregation function (defaults to
                                  sum)
  -g, --group-by TEXT             Group the aggregation on these columns.
                                  Supports multiple
  -s, --show-all                  Show all possible groupings, not only those
                                  in the data.
  --help                          Show this message and exit.

 
Example:
$ csv test/data/Loans.csv -a Amount -g Network -g Product -g Date
```

## Design considerations
- Pandas and similar modules were not allowed
- Uses the built-in Python CSV module for reading files (it felt like np.loadtxt/genfromtxt would be cheating)
- Uses numpy arrays and logical operations on vectors to speed things up.
- Uses a hashtable for looking up existing combinations efficiently unless all possible combinations are required.
- Currently only groups dates by month (this requirement was unfortunately missed due to skimming the assignment :seenoevil: )