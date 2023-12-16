from django.http import JsonResponse
from django.shortcuts import render, redirect, get_object_or_404
from core.models import General, Social
from order.models import Order, OrderItem
from catalog.models import Product, Category
from .forms import NewUserForm, SetPasswordForm, AddressForm, RegistrationForm
from django.contrib.auth import login, authenticate, logout
from django.contrib import messages
from django.contrib.auth.forms import AuthenticationForm  # add this
from django.contrib.auth.decorators import login_required
import json
from .models import  Address, City,PendingUser
from django.contrib.auth import get_user_model

from django.contrib.auth import update_session_auth_hash
from django.http import HttpResponse,HttpResponseBadRequest

from django.db import IntegrityError



CustomUser = get_user_model()

def signin(request):
    main_categories = Category.objects.filter(parent=None)

    if request.user_agent.is_mobile:
        if request.method == "POST":
            form = AuthenticationForm(request, data=request.POST)
            if form.is_valid():
                username = form.cleaned_data.get('username')
                password = form.cleaned_data.get('password')
                remember_me = request.POST.get('remember_me')

                user = authenticate(request, username=username, password=password)

                if user is not None:
                    if user.is_active:
                        login(request, user)

                        if not remember_me:
                            request.session.set_expiry(0)

                        messages.info(request, f"You are now logged in as {username}.")
                        return redirect("profile")
                    else:
                        return render(request, 'mobile/account/pending.html')
                else:
                    messages.error(request, "Invalid username or password.")
            else:
                messages.error(request, "Invalid username or password.")
                form = AuthenticationForm()
                context = {
                    "login_form": form,
                    "failed": True,
                    'main_categories': main_categories,
                }
                return render(request, 'mobile/account/login.html', context)

        form = AuthenticationForm()
        context = {
            "login_form": form,
            'main_categories': main_categories,
        }
        return render(request, 'mobile/account/login.html', context)
    
    else:
        if request.method == "POST":
            form = AuthenticationForm(request, data=request.POST)
            if form.is_valid():
                username = form.cleaned_data.get('username')
                password = form.cleaned_data.get('password')
                user = authenticate(request, username=username, password=password)

                if user is not None:
                    if user.is_active:
                        login(request, user)
                        messages.info(request, f"You are now logged in as {username}.")
                        return redirect("profile")
                    else:
                        return render(request, 'desktop/account/pending.html')
                else:
                    messages.error(request, "Invalid username or password.")
            else:
                messages.error(request, "Invalid username or password.")
                form = AuthenticationForm()
                context = {
                    "login_form": form,
                    "failed": True,
                    'main_categories': main_categories,
                }
                return render(request, 'desktop/account/signin.html', context)

        form = AuthenticationForm()
        context = {
            "login_form": form,
            'main_categories': main_categories,
        }
        return render(request, 'desktop/account/signin.html', context)
    

def signup(request):
    if request.user_agent.is_mobile:
        main_categories = Category.objects.filter(parent=None)

        if request.user.is_authenticated:
            return render(request, 'mobile/account/profile.html')  

        if request.method == "POST":
            form = RegistrationForm(request.POST)
            if form.is_valid():
                username = form.cleaned_data['username']
                email = form.cleaned_data['email']
                password = form.cleaned_data['password1']


                # Check if username (VOEN) or email already exists
                if CustomUser.objects.filter(username=username).exists() or PendingUser.objects.filter(user__username=username).exists():
                    messages.error(request, "Username is already in use.")
                elif CustomUser.objects.filter(email=email).exists():
                    messages.error(request, "Email address is already in use.")
                else:
                    user = CustomUser.objects.create_user(
                        username=username,
                        password=password,
                        email=email,
                        account_type='P',
                        just_registered=True,
                        first_name=form.cleaned_data['first_name'],
                        telephone=form.cleaned_data['telephone'],
                        name=form.cleaned_data['name'], 
                    )

                    user.save()

                    PendingUser.objects.create(user=user)

                    messages.success(request, "Registration successful. Admin approval required.")
                    request.session['just_registered'] = True

                    return render(request, 'mobile/account/pending.html')

            messages.error(request, "Yazdığınız VÖEN artıq istifadə olunub.")
        else:
            form = RegistrationForm()

        context = {
            "register_form": form,
            'main_categories': main_categories,
            'just_registered': request.session.pop('just_registered', False),
        }
        return render(request, 'mobile/account/register.html', context)
    else:
        main_categories = Category.objects.filter(parent=None)

        if request.user.is_authenticated:
            return render(request, 'desktop/account/profile.html')  # Change to your profile page

        if request.method == "POST":
            form = RegistrationForm(request.POST)
            if form.is_valid():
                username = form.cleaned_data['username']
                email = form.cleaned_data['email']
                password = form.cleaned_data['password1']

                if CustomUser.objects.filter(username=username, account_type='P').exists():
                    messages.error(request, "VÖEN artıq istifadə olunur.")
                elif CustomUser.objects.filter(email=email).exists():
                    messages.error(request, "E-poçt artıq istifadə olunur.")
                else:
                    user = CustomUser.objects.create_user(
                        username=username,
                        password=password,
                        email=email,
                        account_type='P',
                        just_registered=True,
                        first_name=form.cleaned_data['first_name'],
                        telephone=form.cleaned_data['telephone'],
                        name=form.cleaned_data['name'], 
                    )

                    user.save()

                    PendingUser.objects.create(user=user)

                    messages.success(request, "Qeydiyyat uğurlu oldu. Admin təsdiqi tələb olunur.")
                    request.session['just_registered'] = True

                    return render(request, 'desktop/account/waiting.html')

            messages.error(request, "Yazdığınız VÖEN artıq istifadə olunub.")
        else:
            form = RegistrationForm()

        context = {
            "register_form": form,
            'main_categories': main_categories,
            'just_registered': request.session.pop('just_registered', False),
        }
        return render(request, 'desktop/account/signup.html', context)



def createaccount(request):
    main_categories = Category.objects.filter(parent=None)

    if request.user.is_authenticated:
        return redirect("profile")

    if request.method == "POST":
        form = RegistrationForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data['username']
            email = form.cleaned_data['email']
            password = form.cleaned_data['password1']

            if CustomUser.objects.filter(username=username).exists() or PendingUser.objects.filter(user__username=username).exists():
                messages.error(request, "Username is already in use.")
                return redirect("signup")

            if CustomUser.objects.filter(email=email).exists():
                messages.error(request, "Email address is already in use.")
                return redirect("signup")

            user = CustomUser.objects.create_user(
                username=username,
                password=password,
                email=email,
                account_type='P',
                just_registered=True,
                first_name=form.cleaned_data['first_name'],
                telephone=form.cleaned_data['telephone'],
                name=form.cleaned_data['name'], 
            )

            PendingUser.objects.create(user=user)
            
            messages.success(request, "Qeydiyyat uğurlu oldu. Admin təsdiqi tələb olunur.")
            request.session['just_registered'] = True

            return render(request, 'mobile/account/pending.html')

        messages.error(request, "Yazdığınız VÖEN artıq istifadə olunub.")
    else:
        form = RegistrationForm()

    context = {
        "register_form": form,
        'main_categories': main_categories,
        'just_registered': request.session.pop('just_registered', False),
    }
    return render(request, 'mobile/account/register.html', context)



def waiting(request):
    
    return render(request, 'desktop/account/waiting.html')

def pending(request):
    
    return render(request, 'mobile/account/pending.html')


def logout_request(request):
    logout(request)
    messages.info(request, "Uğurla çıxış etdiniz.")
    return redirect("index")


@login_required(login_url='/account/signin/')
def profile(request):
    general = General.objects.last()
    socials = Social.objects.all()
    cats = Category.objects.filter(is_active=True)
    total_orders = Order.objects.filter(customer=request.user, is_ordered=True).count()
    
    pending_orders = Order.objects.filter(status='PE', customer=request.user, is_ordered=True).count()
    addresses = Address.objects.filter(customer=request.user)
    main_categories = Category.objects.filter(parent=None)
    main_address = Address.objects.filter(customer=request.user, is_selected=True).last()
    orders = Order.objects.filter(customer=request.user, is_ordered=True)[:3]

    order_in_cart = Order.objects.filter(customer=request.user, is_ordered=False).last()
        

    cart = None
    if request.user.is_authenticated:
        cart = Order.objects.filter(customer=request.user, is_ordered=False).last()
    cart_sum = 0
    if request.user.is_authenticated:
        addresses = Address.objects.filter(customer=request.user)
        if not main_address and addresses:
            main_address = addresses.last()
        order = Order.objects.filter(is_ordered=False, customer=request.user).last()
        if order:
            for o in order.items.all():
                cart_sum = cart_sum + o.quantity * o.product.prices.last().price


    if request.method == "POST":
        type_of_request = request.POST.get('type', '')

        if type_of_request == "addaddress":
            # Check the number of existing addresses
            existing_addresses_count = Address.objects.filter(customer=request.user).count()

            # Limit the user to a maximum of 4 addresses
            if existing_addresses_count >= 4:
                messages.warning(request, 'You can only add up to 4 addresses.')
                return redirect('profile')

            form = AddressForm(request.POST)
            if form.is_valid():
                # Check if the same address already exists for the user
                existing_address = Address.objects.filter(
                    customer=request.user,
                    city=form.cleaned_data['city'],
                    street=form.cleaned_data['street'],
                    building=form.cleaned_data['building'],
                    zip=form.cleaned_data['zip'],
                    note=form.cleaned_data['note'],
                ).first()

                if existing_address:
                    messages.warning(request, 'Address already exists.')
                else:
                    new_address = form.save(commit=False)
                    new_address.customer = request.user
                    new_address.save()
                    messages.success(request, 'Address added successfully.')
                
                return redirect('profile')
            else:
                messages.error(request, 'Error adding the address. Please check the form.')

        if type_of_request == "editaddress":
            address_id = request.POST.get('address_id', '')
            address_instance = get_object_or_404(Address, id=address_id, customer=request.user)

            form = AddressForm(request.POST, instance=address_instance)
            if form.is_valid():
                form.save()
                messages.success(request, 'Address updated successfully.')
                return redirect('profile')
            else:
                messages.error(request, 'Error updating the address. Please check the form.')

       
    if request.method == "POST":
        form = AddressForm(request.POST)
        if form.is_valid():
            new_address = form.save(commit=False)
            new_address.customer = request.user
            new_address.save()
            return redirect('profile')  # Redirect to the profile page after adding the address
    else:
        form = AddressForm()

         # Determine the template based on the user's agent
    template_name = 'desktop/account/dashboard.html'
    if request.user_agent.is_mobile:
        template_name = 'mobile/account/dashboard.html'

    context = {
        "socials": socials,
        "general": general,
        "cats": cats,
        "main_categories": main_categories,
        'cart': cart,
        'cart_sum': cart_sum,
        'addresses': addresses,
        'main_address': main_address,
        'orders': orders,
        'total_orders':total_orders,
        'pending_orders' : pending_orders,
        "order_in_cart": order_in_cart,
        'form': form,

    }
    
    return render(request, template_name, context)


@login_required(login_url='/account/signin/')
def mobile_order_history(request):
    # Reuse the logic from the existing 'profile' view
    general = General.objects.last()
    socials = Social.objects.all()
    cats = Category.objects.filter(is_active=True)
    total_orders = Order.objects.filter(customer=request.user, is_ordered=True).count()
    addresses = Address.objects.filter(customer=request.user)
    main_categories = Category.objects.filter(parent=None)
    orders = Order.objects.filter(customer=request.user, is_ordered=True)
    order_in_cart = Order.objects.filter(customer=request.user, is_ordered=False).last()

    # Determine the template based on the user's agent
    template_name = 'mobile/account/order.html'

    context = {
        "socials": socials,
        "general": general,
        "cats": cats,
        "main_categories": main_categories,
        'addresses': addresses,
        'orders': orders,
        'total_orders': total_orders,
        "order_in_cart": order_in_cart,
    }

    return render(request, template_name, context)

def change_password(request):
    if request.method == 'POST':
        old_password = request.POST.get('old_password')
        new_password = request.POST.get('new_password')
        confirm_password = request.POST.get('confirm_password')

        user = request.user

        if not user.check_password(old_password):
            return HttpResponseBadRequest("Eski şifre yanlış.")

        if new_password != confirm_password:
            return HttpResponseBadRequest("Yeni şifreler eşleşmiyor.")

        user.set_password(new_password)
        user.save()

        update_session_auth_hash(request, user)

        return redirect('profile')

    return HttpResponseBadRequest("Geçersiz istek.")

@login_required(login_url='/account/signin/')
def manage_address(request):
    addresses = Address.objects.filter(customer=request.user)

    if request.method == 'POST':
        type_of_request = request.POST.get('type', '')

        if type_of_request == 'addaddress':
            existing_addresses_count = Address.objects.filter(customer=request.user).count()

            if existing_addresses_count >= 4:
                messages.warning(request, 'You can only add up to 4 addresses.')
                return redirect('manage_address')

            form = AddressForm(request.POST)
            if form.is_valid():
                existing_address = Address.objects.filter(
                    customer=request.user,
                    city=form.cleaned_data['city'],
                    street=form.cleaned_data['street'],
                    building=form.cleaned_data['building'],
                    zip=form.cleaned_data['zip'],
                    note=form.cleaned_data['note'],
                ).first()

                if existing_address:
                    messages.warning(request, 'Address already exists.')
                else:
                    new_address = form.save(commit=False)
                    new_address.customer = request.user
                    new_address.save()
                    messages.success(request, 'Address added successfully.')

                return redirect('manage_address')
            else:
                messages.error(request, 'Error adding the address. Please check the form.')

    else:
        form = AddressForm()

    return render(request, 'mobile/account/manage-address.html', {'addresses': addresses, 'form': form})


@login_required(login_url='/account/signin/')
def new_address(request):
    # Mevcut kodları buraya ekle...

    if request.method == 'POST':
        form = AddressForm(request.POST)
        if form.is_valid():
            existing_addresses_count = Address.objects.filter(customer=request.user).count()

            if existing_addresses_count >= 4:
                messages.warning(request, 'You can only add up to 4 addresses.')
                return redirect('manage_address')  

            new_address = form.save(commit=False)
            new_address.customer = request.user
            new_address.save()
            return redirect('manage_address') 
    else:
        form = AddressForm()

    return render(request, 'mobile/account/new-address.html', {'form': form})


@login_required(login_url='/account/signin/')
def edit_profile(request):
    if request.method == 'POST':
        user = request.user
        new_email = request.POST.get('email', '')
        if new_email != user.email:
            
            if CustomUser.objects.filter(email=new_email).exclude(id=user.id).exists():
                messages.error(request, 'Email already exists. Please choose a different one.')
                return redirect('profile')

        user.email = new_email
        user.first_name = request.POST.get('first_name', '')
        user.telephone = request.POST.get('telephone', '')
        try:
            user.save()
            messages.success(request, 'Profile updated successfully.')
        except IntegrityError as e:
            messages.error(request, 'Error updating the profile. Please try again.')
            
            print(f"IntegrityError in edit_profile: {e}")

        return redirect('profile')

    if request.user_agent.is_mobile:
        
        return redirect('profile')



@login_required(login_url='/account/signin/')
def profile_setting(request):
    return render(request, 'mobile/account/profile-edit.html')



@login_required(login_url='/account/signin/')
def orders(request):
    addresses = None
    main_categories = Category.objects.filter(parent=None)
    orders = Order.objects.filter(customer=request.user, is_ordered=True)
    cart = None
    if request.user.is_authenticated:
        cart = Order.objects.filter(customer=request.user, is_ordered=False).last()
    cart_sum = 0
    if request.user.is_authenticated:
        addresses = Address.objects.filter(customer=request.user)

        order = Order.objects.filter(is_ordered=False, customer=request.user).last()
        if order:
            for o in order.items.all():
                cart_sum = cart_sum + o.quantity * o.product.prices.last().price


    context = {
        "main_categories": main_categories,
        'cart': cart,
        'cart_sum': cart_sum,
        'addresses': addresses,
        'orders': orders,

    }
    return render(request, 'desktop/account/orders.html', context)


@login_required(login_url='/account/signin/')
def order(request, id):
    general = General.objects.last()
    socials = Social.objects.all()

    order_detail = Order.objects.get(pk=id)
    if request.user.id != order_detail.customer.id:
        order_detail = None
    cats = Category.objects.filter(is_active=True)
    ord = Order.objects.filter(pk=id,customer=request.user).last()
    orders = Order.objects.filter(customer=request.user, is_ordered=True)[:3]
    addresses = None
    main_categories = Category.objects.filter(parent=None)
    cart = None
    if request.user.is_authenticated:
        cart = Order.objects.filter(customer=request.user, is_ordered=False).last()
    cart_sum = 0
    if request.user.is_authenticated:
        addresses = Address.objects.filter(customer=request.user)

        order = Order.objects.filter(is_ordered=False, customer=request.user).last()
        if order:
            for o in order.items.all():
                cart_sum = cart_sum + o.quantity * o.product.prices.last().price




    context = {
        "main_categories": main_categories,
        'cart': cart,
        'cart_sum': cart_sum,
        'addresses': addresses,
        'order': ord,
        'general': general,
        'socials': socials,
        "cats": cats,
        "order_detail": order_detail,

    }
    return render(request, 'mobile/account/order.html', context)


@login_required(login_url='/account/signin/')
def infos(request):
    addresses = None
    main_categories = Category.objects.filter(parent=None)



    cart = None
    if request.user.is_authenticated:
        cart = Order.objects.filter(customer=request.user, is_ordered=False).last()
    cart_sum = 0
    if request.user.is_authenticated:
        addresses = Address.objects.filter(customer=request.user)

        order = Order.objects.filter(is_ordered=False, customer=request.user).last()
        if order:
            for o in order.items.all():
                cart_sum = cart_sum + o.quantity * o.product.prices.last().price

    if request.method == "POST" and request.POST.get('isitsearch') == "1":
        print("seaaaaaaaaaarch")
        search = request.POST.get('search')
        search_products = Product.objects.filter(name__icontains=search)

        context = {
            'main_categories': main_categories,
            'cart': cart,
            'cart_sum': cart_sum,
            'search_products': search_products,
            'addresses': addresses,

        }

        return render(request, 'desktop/page/search.html', context)


    if request.method == "POST" and request.POST.get('edit') == "1":
        first_name = request.POST.get('first_name')
        last_name = request.POST.get('last_name')
        email = request.POST.get('email')
        request.user.first_name = first_name
        request.user.last_name = last_name
        request.user.email = email
        request.user.save()


    context = {
        "main_categories": main_categories,
        'cart': cart,
        'cart_sum': cart_sum,
        'addresses': addresses,

    }
    return render(request, 'account/infos.html', context)


@login_required(login_url='/account/signin/')
def foryou(request):
    main_categories = Category.objects.filter(parent=None)
    context = {
        "main_categories": main_categories,
    }
    return render(request, 'account/foryou.html', context)


@login_required(login_url='/account/signin/')
def neocard(request):
    main_categories = Category.objects.filter(parent=None)
    context = {
        "main_categories": main_categories,
    }
    return render(request, 'account/neocard.html', context)


@login_required(login_url='/account/signin/')
def addresses(request):
    addresses = None
    main_categories = Category.objects.filter(parent=None)
    cart = None
    if request.user.is_authenticated:
        cart = Order.objects.filter(customer=request.user, is_ordered=False).last()
    cart_sum = 0
    if request.user.is_authenticated:
        addresses = Address.objects.filter(customer=request.user)
        order = Order.objects.filter(is_ordered=False, customer=request.user).last()
        if order:
            for o in order.items.all():
                cart_sum = cart_sum + o.quantity * o.product.prices.last().price

    if request.method == "POST" and request.POST.get('isitsearch') == "1":
        print("seaaaaaaaaaarch")
        search = request.POST.get('search')
        search_products = Product.objects.filter(name__icontains=search)

        context = {
            'main_categories': main_categories,
            'cart': cart,
            'cart_sum': cart_sum,
            'search_products': search_products,
            'addresses': addresses,
        }

        return render(request, 'desktop/page/search.html', context)


    if request.method == "POST" and request.POST.get('remove') == "1":
        address_id = request.POST.get('address_id')
        addr = Address.objects.get(pk=address_id)
        addr.delete()

        context = {
            'main_categories': main_categories,
            'cart': cart,
            'cart_sum': cart_sum,
            'addresses': addresses,
        }

        return render(request, 'account/addresses.html', context)
    context = {
        "main_categories": main_categories,
        'cart': cart,
        'cart_sum': cart_sum,
        'addresses': addresses,
    }
    return render(request, 'account/addresses.html', context)




@login_required(login_url='/account/signin/')
def addresses_edit(request, id):
    address = Address.objects.filter(pk=id, customer=request.user).last()
    addresses = None
    cities = City.objects.all()
    main_categories = Category.objects.filter(parent=None)
    cart = None
    if request.user.is_authenticated:
        addresses = Address.objects.filter(customer=request.user)
        cart = Order.objects.filter(customer=request.user, is_ordered=False).last()
    cart_sum = 0
    if request.user.is_authenticated:
        order = Order.objects.filter(is_ordered=False, customer=request.user).last()
        if order:
            for o in order.items.all():
                cart_sum = cart_sum + o.quantity * o.product.prices.last().price

    if request.method == "POST" and request.POST.get('isitsearch') == "1":
        search = request.POST.get('search')
        search_products = Product.objects.filter(name__icontains=search)

        context = {
            'main_categories': main_categories,
            'address': address,
            'addresses': addresses,
            'cities': cities,
            'cart': cart,
            'cart_sum': cart_sum,
            'search_products': search_products,
        }

        return render(request, 'desktop/page/search.html', context)


    if request.method == "POST" and request.POST.get('edit') == "1":
        name = request.POST.get('name')
        cty = request.POST.get('city')
        street = request.POST.get('street')
        building = request.POST.get('building')
        apartment = request.POST.get('apartment')
        blok = request.POST.get('blok')
        blok_code = request.POST.get('blok_code')
        phone = request.POST.get('phone')
        default = request.POST.get('default')
        city = City.objects.get(pk=int(cty))

        address.name = name
        address.street = street
        address.city = city
        address.building = building
        address.apartment = apartment
        address.blok = blok
        address.blok_code = blok_code
        address.phone = phone
        address.save()
        if default == "on":
            addresses_all = Address.objects.filter(customer=request.user)
            for a in addresses_all:
                a.is_selected = False
                a.save()
            address.is_selected = True
            address.save()

        context = {
            'main_categories': main_categories,
            'cart': cart,
            'cart_sum': cart_sum,
            'addresses': addresses,
        }

        return render(request, 'account/addresses.html', context)
    context = {
        "main_categories": main_categories,
        'addresses': addresses,
        'cart': cart,
        'cart_sum': cart_sum,
        'address': address,
        'cities': cities,
    }
    return render(request, 'account/addresses_edit.html', context)


@login_required(login_url='/account/signin/')
def addresses_add(request):
    if request.method == 'POST':
        form = AddressForm(request.POST)
        if form.is_valid():
            # Save the form data to the database or perform other actions
            form.save()
    else:
        form = AddressForm()

    return render(request, 'desktop/account/dashboard.html', {'form': form})


@login_required(login_url='/account/signin/')
def password(request):
    addresses = None
    main_categories = Category.objects.filter(parent=None)
    cart = None
    if request.user.is_authenticated:
        cart = Order.objects.filter(customer=request.user, is_ordered=False).last()
    cart_sum = 0
    if request.user.is_authenticated:
        addresses = Address.objects.filter(customer=request.user)
        order = Order.objects.filter(is_ordered=False, customer=request.user).last()
        if order:
            for o in order.items.all():
                cart_sum = cart_sum + o.quantity * o.product.prices.last().price

    if request.method == "POST" and request.POST.get('isitsearch') == "1":
        print("seaaaaaaaaaarch")
        search = request.POST.get('search')
        search_products = Product.objects.filter(name__icontains=search)

        context = {
            'main_categories': main_categories,
            'cart': cart,
            'cart_sum': cart_sum,
            'search_products': search_products,
            'addresses': addresses,
        }

        return render(request, 'desktop/page/search.html', context)


    if request.method == "POST" and request.POST.get('edit') == "1":
        form = SetPasswordForm(request.user, request.POST)
        if form.is_valid():
            form.save()
            user = authenticate(username=request.user.username, password=request.POST.get('new_password1'))
            if user is not None:
                login(request, user)
                return redirect("profile")
        else:
            for error in list(form.errors.values()):
                messages.error(request, error)


    context = {
        "main_categories": main_categories,
        'cart': cart,
        'cart_sum': cart_sum,
        'addresses': addresses,
    }
    return render(request, 'account/password.html', context)



@login_required(login_url='/account/signin/')
def change_item(request):
    if request.method == 'POST':

        if request.user.is_authenticated:
            item_id = int(request.POST.get('item_id'))
            qty = int(request.POST.get('qty'))
            item = OrderItem.objects.get(pk=item_id)
            item.quantity = qty
            item.save()
            resp = {"total":item.total_price,"grand": item.order.get_cart_total,"id":item.id}


        return JsonResponse(resp, status=201)
    
    
@login_required(login_url='/account/signin/')
def select_address(request):
    if request.method == 'POST':
        if request.user.is_authenticated:
            address_id = request.POST.get('id')
            address = Address.objects.get(id=address_id)
            addresses = Address.objects.filter(customer=request.user)
            for a in addresses:
                a.is_selected = False
                a.save()
            address.is_selected = True
            address.save()
            resp = {}

        return JsonResponse(resp, status=201)



