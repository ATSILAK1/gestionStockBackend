from django.db import models



# Create your models here.
class Produit(models.Model):
    prix          = models.DecimalField(max_digits=10, decimal_places=2)
    nom           = models.CharField(max_length=128 , unique=True)
    description   = models.CharField(max_length=512)
    quantiteStock = models.PositiveIntegerField()


class Fournisseur(models.Model):
    nomFournisseur = models.CharField(max_length=128)
    telephoneFournisseur = models.CharField(max_length=20)


class Transaction(models.Model):
    produitTransaction     = models.ForeignKey(Produit,on_delete=models.DO_NOTHING)
    informationTransaction = models.CharField(max_length=256 , null=True , blank=True)
    quantiteTransaction    = models.PositiveIntegerField()
    montantTransaction     = models.DecimalField(max_digits=10, decimal_places=2)
    dateTransaction        = models.DateTimeField()
    dateCreation           = models.DateTimeField(auto_now_add=True,)

    class Meta:
        abstract = True

class TransactionAchat(Transaction):
    fournisseurTransactionAchat = models.ForeignKey(Fournisseur,on_delete=models.PROTECT )

class TransactionVente(Transaction):
    margeVente = models.DecimalField(max_digits=10, decimal_places=2)
