#!/usr/bin/env python3
import os
import sys
import time
import argparse

FILE_PATH="tf/cloudflare_infra/workers.tf"

SITE_MAP={
        "none": [],
        "multitenant": [
            "pay-vehicleapi.s3licensing.com",
            "pay-fulfillmentapi.s3licensing.com"
            ],
        "ar": [
            "ar-controlcenter.s3licensing.com",
            "ar-licensing.s3licensing.com",
            "ar-events.s3licensing.com",
            "ar-agentlicensing.s3licensing.com",
            "ar-webapi.s3licensing.com",
            "ar-scheduledjobs.s3licensing.com"
            ],
        "ebci": [
            "ebci-controlcenter.s3licensing.com",
            "ebci-licensing.s3licensing.com",
            "ebci-events.s3licensing.com",
            "ebci-agentlicensing.s3licensing.com",
            "ebci-webapi.s3licensing.com",
            "ebci-scheduledjobs.s3licensing.com"
            ],
        "la": [
            "la-controlcenter.s3licensing.com",
            "la-agentlicensing.s3licensing.com",
            "la-vehicles.s3licensing.com",
            "la-scheduledjobs.s3licensing.com"
            ],
        "mn": [
            "mn-controlcenter.s3licensing.com",
            "mn-licensing.s3licensing.com",
            "mn-events.s3licensing.com",
            "mn-agentlicensing.s3licensing.com",
            "mn-vehicles.s3licensing.com",
            "mn-webapi.s3licensing.com",
            "mn-scheduledjobs.s3licensing.com"
            ],
        "mo": [
            "mo-controlcenter.s3licensing.com",
            "mo-licensing.s3licensing.com",
            "mo-events.s3licensing.com",
            "mo-agentlicensing.s3licensing.com",
            "mo-webapi.s3licensing.com",
            "mo-scheduledjobs.s3licensing.com"
            ],
        "oh":[
            "oh-controlcenter.s3licensing.com",
            "oh-licensing.s3licensing.com",
            "oh-events.s3licensing.com",
            "oh-agentlicensing.s3licensing.com",
            "oh-scheduledjobs.s3licensing.com"
            ],
        "or":[
                "or-controlcenter.s3licensing.com",
                "or-events.s3licensing.com",
                "or-webapi.s3licensing.com",
                "or-scheduledjobs.s3licensing.com"
                ],
        "maintenance" : [
                "ar-maintenance.azurewebsites.net",
                "ebc-maintenance.azurewebsites.net",
                "mi-maintenance.azurewebsites.net",
                "or-maintenance.azurewebsites.net"
                ]
}

PR_TEMPLATE = """\
#### Description

This disables the Cloudflare proxy for all production (mobilgov.com and payitgov.com) domains.
When troubleshooting is complete, this PR should be reverted by clicking the "Revert" button in the closed pull request.

#### Compliance Checklist
- [X] I have verified that this is not a new project. If it is a new project (new service, new application, new repository), I have contacted the InfoSec team and completed their processes to gain proper approval from the following InfoSec team members:

- [X] I have verified that the backout plan for this change conforms to our standard engineering backout plan located [here](https://payitdev.atlassian.net/wiki/spaces/SEC/pages/2833416205/Standard+Change+Control+Back+Out+Plan). If it does not, I have documented an alternative backout plan below:

- [X] I have verified that this change is backwards compatible. If it is not, I have specified the breaking changes and how they will be handled below:

- [X] I have verified that this change will not impact the security controls built into the application or introduce any new security vulnerabilities. If it will, I have defined the security impact below:

- [X] I have verified that this change will not result in downtime. If it will, I have noted the impact below:

- [X] I have verified that no new dependencies were introduced. If they were, I have vetted them below:

- [X] I have verified that all applicable tests were updated to ensure complete test coverage of any new or modified code.

- [X] I have verified that any relevant documentation such as the README is still up to date and not impacted by my changes. If documentation needs updating for accuracy, I have done so. """


parser = argparse.ArgumentParser()
#-db DATABASE -u USERNAME -p PASSWORD -size 20
parser.add_argument("-e", "--environment", help="Environment to set maintenance mode. '.<domain>/*' will be appended.")
parser.add_argument("-m", "--maintenance", help="Maintenance, true or false")
parser.add_argument("-c", "--commit", action='store_true', help="Commit?")
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

# yes this shells out to git a bunch, but it's a decent way to avoid dependencies
def commit(mm_site, on_off):
    my_time=time.strftime('%Y%m%d%H%M%S')
    branch=f"{my_time}_{mm_site}_{on_off}"
    print(f"branch: {branch}")
    os.system("git config user.name 'github-actions' && git config user.email 'actions@github.com'")
    g_status=os.system("git status | grep -i 'working tree clean'")
    if g_status==0:
        print(f"git tree clean: {g_status}")
        pass
    else:
        print("committing.")
        os.system(f"git checkout -b {branch}")
        os.system(f"git add . && git commit -m 'maintenance {on_off} for {mm_site}' && git push origin {branch}")
        os.system(f"gh pr create --base master --head {branch} --title 'maintenance {on_off} for {mm_site}' --body '{PR_TEMPLATE}'")


# false/true are strings from github actions, converting/parsing here
def str2bool(v):
  return v.lower() in ("yes", "true", "t", "1")

def maint_choice(mm_site, maint):
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

    if args.commit:
        commit(mm_site, maint)


def __main__():

    if args.environment==None:
        print("provide an environment name.")
        sys.exit()

    mm_site=args.environment
    maint=str2bool(args.maintenance)
    print(f"site: {mm_site}, maint: {maint}, path: {FILE_PATH}, commit: {args.commit}")

    if mm_site in SITE_MAP:
        print(f"Looping through {SITE_MAP[mm_site]}")
        for loop_site in SITE_MAP[mm_site]:
            maint_choice(loop_site, maint)
    else:
            maint_choice(mm_site, maint)

    if args.commit:
        commit(mm_site, maint)

if __name__ == "__main__":
    __main__()
