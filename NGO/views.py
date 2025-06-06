from django.shortcuts import render,redirect
from django.contrib.auth import authenticate,login,logout
from django.contrib import messages,auth
from django.contrib.auth.models import User
from .forms import studentform,pledgeform
from django.http import HttpResponseRedirect
from datetime import datetime
from django.views.decorators.csrf import csrf_protect

from .models import pledge,student,totalmoney,estimations,inventory,Donor,expenditure,exphist,Admin

# Create your views here.
def home(request):
    return render(request, 'home.html',{})
def about(request):
    return render(request, 'about.html',{})
@csrf_protect
def adminlogin(request):
    admin=Admin()
    if request.method == "POST":
        username=str(request.POST['username'])
        password=str(request.POST['password'])
        admin.user=authenticate(username=username,password=password)
        
        if admin.user is not None:
                    
            login(request,admin.user)
            messages.success(request,"successfully logged in")
            return render(request,'adminpage.html',{})                
        else:
            messages.success(request,"Please enter correct password")
            return redirect('/adminlogin')

    else:
        if (request.user.is_authenticated and request.user.is_staff):
            return render(request,'adminpage.html',{})
        return render(request,'login_admin.html',{})
def donorlogin(request):
    donor=Donor()
    if request.method == "POST":
        username=str(request.POST['username'])
        password=str(request.POST['password'])
        # print("010")
        donor.user=authenticate(username=username,password=password)
        # print("100")
        if donor.user is not None:
            # print("777")
            login(request,donor.user)
            messages.success(request,"Welcome, you are successfully logged in!!")
            return render(request,'donorpage.html',{})
        else:
            # print("011")
            messages.success(request,"Please enter correct username or password ")
            return redirect('/donorlogin')
    else:
        if (request.user.is_authenticated):
            return render(request,'donorpage.html',{})
        return render(request,'login_donor.html',{})


def donorRegistration(request):
    donor = Donor()
    if request.method == 'POST':
        first_name = request.POST['first_name']
        last_name = request.POST['last_name']
        email_id = request.POST['email_id']
        phone_number = request.POST['phone_number']
        username = request.POST['username']
        address = request.POST['address']
        password1 = request.POST['password1']
        password2 = request.POST['password2']
        
        
        if password1==password2:
            if User.objects.filter(username = username).exists():
                messages.info(request,'Username Already Taken')
                return redirect('/donorRegistration')
            else:
                donor.user = User.objects.create_user(first_name=first_name,last_name=last_name,email = email_id,username=username,password=password1)
                donor.user.save()
                donor.address=address
                donor.phone=phone_number
                donor.save()

                messages.info(request,'User created')
                return redirect('/')

        else:
            messages.info(request,'Password does not match')
            return redirect('/donorRegistration')
    
    else:
        return render(request,'register_donor.html')

def logout(request):
    auth.logout(request)
    return redirect('/')

def donorview(request):
    donors_list=Donor.objects.all()
    return render(request,'donorsview.html',{'donor_list':donors_list})


def addstu(request):
    if ((request.user.is_authenticated) and (request.user.is_staff)):
        if request.method == 'POST':
            new_student = student()
            new_student.fullname=request.POST['fullname']
            new_student.sclass=request.POST['sclass']
            new_student.familyincome=int(request.POST['familyincome'])
            new_student.moneyneeded=request.POST['moneyneeded']
            if "books" in request.POST:
                new_student.books=request.POST['books']
            if "uniform" in request.POST:
                new_student.uniform=request.POST['uniform']
            new_student.performance=float(request.POST['performance'])
            new_student.gender=request.POST['gender']
            new_student.__score__()
            new_student.save()
            messages.info(request,"Student added!")
            return render(request,'adminpage.html')    
        return render(request,'addstudent.html')

def aple(request):
    if (request.user.is_authenticated):
        submitted=False
        if request.method == "POST":
            form=pledgeform(request.POST)
            if form.is_valid():
                dnr=Donor.objects.filter(user=request.user).first()
                pledgeobj=pledge(money=request.POST['money'],books=request.POST['books'],uniform=request.POST['uniform'],frequency=request.POST['frequency'],donor=dnr,status=False,ubstatus=False)#!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
                # pledgeobj.money=form['money']
                # pledgeobj.books=form['books']
                # pledgeobj.uniform=form['uniform']
                # pledgeobj.donor=request.user
                # pledgeobj.status=False
                pledgeobj.time=datetime.now()
                pledgeobj.lastpaid=datetime.now()
                pledgeobj.save()
                messages.info(request,"Done!")
                return HttpResponseRedirect('/aple?submitted=True')
        else:
            form=pledgeform
            if 'submitted' in request.GET:
                submitted=True
        return render(request,'addpledge.html',{'form':form})

def pledgeh(request):
    if ((request.user.is_authenticated) and (request.user.is_staff)):
        Semiannually=pledge.objects.filter(frequency="Semiannually")
        Annually=pledge.objects.filter(frequency="Annually")
        for spledge in Semiannually:
            tyet=(datetime.now().month - spledge.time.month) + 12*(datetime.now().year-spledge.time.year)
            tpyet=(spledge.lastpaid.month - spledge.time.month) + 12*(spledge.lastpaid.year-spledge.time.year)
            months=int(tyet)
            month=int(tpyet)
            mon=(months%12)
            monp=(month%12)
            if (mon>6 & monp<=6) | (mon<=6 & monp>6):
                spledge.status=False
                spledge.save()
        for spledge in Annually:
            tyet=(datetime.now().month - spledge.time.month) + 12*(datetime.now().year-spledge.time.year)
            tpyet=(spledge.lastpaid.month - spledge.time.month) + 12*(spledge.lastpaid.year-spledge.time.year)
            months=int(tyet)
            month=int(tpyet)
            mon=(months%24)
            monp=(month%24)
            if (mon>12 & monp<=12) | (mon<=12 & monp>12):
                spledge.status=False
                spledge.save()
            
        Pledge_list=pledge.objects.all()
        
        return render(request,'Pledgehistory.html',{'pledgelist':Pledge_list})

def viewdonor(request, donor_id):
    donor = Donor.objects.get(id=donor_id)
    return render(request,'donorview.html',{'donor':donor})
def clickub(request, pledge_id):
     if ((request.user.is_authenticated) and (request.user.is_staff)):
        Pledge = pledge.objects.get(pk=pledge_id)
        if Pledge.ubstatus==False:
            Pledge.ubstatus=True
        Pledge.save()
        return redirect('/pledgehist')
def clickp(request, pledge_id):
    if ((request.user.is_authenticated) and (request.user.is_staff)):
        Pledge = pledge.objects.get(pk=pledge_id)
        if Pledge.status==False:
            Pledge.status=True
            Pledge.lastpaid=datetime.now()
            money=int(totalmoney.objects.all().count())
            if money>0:
                # print(money)
                # print("111")
                funds=totalmoney.objects.first()
                funds.Sum=int(Pledge.money)+int(funds.Sum)
                funds.save()
            else:
                # print("222")
                funds=totalmoney(Sum=int(Pledge.money))
                funds.save()
        else:
            Pledge.status=False
        Pledge.save()
        return redirect('/pledgehist')
    
    
    
def delstu(request):
    pass
def editest(request):
    if ((request.user.is_authenticated) and (request.user.is_staff)):
        est_list=estimations.objects.all()

        return render(request,'estimates.html',{'estimationlist':est_list})
def changeestimate(request,row_id):
    if ((request.user.is_authenticated) and (request.user.is_staff)):
        row=estimations.objects.get(pk=row_id)
        if request.method == 'POST':
                row.books=request.POST['book']
                row.uniforms=request.POST['uniform']
                row.save()
        return render(request,'est.html',{'row':row})


def vstats(request):
    if request.user.is_authenticated and request.user.is_staff:
        stu = student.objects.all()
        money_needed = 0
        books_count = [0, 0, 0, 0, 0, 0, 0, 0]
        uniforms_count = [0, 0, 0, 0, 0, 0, 0, 0]
        for stud in stu:
            money_needed += int(stud.moneyneeded)
            sclass = stud.sclass
            if 0 <= sclass < len(books_count):
                books_count[sclass] += 1
            if stud.uniform and 0 <= sclass < len(uniforms_count):
                uniforms_count[sclass] += 1

        for s in range(1, 6):
            inv = inventory.objects.filter(sclass=s).first()
            es = estimations.objects.filter(sclass=s).first()
            if inv and es:
                books_needed = min(books_count[s], inv.books)
                uniforms_needed = min(uniforms_count[s], inv.uniforms)
                money_needed += books_needed * int(es.books) + uniforms_needed * int(es.uniforms)

        funds = totalmoney.objects.first()
        if funds and funds.Sum >= money_needed:
            messages.info(request, "Congrats!! we have enough funds")
        elif funds:
            shortage = money_needed - funds.Sum
            messages.info(request, f"Caution not enough funds!! short by {shortage} Rupees")
        else:
            messages.info(request, "Error: Total funds not available!")

    return render(request, 'workingstats.html', {'money': money_needed, 'totalmoney': funds})

def pref(request):
    pass

def minventory(request):
    if ((request.user.is_authenticated) and (request.user.is_staff)):
        inv=inventory.objects.all()
        
        return render(request,'inventoryview.html',{'inventorylist':inv})
def inven(request,inv_id):
    if ((request.user.is_authenticated) and (request.user.is_staff)):
        inv=inventory.objects.get(pk=inv_id)
        if request.method=='POST':
            inv.books=request.POST['book']
            inv.uniforms=request.POST['uniform']
            inv.save()
        return render(request,'inve.html',{'inven':inv})
def updatetexp(request):
    if ((request.user.is_authenticated) and (request.user.is_staff)):
        money=expenditure.objects.all().count()
        if request.method=='POST':
            m=int(request.POST['money'])
            r=request.POST['reason']
            tam=totalmoney.objects.first()
            if tam.Sum> m:
                tam.Sum=tam.Sum-int(m)
                tam.save()
            else:
                # print("333")
                messages.info(request,'not enough money with NGO')
                return redirect('/addexpend')
            if money>0:
                # print("222")
                texp=expenditure.objects.first()
                texp.exp=texp.exp+int(m)
                texp.save()
            else:
                # print("111")
                texp=expenditure(exp=int(m))
                texp.save()
            t=exphist(expe=int(m),rec=r)
            t.save()
            return redirect('/viewexpenditure')
        return render(request,'update_expenditure.html')

def exph(request):
    if ((request.user.is_authenticated) and (request.user.is_staff)):
        m=expenditure.objects.all().count()
        if m>0:
            # print(m)
            expend=exphist.objects.all()
            money=expenditure.objects.first()
            return render(request,'expenditurehist.html',{'hist':expend,'total':money})
        else:
            # print(m)
            return render(request,'update_expenditure.html')
        
    
    
    
def studentdetails(request):
    students = student.objects.order_by('-score').values()
    
        
    return render(request,'studentlist.html',{'students':students})

def deletestudent(request,student_id):
    if request.method=="GET":
        student.objects.get(id=student_id).delete()
        return redirect(studentdetails)

def modifystudent(request,student_id):
    instance = student.objects.get(id=student_id)
    if request.method == 'POST':
            instance.fullname=request.POST['fullname']
            instance.sclass=request.POST['sclass']
            instance.familyincome=int(request.POST['familyincome'])
            instance.moneyneeded=request.POST['moneyneeded']
            if "books" in request.POST:
                instance.books=request.POST['books']
            if "uniform" in request.POST:
                instance.uniform=request.POST['uniform']
            instance.performance=float(request.POST['performance'])
            instance.gender=request.POST['gender']
            instance.__score__()
            instance.save()
            return redirect(studentdetails)
    return render(request,'modifystudent.html',{'instance':instance,'id':student_id})
    

    