# EKS Usage Slack Notifier

This Python project retrieves usage data from an Amazon EKS cluster and sends it to a Slack channel. It allows users to specify the AWS profile, label selector, Kubernetes config file, context, and cluster name for display.

## Prerequisites

Before using this project, ensure you have the following:

- Python installed
- Access to an Amazon EKS cluster
- Slack API credentials (bot token and channel ID)

## Setup

1. Clone the repository:

```bash
git clone git@github.com:ShaiHalfon96/eks-usage-slack-notifier.git
cd eks-usage-slack-notifier
```
2. Install dependencies:
  ```bash
  pip install -r requirements.txt
  ```
3. Update the configuration file:
  Open consts.py in a text editor.
  Set SLACK.BOT_TOKEN to your Slack bot token.
  Set SLACK.CHANNEL_ID to your Slack channel ID.
  Save and close the file.

## Usage
Run the main script to retrieve EKS cluster usage data and send it to Slack. Use the following command:

```bash
python main.py -a <AWS_PROFILE_NAME> -l <LABEL_SELECTOR> -f <CONFIG_FILE> -c <CONTEXT> -n <CLUSTER_NAME> -r
```
Replace the placeholders with your specific values:

* `<AWS_PROFILE_NAME>`: Name of the AWS profile to use (optional).
* `<LABEL_SELECTOR>`: Node label selector to filter by (optional).
* `<CONFIG_FILE>`: Kubernetes config file to use (optional).
* `<CONTEXT>`: Kubernetes context to use (optional).
* `<CLUSTER_NAME>`: Kubernetes cluster name for display (optional).
* `-r` or `--run-local`: Flag to indicate running on a local EKS (optional).

For example:
```bash
python main.py -a my-aws-profile -l node-role.kubernetes.io/worker -f ~/.kube/config -c my-cluster -n MyCluster -r
```