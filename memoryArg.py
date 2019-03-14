import argparse
parser = argparse.ArgumentParser(description="Plugin shows the memory state in terms of memory percentage")
parser.add_argument('-s', '--size', nargs=1, required=False, help='disk size in percentage', dest='disk_size', type=str, default=['85%'])
parser.add_argument("memoryOK" ,help="range of memory OK", type=int)
parser.add_argument("warning" ,help="range of memory warning", type=int)
parser.add_argument("critical" ,help="range of memory warning", type=int)
args = parser.parse_args()

print(args.memoryOK)
print(args.warning)
print(args.critical)
