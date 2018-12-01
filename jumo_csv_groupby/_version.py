import os

# read version number out of version.properties
ver_file = os.path.join(os.path.dirname(os.path.realpath(__file__)), 'version.properties')
with open(ver_file) as f:
    config = dict(line.strip().split('=') for line in f if line and not line.strip().startswith('#'))

# set __version__ variable
__version__ = config['version']