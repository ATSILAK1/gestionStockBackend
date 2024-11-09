from django.db import models



# Create your models here.
class Produit(models.Model):
    prix          = models.FloatField()
    nom           = models.CharField(max_length=128 , unique=True)
    description   = models.CharField(max_length=512)
    quantiteStock = models.PositiveIntegerField()


class Fournisseur(models.Model):
    nomFournisseur = models.CharField(max_length=128)
    telephoneFournisseur = models.CharField(max_length=20)


class Transaction(models.Model):
    produitTransaction     = models.ForeignKey(Produit,on_delete=models.DO_NOTHING)
    informationTransaction = models.CharField(max_length=256)
    
    quantiteTransaction    = models.PositiveIntegerField()
    montantTransaction     = models.FloatField()
    dateTransaction        = models.DateTimeField()
    dateCreation           = models.DateTimeField(auto_now_add=True,)

    class Meta:
        abstract = True

class TransactionAchat(Transaction):
    fournisseurTransactionAchat = models.ForeignKey(Fournisseur,on_delete=models.PROTECT)

class TransactionVente(Transaction):
    pass    