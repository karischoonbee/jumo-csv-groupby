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

    def len(self):
        return self.__len

    def size(self):
        return (self.__len, len(self.columns.keys()))

    def __str__(self):
        if self.__len < 2:
            ret = tabulate([self.columns.values()], headers=self.get_column_names())
        elif self.__len <= 10:
            ret = tabulate([row for row in zip(*[arr for arr in self.columns.values()])],
                           headers=self.get_column_names())
        else:
            ret = tabulate([row for row in zip(*[arr for arr in self.columns.values()])][:5],
                           headers=self.get_column_names())
            ret += '\n...\n'
            ret += tabulate([row for row in zip(*[arr for arr in self.columns.values()])][-5:],
                           headers=self.get_column_names())

        return ret

    def head(self):
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

    def aggregate_on(self, column, agg=np.sum, group_by=None, all_groups=False):
        """
        :param column: Column name on which to aggregate
        :param group_by: List of column names on which to group (default: None)
        :param agg: Aggregation function to apply (default: np.sum)
        :param all_groups: Group by all possible combinations (default: False)
        :return:
        """
        if column not in self.columns:
            raise ValueError("No column named '{}' found in table.".format(column))

        if not np.issubdtype(self.columns[column].dtype, np.number):
            raise ValueError('Column not of numeric type')

        res_frame = Frame()

        if group_by is not None:
            grouper = self.group_by(group_by, all_groups)
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

    def group_by(self, columns, all_groups=False):
        """
        :param columns: A column name or list of column names to group the data on
        :param all_groups: Return all possible groupings (True), or only those in the data (False)
        :return:
        """
        return GroupBy(self, columns, all_groups=all_groups)

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

    def __init__(self, frame, columns, all_groups=False):

        if isinstance(frame, Frame):
            self.f = frame
        else:
            raise(TypeError("Frame is not a valid Frame object"))

        if isinstance(columns, str):
            self.grouping_columns = [columns]
        elif all(isinstance(item, str) for item in columns):
            self.grouping_columns = columns
        else:
            raise TypeError("'Columns' should be a column name or a list of column names")
        self.__check_columns_exist(self.grouping_columns)

        if not all_groups:
            self.__group_existing()
        else:
            self.__group_all_possible()

    def __check_columns_exist(self, columns):
        if isinstance(columns, str):
            if columns not in self.f.columns:
                raise ValueError("No column named '{}' found in table.".format(columns))
        elif isinstance(columns, list):
            for col in columns:
                if col not in self.f.columns:
                    raise ValueError("No column named '{}' found in table.".format(col))
        else:
            raise ValueError("Columns names should be a string or list of strings")

    def __get_combinations(self, columns):
        combos = dict()
        for row in range(self.f.len()):
            combo = []
            for col in columns:
                combo.append(self.f.columns[col][row])
            combos[tuple(combo)] = True
        return combos.keys()

    def __group_existing(self):
        self.groups = dict()
        for combo in self.__get_combinations(self.grouping_columns):
            indices = np.all(np.column_stack([(self.f.columns[key] == value) for key, value in
                                              zip(self.grouping_columns, combo)]), axis=1)
            self.groups[combo] = indices

    def __get_unique_vals(self, col):
        self.__check_columns_exist(col)
        unique_vals = np.unique(self.f.columns[col])
        return unique_vals

    def __group_all_possible(self):
        self.__unique_values = OrderedDict()
        for col in self.grouping_columns:
            self.__unique_values[col] = self.__get_unique_vals(col)

        self.groups = dict()
        for combo in product(*[self.__unique_values[col] for col in self.grouping_columns]):
            indices = np.all(np.column_stack([(self.f.columns[key] == value) for key, value in
                                              zip(self.grouping_columns, combo)]), axis=1)
            self.groups[combo] = indices

    def get_groups(self):
        for group in self.groups.items():
            yield self.grouping_columns, group

