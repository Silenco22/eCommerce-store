import sys

from paypalcheckoutsdk.core import PayPalHttpClient, SandboxEnvironment


class PayPalClient:
    def __init__(self):
        self.client_id = "AdZMo8dnqgqBhuTbF-s44pFVj7hX8wZx2Xclw7F4wtlj4rx1o1m2W8_x5iR0F3C6OLWJcdmN-SMhvDlm"
        self.client_secret = "EJ82q0LrOEnAyXAAHk9UgvUSqvUdeX2fTMCnS90IV9vGhk5xqDWv2xRBLJCrGuiqixgESGSdI5vt32aM"
        self.environment = SandboxEnvironment(client_id=self.client_id, client_secret=self.client_secret)
        self.client = PayPalHttpClient(self.environment)