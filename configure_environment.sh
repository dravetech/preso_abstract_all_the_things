#!/bin/bash
ANSIBLE_HOST_FILE="ansible/hosts"
ST2_BOOTSTRAP_SCRIPT="vagrant/st2/st2bootstrap-deb.sh"
DEPLOY_FABRIC_WORFLOW_API="packs/chatops_demo/actions/workflows/deploy_fabric_api.yaml"
WEBHOOK_TO_SLACK="packs/chatops_demo/rules/webhook_to_slack.yaml"

echo -n "Enter the IP vmx1: "
read VMX1
echo -n "Enter the IP vmx2: "
read VMX2
echo -n "Enter the IP eos-spine1: "
read SPINE1
echo -n "Enter the IP eos-spine1: "
read SPINE2
echo -n "Enter your slack channel name: "
read SLACK_CHANNEL
echo -n "Enter your slack token: "
read SLACK_TOKEN

sed -i -r "s/vmx.core1 ansible_host=.*/vmx.core1 ansible_host=$VMX1/" $ANSIBLE_HOST_FILE
sed -i -r "s/vmx.core2 ansible_host=.*/vmx.core2 ansible_host=$VMX2/" $ANSIBLE_HOST_FILE
sed -i -r "s/eos.spine1 ansible_host=.*/eos.spine1 ansible_host=$SPINE1/" $ANSIBLE_HOST_FILE
sed -i -r "s/eos.spine2 ansible_host=.*/eos.spine2 ansible_host=$SPINE2/" $ANSIBLE_HOST_FILE

sed -i -r "s/HUBOT_SLACK_TOKEN=.*/HUBOT_SLACK_TOKEN='$SLACK_TOKEN'/" $ST2_BOOTSTRAP_SCRIPT

sed -i -r "s/source_channel: .*/source_channel: '$SLACK_CHANNEL'/" $DEPLOY_FABRIC_WORFLOW_API
sed -i -r "s/source_channel: .*/source_channel: '$SLACK_CHANNEL'/" $WEBHOOK_TO_SLACK
