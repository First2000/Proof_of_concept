from decimal import Decimal
from customers.repositories import CustomerRepository

class RevenueService:
    def __init__(self, repo: CustomerRepository, hsm_client):
        self.repo = repo
        self.hsm = hsm_client

    def compute_average(self, sign_result: bool = False) -> dict:
        avg = self.repo.average_revenue()
        if avg is None:
            return {"average": None}

        avg = Decimal(avg)
        result = {"average": str(avg)}

        if sign_result:
            signature = self.hsm.sign_data(str(avg).encode('utf-8'))
            result['signature'] = signature.hex()

        return result
