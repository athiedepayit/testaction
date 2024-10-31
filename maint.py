#!/usr/bin/env python3
import os
import sys
import argparse

os.system("pwd")
os.system("ls")

FILE_PATH="stuff/workers.tf"
MAINT_MODE=True

parser = argparse.ArgumentParser()
#-db DATABASE -u USERNAME -p PASSWORD -size 20
parser.add_argument("-e", "--environment", help="Environment to set maintenance mode. '.<domain>/*' will be appended.")
parser.add_argument("-m", "--maintenance", action='store_true', help="this argument adds maintenance mode. Run without to disable.")
parser.add_argument("-d", "--domain", help="Domain, s3licensing.net, s3licensing.com, etc.")
args = parser.parse_args()

def check_if_maint():
    f=open(FILE_PATH, "r")
    lines=f.readlines()
    f.close()
    line_pre="    \""
    line_post=f".{args.domain}/*\",\n"
    my_line=line_pre+args.environment+line_post
    if lines.count(my_line)>0:
        print("maintenance is on")
        return True
    else:
        print("maintenance is off")
        return False

def set_maint_mode(on_off):
    f=open(FILE_PATH, "r")
    lines=f.readlines()
    f.close()
    f=open(FILE_PATH, "w")
    if on_off:
        patterns_index=lines.index("  patterns = [\n")
        site_add=f"    \"{args.environment}.{args.domain}/*\",\n"
        lines.insert(patterns_index+1,site_add)
        newtext=''.join(lines)
        print(newtext)
        f.write(newtext)
    else:
        line_pre="    \""
        line_post=f".{args.domain}/*\",\n"
        my_line=line_pre+args.environment+line_post
        lines.remove(my_line)
        newtext=''.join(lines)
        print(newtext)
        f.write(newtext)

    f.close()

def __main__():

    if args.environment==None:
        print("provide an environment name.")
        sys.exit()
    if args.domain==None:
        print("provide a domain name.")
        sys.exit()

    print(f"env: {args.environment}, maint: {args.maintenance}, path: {FILE_PATH}")

    if args.maintenance:
        print(f"put {args.environment} into maintenance")
        in_maint=check_if_maint()
        if in_maint is False:
            set_maint_mode(True)
    else:
        print(f"remove {args.environment} from maintenance")
        in_maint=check_if_maint()
        if in_maint:
            set_maint_mode(False)

if __name__ == "__main__":
    __main__()
