from DMC.dmcclass import DMCClass

try:
	from IPython import embed
except ImportError:
	import code

import argparse
import ipaddress

parser = argparse.ArgumentParser()
 
# Adding optional argument
parser.add_argument("-ip", "--ip", help = "Show Output")
 
# Read arguments from command line
args = parser.parse_args()
 

if "__main__":
	a = DMCClass(args.ip)
	embed()





