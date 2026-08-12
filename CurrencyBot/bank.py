from json_storage import save_operation, read_operations


class Bank:

    def __init__(self) -> None:
        self.operations = None

    def add_operation(self, operation):
        self.operations = operation
        save_operation(self.operations)

    def show_operations(self):
        data_json = read_operations()
        operations = []

        for data in data_json[-5:]:
            operations.append(
                (
                    data["currency_from"],
                    data["balance_from"],
                    round(data["balance_to"], 2),
                    data["currency_to"],
                )
            )

        return operations
