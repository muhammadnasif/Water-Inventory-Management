from django.db import models


# Create your models here.

class ROOM(models.Model):
    room_no = models.CharField(max_length=20, primary_key=True)

    def __str__(self):
        return self.room_no


class BRAND(models.Model):
    brand_name = models.CharField(max_length=20, primary_key=True)

    def __str__(self):
        return self.brand_name


class SIZE(models.Model):
    bottle_size = models.DecimalField(decimal_places=2, max_digits=4, primary_key=True)

    def __str__(self):
        return str(self.bottle_size)


class BOTTLE(models.Model):
    brand_name = models.ForeignKey(BRAND, on_delete=models.CASCADE)
    bottle_size = models.ForeignKey(SIZE, on_delete=models.CASCADE)

    def __str__(self):
        return str(self.brand_name) + " | " + str(self.bottle_size) + "L"


class BOTTLE_DETAILS(models.Model):
    bottle = models.ForeignKey(BOTTLE, on_delete=models.CASCADE)
    buy_price = models.DecimalField(max_digits=4, decimal_places=2)
    sell_price = models.DecimalField(max_digits=4, decimal_places=2, null=True)

    def __str__(self):
        return str(self.bottle) + " | " + str(self.buy_price) + "Tk"


class STOCK(models.Model):
    stock_name = models.OneToOneField(BOTTLE_DETAILS, on_delete=models.CASCADE)
    quantity = models.IntegerField()

    def __str__(self):
        return str(self.stock_name)


class HISTORY(models.Model):
    room = models.ForeignKey(ROOM, on_delete=models.CASCADE)
    date = models.DateField()

    def __str__(self):
        return str(self.room) + " " + str(self.date)


class HISTORYDETAIL(models.Model):
    history = models.ForeignKey(HISTORY, on_delete=models.CASCADE)
    bottle_detail = models.ForeignKey(BOTTLE_DETAILS, on_delete=models.CASCADE, default=None)
    quantity = models.IntegerField(null=True)
    notcomplimentary = models.IntegerField(default=1)
    def __str__(self):
        return str(self.history)


