import datetime
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Layout, Fieldset, Submit, Row, Column, Div, Field, ButtonHolder, Button
from django import forms
from water.models import *


# This is widget specifically built for DatePicker
class DatePicker(forms.DateInput):
    input_type = 'date'


# This form is used ot create a new record in the BOTTLE table
class CreateNewBottleForm(forms.Form):
    brand = forms.ModelChoiceField(queryset=BRAND.objects.all(), initial=0)
    size = forms.ModelChoiceField(queryset=SIZE.objects.all(), initial=0)
    buyPrice = forms.DecimalField(max_digits=4, decimal_places=2,
                                  widget=forms.TextInput(attrs={'placeholder': 'Buying Price'}))
    sellPrice = forms.DecimalField(max_digits=4, decimal_places=2,
                                   widget=forms.TextInput(attrs={'placeholder': 'Selling Price'}))

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.form_show_labels = False
        self.helper.form_id = 'createBottle'
        # self.helper.form_tag = False
        self.helper.layout = Layout(
            Div(
                Column('brand', css_class='custom-select col mx-2'),
                Column('size', css_class='custom-select col mx-2'),
                css_class='form-row d-flex justify-content-center align-content-center mb-2'
            ),
            Div(
                Div('buyPrice', css_class='col-3 mx-2'),
                Div('sellPrice', css_class='col-3 mx-2'),
                # Submit('submit', 'Create', css_class='btn-secondary btn-outline-success text-white mb-3 mx-2'),
                Button('create-bottle', 'Create', css_class='btn-dark btn-outline-success text-white mb-3 mx-2'),
                css_class='form-row d-flex justify-content-center align-content-center'
            )
        )


# This form is for creating new brand
class CreateBrandForm(forms.Form):
    brand = forms.CharField(max_length=30, widget=forms.TextInput(attrs={'placeholder': 'Enter Here'}))

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.form_show_labels = False
        self.helper.form_tag = False
        self.helper.layout = Layout(
            Row(
                Column('brand', css_class='col-8 my-2 mx-2'),
                Div(
                    Button('create-brand', 'Create', css_class='btn btn-dark my-2 mx-2'),
                    css_class='col'
                ),

                css_class="d-flex justify-content-center align-content-center text-wrap my-2"
            )
        )

    # This form is for creating new size


# This form is for creating new record in SIZE table
class CreateSizeForm(forms.Form):
    size = forms.DecimalField(max_digits=4, decimal_places=2,
                              widget=forms.TextInput(attrs={'placeholder': 'Enter Here'}))

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.form_show_labels = False
        self.helper.form_tag = False
        self.helper.layout = Layout(
            Row(
                Column('size', css_class='col-8 my-2 mx-2'),
                Div(
                    Button('create-size', 'Create', css_class='btn btn-dark my-2 mx-2'),
                    css_class='col'
                ),

                css_class="d-flex justify-content-center align-content-center text-wrap my-2"
            )
            # Div(
            #     Column('size', css_class='col mb-3 mx-2'),
            #     # Submit('submit', 'Create', css_class='btn-secondary btn-outline-success text-white mb-3 mx-2'),
            #     Button('create-size', 'Create', css_class='btn-sm btn-dark mb-3 mx-2'),
            #     css_class='form-row d-flex justify-content-center align-content-center'
            # )
        )
