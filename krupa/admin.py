from django.contrib import admin
# from .models import CustomUser, Category, Products, Subcategory, Orders, Request, SupportTicket, UserAddress, Invoice, Estimate, EstimateItem, SalesOrderItem
from .models import*
# Register your models here.

admin.site.register(CustomUser)
admin.site.register(Category)
admin.site.register(Subcategory)
admin.site.register(Products)
admin.site.register(Orders)
admin.site.register(Request)
admin.site.register(SupportTicket)
admin.site.register(UserAddress)
admin.site.register(Invoice)
admin.site.register(EstimateItem)
admin.site.register(Estimate)
admin.site.register(InvoiceEstimate)
admin.site.register(Item)
admin.site.register(SalesOrder)
admin.site.register(Payment)
admin.site.register(SalesOrderItem)
admin.site.register(CompanyInfo)
admin.site.register(Vendor)
admin.site.register(Purchase)
admin.site.register(PurchaseItem)
admin.site.register(Bill)
admin.site.register(BillItem)
admin.site.register(ShippingAddress)


