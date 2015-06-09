cores="$(nproc)"

echo "

User: $USER 
PATH: $PATH
Cores: $cores
"

cd /home/yuan/coverity

#clean up
make clean
rm -rf cov_idir cov_config

# Coverity commands
cov-configure --config cov_config/coverity_config.xml --gcc --template
cov-build --config cov_config/coverity_config.xml --dir cov_idir --record-only make
cov-build --config cov_config/coverity_config.xml --dir cov_idir --replay -j $cores
cov-import-scm --dir cov_idir --scm git --log cov_scm_log.txt
cov-analyze --dir cov_idir --all --aggressiveness-level high --security --concurrency -j $cores
cov-commit-defects --dir cov_idir --host 192.168.221.1 --port 8080 --stream Test --user admin --password coverity 


