import consts
from slack_integration import SlackIntegration
from eks_integration import EKSClusterData
import argparse


def main(aws_profile_name: str = None, label_selector: str = None, config_file: str = None, context: str = None,
         run_local: bool = False, cluster_name: str = ""):
    eks_integration = EKSClusterData(aws_profile_name=aws_profile_name, label_selector=label_selector,
                                     config_file=config_file,
                                     context=context, run_local=run_local)
    slack_table_headers, slack_table_data = eks_integration.outputer()
    number_of_node = eks_integration.get_number_of_node()
    if cluster_name:
        SlackIntegration().send_message(message=f'{cluster_name} EKS Cluster Data', channel_id=consts.SLACK.CHANNEL_ID)
    SlackIntegration().send_table_message(table_headers=slack_table_headers, table_data=slack_table_data, channel_id=consts.SLACK.CHANEL_ID, footnotes=f'Number of nodes - {number_of_node}')


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Description of your script.")

    # Define the command line arguments
    parser.add_argument('-a', '--aws-profile-name', type=str,
                        help='Name of AWS profile to use, If not mention default will be used', required=False)
    parser.add_argument('-l', '--label-selector', type=str, help='Node label selector to filter by', required=False)
    parser.add_argument('-f', '--config-file', type=str,
                        help='Kubernetes config file to use, If not mention the default will be uses', required=False)
    parser.add_argument('-c', '--context', type=str,
                        help='Kubernetes context to use.', required=False)
    parser.add_argument('-n', '--cluster-name', type=str,
                        help='Kubernetes cluster name for display.', required=False)
    parser.add_argument('-r', '--run-local',
                        help='Running on a local eks', action='store_true')

    # Parse the command line arguments
    args = parser.parse_args()

    # Call the main function with the arguments
    main(args.aws_profile_name, args.label_selector, args.config_file, args.context, args.run_local, args.cluster_name)
