#!/usr/bin/env python

import argparse
import logging
import os, sys

# NAGIOS return codes :
# https://nagios-plugins.org/doc/guidelines.html#AEN78
OK       = 0
WARNING  = 1
CRITICAL = 2
UNKNOWN  = 3

mylogger = logging.getLogger(__name__)
cmd_df = "df -h / | grep -v Filesystem | tail -1 | awk '{print $5}'"

def debug_factory(logger, debug_level):
   """
   Decorate logger in order to add custom levels for Nagios
   """
   def custom_debug(msg, *args, **kwargs):
       if logger.level >= debug_level:
           return
       logger._log(debug_level, msg, args, kwargs)
   return custom_debug


def get_args():
   """
   Supports the command-line arguments listed below.
   """
   parser = argparse.ArgumentParser(description="Disk Check")
   parser._optionals.title = "Options"
   parser.add_argument('-s', '--size', nargs=1, required=False, help='disk size in percentage', dest='disk_size', type=str, default=['85%'])
   parser.add_argument('-v', '--verbose', required=False, help='enable verbose output', dest='verbose', action='store_true')
   parser.add_argument('--log-file', nargs=1, required=False, help='file to log to (default = stdout)', dest='logfile', type=str)
   parser.add_argument('--nagios', required=False, help='enable Nagios output mode', dest='nagios_output', action='store_true')
   args = parser.parse_args()
   return args


def main():
   """
   CMD Line tool
   """

   # Handling arguments
   args            = get_args()
   disk_size       = args.disk_size[0]
   verbose         = args.verbose
   nagios_output   = args.nagios_output

   log_file = None
   if args.logfile:
       log_file = args.logfile[0]

   # Logging settings
   if verbose:
       log_level = logging.DEBUG
   else:
       log_level = logging.INFO

   if nagios_output:
       # Add custom level unknown
       logging.addLevelName(logging.DEBUG+1, 'UNKOWN')
       setattr(mylogger, 'unkown', debug_factory(mylogger, logging.DEBUG+1))

       # Change INFO LevelName to OK
       logging.addLevelName(logging.INFO, 'OK')

       # Setting output format for Nagios
       logging.basicConfig(filename=log_file,format='%(levelname)s - %(message)s',level=logging.INFO)
   else:
       logging.basicConfig(filename=log_file,format='%(asctime)s %(levelname)s %(message)s',level=log_level)


   #####################################
   # Disk usage example check          #
   #####################################

   mylogger.debug("Running os command line : %s" % cmd_df)
   used_space=os.popen(cmd_df).readline().strip()

   if used_space < disk_size:
       mylogger.info("%s" % used_space)
       sys.exit(OK)
   elif used_space == disk_size:
       mylogger.warning("%s" % used_space)
       sys.exit(WARNING)
   elif used_space > disk_size:
       mylogger.critical("%s" % used_space)
       sys.exit(CRITICAL)
   else:
       mylogger.unkown("%s" % used_space) if nagios_output else mylogger.info("%s" % used_space)
       sys.exit(UNKNOWN)

if __name__ == "__main__":
    main()
