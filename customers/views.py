from django.shortcuts import render, redirect
from .repositories import CustomerRepository
from services.revenue_service import RevenueService
from django.conf import settings
from .forms import CustomerForm
from .models import Customer



def add_customer(request):
    if request.method == "POST":
        form = CustomerForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('customer_list')  # redirige vers la liste des clients
    else:
        form = CustomerForm()
    return render(request, 'add_customer.html', {'form': form})


def customer_list(request):
    customers = Customer.objects.all()
    return render(request, 'customer_list.html', {'customers': customers})



def average_page(request):
    sign = request.GET.get('sign', 'false').lower() == 'true'
    repo = CustomerRepository()

    # 🔹 Si les variables Azure sont présentes -> AzureHSMClient
    if getattr(settings, 'AZURE_KEY_VAULT_URL', None) and getattr(settings, 'AZURE_KEY_NAME', None):
        from hsm.azure_hsm_client import AzureHSMClient
        hsm = AzureHSMClient(
            vault_url=getattr(settings, 'AZURE_KEY_VAULT_URL', None),
            key_name=getattr(settings, 'AZURE_KEY_NAME', None),
            key_version=getattr(settings, 'AZURE_KEY_VERSION', None)
        )
    else:
        # 🔹 Sinon -> DummyHSM (bypass signature)
        class DummyHSM:
            def sign_data(self, data: bytes):
                return b"dummy-signature"
            def close(self): 
                pass
        hsm = DummyHSM()

    service = RevenueService(repo, hsm)
    try:
        result = service.compute_average(sign_result=sign)
    finally:
        hsm.close()

    return render(request, 'average.html', result)



