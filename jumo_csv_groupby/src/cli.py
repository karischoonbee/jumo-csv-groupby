import click
import os
from jumo_csv_groupby.src.jumo_csv import Frame
import numpy as np


def print_version(ctx, param, value):
    if not value or ctx.resilient_parsing:
        return
    from jumo_csv_groupby._version import __version__
    click.echo('----------------------------------')
    click.echo(' Jumo CSV Groupby version: {0}'.format(__version__))
    click.echo('----------------------------------')
    ctx.exit(0)


@click.command()
@click.argument('filename',  type=click.Path(exists=True, resolve_path=True))
@click.option('-o', '--output',  type=click.Path(exists=False, resolve_path=True), help='Output CSV path')
@click.option('-v', '--version', is_flag=True, callback=print_version, expose_value=False, is_eager=True,
              help='Print the version.')
@click.option('-p','--peak', is_flag=True, expose_value=True, is_eager=True,
              help='Show the first 5 rows of the CSV.')
@click.option('-a','--aggregate-on', type=str, help='Enter the column to aggregate on')
@click.option('-t','--aggregation-type', type=click.Choice(['sum', 'mean', 'median']), default='sum',
              help='Choose the aggregation function (defaults to sum)')
@click.option('-g','--group-by', type=str, multiple=True, help='Group the aggregation on these columns. Supports multiple')
@click.option('-s','--show-all', is_flag=True, help='Show all possible groupings, not only those in the data.')
def csv(filename, output=None, version=None, peak=False, aggregate_on=None, aggregation_type='sum', group_by=None, show_all=False):

    filename = os.path.expanduser(filename)

    try:
        f = Frame().from_csv(filename)
    except IOError as e:
        click.echo(e)

    if peak:
        click.echo(f)

    if aggregation_type == 'sum':
        aggregation_type = np.sum
    elif aggregation_type == 'mean':
        aggregation_type = np.mean
    elif aggregation_type == 'median':
        aggregation_type = np.median
    group_by = list(group_by)

    try:
        if aggregate_on is not None:
            if len(group_by):
                res = f.aggregate_on(column=aggregate_on, group_by=group_by, agg=aggregation_type, all_groups=show_all)
            else:
                res = f.aggregate_on(column=aggregate_on, agg=aggregation_type)

            if output is not None:
               res.write_csv(output, f.dialect)
            else:
                click.echo(res)

    except ValueError as e:
        click.echo(e)