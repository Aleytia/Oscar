import os
import sys
import pprint as pp

from argparse import ArgumentParser

from src import loader
from src import ripper
from src import saver

def parse_args():
    parser = ArgumentParser(description=__doc__)

    parser.add_argument('-c', help="YAML file containing configuration file",
                        type=str, metavar=('file'),
                        nargs=1, dest="c")
    parser.add_argument('-x', help="YAML file containing history",
                        type=str,metavar=('file'),
                        nargs=1, dest="x")

    return parser.parse_args()

def main():
	args = parse_args()

    # Load config and history
	config = loader.load_config(args.c[0]) if args.c else loader.load_config("config.yml")
	history = loader.load_history(args.x[0]) if args.x else loader.load_history("history.yml")

	dir_path = os.path.dirname(os.path.realpath(__file__)) + '/'
	new_history = ripper.rip(config, history, dir_path)

	hsyml = args.x[0] if args.x else "history.yml"
	saver.update(new_history, hsyml)

if __name__ == "__main__":
    main()
