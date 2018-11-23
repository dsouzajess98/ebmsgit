from __future__ import unicode_literals
from math import *
from django.db import models
from market.models import *
import datetime

tx_id = 0 #keep incrementing it per transaction to generate t_id and then hash it to make it look complex
# Create your models here.




class Banker(models.Model):
	b_name = models.CharField(max_length=35) #actually, we maintain a the list of stored banks using this. and then we add new each time (as admin) and the user selects one while payment procedure
	status_bit = models.BooleanField(default=True) #we can claim the current bank chosen is down, but only as admin
	def __str__(self):
		return str(self.b_name)


class NetBankAcc(models.Model):
	#this is valid only while netbanking
	user_name = models.CharField(max_length=25)
	psswd = models.CharField(max_length=25)
	
	def __str__(self):
		return str(self.user_name)

class DebCard(models.Model):
	cardno = models.IntegerField()
	cvv = models.IntegerField()
	pin = models.IntegerField(null=True)
	exp = models.DateField()
	name = models.CharField(max_length=35)
	pay_service = models.BooleanField() # 0 for visa and 1 for mc
	

	def __str__(self):
		return str(self.cardno)
	def is_valid(self): #to check if the entered card no is valid.
		n = self.cardno
		r = [int(ch) for ch in str(n)][::-1]
   		return (sum(r[0::2]) + sum(sum(divmod(d*2,10)) for d in r[1::2])) % 10 == 0


class txn(models.Model):
	cur_user = models.ForeignKey('market.Customer', on_delete=models.CASCADE)
	time = models.TimeField(auto_now_add=True)
	date = models.DateField(default=datetime.date.today)
	amount = models.DecimalField(decimal_places=3, max_digits=15)
	cardno = models.ForeignKey(DebCard, on_delete=models.CASCADE)
	t_id = tx_id+1
	def __str__(self):
		return str(cardno) + str(tx_id) #this is the new tx_id hash val (change this later to make it more complex)


