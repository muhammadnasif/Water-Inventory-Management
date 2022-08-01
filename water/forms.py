import datetime
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Layout, Fieldset, Submit, Row, Column, Div, Field, ButtonHolder, Button
from django import forms
from .models import *


# This is widget specifically built for DatePicker
class DatePicker(forms.DateInput):
    input_type = 'date'


# This form is used to sell a product. The ROOM is taken as input to store
# the history of the sold products to a certain room
class SellBottleForm(forms.Form):
    room = forms.ModelChoiceField(queryset=ROOM.objects.all().order_by('room_no'), initial=0)
    bottle = forms.ModelChoiceField(queryset=BOTTLE.objects.all(), initial=0)
    quantity = forms.IntegerField(widget=forms.TextInput(attrs={'placeholder': 'Quantity'}))
    date = forms.DateField(initial=datetime.date.today(), widget=DatePicker)

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.form_method = 'POST'
        self.helper.form_show_labels = False
        self.helper.layout = Layout(
            Div(
                Column('room', css_class='custom-select col ms-2'),
                Column('bottle', css_class='custom-select col ms-2'),
                Column('quantity', css_class='custom-select col ms-2'),
                Column('date', css_class='col ms-2'),

                css_class='d-flex justify-content-evenly align-content-center m-2'
            ),
            Div(
                Button('complimentary', 'Complimentary', css_class='btn-dark btn-outline-success text-white m-sm-3'),
                Button('sell', 'Sell Bottle', css_class='btn-dark btn-outline-success text-white m-sm-3'),
                # Button('undo', 'Undo', css_class='btn-dark btn-outline-success text-white m-sm-3'),
                css_class='d-flex justify-content-center align-content-center m-2',
            ),
        )


# This form is used to create a new record in the STOCK table. If the record
# already exists then the input quantity is used to increase the stock amount
# of the respective product.
class AddNewStock(forms.Form):
    stock = forms.ModelChoiceField(queryset=BOTTLE_DETAILS.objects.all().order_by('bottle__brand_name'))
    quantity = forms.IntegerField(widget=forms.TextInput(attrs={'placeholder': 'Quantity'}))

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.form_show_labels = False
        self.helper.layout = Layout(
            Div(
                Column('stock', css_class='custom-select col mx-2'),
                Column('quantity', css_class='col mx-2', placeholder='Quantity'),
                css_class='form-row d-flex justify-content-center align-content-center mb-2'
            ),
            Div(
                Button('add-stock', 'Add Stock', css_class='btn-dark btn-outline-success text-white mb-3'),
                css_class='d-flex justify-content-center align-content-center',
            ),

        )




class HistoryTableSearchBarForm(forms.Form):
    DateFrom = forms.DateField(widget=DatePicker, label="From")
    DateTo = forms.DateField(widget=DatePicker, label="To")

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.form_show_labels = False
        self.helper.layout = Layout(
            Row(
                Column(
                    Div('DateFrom', css_class='col-3 mx-2', data_label_text="From"),
                    Div('DateTo', css_class='col-3 mx-2', data_label_text="To"),
                    Button('history-filter', 'Filter', css_class='btn-dark btn-outline-success text-white mb-3 mx-2'),
                    css_class='d-flex justify-content-center'
                ),

            )
        )
