from prettytable import prettytable, PrettyTable
from tabulate import tabulate


def prettytable_to_tabulate(pretty_table: prettytable):
    # Convert PrettyTable to a string
    table_string = pretty_table.get_string()

    # Split the string into lines and remove the first line (column names)
    table_lines = table_string.split('\n')[1:]

    # Join the remaining lines to form a string compatible with tabulate
    tabulate_string = '\n'.join(table_lines)

    orgtbl_string = tabulate(pretty_table.get_string(), headers=[pretty_table.field_names], tablefmt="orgtbl")

    return orgtbl_string


def format_to_pretty_table(headers, data, title: str = None):
    data_table = PrettyTable()
    data_table.align = "l"
    data_table.title = title
    data_table.field_names = headers

    for row in data:
        data_table.add_row(row)

    return data_table


def format_to_tabulate_table(headers, data):
    data_table = tabulate(data, headers=headers, tablefmt="pretty", showindex=True, numalign="left",
                          stralign="left")
    return data_table


class UnitConverter:
    @staticmethod
    def kilobytes_to_gigabytes(size_in_kilobytes: int) -> float:
        return size_in_kilobytes / 1e6  # Convert kilobytes to gigabytes

    @staticmethod
    def nanocores_to_millicores(nanocores: int) -> float:
        return nanocores * 0.000001

    @staticmethod
    def vcpu_to_millicores(vcpu: int) -> int:
        millicores = int(vcpu * 1000)
        return millicores


