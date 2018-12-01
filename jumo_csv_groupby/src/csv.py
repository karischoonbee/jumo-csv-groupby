import numpy as np
import csv
from collections import OrderedDict
from itertools import product
from tabulate import tabulate


class Frame:

    def __init__(self):

        # TODO: Initialise Frame from np.array or dictionary
        # TODO: Implement slicing
        # TODO: Add dtypes to columns

        self.columns = OrderedDict()
        self.__len = 0

    def __str__(self):
        if self.__len < 2:
            ret = tabulate([self.columns.values()], headers=self.get_column_names())
        else:
            ret = tabulate([row for row in zip(*[arr for arr in self.columns.values()])][:min(self.__len, 5)],
                           headers=self.get_column_names())
            if self.__len > 5:
                ret += '\n...'
        return ret

    def get_column_names(self):
        return self.columns.keys()

    def aggregate_on(self, column, group_by=None, agg=np.sum):
        """

        :param column: Column name on which to aggregate
        :param group_by: (default: None) List of column names on which to group
        :param agg: (default: np.sum) Aggregation function to apply]
        :return:
        """
        if column not in self.columns.keys():
            raise ValueError("No column named '{}' found in table.".format(column))

        res_frame = Frame()

        if group_by is not None:
            grouper = self.group_by(group_by)
            for grouping_col in grouper.grouping_columns:
                res_frame.columns[grouping_col] = list()
            res_frame.columns[column] = list()

            for grouping_columns, (group, indices) in grouper.get_groups():
                for grouping_col, value in zip(grouping_columns, group):
                    res_frame.columns[grouping_col].append(value)
                res_frame.columns[column].append(agg(self.columns[column][indices]))
                res_frame.__len += 1
        else:
            res_frame.columns['index'] = column
            res_frame.columns[agg.__name__] = agg(self.columns[column])
            res_frame.__len += 1

        return res_frame

    def group_by(self, columns):
        """
        :param columns: A column name or list of column names to group the data on
        :return:
        """
        return GroupBy(self, columns)

    def from_csv(self, filepath, column_names=None):
        """
        :param filepath: Path to the CSV file to read
        :param column_names: (default: None) None reads the column names from the first row of the file,
                             otherwise specify the column headers.
        :return:
        """
        self.__init__()

        with open(filepath, 'r') as csvfile:
            dialect = csv.Sniffer().sniff(csvfile.read(1024))
            csvfile.seek(0)

            if column_names is None:
                reader = csv.DictReader(csvfile, dialect=dialect, fieldnames=None)
            else:
                reader = csv.DictReader(csvfile, dialect=dialect, fieldnames=column_names.split(','))
                print(reader.fieldnames)

            # create the columns
            for column_name in reader.fieldnames:
                self.columns[column_name] = list()

            # read the data row by row from the file
            for ind, row in enumerate(reader):
                self.__len += 1

                for column_name in reader.fieldnames:
                    try:
                        val = np.float64(row[column_name])
                    except ValueError:
                        val = row[column_name]

                    self.columns[column_name].append(val)

        # convert the columns to numpy arrays
        for name in self.get_column_names():
            self.columns[name] = np.asarray(self.columns[name])
        return self

class GroupBy:

    def __init__(self, frame, columns):

        if isinstance(frame, Frame):
            self.f = frame
        else:
            raise(TypeError("Frame is not a valid Frame object"))

        self.__unique_values = OrderedDict()
        if isinstance(columns, str):
            self.grouping_columns = [columns]
        elif all(isinstance(item, str) for item in columns):
            self.grouping_columns = columns
        else:
            raise TypeError("'Columns' should be a column name or a list of column names")

        for col in self.grouping_columns:
            self.__unique_values[col] = self.__get_unique_vals(col)

        self.groups = dict()

        for combo in product(*[self.__unique_values[col] for col in self.__unique_values.keys()]):
            indices = np.all(np.column_stack([(self.f.columns[key] == value) for key, value in
                                                         zip(self.__unique_values.keys(), combo)]), axis=1)
            if np.any(indices):
                self.groups[combo] = indices

    def __get_unique_vals(self, col):
        if col in self.f.columns.keys():
            unique_vals = np.unique(self.f.columns[col])
        else:
            raise ValueError("No column named '{}' found in table.".format(col))
        return unique_vals

    def get_groups(self):
        for group in self.groups.items():
            yield self.grouping_columns, group


if __name__ == '__main__':
    f = Frame()
    f.from_csv('../Loans.csv')
    print(f)
    print(f.aggregate_on('Amount', group_by=['Network', 'Product'], agg=np.sum))
    print(f.aggregate_on('Amount', agg=np.sum))
