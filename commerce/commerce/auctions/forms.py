
from django import forms
from .models import Listing, Category

class ListingForm(forms.ModelForm):
    category = forms.ModelChoiceField(
        queryset=Category.objects.all(),
        required=False,
        empty_label="Select a category"
    )

    class Meta:
        model = Listing
        fields = ['title', 'description', 'starting_bid', 'image_url', 'category']
        widgets = {
            'description': forms.Textarea(attrs={'rows': 4}),
            'starting_bid': forms.NumberInput(attrs={'step': '0.01'}),
        }
