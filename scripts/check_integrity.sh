#!/usr/bin/env bash
#
# This bash macro allows to perform some integrity checks, similar to the
# workflows that are run at the GitHub server, but that can be run locally.
#
# Written by O. Gonzalez (2025_03_11)
#

# It should be run from the top of the package/release

if [ ! -d src ] ; then
    echo "ERROR: Run this scripts from the head of the local release"
    exit 10
fi
#
# First: We are running on a EL9 container some check given by the following
# code:
#
cat <<EOF  > tmp$$_integrity_el9.sh
echo
echo "Starting check inside container!"
stat -c %U /root
pwd
# Trying to compile the python version
python3 -V
\rm -rf src/cmsstyle/__pycache__ &> /dev/null
python3 -m py_compile src/cmsstyle/cmsstyle.py
ls -lh src/cmsstyle/__pycache__/
\rm -rf src/cmsstyle/__pycache__ &> /dev/null

# Trying to compile for ROOT
echo 'ROOT VERSION='`root-config --version`
cd src
echo '{gROOT->LoadMacro("cmsstyle.C++");}' > /tmp/compiling.C
root -q /tmp/compiling.C
ls -lh cmsstyle_C.so
\rm -rf cmsstyle_C* &> /dev/null
cd ..
echo
EOF
chmod a+x tmp$$_integrity_el9.sh

# Running in a container
apptainer exec -B /cvmfs /cvmfs/unpacked.cern.ch/registry.hub.docker.com/rootproject/root:6.32.00 ./tmp$$_integrity_el9.sh
\rm -rf tmp$$_integrity_el9.sh &> /dev/null
#
# We also try to compile in python2.7:
#
cat <<EOF  > tmp$$_integrity_cc7.sh
echo
echo "Running in a CC7 container for python 2.7"
python -V
\rm -rf src/cmsstyle/cmsstyle.pyc &> /dev/null
python -m py_compile src/cmsstyle/cmsstyle.py
ls -lh src/cmsstyle/cmsstyle.pyc
\rm -rf src/cmsstyle/cmsstyle.pyc &> /dev/null
echo
EOF
chmod a+x tmp$$_integrity_cc7.sh
# Running in a container
apptainer exec -B /cvmfs /cvmfs/unpacked.cern.ch/gitlab-registry.cern.ch/cms-cloud/cmssw-docker/cc7-cms:latest ./tmp$$_integrity_cc7.sh

\rm -rf tmp$$_integrity_cc7.sh &> /dev/null
#
