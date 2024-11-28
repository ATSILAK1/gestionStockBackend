from django.contrib.auth.models import Group, User
from django.db import transaction
from rest_framework import serializers
from GestStock.models import *


class UserSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = User
        fields = ['url', 'username', 'email', 'groups']


class GroupSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Group
        fields = ['url', 'name']

class ProductSerializer(serializers.ModelSerializer):
    class Meta:
        model = Produit 
        fields ='__all__'


class FournisseurSerializer(serializers.ModelSerializer):
    class Meta:
        model=Fournisseur
        fields= '__all__'

class TransactionAchatSerializer(serializers.ModelSerializer):
    productData = ProductSerializer(read_only=True , source='produitTransaction')
    fournisseurData = FournisseurSerializer(read_only=True , source='fournisseurTransactionAchat')
    class Meta:
        model=TransactionAchat
        fields = '__all__'


    def create(self, validated_data):
        with transaction.atomic():
            transaction_instance:TransactionAchat = super().create(validated_data)
            product:Produit = transaction_instance.produitTransaction
            product.quantiteStock += transaction_instance.quantiteTransaction
            product.prix = transaction_instance.montantTransaction / transaction_instance.quantiteTransaction
            product.save()
        return transaction_instance



class TransactionVenteSerializer(serializers.ModelSerializer):
    productData = ProductSerializer(read_only=True, source='produitTransaction')

    class Meta:
        model=TransactionVente
        fields = '__all__'
        read_only_fields = ['margeVente']

    def validate_quantiteTransaction(self, value):
        # Check that the quantity is positive
        if value <= 0:
            raise serializers.ValidationError("Quantite doit etre positive .")
        prod_pk = self.initial_data.get('produitTransaction')
        product = Produit.objects.get(pk = prod_pk)
        if product and value > product.quantiteStock:
            raise serializers.ValidationError("Stock insuffisant.")

        return value

   
    def create(self, validated_data):
        with transaction.atomic():
            produit = validated_data.get('produitTransaction')
            quantite = validated_data.get('quantiteTransaction')
            montant = validated_data.get('montantTransaction')


            marge = montant - (quantite * produit.prix)
            validated_data['margeVente'] = marge
            transaction_instance:TransactionVente = super().create(validated_data)
            product:Produit = transaction_instance.produitTransaction
            product.quantiteStock -= transaction_instance.quantiteTransaction
            transaction_instance.margeVente = transaction_instance.montantTransaction - transaction_instance.quantiteTransaction * product.prix
            product.save()
            return transaction_instance
        
    
