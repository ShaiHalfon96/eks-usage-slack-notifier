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
## Output Example
Below is an example of the kind of report generated by our Python script when monitoring an Amazon EKS cluster. This report provides valuable insights into the cluster's CPU and memory usage, as well as other key metrics.

``` bash
Dev EKS Cluster Data
| Metric                             | CPU         | Memory     | Description                                         |
|:-----------------------------------|:------------|:-----------|:----------------------------------------------------|
| Capacity                           | 144000 m    | 861.45 gi  | Computing resources available for running workloads |
| Usage                              | 23131.847 m | 231.011 gi | Real-time resource utilization statistics           |
| Nodes Usage % (Out of Allocatable) | 18.359 %    | 27.789 %   | Nodes usage out of allocatable                      |
| Node Usage % (Out of Capacity)     | 16.064 %    | 26.817 %   | Node Usage out of total capacity                    |
| Average Node Usage                 | 1285.103 m  | 12.834 gi  | Average usage per node                              |
| Allocatable                        | 126000 m    | 831.295 gi | Total capacity that can be utilized by Pods         |
| Allocatable %                      | 87.5 %      | 96.5 %     | Allocatable out of total capacity                   |

Number of nodes - 18
```
In this example, you can see how the report provides a clear overview of the cluster's resource utilization, making it easy for users to interpret the data at a glance. The table format allows for quick comparison of different metrics, helping users identify any potential issues or areas for optimization.