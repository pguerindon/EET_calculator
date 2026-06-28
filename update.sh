#!/bin/bash

cd /opt/eet_calculator || exit 1

source venv/bin/activate

pip install -r requirements.txt

deactivate

sudo systemctl restart eet

echo
echo "===== Etat du service ====="
sudo systemctl is-active eet

echo
echo "===== Statut du service ====="
sudo systemctl status eet --no-pager
