#!/bin/bash

if [ "$#" -lt 1 ]; then
  echo Usage: $0 profileName [MPI]
  echo Example: $0 local01
  echo Example: $0 mpi01 MPI
  exit 1
fi

PROFILE=$1

if [ -d "/home/$USER/.ipython/profile_$PROFILE" ]; then
  echo Error: Profile \"$PROFILE\" already exists
  exit 1
fi

echo Creating profile \"$PROFILE\"...

module purge
module add python
module add zeromq

ipython profile create --parallel --profile=$PROFILE
cd ~/.ipython/profile_$PROFILE/

sed -i "s/# c.HubFactory.ip = '127.0.0.1'/c.HubFactory.ip = '*'/" ipcontroller_config.py
grep c.HubFactory.ip ipcontroller_config.py

if [ "$2" = "MPI" ]; then
  IPVARIABLE="c.IPClusterEngines.engine_launcher_class"
  IPVALUE="EngineSetLauncher"
  sed -i "s/# $IPVARIABLE = 'Local$IPVALUE'/$IPVARIABLE = 'MPI$IPVALUE'/" ipcluster_config.py
  grep $IPVARIABLE ipcluster_config.py
fi
