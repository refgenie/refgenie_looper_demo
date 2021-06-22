# Simple pipeline that takes some arguments and prints them
# Demonstrates how to use refgenie to pass assets to an arbitrary pipeline.

import sys
from argparse import ArgumentParser
__version__ = "0.0.1"

def parse_arguments():
    """
    Parse command-line arguments passed to the pipeline.
    """
    # Argument Parsing from yaml file
    ###########################################################################
    parser = ArgumentParser(description='PEPATAC version ' + __version__)

    # Pipeline-specific arguments
    parser.add_argument("--fasta-file", dest="fasta_file",
                        help="Path to fasta file")
  
    parser.add_argument("--sample-name", dest="sample_name",
                        help="Sample name")	

    parser.add_argument("--index", default=None,
                        dest="index_file", type=str,
                        help="Path to genome index.")

    parser.add_argument("--anno-name", default=None,
                        dest="anno_name", type=str,
                        help="Path to reference annotation file (BED format) for calculating FRiF")

    parser.add_argument("--custom-config", default=None,
                        dest="custom_config", type=str,
                        help="Path to custom configuration file")



    args = parser.parse_args()
    return args


def main():
    """
    Main pipeline process.
    """

    args = parse_arguments()

    # print out the values you passed:

    print(f'Sample name: {args.sample_name}')
    print(f'Fasta file: {args.fasta_file}')
    print(f'Index file: {args.index_file}')
    print(f'Annotation file: {args.anno_name}')
    print(f'Custom config file: {args.custom_config}')

if __name__ == '__main__':
    pm = None
    # TODO: remove once ngstk become less instance-y, more function-y.
    ngstk = None
    try:
        sys.exit(main())
    except KeyboardInterrupt:
        sys.exit("Pipeline aborted")
