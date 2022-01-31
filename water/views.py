from datetime import date

from django.db.models import Sum
from django.shortcuts import render, redirect
from django.http import HttpResponse, JsonResponse

from hoteladmin.views import LogIn
from .forms import *
from hoteladmin.forms import *
from django.core import serializers


# Create your views here.

# class VAR:
#     undo_id = []


def index(request):
    # form = stockForm()
    # form = addNewStock()

    context = {
        'SellBottleForm': SellBottleForm(),
        'AddNewStock': AddNewStock(),
        'CreateNewBottleForm': CreateNewBottleForm(),
    }
    # return render(request, 'water/createNewBottleForm.html', context)
    return render(request, 'hoteladmin/admin.html', context)
    # return render(request, 'water/sellBottleForm.html', context)
    # return render(request, 'water/addNewStock.html', context)


# this method loads the home page
def LoadHome(request):
    if 'username' in request.session:
        if request.session['designation'] != 'ceo':
            context = {
                'SellBottleForm': SellBottleForm(),
                'history': getHistory(),
                'historyTableFilterBar': HistoryTableSearchBarForm(),
                'ceo': 0,
            }

            if request.session['designation'] == 'ceo':
                context['ceo'] = 1

            return render(request, 'water/home.html', context)
    return redirect(LogIn)


# this method loads the status page
def LoadStatus(request):
    if 'username' in request.session:
        if request.session['designation'] != 'ceo':
            StockTable, bottleSize = GetStockTableInfo()
            context = {
                'AddNewStock': AddNewStock(),
                'CreateNewBottleForm': CreateNewBottleForm(),
                'StockTable': StockTable,
                'bottleSize': bottleSize,
            }
            if request.session['designation'] == 'ceo':
                context['ceo'] = 1
            return render(request, 'water/status.html', context)
    else:
        return redirect(LogIn)


# This method is used to sell bottles and record the history in the
# HISTORY, HISTORY_DETAILS table.
def sellBottleMethod(request, notComp=1):
    notEnough = 1
    if request.method == "POST":
        form = SellBottleForm(request.POST)

        if form.is_valid():

            room = form.cleaned_data['room']
            bottle = form.cleaned_data['bottle']
            quantity = form.cleaned_data['quantity']
            sellDate = form.cleaned_data['date']
            bottle_details = BOTTLE_DETAILS.objects.filter(bottle_id=bottle.pk).order_by('buy_price')

            executed = False

            # add to history
            sellHistory = HISTORY(room_id=room, date=sellDate)

            sellHistory.save()

            # add to HISTORY_DETAILS

            if len(bottle_details) != 0:
                totalBottleStock = 0

                # counting the total same types of bottles with different stockIn pricing
                # and checking afterwards if that total bottle number is sufficient for
                # the request to fulfill

                for bottleDetailsObj in bottle_details:
                    bottleStockObj = STOCK.objects.filter(stock_name_id=bottleDetailsObj.pk)
                    if len(bottleStockObj) != 0:
                        # getting the record from QuerySet by indexing
                        bottleStockObj = bottleStockObj[0]
                        totalBottleStock += bottleStockObj.quantity

                if totalBottleStock >= quantity:
                    notEnough = 0
                    for bottleDetailsObj in bottle_details:
                        bottleStockObj = STOCK.objects.filter(stock_name_id=bottleDetailsObj.pk)
                        # check if that record of BOTTLE_HISTORY exists in the STOCK table
                        # As BOTTLE_HISTORY and STOCK table are in one-to-one relationship
                        # the returned QuerySet will either contain 1 value or 0 value. Hence
                        # checking by != 0 means if there ary any value in the QuerySet.
                        if len(bottleStockObj) != 0:

                            # getting the record from QuerySet by indexing
                            bottleStockObj = bottleStockObj[0]
                        else:
                            # ============ SEND MESSAGE TO USER ==================
                            # ########## THE BOTTLE IS NOT IN STOCK ##############
                            # ====================================================
                            # print("The bottle is not in stock")
                            break

                        # if the stock amount is greater than the requested quantity then decrease
                        # the stock count by quantity. Finally update the STOCK record. To update
                        # we need to specify the 'id'. 'id' is the primary-key of that STOCK record.
                        # If not mentioned, dJango will execute the command as a new object and add
                        # a new record

                        if bottleStockObj.quantity <= quantity:
                            # add to HISTORY_DETAIL table
                            history_details = HISTORYDETAIL(history=sellHistory, bottle_detail=bottleDetailsObj,
                                                            quantity=quantity, notcomplimentary=notComp)
                            history_details.save()

                            quantity -= bottleStockObj.quantity

                            bottleStockObj = STOCK(id=bottleStockObj.pk, stock_name_id=bottleStockObj.stock_name_id,
                                                   quantity=0)
                            bottleStockObj.save()

                            # VAR.undo_id.append(history_details.pk)
                            tempList = request.session["undo_id"]
                            tempList.append(history_details.pk)
                            request.session["undo_id"] = tempList
                            # request.session['undo_id'].append(history_details.pk)
                            # print(f'undo id --- {request.session["undo_id"]}')
                            executed = True
                        else:
                            bottleStockObj = STOCK(id=bottleStockObj.pk, stock_name_id=bottleStockObj.stock_name_id,
                                                   quantity=bottleStockObj.quantity - quantity)
                            bottleStockObj.save()

                            # add to HISTORY_DETAIL table
                            history_details = HISTORYDETAIL(history=sellHistory, bottle_detail=bottleDetailsObj,
                                                            quantity=quantity, notcomplimentary=notComp)
                            history_details.save()
                            # VAR.undo_id.append(history_details.pk)
                            tempList = request.session["undo_id"]
                            tempList.append(history_details.pk)
                            request.session["undo_id"] = tempList
                            executed = True
                            break
                # if not executed:
                #     # ================= SEND MESSAGE TO USER =================
                #     # ============ NOT SUFFICIENT BOTTLE IN STOCK ============
                #     # ========================================================
                #     print("Not sufficient bottle in stock")
                else:
                    notEnough = 1
    context = {
        'status': notEnough,
        'history': getHistory(),
    }
    return JsonResponse(context)


# this method is for selling the complimentary bottles
def sellBottleComplimentary(request):
    jsonVar = sellBottleMethod(request, 0)
    return jsonVar


# This method is used to add a certain amount of products
# in the stock. == addNewStockMethod() ==
def addNewStockMethod(request):
    if request.method == 'POST':
        form = AddNewStock(request.POST)
        if form.is_valid():

            bottleDetailsObject_PK = request.POST['stock']
            stockQuantity = form.cleaned_data['quantity']
            bottleDetailsObject = form.cleaned_data['stock']

            # check if the stock exists with the following if-else
            # if stock does not exist
            if len(STOCK.objects.filter(stock_name_id=bottleDetailsObject_PK)) == 0:
                # create a new STOCK instance and save it.
                newStock = STOCK(quantity=stockQuantity, stock_name=bottleDetailsObject)
                newStock.save()

            # if stock exists
            else:
                # fetch the stock object using foreign key and use it afterwards to access
                # the initial quantity via 'existingStock'
                existingStock = STOCK.objects.filter(stock_name_id=bottleDetailsObject_PK)[0]
                existingStock = STOCK(id=existingStock.pk, stock_name_id=bottleDetailsObject_PK,
                                      quantity=existingStock.quantity + stockQuantity)
                existingStock.save()

        # else:
        #     print("Form is not valid")
    StockTable, bottleSize = GetStockTableInfo()
    context = {
        'status': 1,
        'StockTable': StockTable,
        'bottleSize': bottleSize,
    }
    return JsonResponse(context)


# This method is used to create a new instance of bottle and
# create a new record of bottle in the BOTTLE table.
# == createNewBottleMethod() ==
def createNewBottleMethod(request):
    print(request.GET)
    print(request.POST)
    if request.method == "POST":
        form = CreateNewBottleForm(request.POST)
        if form.is_valid():
            brand = form.cleaned_data['brand']
            size = form.cleaned_data['size']
            buy = form.cleaned_data['buyPrice']
            sell = form.cleaned_data['sellPrice']
            newBottle = BOTTLE(brand_name=brand, bottle_size=size)
            # checks if the bottle already exists in the database. If it does not
            # exist then it creates a new instance of that bottle and adds a
            # relation of that bottle with a corresponding BOTTLE_DETAILS object

            if not BOTTLE.objects.filter(brand_name=brand, bottle_size=size):
                newBottle.save()
                newBottleDetails = BOTTLE_DETAILS(buy_price=buy, sell_price=sell, bottle=newBottle)
                newBottleDetails.save()

            else:
                if not BOTTLE_DETAILS.objects.filter(buy_price=buy):
                    existingBottle = BOTTLE.objects.filter(brand_name=brand, bottle_size=size)[0]
                    newBottleDetails = BOTTLE_DETAILS(buy_price=buy, sell_price=sell, bottle=existingBottle)
                    newBottleDetails.save()

                # else:
                # =================== ADD SOMETHING TO SEND MESSAGE ===================
                # send a message to user that " Bottle already exists. "
                # =====================================================================
                # print("BOTTLE ALREADY EXISTS....")

    context = {
        'status': 1,
        'bottleDetailsDropdown': GetBottleDetailsDropdown(),
    }
    GetBottleDetailsDropdown()
    return JsonResponse(context)


# this method returns the BottleDetails record objects in bottle[bottle_details_pk]=bottle_detail_name
def GetBottleDetailsDropdown():
    bottledetails = BOTTLE_DETAILS.objects.all().order_by('bottle__brand_name')

    context = {}
    for bottle in bottledetails:
        context[bottle.pk] = str(bottle)

    return context


# this method is used to generate the data for historyTable.html
def getHistory():
    today = date.today()
    # context = {
    #     str(today): {},
    # }

    context = {}

    # history = list(HISTORY.objects.filter(date=today).values())
    history_prev = list(HISTORY.objects.filter(date=today).values())
    history = list(HISTORY.objects.all().values())

    for info in history_prev:
        history_detail = list(HISTORYDETAIL.objects.filter(history_id=info["id"]).values())
        if (len(history_detail)) == 0:
            continue
        bottle_detail = list(BOTTLE_DETAILS.objects.filter(id=history_detail[0]["bottle_detail_id"]).values())
        bottle = list(BOTTLE.objects.filter(id=bottle_detail[0]["bottle_id"]).values())
        brand = bottle[0]["brand_name_id"]
        size = bottle[0]["bottle_size_id"]
        if str(info["date"]) not in context:
            context[str(info["date"])] = {}

        if info["room_id"] not in context[str(info["date"])].keys():
            if history_detail[0]["notcomplimentary"] == 0:
                context[str(info["date"])][str(info["room_id"])] = {
                    "bottle": [f"{brand} | {size}L (Compl.)"],
                    "quantity": [history_detail[0]["quantity"]],
                }
            else:
                context[str(info["date"])][str(info["room_id"])] = {
                    "bottle": [f"{brand} | {size}L"],
                    "quantity": [history_detail[0]["quantity"]],
                }


        else:
            if history_detail[0]["notcomplimentary"] == 0:
                context[str(info["date"])][info["room_id"]]["bottle"].append(f"{brand} | {size}L (Compl.)")
                context[str(info["date"])][info["room_id"]]["quantity"].append(history_detail[0]["quantity"])
            else:
                context[str(info["date"])][info["room_id"]]["bottle"].append(f"{brand} | {size}L")
                context[str(info["date"])][info["room_id"]]["quantity"].append(history_detail[0]["quantity"])

    return context


# this method is used to generate the data for stockTable.html
def GetStockTableInfo():
    context = {}
    bottleSize = {}
    for brand in list(BRAND.objects.all()):

        context[str(brand)] = {}

        for size in list(SIZE.objects.all()):
            bottleSize[str(size)] = str(size)
            context[str(brand)][str(size)] = "N/A"

            bottles = BOTTLE.objects.filter(brand_name_id=brand.pk, bottle_size_id=size.pk)

            for bottle in bottles:
                bottleDetails = BOTTLE_DETAILS.objects.filter(bottle_id=bottle.pk)
                once = True
                for stockInfo in bottleDetails:

                    stock = STOCK.objects.filter(stock_name_id=stockInfo.pk)
                    if len(stock) == 0:
                        continue
                    x = list(stock.values())[0]["quantity"]
                    if list(stock.values())[0]["quantity"] == 0:
                        context[str(brand)][str(size)] = 0
                    else:
                        if once:
                            context[str(brand)][str(size)] = 0
                            once = False
                        context[str(brand)][str(size)] += list(stock.values())[0]["quantity"]

    return context, bottleSize


# this method is for customer history filter
def FilterSearch(request):
    dFrom = request.POST['dateFrom']
    dTo = request.POST['dateTo']

    context = {}

    # history = list(HISTORY.objects.filter(date=today).values())
    # history_prev = list(HISTORY.objects.filter(date=today).values())
    history = list(HISTORY.objects.filter(date__gte=dFrom, date__lte=dTo).values())

    for info in history:
        history_detail = list(HISTORYDETAIL.objects.filter(history_id=info["id"]).values())
        if (len(history_detail)) == 0:
            continue
        bottle_detail = list(BOTTLE_DETAILS.objects.filter(id=history_detail[0]["bottle_detail_id"]).values())
        bottle = list(BOTTLE.objects.filter(id=bottle_detail[0]["bottle_id"]).values())
        brand = bottle[0]["brand_name_id"]
        size = bottle[0]["bottle_size_id"]
        if str(info["date"]) not in context:
            context[str(info["date"])] = {}

        if info["room_id"] not in context[str(info["date"])].keys():
            if history_detail[0]["notcomplimentary"] == 0:
                context[str(info["date"])][str(info["room_id"])] = {
                    "bottle": [f"{brand} | {size}L (Compl.)"],
                    "quantity": [history_detail[0]["quantity"]],
                }
            else:
                context[str(info["date"])][str(info["room_id"])] = {
                    "bottle": [f"{brand} | {size}L"],
                    "quantity": [history_detail[0]["quantity"]],
                }


        else:
            if history_detail[0]["notcomplimentary"] == 0:
                context[str(info["date"])][info["room_id"]]["bottle"].append(f"{brand} | {size}L (Compl.)")
                context[str(info["date"])][info["room_id"]]["quantity"].append(history_detail[0]["quantity"])
            else:
                context[str(info["date"])][info["room_id"]]["bottle"].append(f"{brand} | {size}L")
                context[str(info["date"])][info["room_id"]]["quantity"].append(history_detail[0]["quantity"])

    return JsonResponse({'history': context})


# this method is for customer history undo move
def HistoryDetailsUndo(request):
    tempList = request.session['undo_id']
    if len(tempList) != 0:
        undoID = tempList.pop()
        object = HISTORYDETAIL.objects.get(id=undoID)

        # increase the corresponding stock by the decremented quantity. Basically
        # updating the stock of the corresponding bottle.
        soldQuantity = object.quantity
        bottleStock = STOCK.objects.get(stock_name_id=object.bottle_detail.pk)
        fixedStock = STOCK(id=bottleStock.pk, stock_name_id=bottleStock.stock_name_id,
                           quantity=bottleStock.quantity + soldQuantity)
        fixedStock.save()

        object.delete()
    request.session['undo_id'] = tempList
    context = {
        'history': getHistory()
    }
    return JsonResponse(context)
