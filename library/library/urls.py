from django.urls import path
from .views import *

urlpatterns = [
    path('book/',add_book),
    path('member/',add_member),
    path('transaction/',add_transaction),
    path('staff/',add_staff),
    path('dashboard/',dashboard_view),
    path('book/feature/<int:book_id>/', toggle_featured, name='toggle_featured'),
    path('transaction/lost/<int:transaction_id>/', mark_as_lost, name='mark_as_lost'),
    path('listbook/', book_list, name='book_list'),
    
    path('transaction_list/', transaction_list, name='transaction_list'),
]
