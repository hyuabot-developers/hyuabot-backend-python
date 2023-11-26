from enum import Enum


class Environment(str, Enum):
    LOCAL = "local"
    STAGING = "staging"
    TESTING = "testing"
    PRODUCTION = "production"

    @property
    def is_debug(self):
        return self in (self.LOCAL, self.STAGING, self.TESTING)

    @property
    def is_testing(self):
        return self == self.TESTING

    @property
    def is_deployed(self):
        return self in (self.STAGING, self.PRODUCTION)
