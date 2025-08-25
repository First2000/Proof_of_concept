from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .repositories import CustomerRepository
from services.revenue_service import RevenueService
from hsm.azure_hsm_client import AzureHSMClient
from django.conf import settings


class FakeHSM:
    def sign_data(self, data: bytes):
        return b'fake-signature-' + data
    def close(self):
        pass


class AverageRevenueAPIView(APIView):
    def get(self, request):
        sign = request.query_params.get('sign', 'false').lower() == 'true'
        repo = CustomerRepository()

        # ✅ Si les variables Azure sont définies, on utilise l’HSM réel
        if getattr(settings, 'AZURE_KEY_VAULT_URL', None) and getattr(settings, 'AZURE_KEY_NAME', None):
            hsm = AzureHSMClient(
                vault_url=settings.AZURE_KEY_VAULT_URL,
                key_name=settings.AZURE_KEY_NAME,
                key_version=getattr(settings, 'AZURE_KEY_VERSION', None),
            )
        else:
            # ✅ Sinon, on bypass avec FakeHSM
            hsm = FakeHSM()

        service = RevenueService(repo, hsm)

        try:
            result = service.compute_average(sign_result=sign)
            return Response(result)
        except Exception as exc:
            return Response({'error': str(exc)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        finally:
            hsm.close()
