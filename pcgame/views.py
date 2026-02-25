from django.shortcuts import render, redirect
from django.contrib.auth.models import User
from django.contrib import messages
from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login
from django.contrib.auth import logout
from .models import *
from django.shortcuts import render, redirect, get_object_or_404

# Create your views here.

def home(request):
    return render(request,'home.html')


def login_view(request):
    if request.method == "POST":
        username = request.POST.get("username")
        password = request.POST.get("password")

        # Validation: Empty fields
        if not username or not password:
            messages.error(request, "Both fields are required.")
            return redirect("login")

        # Authenticate user
        user = authenticate(request, username=username, password=password)

        if user is not None:
            login(request, user)
            messages.success(request, "Login successful!")

            #  Admin Dashboard Redirection
            if user.is_superuser:
                return redirect("admin_dashboard")
            else:
                return redirect("user_dashboard")

        else:
            messages.error(request, "Invalid username or password.")
            return redirect("login")

    return render(request, "login.html")

def register(request):
    if request.method == "POST":
        username = request.POST.get("username")
        email = request.POST.get("email")
        password1 = request.POST.get("password1")
        password2 = request.POST.get("password2")

        # Check if passwords match
        if password1 != password2:
            messages.error(request, "Passwords do not match.")
            return redirect("register")

        # Check if username already exists
        if User.objects.filter(username=username).exists():
            messages.error(request, "Username already taken.")
            return redirect("register")

        # Check if email already exists
        if User.objects.filter(email=email).exists():
            messages.error(request, "Email already registered.")
            return redirect("register")

        # Create user
        user = User.objects.create_user(
            username=username,
            email=email,
            password=password1
        )

        # Automatically login after registration (optional but professional)
        login(request, user)

        messages.success(request, "Account created successfully!")
        return redirect("login")

    return render(request, "register.html")



def admin_dashboard(request):

    return render(request, "admin_dashboard.html")


def logout_view(request):
    logout(request)
    return redirect("login")


def user_dashboard(request):
    products = PCProduct.objects.all()
    bookings = Booking.objects.filter(user=request.user).order_by('-booked_at')

    context = {
        "products": products,
        "bookings": bookings
    }

    return render(request, "user_dashboard.html", context)



def add_pc_product(request):
    if not request.user.is_superuser and not request.user.is_staff:
        messages.error(request, "You are not authorized.")
        return redirect("user_dashboard")

    categories = Category.objects.all()

    if request.method == "POST":
        category_id = request.POST.get("category")
        product_name = request.POST.get("product_name")
        brand = request.POST.get("brand")
        description = request.POST.get("description")
        price = request.POST.get("price")
        stock = request.POST.get("stock")
        image = request.FILES.get("image")

        if not product_name or not price or not stock:
            messages.error(request, "Please fill all required fields.")
            return redirect("add_pc_product")

        category = Category.objects.get(id=category_id)

        PCProduct.objects.create(
            category=category,
            product_name=product_name,
            brand=brand,
            description=description,
            price=price,
            stock=stock,
            image=image
        )

        messages.success(request, "Product added successfully!")
        return redirect("add_pc_product")

    return render(request, "add_pc_products.html", {"categories": categories})


# 🔹 Product List (Admin + User View)

def product_list(request):
    products = PCProduct.objects.all().order_by("-created_at")
    return render(request, "product_list.html", {"products": products})



def add_category(request):
    if not request.user.is_staff and not request.user.is_superuser:
        messages.error(request, "You are not authorized.")
        return redirect("product_list")

    if request.method == "POST":
        name = request.POST.get("name")

        if not name:
            messages.error(request, "Category name is required.")
            return redirect("add_category")

        if Category.objects.filter(name=name).exists():
            messages.error(request, "Category already exists.")
            return redirect("add_category")

        Category.objects.create(name=name)
        messages.success(request, "Category added successfully!")
        return redirect("add_category")

    return render(request, "add_category.html")


def book_product(request, product_id):
    product = get_object_or_404(PCProduct, id=product_id)

    if request.method == "POST":
        quantity = int(request.POST.get("quantity"))

        if quantity <= product.stock:
            Booking.objects.create(
                user=request.user,
                product=product,
                quantity=quantity
            )

            product.stock -= quantity
            product.save()

            messages.success(request, "Product booked successfully!")
            return redirect("user_dashboard")
        else:
            messages.error(request, "Not enough stock available!")

    return render(request, "book_product.html", {"product": product})


def your_bookings(request):
    bookings = Booking.objects.filter(user=request.user).order_by('-booked_at')

    return render(request, "your_bookings.html", {
        "bookings": bookings
    })


    
    
