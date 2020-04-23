from django.shortcuts import render, redirect, HttpResponse
from django.contrib import messages
from .models import User, Quotes
import bcrypt

def index(request):
    print("you are in the index")
    return render(request,'belt_ex/index.html')

def register_val(request):
    if request.method == "POST":

        errors = User.objects.basic_validator(request.POST)
        if len(errors):
            for key, value in errors.items():
                messages.error(request, value)
            return redirect('/')

        else:
            hashpass = bcrypt.hashpw(request.POST['password'].encode(), bcrypt.gensalt())
            creating_a_user = User.objects.create(fname=request.POST["fname"],lname=request.POST["lname"],email=request.POST["email"],password= hashpass.decode())
            request.session['fname'] = creating_a_user.fname
            request.session['id'] = creating_a_user.id
        return redirect('/register')

def register(request):
    print("you are in the register page")
    return render(request,'belt_ex/register.html')

def home_login(request):

    if request.method == "POST":
        # define variables
        login_user = User.objects.filter(email=request.POST['login_email'])	
        errors = User.objects.login_validator(request.POST)

        # fail stuff
        if len(errors):
            for key, value in errors.items():
                messages.error(request, value)
                print("login didn't work")
                return redirect('/')

        # check for errors (i.e. validate the form)
        if bcrypt.checkpw(request.POST['login_password'].encode(), login_user[0].password.encode()):
            request.session['fname'] = login_user[0].fname
            request.session['id'] = login_user[0].id
            # success stuff
            print("Login was successful")
            return redirect('/login')

    print("you are in the register page")
    return redirect('/')

def home(request):
    print("you are in the quotes page")

    context = {
        'user': User.objects.get(id=request.session['id']),
        'quotes': Quotes.objects.all().order_by('-created_on')
    }

    print("it works")
    return render(request, 'belt_ex/home.html', context)

def logout(request):
    request.session.flush()
    return redirect('/')

def create(request):
    if request.method == "POST":
        errors = Quotes.objects.quotes_validator(request.POST)
        if len(errors):
            for key, value in errors.items():
                messages.error(request, value)
            return redirect("/login")
        else:
            user = User.objects.get(id = request.session['id'])
            Quotes.objects.create(author = request.POST['author'],
                                content = request.POST['content'],
                                posted_by=user),  
    return redirect("/login")

def delete(request, id):
    context = {
        'quotes': Quotes.objects.get(id=id).delete()
    }
    return redirect('/login',context)

def show(request, id):
    user = User.objects.get(id=id)
    context = {
        'quotes':Quotes.objects.filter(posted_by_id=id),
        'user': user
    }
    return render(request,"belt_ex/show.html", context)

def edit(request):

    context = {
        "user":User.objects.get(id=request.session["id"])
    }
    
    return render(request,'belt_ex/edit.html', context)

def create_edit(request):
    errors = User.objects.edit_validator(request.POST)
    user = User.objects.get(id=request.session["id"])
    if len(errors):
        for key, value in errors.items():
            messages.error(request, value)
        return redirect("/edit")
    else:    
        user.fname=request.POST["fname"]
        user.lname=request.POST["lname"]
        user.email=request.POST["email"]
        user.save()
        request.session['fname'] = user.fname       
        return redirect("/login")
# Create your views here.
def likes(request, id):
    this_quote = Quotes.objects.get(id=id)
    this_user = User.objects.get(id=request.session["id"])
    this_quote.users_liked.add(this_user)

    return redirect('/login')