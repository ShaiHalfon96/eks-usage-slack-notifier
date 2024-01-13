from typing import Any
from kubernetes import config, client
from utils import UnitConverter
from aws_integration import AWSConnection


class EKSConnection:
    """
    PreRequisites: Have kube config file.
    The following class connect to aws and create api clients to the EKS.
    """

    def __init__(self, aws_profile_name: str, config_file: str = None, context: str = None, run_local: bool = False):

        if run_local:
            config.load_incluster_config()
            return

        self.aws_client = AWSConnection(aws_profile_name=aws_profile_name, aws_service_type="eks")

        # Load Kubernetes configuration from default location
        if config_file:
            config.load_kube_config(config_file=config_file, context=context)
        else:
            config.load_kube_config()

    def get_custom_object_api(self):
        return client.CustomObjectsApi()  # Create a Kubernetes API client

    def get_api_instance(self):
        return client.CoreV1Api()  # Create a Kubernetes API client


class EKSClusterData:
    """
        PreRequisites: Have kube config file.
        Using the eks cluster as a data source, the class queries for metrics and properties in order to determine the cluster's utilization.
        You can either print or get the result as a dictionary.
        The system default configurations will be used if no class parameters are provided.
    """

    def __init__(self, aws_profile_name: str, label_selector: str = "", config_file: str = None, context: str = None,
                 run_local: bool = False):
        eks_connection = EKSConnection(aws_profile_name=aws_profile_name, config_file=config_file, context=context,
                                       run_local=run_local)
        custom_object_api = eks_connection.get_custom_object_api()
        api_instance = eks_connection.get_api_instance()

        self.k8s_nodes_metrics = custom_object_api.list_cluster_custom_object("metrics.k8s.io",
                                                                                   "v1beta1", "nodes",
                                                                                   label_selector=label_selector)
        self.k8s_nodes_properties: list = []
        nodes = api_instance.list_node(label_selector=label_selector).items  # Get the list of nodes
        for node in nodes:
            node_properties = node.status
            self.k8s_nodes_properties.append(node_properties)

    @staticmethod
    def _format_param(name: str, cpu_value: float, cpu_unit: str, memory_value: float, memory_unit: str,
                      description: str):
        return {
            'name': name,
            'cpu': {'value': round(cpu_value, 3), 'unit': cpu_unit},
            'memory': {'value': round(memory_value, 3), 'unit': memory_unit},
            'description': description
        }

    @staticmethod
    def _get_kilobytes_memory(usage: dict) -> int:
        return 0 if usage.get('memory') == '0' else int(usage.get('memory')[:-2])

    @staticmethod
    def _get_nanocores_cpu(usage: dict) -> int:
        return 0 if usage.get('cpu') == '0' else int(usage.get('cpu')[:-1])

    def get_number_of_node(self) -> int:
        return len(self.k8s_nodes_metrics['items'])

    def _sum_nodes_resources_usage(self) -> None:
        total_cpu_nanocores_usage = 0
        total_memory_kilobytes_usage = 0
        for stats in self.k8s_nodes_metrics['items']:
            usage = stats.get('usage')
            total_cpu_nanocores_usage += self._get_nanocores_cpu(usage)
            total_memory_kilobytes_usage += self._get_kilobytes_memory(usage)
        self.total_cpu_millicores_usage = UnitConverter.nanocores_to_millicores(total_cpu_nanocores_usage)
        self.total_memory_gibibytes_usage = UnitConverter.kilobytes_to_gigabytes(total_memory_kilobytes_usage)

    def _average_nodes_resources_usage(self) -> None:
        number_of_nodes = self.get_number_of_node()
        self.cpu_average_usage = self.total_cpu_millicores_usage / number_of_nodes
        self.memory_average_usage = self.total_memory_gibibytes_usage / number_of_nodes

    def _sum_nodes_resources_allocatable(self) -> None:
        total_vcpu_allocatable = 0
        total_memory_kilobytes_allocatable = 0
        for node in self.k8s_nodes_properties:
            allocatable = node.allocatable
            total_vcpu_allocatable += int(allocatable['cpu'])
            total_memory_kilobytes_allocatable += self._get_kilobytes_memory(allocatable)
        self.total_cpu_millicores_allocatable = UnitConverter.vcpu_to_millicores(total_vcpu_allocatable)
        self.total_memory_gibibytes_allocatable = UnitConverter.kilobytes_to_gigabytes(
            total_memory_kilobytes_allocatable)

    def _sum_nodes_resources_capacity(self) -> None:
        total_vcpu_capacity = 0
        total_memory_kilobytes_capacity = 0
        for node in self.k8s_nodes_properties:
            capacity = node.capacity
            total_vcpu_capacity += int(capacity['cpu'])
            total_memory_kilobytes_capacity += self._get_kilobytes_memory(capacity)
        self.total_cpu_millicores_capacity = UnitConverter.vcpu_to_millicores(total_vcpu_capacity)
        self.total_memory_gibibytes_capacity = UnitConverter.kilobytes_to_gigabytes(total_memory_kilobytes_capacity)

    def _sum_nodes_usage(self):
        total_cpu_usage = 0
        total_memory_usage = 0
        try:
            for node in self.k8s_nodes_metrics["items"]:
                total_cpu_usage += self._get_nanocores_cpu(node["usage"])
                total_memory_usage += self._get_kilobytes_memory(node["usage"])
            self.nodes_cpu_millicores_usage = UnitConverter.nanocores_to_millicores(total_cpu_usage)
            self.nodes_memory_gigabytes_usage = UnitConverter.kilobytes_to_gigabytes(total_memory_usage)
        except Exception as e:
            raise Exception

    def get_eks_data(self) -> list[Any]:
        self._sum_nodes_resources_usage()
        self._sum_nodes_resources_allocatable()
        self._sum_nodes_resources_capacity()
        self._average_nodes_resources_usage()
        self._sum_nodes_usage()
        cpu_usage_percentage = self.total_cpu_millicores_usage / self.total_cpu_millicores_capacity * 100
        memory_usage_percentage = self.total_memory_gibibytes_usage / self.total_memory_gibibytes_capacity * 100

        cpu_allocatable_percentage = self.total_cpu_millicores_allocatable / self.total_cpu_millicores_capacity * 100
        memory_allocatable_percentage = self.total_memory_gibibytes_allocatable / self.total_memory_gibibytes_capacity * 100

        nodes_cpu_usage_percentage = self.nodes_cpu_millicores_usage / self.total_cpu_millicores_allocatable * 100
        nodes_memory_usage_percentage = self.nodes_memory_gigabytes_usage / self.total_memory_gibibytes_allocatable * 100

        return [
            self._format_param("Capacity", self.total_cpu_millicores_capacity, 'm',
                               self.total_memory_gibibytes_capacity, 'gi',
                               "Computing resources available for running workloads"),
            self._format_param("Usage", self.total_cpu_millicores_usage, 'm',
                               self.total_memory_gibibytes_usage, 'gi', "Real-time resource utilization statistics"),
            self._format_param("Nodes Usage % (Out of Allocatable)", nodes_cpu_usage_percentage, '%',
                               nodes_memory_usage_percentage, '%',
                               "Nodes usage out of allocatable"),
            self._format_param("Node Usage % (Out of Capacity)", cpu_usage_percentage, '%',
                               memory_usage_percentage, '%', "Node Usage out of total capacity"),
            self._format_param("Average Node Usage", self.cpu_average_usage, 'm',
                               self.memory_average_usage, 'gi',
                               "Average usage per node"),
            self._format_param("Allocatable", self.total_cpu_millicores_allocatable, 'm',
                               self.total_memory_gibibytes_allocatable, 'gi',
                               "Total capacity that can be utilized by Pods"),
            self._format_param("Allocatable %", cpu_allocatable_percentage, '%',
                               memory_allocatable_percentage, '%', "Allocatable out of total capacity")
        ]

    def outputer(self) -> [list[str], list[Any]]:
        eks_data = self.get_eks_data()
        headers = ["Metric", "CPU", "Memory", "Description"]
        all_data = []
        for param in eks_data:
            cpu_value_and_unit = f'{param["cpu"]["value"]} {param["cpu"]["unit"]}'
            memory_value_and_unit = f'{param["memory"]["value"]} {param["memory"]["unit"]}'
            all_data.append([param["name"], cpu_value_and_unit, memory_value_and_unit, param["description"]])

        return headers, all_data
