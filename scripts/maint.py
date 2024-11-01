#!/usr/bin/env python3
import os
import sys
import argparse

FILE_PATH="tf/cloudflare_infra/workers.tf"

parser = argparse.ArgumentParser()
#-db DATABASE -u USERNAME -p PASSWORD -size 20
parser.add_argument("-e", "--environment", help="Environment to set maintenance mode. '.<domain>/*' will be appended.")
parser.add_argument("-m", "--maintenance", help="Maintenance, true or false")
args = parser.parse_args()

def check_if_maint(mm_site):
    f=open(FILE_PATH, "r")
    lines=f.readlines()
    f.close()
    line_pre="    \""
    line_post=f"/*\",\n"
    my_line=line_pre+mm_site+line_post
    if lines.count(my_line)>0:
        print("maintenance is on")
        return True
    else:
        print("maintenance is off")
        return False

def set_maint_mode(on_off, mm_site):
    f=open(FILE_PATH, "r")
    lines=f.readlines()
    f.close()
    f=open(FILE_PATH, "w")
    if on_off:
        patterns_index=lines.index("  patterns = [\n")
        site_add=f"    \"{mm_site}/*\",\n"
        lines.insert(patterns_index+1,site_add)
        newtext=''.join(lines)
        print(newtext)
        f.write(newtext)
    else:
        line_pre="    \""
        line_post=f"/*\",\n"
        my_line=line_pre+mm_site+line_post
        lines.remove(my_line)
        newtext=''.join(lines)
        print(newtext)
        f.write(newtext)

    f.close()

# false/true are strings from github actions, converting/parsing here
def str2bool(v):
  return v.lower() in ("yes", "true", "t", "1")

def __main__():

    if args.environment==None:
        print("provide an environment name.")
        sys.exit()

    mm_site=args.environment
    maint=str2bool(args.maintenance)

    print(f"site: {mm_site}, maint: {maint}, path: {FILE_PATH}")

    if maint:
        print(f"put {mm_site} into maintenance")
        in_maint=check_if_maint(mm_site)
        if in_maint is False:
            set_maint_mode(True, mm_site)
    else:
        print(f"remove {mm_site} from maintenance")
        in_maint=check_if_maint(mm_site)
        if in_maint:
            set_maint_mode(False, mm_site)

if __name__ == "__main__":
    __main__()
