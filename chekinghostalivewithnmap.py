#! /usr/bin/env python
# -*- coding: utf8 -*-
#
import argparse
import nmap

parser = argparse.ArgumentParser(description="Process some options.")
parser.add_argument('-H', help="Hostname or IP address to check.")
args = parser.parse_args()

def main():
  nm = nmap.PortScanner()
  nm.scan(hosts=args.H, arguments='-sn')
  result = [nm[host] for host in nm.all_hosts()]

  if result == []:
    print "NMAP HOST ALIVE: CRITICAL"
    return 2
  else:
    print "NMAP HOST ALIVE: OK"
    return 0

if __name__ == "__main__":
  main();
