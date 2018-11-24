from django.contrib import admin
from .models import Banker,DebCard,NetBankAcc,txn
# Register your models here.
admin.site.register(Banker)
admin.site.register(DebCard)
admin.site.register(NetBankAcc)
admin.site.register(txn)
