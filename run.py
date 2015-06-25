#!/usr/bin/env python
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

#Function to control option parsing in Python
def controller():
    global FORCE_COMMIT
    global COMMIT_STREAM
    #To-Do exception handling
    parser = argparse.ArgumentParser(description='Coverity build script')
    parser.add_argument('-s', '--stream',
                        default="Test",
                        help='specify commit stream. Default is Test')
    parser.add_argument('-f', '--force',
                        nargs='?',
                        default=False,
                        const=True,
                        type=bool,
                        help='force commit if new defect is detected')
    args = parser.parse_args()
    #print parser.parse_args('-f'.split())
    #print parser.parse_args(''.split())

def cov_temp():
    temp = '''
            echo "User: $USER"
            echo "PATH: $PATH"

            cd $HOME/cov_play

            #clean up
            make clean
            rm -rf cov_idir cov_config report_v2.json

            cov-configure --config cov_config/coverity_config.xml --gcc --template
            cov-build --config cov_config/coverity_config.xml --dir cov_idir --record-only make
            cov-build --config cov_config/coverity_config.xml --dir cov_idir --replay -j auto
            #cov-import-scm --dir cov_idir --scm git --log cov_scm_log.txt
            cov-analyze --dir cov_idir --all --aggressiveness-level high --security --concurrency -j auto
        '''
    runBash(temp)

def git_commit():
    runBash('git commit')
    print 'Now you can commit on git.'
    
def cov_commit():
    global FORCE_COMMIT
    global COMMIT_STREAM
    print "Performing commit to stream: " + COMMIT_STREAM

    base_commit = "cov-commit-defects --dir cov_idir --host 192.168.221.1 --port 8080 --stream " +\
                  COMMIT_STREAM +\
                  " --user admin --password coverity"
    preview_commit = base_commit + " --preview-report-v2 report_v2.json"

    #Coverity defect check
    if FORCE_COMMIT is True:
        print "Force commit"
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

    #runBash(base_commit)
    
    #Commit on git
    git_commit()

def main():
    controller()
    cov_temp()
    cov_commit()

if __name__ == '__main__':
    main()
