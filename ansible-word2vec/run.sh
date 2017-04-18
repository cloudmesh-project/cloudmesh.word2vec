#!/bin/bash

echo "upgrading spark ..."
ansible-playbook install_upgrade_spark.yaml
echo "upgrading spark ... done"
echo "setting up environment, copying files installing dependencies ..."
ansible-playbook word2vec_setup.yaml
echo "setting up environment, copying files installing dependencies ... done"
echo "running word2vec ..."
ansible-playbook word2vec_execute.yaml
echo "running word2vec ... done"

