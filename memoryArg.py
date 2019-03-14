import argparse
parser = argparse.ArgumentParser(description="Plugin shows the memory state in terms of memory percentage")
parser.add_argument("-ok","memoryOK" ,help="range of memory OK", type=int)
parser.add_argument("-w","warning" ,help="range of memory warning", type=int)
parser.add_argument("-c","critical" ,help="range of memory warning", type=int)
args = parser.parse_args()

print(args.memoryOK)
print(args.warning)
print(args.critical)
