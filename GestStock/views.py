from django.http import HttpResponse
from django.db import IntegrityError
from django.shortcuts import render
from django.utils.regex_helper import contains
from rest_framework import generics ,status 
from rest_framework.response import Response
from GestStock.serializers import ProductSerializer ,TransactionAchatSerializer , FournisseurSerializer , TransactionVenteSerializer
from GestStock.models import Fournisseur, Produit, TransactionAchat, TransactionVente
from rest_framework.views import APIView

import authentication
# Create your views here.



#Produit View

class ProduitCreation(generics.ListCreateAPIView):
    serializer_class = ProductSerializer 
    queryset = Produit.objects.all()
    lookup_field = "pk" 

    def create(self, request, *args, **kwargs):
        try:
            return super().create(request, *args, **kwargs)   
        except IntegrityError:
            return Response(data={"erreur":"objet deja existant"},status=status.HTTP_400_BAD_REQUEST )

class ProduitDetails(generics.RetrieveUpdateDestroyAPIView):
    serializer_class = ProductSerializer
    queryset = Produit.objects.all()
    lookup_field = "pk"


class ProduitAutocompleteView(generics.ListAPIView):
    serializer_class = ProductSerializer

    def get_queryset(self):
        query = self.request.query_params.get('nom', None)

        if query is not None:
            return Produit.objects.filter(nom__icontains=query)

        return Produit.objects.none()

    def list(self, request, *args, **kwargs):
        queryset = self.get_queryset()
        serializer = self.get_serializer(queryset, many=True)
        return Response({
            'results': serializer.data
        })

## Fournisseur View

class FrounisseurListCreation(generics.ListCreateAPIView):
    serializer_class = FournisseurSerializer
    queryset = Fournisseur.objects.all()
    lookup_field= "pk"

class FournisseurDetails(generics.RetrieveUpdateDestroyAPIView):
    serializer_class = FournisseurSerializer
    queryset = Fournisseur.objects.all()
    lookup_field = "pk"

class FournisseurAutocompleteView(generics.ListAPIView):
    serializer_class = FournisseurSerializer
    queryset = Fournisseur.objects.all()
    lookup_field = "pk"
    def get_queryset(self):
        query = self.request.query_params.get('nomfournisseur', None)
        if query is not None:
            return Fournisseur.objects.filter(nomFournisseur__icontains=query)
        return Fournisseur.objects.none()

    def list(self, request, *args, **kwargs):
        queryset = self.get_queryset()
        serializer = self.get_serializer(queryset, many=True)
        return Response({
            'results': serializer.data
        })


## Transaction_Achat view

class TranscationAchatListCreation(generics.ListCreateAPIView):
    serializer_class = TransactionAchatSerializer
    queryset = TransactionAchat.objects.all()
    lookup_field = 'pk'



class TransactionAchatDetails(generics.RetrieveUpdateDestroyAPIView):
    serializer_class = TransactionAchatSerializer
    queryset = TransactionAchat.objects.all()
    lookup_field = 'pk'
    def delete(self, request, *args, **kwargs):
        instance:TransactionAchat = self.get_object()
        instance.produitTransaction.quantiteStock -= instance.quantiteTransaction
        instance.produitTransaction.save()
        self.perform_destroy(instance)
        return Response({"success": "Transaction deleted successfully."},status=status.HTTP_204_NO_CONTENT)



## Transation Vente 
class TranscationVenteListCreation(generics.ListCreateAPIView):
    serializer_class = TransactionVenteSerializer
    queryset = TransactionVente.objects.all()
    lookup_field = 'pk'

class TransactionVenteDetails(generics.RetrieveUpdateDestroyAPIView):
    serializer_class = TransactionVenteSerializer
    queryset = TransactionVente.objects.all()
    lookup_field = 'pk'

    def delete(self, request, *args, **kwargs):
        instance:TransactionVente = self.get_object()
        instance.produitTransaction.quantiteStock += instance.quantiteTransaction
        instance.produitTransaction.save()
        self.perform_destroy(instance)
        return Response({"success": "Transaction deleted successfully."}, status=status.HTTP_204_NO_CONTENT)

    
## Statistics
