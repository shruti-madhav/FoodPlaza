import datetime
from django.db import connection, transaction
from django.http import JsonResponse
from django.shortcuts import render, HttpResponse, redirect
from . import forms
from .models import Food, Customer, Admin, Cart, Orders, OrderSummary
import pandas as pd
import matplotlib.pyplot as plt

# Create your views here.
# cross site request frogery
# object relational

cursor = connection.cursor()
def home(request):
    return render(request, "home.html")

def addfood(request):
    form = forms.FoodForm()
    if request.method == "POST":
        form = forms.FoodForm(request.POST, request.FILES)
        if form.is_valid():
            try:
                form.save(commit=True)
                return redirect("/menu")
            except:
                return HttpResponse("error")
        else:
            form = forms.FoodForm()
    return render(request, "addfood.html", {"form": form})

def menu(request):
    mainmenu = Food.objects.all()
    return render(request, "menu.html", {"menu": mainmenu})

def update(request, id):
    data = Food.objects.get(foodid=id)
    if request.method == "POST":
        form = forms.FoodForm(request.POST, instance=data)
        if form.is_valid():
            form.save()
            return redirect("/menu")
    return render(request, "update.html", {"data": data})

def delete(request, id):
    data = Food.objects.get(foodid=id)
    data.delete()
    return redirect("/menu")

def allcust(request):
    customers = Customer.objects.all()
    print(customers)
    return render(request, "allcust.html", {"customers": customers})

def addcustomer(request):
    if request.method == "POST":
        custname = request.POST.get("custname")
        custemail = request.POST.get("custemail")
        custpass = request.POST.get("custpass")
        custcont = request.POST.get("custcont")
        custaddress = request.POST.get("custaddress")
        sql = 'insert into Customer(custname,custemail,custpass,custcontact,custaddress) values("%s","%s","%s","%s","%s")'%(custname, custemail, custpass, custcont, custaddress)
        cursor.execute(sql)
        transaction.commit()
        return render(request, "login.html")
    else:
        return rener(request, "register.html")

def updatecust(request, id):
    form = Customer.objects.get(id=id)
    if request.method == "POST":
        form = forms.CustForm(request.POST, instance=form)
        if form.is_valid():
            form.save()
            return redirect("/allcustomers")
    return render(request, "updatecustomer.html", {"form": form})

def deletecust(request, id):
    data = Customer.objects.get(id=id)
    data.delete()
    return redirect("/allcustomers")

def login(request):
    return render(request, "login.html")

def dologin(request):
    if request.method == "POST":
        userid = request.POST.get("userid", "")
        passwd = request.POST.get("passwd", "")
        type = request.POST.get("type", "")
        print("user = ", userid, "pass = ", passwd)
        if type == "User":
            for c in Customer.objects.raw('select * from Customer where custemail="%s" and custpass="%s"' % (userid, passwd)):
                if c.custemail == userid:
                    request.session['userid'] = userid
                    return render(request, 'home.html', {'success': 'Welcome ' + c.custname})
            else:
                return render(request, 'login.html', {'fail': 'login failed'})
        elif type == "Admin":
            for a in Admin.objects.raw('select * from Admin where adminname="%s" and adminpass="%s"' % (userid, passwd)):
                if a.adminname == userid:
                    request.session['adminid'] = userid
                    return render(request, 'home.html', {'success': 'Welcome Admin, ' + a.adminname})
            else:
                return render(request, 'login.html', {'fail': 'login failed'})
    else:
        return render(request, "login.html")

def logout(request):
    session_keys = list(request.session.keys())
    for key in session_keys:
        del request.session[key]
    return render(request, "home.html", {'success': 'you are successfully logged out'})

def register(request):
    return render(request, "register.html")

def addtocart(request):
    fid = int(request.GET.get('foodid', ''))
    data = Food.objects.get(foodid=fid)
    foodprice = data.foodprice
    sql = 'insert into Cart(custemail,fid,foodqnty,total) values("%s","%d","%d","%d")' %(request.session['userid'], fid, 1, foodprice)
    cursor.execute(sql)
    transaction.commit()
    return JsonResponse({'done': 'true'})

def showcart(request):
    data = Cart.objects.raw('select cartid,foodname,foodprice,foodqnty,total from Food as f inner join Cart as c on f.foodid=c.fid where custemail = "%s"' % request.session['userid'])
    return render(request, 'cart.html', {'mycart': data})

def updatequantity(request):
    id = int(request.POST['id'])
    q = int(request.POST.get('q'))
    p = int(request.POST.get('p'))
    s = "update Cart set foodqnty='%d', total='%d' where cartid='%d'" % (q, p, id)
    cursor.execute(s)
    transaction.commit()
    return JsonResponse({'status': True})

def deletecart(request, id):
    data = Cart.objects.get(cartid=id)
    data.delete()
    return redirect("/showcart")

def order(request):
    if request.method == "POST":
        print("hello")
        price = request.POST.getlist('totalperprice')
        q = request.POST.getlist('foodqnt')
        total = request.POST.get('Totalbill', '')
        date = datetime.datetime.now()
        foodid = request.POST.getlist('foodid')
        print(total, "total")
        sql = "insert into Orders(custemail,date,totalbill) values('%s','%s','%s')" %(request.session['userid'],str(date),total)
        cursor.execute(sql)
        #transaction.commit()
        sql1 = "delete from Cart where custemail='%s'" %(request.session['userid'])
        cursor.execute(sql1)
        transaction.commit()
        dta = Orders.objects.filter(custemail = request.session['userid'])
        print("dta ",dta)
        for i in dta:
            Oid = i.orderid
        for i in range(len(foodid)):
            print(foodid, q, price)
            qe = "insert into OrderSummary(fid, odrid, foodquant, price) values('%s','%d','%s','%s')" %(foodid[i],Oid,q[i],price[i])
            cursor.execute(qe)
            transaction.commit()
        if price is '' and q is '':
            return render(request, "home.html", {'success': 'Cart is empty'})
        else:
            orderr = Orders()
            for o in Orders.objects.raw("select * from Orders where custemail='%s' and date='%s'" %(request.session['userid'], str(date))):
                orderr = o
        return render(request, "home.html", {'success': 'order has been placed your Order Id is %s and Total Amount is Rs.%s' %(orderr.orderid, orderr.totalbill)})

def showorder(request):
    orders = Orders.objects.all()
    return render(request, "order.html", {"orders": orders})

def validate_user(request):
    custemail = request.GET.get('custemail', '')
    val = Customer.objects.filter(custemail=custemail).exists()
    if val:
        data = {"is_taken": "true"}
    else:
        data = {"is_taken": "false"}
    return JsonResponse(data)

def changepass(request):
    return render(request, "changepass.html")

def aboutus(request):
    return render(request, "aboutus.html")

def payment(request):
    cartitems = Cart.objects.raw('select cartid,foodname,foodprice,foodqnty,total from Food as f inner join Cart as c on f.foodid=c.fid where custemail = "%s"' % request.session['userid'])
    return render(request, "payment.html", {"cartitems": cartitems})

def updatepassword(request):
    if request.method == "POST":
        oldpass = request.POST.get("old")
        newpass = request.POST.get("new")
        print("user", request.session.keys())
        if request.session.get('userid'):
            sql = "update Customer set custpass='%s' where custpass='%s'" % (newpass, oldpass)
            cursor.execute(sql)
            transaction.commit()
            return redirect("/login")
        elif request.session.get('adminid'):
            sql = "update Admin set adminpass='%s' where adminpass='%s'" % (newpass, oldpass)
            cursor.execute(sql)
            transaction.commit()
            return redirect("/login")
        else:
            pass
    return render(request, "changepass.html")

def myorders(request):
    orders = Orders.objects.raw("select orderid, foodname, foodquant, foodprice, date, price from Food as f inner join OrderSummary as o on f.foodid=o.fid inner join Orders as o1 on o.odrid=o1.orderid where custemail='%s'" %(request.session['userid']))
    print(orders)
    return render(request,"myorder.html",{'myorders':orders})
# select clm1 clm2 from tb1 inner join tb2 on tb1.clm=tb2.clm inner join tb3 on tb3 on tb3.clm=tb2.clm where c
'''
def order(request):
    orderr = Orders()
    if request.method == "POST":
        price = request.POST.get('totalperprice')
        q = request.POST.get('foodqnty')
        total = request.POST.get('Totalbill', '')
        date = datetime.datetime.now()
        print(total, "total")
        sql = "insert into Orders(custemail,date,totalbill) values('%s','%s','%s')" %(request.session['userid'],str(date),total)
        cursor.execute(sql)
        transaction.commit()
        sql1 = "delete from Cart where custemail='%s'" %(request.session['userid'])
        cursor.execute(sql1)
        transaction.commit()
        data = Orders.objects.filter(custemail=request.session['userid'])
        for odetail in data :
            oid = odetail.orderid
        for i in range(len(foodid)):
            sql1 = "insert into OrderSummary(orderid, foodquant, price, foodid value('%s','%s','%s','%s'))" %(oid, q[i], price[i], foodid[i])
            cursor.execute(sql1)
            transaction.commit()
        if price is '' and q is '':
            return render(request, "home.html", {'success': 'Cart is empty'})
        else:
            orderr = Orders()
            for o in Orders.objects.raw("select * from Orders where custemail='%s' and date='%s'" % (request.session['userId'], str(date))):
                orderr = o
    return render(request, "home.html", {'success': 'order has been placed your orderid is "%s" and bill "%s"' % (orderr.orderid, orderr.totalbill)})
'''
def graph(request):
    food=Food.objects.all().count()
    cust=Customer.objects.all().count()
    oder=Orders.objects.all().count()
    amount=Orders.objects.all().values_list('totalbill')
    totalamount=0
    for i in amount:
        for j in i:
            totalamount+=j
    return render(request,"graph.html",{'food':food,'cust':cust,'oder':oder,'totalamount':totalamount})

def graphone(request):
    # customer n no of orders
    orderall = "select orderid,custemail from Orders"
    i = cursor.execute(orderall)
    df = pd.DataFrame(i, columns=["id", "email"])
    cust = df.groupby('email').count().sort_values(by=['email'])
    plt.scatter(cust.index, cust['id'])
    plt.xlabel("Users")
    plt.ylabel("Orders")
    plt.title("User Per Order Plot")
    plt.show()
    return render(request, "graph.html")

def graphtwo(request):
    orderall = "select totalbill,date from Orders"
    i = cursor.execute(orderall)
    df = pd.DataFrame(i, columns=["bill", "date"])
    data = df.groupby('date')['bill'].sum()
    plt.xticks(rotation=7)
    plt.plot(data.index,data)
    plt.title("Date Per Totalbill Plot")
    plt.xlabel("Date")
    plt.ylabel("Totalbill")
    plt.show()
    return render(request,"graph.html")

def graphthree(request):
    orderall = "select custaddress from Customer"
    i = cursor.execute(orderall)
    df = pd.DataFrame(i,columns=["address"])
    data = df.groupby('address')['address'].count()
    plt.pie(data,labels=data.index,autopct='%1.1f%%')
    plt.title("Customer coming from places Plot")
    plt.show()
    return render(request,"graph.html")

def graphfour(request):
    orderall = "select foodcat from Food"
    i = cursor.execute(orderall)
    df = pd.DataFrame(i,columns=["type"])
    data = df.groupby('type')['type'].count()
    plt.bar(data.index, data)
    plt.title("Type of food Plot")
    plt.xlabel("Types")
    plt.ylabel("Numbers")
    plt.show()
    return render(request, "graph.html")