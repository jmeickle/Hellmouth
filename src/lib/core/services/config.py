import yaml

from src.lib.core.kernel import Kernel
from src.lib.core.services.service import Service

class ConfigService(Service):
    def __init__(self, directory):
        self.directory = directory

    def load(self, filenname):
        # TODO: Directory joining
        with open(self.directory + '/' + filenname) as f:
            return yaml.load(f)