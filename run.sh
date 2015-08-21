#! /bin/bash

# Demo script that can be run on centralized server for nightly build

echo "

User: $USER 
PATH: $PATH
"

STREAM="Demo"
if [ -z "$1" ]
    then
        echo "use default commit stream: Demo"
    else
        echo "Commit stream: $1"
        STREAM=$1
fi

cd $HOME/cov_play

#clean up
make clean
rm -rf cov_idir cov_config

# Coverity commands

#Step 1: Configure
#configure a standard gcc template compiler, which is stored in xml
cov-configure --config cov_config/coverity_config.xml --gcc --template

#Step 2: Build
#record native build (C/C++ only)
cov-build --config cov_config/coverity_config.xml --dir cov_idir --record-only make

#replay in multiple processes
cov-build --config cov_config/coverity_config.xml --dir cov_idir --replay -j auto

#Alternatively, you can just run:
#   cov-build --config cov_config/coverity_config.xml --dir cov_idir
#But the record/replay can save your time
#Coverity stores emit files in cov_dir folder
#See build-log.txt for detailed build log

#Step 3: import scm data
cov-import-scm --dir cov_idir --scm git --log cov_scm_log.txt

#Step 4: analyze build result
#Optimize your analysis by choosing appropriate flags
cov-analyze --dir cov_idir --all --aggressiveness-level high --security --concurrency -j auto

#Step 5: commit analyze result to Coverity Connect
if [ -e "admin_key" ]
    then
        echo "admin_key exists, continue to commit"
    else
        cov-manage-im --host 192.168.221.1 --port 8080 --user admin --password coverity --mode auth-key --create --output-file admin_key
        echo "admin_key created"
fi
cov-commit-defects --stream $STREAM --dir cov_idir --host 192.168.221.1 --auth-key-file admin_key

#For easy commit but expose password in script:
#   cov-commit-defects --dir cov_idir --host 192.168.221.1 --port 8080 --stream Test --user admin --password coverity