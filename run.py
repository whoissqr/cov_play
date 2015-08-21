#!/usr/bin/env python

# This script enables developer to perform incremental build analysis or clean build analysis.

import subprocess
import argparse
import re

FORCE_COMMIT = False
COMMIT_STREAM = "Demo"

#This function takes Bash commands and returns them
def runBash(cmd):
    p = subprocess.Popen(cmd, shell=True, stdout=subprocess.PIPE)
    p.wait()
    print p.stdout.read().strip()

def returnBash(cmd):
    p = subprocess.Popen(cmd, shell=True, stdout=subprocess.PIPE)
    p.wait()
    return p.stdout.read().strip()

#Function to control option parsing in Python
def controller():
    global FORCE_COMMIT
    global COMMIT_STREAM
    #To-Do exception handling
    parser = argparse.ArgumentParser(description='Coverity build script')
    parser.add_argument("action", help='cbuild(clean build) or ibuild (incremental build) or commit (Preview and commit change on git)')
    parser.add_argument("-s", "--stream", help='Stream name. Default is Demo')
    parser.add_argument("-f", "--force", help='Force commit to Coverity', action="store_true")
    args = parser.parse_args()

    if args.stream:
        if streamExists(args.stream):
            COMMIT_STREAM = args.stream
        else:
            print('Error: Stream '+args.stream+' doesn\'t exist')
            return
    print("Working on stream: " + COMMIT_STREAM + "...")

    if args.force:
        FORCE_COMMIT = True
        print("Will commit code change to Coverity ...")

    if args.action == 'cbuild':
        clean_build()
    elif args.action == 'ibuild':
        inc_build()
    elif args.action == 'commit':
        cov_commit()
    else:
        print("Action is invalid. -h for help.")

# Check if a target stream exists on CC
def streamExists(stream):
    build = "cov-manage-im --host 192.168.221.1 --user admin --password coverity --mode streams --show --name " + stream + " | wc -l"
    return returnBash(build).find('2') != -1

# clean build: clean up everything and start a full build and analyze
def clean_build():
    build = '''
            cd $HOME/cov_play

            #clean up
            make clean
            rm -rf cov_idir cov_config report_v2.json

            cov-configure --config cov_config/coverity_config.xml --gcc --template
            cov-build --config cov_config/coverity_config.xml --dir cov_idir --record-only make
            cov-build --config cov_config/coverity_config.xml --dir cov_idir --replay -j auto
            cov-import-scm --dir cov_idir --scm git --log cov_scm_log.txt
            cov-analyze --dir cov_idir --all --aggressiveness-level high --security --concurrency -j auto
        '''
    runBash(build)

# Incremental build:
# - work only if previous cov_idir exists
# - build only the modified files
# - Coverity emits for the modified files only
# - Based on version control, analyze is only done for modified files
# - ONLY for fast speed!!!
# To-Do: --restrict-modified-file-regex is hard-coded
def inc_build():
    build = '''
            cd $HOME/cov_play
            rm -rf report_desktop.json
            if [ -d "cov_idir" ]; then
                cov-build --config cov_config/coverity_config.xml --dir cov_idir --record-only make
                cov-build --config cov_config/coverity_config.xml --dir cov_idir --replay -j auto
                cov-run-desktop --analyze-scm-modified --dir cov_idir --host 192.168.221.1 --stream Demo --user admin --password coverity --scm git --restrict-modified-file-regex "Demo.cpp" --json-output-v3 report_desktop.json
                echo "Read detail of defects in report_desktop.json"
            else
                echo "Error: No incremental build as cov_idir is not found. Run clean build first."
            fi
        '''
    runBash(build)

def git_commit():
    runBash('git commit')

# perform preview commit and git commit
def cov_commit():
    global FORCE_COMMIT
    global COMMIT_STREAM
    print "Performing commit to stream: " + COMMIT_STREAM

    base_commit = "cov-commit-defects --dir cov_idir --host 192.168.221.1 --port 8080 --stream " +\
                  COMMIT_STREAM +\
                  " --user admin --password coverity"
    preview_commit = base_commit + " --preview-report-v2 report_v2.json"

    # Coverity defect check
    # By checking presentInComparisonSnapshot in preview report, we can see if any defect is newly introduced
    # If yes, developer should first check the report, then decide whether to commit - use force commit when necessary
    # If no, git commit is directly followed
    if FORCE_COMMIT is True:
        print "Force commit"
        # I think a commit to CC for a single pull request from developer is not ideal
        # A nightly build is responsible for analyzing all the pull requests and commit to CC
        # But I preserve the option here
        runBash(base_commit)
    else:
        print "preview commit"
        runBash(preview_commit)
        if (subprocess.call(['grep', '-q', '"presentInComparisonSnapshot" : false,', 'report_v2.json']) == 0):
            print '''
                New defect is found from your commit.
                Find details in report_v2.json or use run.sh -f to force commit.
                '''
            return
        else:
            print "No new defect is introduced"

    #Commit on git
    git_commit()

if __name__ == '__main__':
    controller()
