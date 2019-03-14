import argparse
parser = argparse.ArgumentParser(description="Plugin shows the memory state in terms of memory percentage")
parser.add_argument('-s', '--size', nargs=1, required=False, help='disk size in percentage', dest='disk_size', type=str, default=['85%'])
parser.add_argument("memoryOKmax" ,help="range of memory OK", type=int)
parser.add_argument("warningMin" ,help="range of memory warning", type=int)
parser.add_argument("warningMax" ,help="range of memory warning Maximum", type=int)
parser.add_argument("criticalMin" ,help="range of memory critical Minimum", type=int)
args = parser.parse_args()

print(args.memoryOK)
print(args.warning)
print(args.critical)
