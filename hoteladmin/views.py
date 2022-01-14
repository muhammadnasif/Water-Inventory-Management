from datetime import date

from django.db.models import Sum
from django.shortcuts import render, redirect
from django.http import HttpResponse, JsonResponse

import water
from water.forms import *
from water.views import *
import water.views as water_views
from .models import *
from .forms import *




# this method is for loading the Dashboard page [ ADMIN PAGE ]
def LoadDashboard(request):
    if 'username' in request.session:
        if request.session['designation'] == 'ceo':

            # this if is for Dashboard Data filtration
            from_date = ""
            to_date = ""
            bottleDetails = list(BOTTLE_DETAILS.objects.all())
            BrandForm = CreateBrandForm()
            StockTable, bottleSize = water_views.GetStockTableInfo()
            if request.method == 'POST':
                from_date = request.POST['dashboard_from']
                to_date = request.POST['dashboard_to']
                tableInfo, profitInfo, quantityInfo, totalSold, totalProfit = GetDashboardTable(from_date, to_date)
            else:
                tableInfo, profitInfo, quantityInfo, totalSold, totalProfit = GetDashboardTable()

            context = {
                'table': tableInfo,
                'profitInfo': profitInfo,
                'quantityInfo': quantityInfo,
                'totalSold': totalSold,
                'totalProfit': totalProfit,
                'fromDate': from_date,
                'toDate': to_date,
                'BottleDetails': bottleDetails,
                'BrandForm': CreateBrandForm(),
                'SizeForm': CreateSizeForm(),
                'brand': list(BRAND.objects.all()),
                'StockTable': StockTable,
                'bottleSize': bottleSize,
                'size': list(SIZE.objects.all()),
                'ceo': 1,
            }

            GetDashboardTable()
            if request.session['designation'] == 'ceo':
                context['ceo'] = 1

            return render(request, 'hoteladmin/Dashboard.html', context)
    else:
        return redirect(water_views.LoadHome)


# this method is for fetching the data for "Dashboard Bottle Report" and Pie Chart
def GetDashboardTable(from_date=None, to_date=None):
    #     history = list(HISTORY.objects.filter(date__gte=dFrom, date__lte=dTo).values())
    allHistoryDetails = 0
    if from_date is not None:
        allHistoryDetails = HISTORYDETAIL.objects.filter(history__date__gte=from_date, history__date__lte=to_date)
    else:
        allHistoryDetails = list(HISTORYDETAIL.objects.all())
    contextQuantity = {}
    contextSold = {}
    contextProfit = {}
    contextBuy = {}
    # for counting quantity
    for data in allHistoryDetails:
        if str(BOTTLE_DETAILS.objects.get(id=data.bottle_detail.pk).bottle) not in contextQuantity:
            contextQuantity[str(BOTTLE_DETAILS.objects.get(id=data.bottle_detail.pk).bottle)] = data.quantity
            contextBuy[str(BOTTLE_DETAILS.objects.get(
                id=data.bottle_detail.pk).bottle)] = float(data.bottle_detail.buy_price * data.quantity)
            contextSold[str(BOTTLE_DETAILS.objects.get(
                id=data.bottle_detail.pk).bottle)] = float(data.bottle_detail.sell_price * data.notcomplimentary * data.quantity)
        else:
            contextQuantity[str(BOTTLE_DETAILS.objects.get(id=data.bottle_detail.pk).bottle)] += data.quantity
            contextBuy[str(BOTTLE_DETAILS.objects.get(
                id=data.bottle_detail.pk).bottle)] += float(data.bottle_detail.buy_price * data.quantity)
            contextSold[str(BOTTLE_DETAILS.objects.get(
                id=data.bottle_detail.pk).bottle)] += float(
                data.bottle_detail.sell_price * data.quantity * data.notcomplimentary)

    for bottle in contextQuantity.keys():
        contextProfit[bottle] = contextSold[bottle] - contextBuy[bottle]

    context = {}
    totalSold = 0
    totalProfit = 0
    for bottle in contextQuantity.keys():
        context[bottle] = []
        context[bottle].append(bottle)
        context[bottle].append(contextQuantity[bottle])
        context[bottle].append(contextSold[bottle])
        context[bottle].append(contextProfit[bottle])
        totalSold += contextSold[bottle]
        totalProfit += contextProfit[bottle]

    return context, contextProfit, contextQuantity, totalSold, totalProfit


# this method here is for deleting objects in BOTTLE_DETAILS table
def DeleteBottleDetails(request):
    StockTable, bottleSize = water_views.GetStockTableInfo()
    if request.method == "POST":
        id = request.POST.get('sid')
        object = BOTTLE_DETAILS.objects.get(pk=id)
        object.delete()
        context = {
            'status': 1,
            'StockTable': StockTable,
            'bottleSize': bottleSize,
        }
    else:
        context = {
            'status': 0,
            'StockTable': StockTable,
            'bottleSize': bottleSize,
        }
    return JsonResponse(context)


# this method here is for creating new record of BRAND table
def CreateBrand(request):
    context = {
        'status': 0
    }
    if request.method == "POST":
        BrandForm = CreateBrandForm(request.POST)
        if BrandForm.is_valid():
            context['status'] = 1
            brand = BrandForm.cleaned_data['brand']
            object = BRAND(brand_name=brand)
            object.save()
            context['status'] = 1
    # context['brand'] = serializers.serialize('json',list(BRAND.objects.all()))
    context['brand'] = list(BRAND.objects.values())
    StockTable, bottleSize = water_views.GetStockTableInfo()

    context['bottleSize'] = bottleSize
    context['StockTable'] = StockTable

    return JsonResponse(context)


# this method is for deleting a brand
def DeleteBrand(request):
    context = {
        'status': 0
    }
    if request.method == "POST":
        id = request.POST['sid']
        object = BRAND.objects.get(pk=id)
        object.delete()
        context['status'] = 1
    StockTable, bottleSize = water_views.GetStockTableInfo()

    context['bottleSize'] = bottleSize
    context['StockTable'] = StockTable

    return JsonResponse(context)


# this method is for creating a record of size
def CreateSize(request):
    context = {
        'status': 0
    }
    if request.method == "POST":
        SizeForm = CreateSizeForm(request.POST)
        if SizeForm.is_valid():
            context['status'] = 1
            size = SizeForm.cleaned_data['size']
            object = SIZE(bottle_size=size)
            object.save()
            context['status'] = 1
    # context['brand'] = serializers.serialize('json',list(BRAND.objects.all()))
    context['sizeTable'] = list(SIZE.objects.values())
    StockTable, bottleSize = water_views.GetStockTableInfo()

    context['bottleSize'] = bottleSize
    context['StockTable'] = StockTable

    return JsonResponse(context)


# this method is for deleting record of size
def DeleteSize(request):
    context = {
        'status': 0
    }
    if request.method == "POST":
        id = request.POST['sid']
        object = SIZE.objects.get(pk=id)
        object.delete()
        context['status'] = 1
    StockTable, bottleSize = water_views.GetStockTableInfo()
    context['sizeTable'] = list(SIZE.objects.values())
    context['bottleSize'] = bottleSize
    context['StockTable'] = StockTable

    return JsonResponse(context)


# this method is for creating new session
def CreateNewSession(request, username, designation):
    request.session['username'] = username
    request.session['designation'] = designation
    request.session['undo_id'] = []


# the cookies of the sessions are removed here
def RemoveSession(request):
    request.session.flush()
    request.session.clear_expired()
    return redirect(LogIn)


# this method is for user authentication
def LogIn(request):
    if 'username' in request.session:
        if request.session['designation'] == 'ceo':
            return redirect(LoadDashboard)
    if request.method == "POST":
        username = request.POST['username']
        password = request.POST['password']
        user = USER.objects.filter(username=username, password=password)
        if len(user) == 0:
            return redirect(LogIn)
        else:
            user = list(user.values())[0]
            CreateNewSession(request, user['username'], user['designation'])
            if user['designation'] == 'ceo':
                return redirect(LoadDashboard)
            else:
                return redirect(water_views.LoadHome)
    return render(request, 'commonHTML/LogIn.html', {})
