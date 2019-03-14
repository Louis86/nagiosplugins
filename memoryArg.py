import argparse
parser = argparse.ArgumentParser(description="Plugin shows the memory state in terms of memory percentage")
parser.add_argument('-Ok',dest="memoryOKmax" ,help="percentage Maximum of memory OK", type=int ,required=True )
parser.add_argument('-wMin',dest="warningMin" ,help="percentage Minimum of memory warning", type=int ,required=True)
parser.add_argument('-wMax',dest="warningMax" ,help="percentage Maximum of memory : state warning", type=int ,required=True)
parser.add_argument('-cMin',dest="criticalMin" ,help="percentage Minimum of memory :  stage critical", type=int ,required=True)
args = parser.parse_args()

print(args.memoryOKmax)
print(args.warningMin)
print(args.warningMax)
print(args.criticalMin)
