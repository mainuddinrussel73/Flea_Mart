from django.contrib.auth.models import User
from django import forms
from User.models import SellItemInfo,Comments,Auctions

class SellItemInfoForm(forms.ModelForm):
    class Meta():
        model = SellItemInfo
        fields = ('item_name','item_type','item_location','item_exprice','item_usetime','item_reason','item_pic','item_lat','item_long')


class CommentsForm(forms.ModelForm):
    class Meta():
        model = Comments
        fields = ('content','username')


class AuctionsForm(forms.ModelForm):
    class Meta():
        model = Auctions
        fields = ('bids','biders')