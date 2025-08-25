from decimal import Decimal
import unittest
from customers.repositories import CustomerRepository
from services.revenue_service import RevenueService

class FakeRepo:
    def __init__(self, avg):
        self._avg = avg
    def average_revenue(self):
        return self._avg

class FakeHSM:
    def sign_data(self, data: bytes):
        return b'signature-' + data

class RevenueServiceTest(unittest.TestCase):
    def test_compute_average(self):
        repo = FakeRepo('123.45')
        hsm = FakeHSM()
        svc = RevenueService(repo, hsm)
        r = svc.compute_average(sign_result=True)
        assert r['average'] == '123.45'
        assert 'signature' in r

if __name__ == '__main__':
    unittest.main()
