class AWSConnectionFailed(Exception):
    def __init__(self, message):
        self.message = message
        super().__init__(f'Failed to connect AWS with the following error: {self.message}')


class AWSConfigFileMissingField(Exception):
    def __init__(self, message):
        self.message = message
        super().__init__(f'Failed to connect AWS due to missing field in config file. {self.message}')


class RetrievingPodMetrics(Exception):
    def __init__(self, message):
        self.message = message
        super().__init__(f'Error retrieving pod metrics. {self.message}')
