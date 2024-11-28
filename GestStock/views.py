from datetime import datetime, date, timedelta

from django.db.models import Sum

from django.db import IntegrityError

from pymysql.times import TimeDelta
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
    queryset = TransactionAchat.objects.all().order_by('-dateTransaction')
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
    queryset = TransactionVente.objects.all().order_by('-dateTransaction')
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
def GetTransactionBenefice():
    querySet = TransactionVente.objects.all()
    result = querySet.aggregate(Sum('margeVente'))
    return result['margeVente__sum']
def GetTransactionBeneficeDate(date_debut, date_fin):
    querySet = TransactionVente.objects.filter(dateTransaction__range=(date_debut, date_fin))
    result = querySet.aggregate(Sum('margeVente'))
    return result['margeVente__sum']
def GetTransactionVenteBestProduit():
    querySet =  TransactionVente.objects.values('produitTransaction__nom')
    result = querySet.annotate(quantite_vendu=Sum('quantiteTransaction')  ).order_by('-quantite_vendu')
    return result
def GetTransactionAchatProduit():
    querySet =  TransactionAchat.objects.values('produitTransaction__nom')
    result = querySet.annotate(quantite_achete=Sum('quantiteTransaction')  ).order_by('-quantite_achete')
    return result
def GetNombreTransactionVenteParJour(dateJour):
    querySet = TransactionVente.objects.filter(dateTransaction__range=(dateJour, dateJour + timedelta(days=1)))
    result = querySet.count()
    return result

def GetNombreTransactionAchatParJour(dateJour):
    querySet = TransactionAchat.objects.filter(dateTransaction__range=(dateJour, dateJour + timedelta(days=1)))
    result = querySet.count()
    return result


class StatisticView(APIView):
    def get(self, request, *args, **kwargs):
        try:
            response = {
                "marge_total": GetTransactionBenefice(),
                "marge_total_par_jour": GetTransactionBeneficeDate(date_debut=date.today() , date_fin=date.today() +timedelta(days=1)),
                "transaction_vente_par_jour":GetNombreTransactionVenteParJour(dateJour=date.today() ),
                "transaction_achat_par_jour": GetNombreTransactionAchatParJour(dateJour=date.today() ),
                "quantite_produit_vendu": GetTransactionVenteBestProduit(),
                "quantite_produit_achete": GetTransactionAchatProduit(),


            }
            return Response(response , status=status.HTTP_200_OK)
        except Exception as e:
            return Response({'Ereur':"Erreur Produite " , 'exepction ':str(e) }, status=status.HTTP_400_BAD_REQUEST)

