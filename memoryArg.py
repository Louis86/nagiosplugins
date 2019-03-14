import argparse
parser = argparse.ArgumentParser(description="Plugin shows the memory state in terms of memory percentage")
parser.add_argument('-s', '--size', nargs=1, required=False, help='disk size in percentage', dest='disk_size', type=str, default=['85%'])
parser.add_argument('-Ok',dest="memoryOKmax" ,help="Maximum of memory OK", type=int)
parser.add_argument('-wMin',dest="warningMin" ,help="rMinimum of memory warning", type=int)
parser.add_argument('-wMaw',dest="warningMax" ,help="Maximum of memory : state warning", type=int)
parser.add_argument('-cMin',dest="criticalMin" ,help="Minimum of memory :  stage critical", type=int)
args = parser.parse_args()

print(args.memoryOKmax)
print(args.warningMin)
print(args.warningMax)
print(args.criticalMin)
