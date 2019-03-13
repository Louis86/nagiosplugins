import argparse

parser = argparse.ArgumentParser(description='Plugin shows the memory state in terms of memory percentage')
parser.add_argument('memoryOK' ,type= int help='range of memory OK')
parser.add_argument('integers', metavar='N', type=int, nargs='+',
                    help='an integer for the accumulator')
parser.add_argument('--sum', dest='accumulate', action='store_const',
                    const=sum, default=max,
                    help='sum the integers (default: find the max)')

args = parser.parse_args()
print(args.accumulate(args.integers))
