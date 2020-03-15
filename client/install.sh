#!/bin/bash

INSTALL_FILE="/usr/local/bin/ldeploy"
INSTALL_FOLDER="/usr/local/bin/"
TAR_FOLDER="$HOME/local-deployer-tarfolder"

pip install -r requirements.txt
sudo mkdir "$TAR_FOLDER"
sudo chmod u+x deploy.py
sudo cp deploy.py "$INSTALL_FILE"
exit 0