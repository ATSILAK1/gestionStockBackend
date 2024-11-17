from django.contrib import admin
from django.urls import path
from django.urls import include, path
from rest_framework import routers
from GestStock.views import *
from authentication import views

# Wire up our API using automatic URL routing.
# Additionally, we include login URLs for the browsable API.
urlpatterns = [
    
  #Produit Url 
  path('produit',ProduitCreation.as_view(),name='produitCreation'),
  path('produit/<int:pk>',ProduitDetails.as_view(),name='ProduitUpdate'),
  path('produit/autocomplete', ProduitAutocompleteView.as_view(), name='product-autocomplete'),

  #fournisseur Url 
  path('fournisseur',FrounisseurListCreation.as_view(),name='fournisseurCreation'),
  path('fournisseur/<int:pk>',FournisseurDetails.as_view(),name='fournisseurDetails'),
  path('fournisseur/autocomplete', FournisseurAutocompleteView.as_view(), name='product-autocomplete'),
  #TransactionAchat Url 
  path('transactionachat',TranscationAchatListCreation.as_view(),name='transactionachatlist'),
  path('transactionachat/<int:pk>',TransactionAchatDetails.as_view(),name='transactionachatDetails'),
  #TransactionVente Url 
  path('transactionvente',TranscationVenteListCreation.as_view(),name='transactionachatlist'),
  path('transactionvente/<int:pk>',TransactionVenteDetails.as_view(),name='transactionachatDetails'),
]