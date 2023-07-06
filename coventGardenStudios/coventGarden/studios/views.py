from datetime import datetime, time

import django.contrib.auth.password_validation
from django.shortcuts import redirect, render, get_object_or_404

# Class-based views
from django.views import View

# Account
from django.contrib.auth import authenticate, login, logout, get_user_model

# Password Reset
from django.contrib.auth.views import (
    PasswordResetView, PasswordResetDoneView, PasswordResetConfirmView, PasswordResetCompleteView)

# Booking
from django.http import JsonResponse
from django.contrib.auth.decorators import login_required, user_passes_test
from datetime import timedelta, datetime, time

# Pro Area
from django.contrib import messages

# Import
from .models import CustomGroup, Event, Concert, TechnicalSheet, CustomUser, Reservation, Salle
from .forms import (
    SignInForm, SignUpForm,
    UserUpdateForm, ConfirmPasswordForm,
    UserPasswordResetForm, UserPasswordSetForm,
    CustomGroupForm, TechnicalSheetForm, ConcertForm,
    EventForm, ReservationForm)

User = get_user_model()

# Create your views here.
"""
Placeholder
"""
def placeholder(request):
    return render(request, 'home.html')


"""
Navigation
    - HomeView
    - NewsView
    - StudiosView
    - ConcertView
    - BarView
    - booking
    - ContactView
"""
class HomeView(View):
    template_name = "home.html"
    context = {
        "title": "Covent Garden"
    }

    def get(self, request):
        return render(request, self.template_name, self.context)


class NewsView(View):
    template_name = "news.html"
    context = {
        "title": "Actualités",
        "breadcrumb": [
            {"view": "home", "name": "Accueil"},
            {"view": None, "name": "Actualités"}]
    }

    def get(self, request):
        return render(request, self.template_name, self.context)


class StudiosView(View):
    template_name = "studios.html"
    context = {
        "title": "Studios",
        "breadcrumb": [
            {"view": "home", "name": "Accueil"},
            {"view": None, "name": "Studios"}]
    }

    def get(self, request):
        return render(request, self.template_name, self.context)


class ConcertView(View):
    template_name = "concert.html"
    context = {
        "title": "Concert",
        "breadcrumb": [
            {"view": "home", "name": "Accueil"},
            {"view": None, "name": "Concert"}]
    }

    def get(self, request):
        return render(request, self.template_name, self.context)


class BarView(View):
    template_name = "bar.html"
    context = {
        "title": "Bar",
        "breadcrumb": [
            {"view": "home", "name": "Accueil"},
            {"view": None, "name": "Bar"}]
    }

    def get(self, request):
        return render(request, self.template_name, self.context)


def booking(request):
    salles = Salle.objects.all()
    return render(request, 'booking.html', context={"salles": salles})


class ContactView(View):
    template_name = "contact.html"
    context = {
        "title": "Contact",
        "breadcrumb": [
            {"view": "home", "name": "Accueil"},
            {"view": None, "name": "Contact"}]
    }

    def get(self, request):
        return render(request, self.template_name, self.context)


"""
Account
    - AccountSignInView
    - AccountSignUpView
    - Log out (Redirect)
"""
class AccountSignInView(View):
    form_class = SignInForm
    template_name = "account/account_sign_in.html"
    context = {
        "title": "Se connecter à son compte",
        "breadcrumb": [
            {"view": "home", "name": "Accueil"},
            {"view": None, "name": "Connexion"}]
    }

    def get(self, request):
        self.context["form"] = self.form_class()
        return render(request, self.template_name, self.context)

    def post(self, request):
        # Form input
        form = self.form_class(request.POST)

        # Success
        if form.is_valid():
            # Form processing
            username = request.POST["username"]
            password = request.POST["password"]

            # Log in the user
            user = authenticate(request, username=username, password=password)
            if user is not None:
                login(request, user)

                # Redirect on success
                return redirect('profile_detail')

            # User not found
            else:
                self.context["form"] = form
                return render(request, self.template_name, self.context)

        # Failure
        else:
            self.context["form"] = form
            return render(request, self.template_name, self.context)


class AccountSignUpView(View):
    form_class = SignUpForm
    template_name = "account/account_sign_up.html"
    context = {
        "title": "Créer un compte",
        "breadcrumb": [
            {"view": "home", "name": "Accueil"},
            {"view": None, "name": "Inscription"}]
    }

    def get(self, request):
        self.context["form"] = self.form_class()
        return render(request, self.template_name, self.context)

    def post(self, request):
        # Form input
        form = self.form_class(request.POST)

        # Success
        if form.is_valid():
            # Form processing
            username = request.POST["username"]
            first_name = request.POST["first_name"]
            last_name = request.POST["last_name"]
            email = request.POST["email"]
            password = request.POST["password"]
            confirm_password = request.POST["confirm_password"]

            print()
            print(django.contrib.auth.password_validation.password_validators_help_texts())

            # Password verification successful
            if password == confirm_password:
                # Create a new user
                user = User.objects.create_user(
                    username=username, email=email, password=password,
                    last_name=last_name, first_name=first_name)
                user.save()

                # Log in the user
                user = authenticate(request, username=username, password=password)
                if user is not None:
                    login(request, user)

                    # Redirect on success
                    return redirect('profile_detail')

            # Password verification failed
            else:
                self.context["form"] = form
                return render(request, self.template_name, self.context)

        # Failure
        else:
            self.context["form"] = form
            return render(request, self.template_name, self.context)


def account_log_out(request):
    logout(request)
    return redirect('account_sign_in')


"""
Password Reset
    - CustomPasswordResetForgot
    - CustomPasswordResetDone
    - CustomPasswordResetConfirm
    - CustomPasswordResetComplete
"""
class CustomPasswordResetForgot(PasswordResetView):
    form_class = UserPasswordResetForm
    template_name = 'password_reset/password_reset_forgot.html'
    email_template_name = 'password_reset/password_reset_email.html'
    extra_context = {
        "title": "Récupérer son compte",
        "breadcrumb": [
            {"view": "home", "name": "Accueil"},
            {"view": None, "name": "Mot de passe oublié"}]
    }


class CustomPasswordResetDone(PasswordResetDoneView):
    template_name = 'password_reset/password_reset_done.html'
    extra_context = {
        "title": "Validation de la demande",
        "breadcrumb": [
            {"view": "home", "name": "Accueil"},
            {"view": "password_reset_forgot", "name": "Mot de passe oublié"},
            {"view": None, "name": "Envoi"}]
    }


class CustomPasswordResetConfirm(PasswordResetConfirmView):
    form_class = UserPasswordSetForm
    template_name = 'password_reset/password_reset_confirm.html'
    extra_context = {
        "title": "Modifier mon mot de passe",
        "breadcrumb": [
            {"view": "home", "name": "Accueil"},
            {"view": "password_reset_forgot", "name": "Mot de passe oublié"},
            {"view": None, "name": "Envoi"},
            {"view": None, "name": "Modifier"}]
    }


class CustomPasswordResetComplete(PasswordResetCompleteView):
    template_name = 'password_reset/password_reset_complete.html'
    extra_context = {
        "title": "Confirmation",
        "breadcrumb": [
            {"view": "home", "name": "Accueil"},
            {"view": "password_reset_forgot", "name": "Mot de passe oublié"},
            {"view": None, "name": "Envoi"},
            {"view": None, "name": "Modifier"},
            {"view": None, "name": "Confirmation"}]
    }


"""
Profile
    - ProfileDetailView
    - ProfileUpdateView
"""
class ProfileDetailView(View):
    template_name = "profile/profile_detail.html"
    context = {
        "title": "Mon compte",
        "breadcrumb": [
            {"view": "home", "name": "Accueil"},
            {"view": None, "name": "Compte"}]
    }

    def get(self, request):
        # Redirect to login page if user is not logged in
        if not request.user.is_authenticated:
            return redirect("account_sign_in")

        return render(request, self.template_name, self.context)


class ProfileUpdateView(View):
    form_class = UserUpdateForm
    form_confirm_class = ConfirmPasswordForm
    template_name = "profile/profile_update.html"
    context = {
        "title": "Modifier mon profil",
        "breadcrumb": [
            {"view": "home", "name": "Accueil"},
            {"view": "profile_detail", "name": "Compte"},
            {"view": None, "name": "Modifier"}],
    }

    def form_class_initial(self):
        initial = {
            "username": self.request.user.username,
            "email": self.request.user.email,
            "last_name": self.request.user.last_name,
            "first_name": self.request.user.first_name
        }
        return initial

    def get(self, request):
        # Redirect to login page if user is not logged in
        if not request.user.is_authenticated:
            return redirect("account_sign_in")

        self.context["form"] = self.form_class(initial=self.form_class_initial())
        self.context["form_confirm"] = self.form_confirm_class()
        return render(request, self.template_name, self.context)

    def post(self, request):
        # Form input
        form = self.form_class(request.POST)
        form_confirm = self.form_confirm_class(request.POST)

        # Success
        if form.is_valid() and form_confirm.is_valid():
            # Password verification successful
            if request.POST["current_password"] == request.POST["confirm_password"]:
                # Form processing
                user = request.user
                user.username = request.POST["username"]
                user.email = request.POST["email"]
                user.last_name = request.POST["last_name"]
                user.first_name = request.POST["first_name"]

                # Update the user
                user.save()

                # Redirect on success
                return redirect('profile_detail')

            # Password verification failed
            else:
                self.context["form"] = form
                self.context["form_confirm"] = form_confirm
                return render(request, self.template_name, self.context)

        # Failure
        else:
            self.context["form"] = form
            self.context["form_confirm"] = form_confirm
            return render(request, self.template_name, self.context)


"""
Groups
    - GroupDetailView
    - GroupCreateView
    - GroupUpdateView
    - GroupDeleteView
"""
class GroupDetailView(View):
    template_name = "groups/groups_detail.html"
    context = {
        "title": "Mes groupes",
        "breadcrumb": [
            {"view": "home", "name": "Accueil"},
            {"view": None, "name": "Groupes"}]
    }

    def get(self, request):
        # Redirect to login page if user is not logged in
        if not request.user.is_authenticated:
            return redirect("account_sign_in")

        self.context["my_groups"] = request.user.my_groups.all()
        return render(request, self.template_name, self.context)


class GroupCreateView(View):
    form_class = CustomGroupForm
    template_name = "groups/groups_create.html"
    context = {
        "title": "Créer un groupe",
        "breadcrumb": [
            {"view": "home", "name": "Accueil"},
            {"view": "groups_detail", "name": "Groupes"},
            {"view": None, "name": "Créer"}]
    }

    def form_class_initial(self):
        initial = {
            "email": self.request.user.email,
            "phone": self.request.user.phone,
        }
        return initial

    def get(self, request):
        # Redirect to login page if user is not logged in
        if not request.user.is_authenticated:
            return redirect("account_sign_in")

        self.context["form"] = self.form_class(initial=self.form_class_initial())
        return render(request, self.template_name, self.context)

    def post(self, request):
        # Form input
        form = self.form_class(request.POST)

        # Success
        if form.is_valid():
            # Associate the current user to the group
            group = form.save(commit=False)
            group.user = request.user

            # Create a new group
            group.save()

            # Redirect on success
            return redirect('groups_detail')

        # Failure
        else:
            self.context["form"] = form
            return render(request, self.template_name, self.context)


class GroupUpdateView(View):
    form_class = CustomGroupForm
    template_name = "groups/groups_create.html"
    context = {
        "title": "Modifier un groupe",
        "breadcrumb": [
            {"view": "home", "name": "Accueil"},
            {"view": "groups_detail", "name": "Groupes"},
            {"view": None, "name": "Modifier"}]
    }

    def get(self, request, group_id):
        # Redirect to login page if user is not logged in
        if not request.user.is_authenticated:
            return redirect("account_sign_in")

        group = CustomGroup.objects.get(id=group_id)
        self.context["form"] = self.form_class(instance=group)
        return render(request, self.template_name, self.context)

    def post(self, request, group_id):
        # Get group object with its id
        group = CustomGroup.objects.get(id=group_id)

        # Form input
        form = self.form_class(request.POST, instance=group)

        # Success
        if form.is_valid():
            # Associate the current user to the group
            group = form.save(commit=False)
            group.user = request.user

            # Create a new group
            group.save()

            # Redirect on success
            return redirect('groups_detail')

        # Failure
        else:
            self.context["form"] = form
            return render(request, self.template_name, self.context)


class GroupDeleteView(View):
    template_name = "groups/groups_delete.html"
    context = {
        "title": "Supprimer un groupe",
        "breadcrumb": [
            {"view": "home", "name": "Accueil"},
            {"view": "groups_detail", "name": "Groupes"},
            {"view": None, "name": "Supprimer"}]
    }

    def get(self, request, group_id):
        # Redirect to login page if user is not logged in
        if not request.user.is_authenticated:
            return redirect("account_sign_in")

        return render(request, self.template_name, self.context)

    def post(self, request, group_id):
        # Redirect to login page if user is not logged in
        if not request.user.is_authenticated:
            return redirect("account_sign_in")

        # Delete the group
        group = CustomGroup.objects.get(id=group_id)
        group.delete()

        # Redirect on success
        return redirect('groups_detail')


"""
Bookings
    - BookingsDetailView
    - BookingsCreateView
"""
class BookingsDetailView(View):
    template_name = "bookings/bookings_detail.html"
    context = {
        "title": "Historique des réservations",
        "breadcrumb": [
            {"view": "home", "name": "Accueil"},
            {"view": None, "name": "Réservations"}]
    }

    def get(self, request):
        # Redirect to login page if user is not logged in
        if not request.user.is_authenticated:
            return redirect("account_sign_in")

        # Get all groups object related to the current user
        self.context["my_groups"] = request.user.my_groups.all()

        # Get all reservations for user
        reservations = Reservation.objects.filter(user_id=request.user.id)
        self.context["reservations"] = reservations

        return render(request, self.template_name, self.context)


class BookingsCreateView(View):
    template_name = "bookings/bookings_create.html"
    context = {
        "title": "Créer une réservation",
        "breadcrumb": [
            {"view": "home", "name": "Accueil"},
            {"view": "bookings_detail", "name": "Réservations"},
            {"view": None, "name": "Créer"}]
    }

    def get(self, request):
        # Redirect to login page if user is not logged in
        if not request.user.is_authenticated:
            return redirect("account_sign_in")

        return render(request, self.template_name, self.context)


"""
Pro area
    - ProAreaView
    - Delete technical sheet
"""
class ProAreaView(View):
    template_name = "pro_area.html"
    context = {
        "title": "Espace Pro",
        "breadcrumb": [
            {"view": "home", "name": "Accueil"},
            {"view": None, "name": "Espace Pro"}]
    }

    def get(self, request):
        # Redirect to login page if user is not logged in
        if not request.user.is_authenticated:
            return redirect("account_sign_in")

        self.context["user_files"] = TechnicalSheet.objects.filter(user=request.user)
        self.context["form"] = TechnicalSheetForm()
        self.context["form2"] = ConcertForm()
        return render(request, self.template_name, self.context)

    def post(self, request):
        self.context["form"] = TechnicalSheetForm(request.POST, request.FILES)
        if self.context["form"].is_valid():
            deposited_files = request.FILES.getlist('pdf_file')
            for file in deposited_files:
                technical_sheet = TechnicalSheet(pdf_file=file, user=request.user)
                technical_sheet.save()
            messages.success(request, 'Vos fiches techniques ont été déposées avec succès !')
            return redirect('pro_area')

        self.context["form2"] = ConcertForm(request.POST)
        if self.context["form2"].is_valid():
            self.context["form2"].save()
            messages.success(request,
                             'Merci pour votre proposition de concert! Un administrateur examinera votre proposition prochainement.',
                             extra_tags='concert_for')
            return redirect('pro_area')


def delete_technical_sheet(request, pk):
    # Log-in required
    if not request.user.is_authenticated:
        technical_sheet = get_object_or_404(TechnicalSheet, pk=pk, user=request.user)
        technical_sheet.delete()
        messages.success(request, 'La fiche technique a été supprimée avec succès !')
        return redirect('pro_area')


"""
Planning
"""
def generate_occurrences(event):
    occurrences = [event.start_time]

    if event.recurrence == 'daily':
        current_time = event.start_time
        while current_time < event.end_time:
            current_time += timedelta(days=1)
            occurrences.append(current_time)

    return occurrences


def add_event(request):
    # Submit form
    if request.method == 'POST':
        form = EventForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('calendar')
    else:
        form = EventForm()
    return render(request, 'create_event.html', {'form': form})


def index(request):
    all_events = Event.objects.all()

    events = []
    for event in all_events:
        occurrences = generate_occurrences(event)
        for occurrence in occurrences:
            events.append({
                'title': event.title,
                'id': event.id,
                'start': occurrence.strftime("%Y-%m-%d %H:%M:%S"),
                'end': occurrence.strftime("%Y-%m-%d %H:%M:%S"),
            })

    context = {
        "events": events,
    }
    return render(request, 'index.html', context)


def all_events(request):
    events = Event.objects.all()
    out = []
    for event in events:
        out.append({
            'title': event.title,
            'id': event.id,
            'start': event.start_time.strftime("%Y-%m-%d %H:%M:%S"),
            'end': event.end_time.strftime("%Y-%m-%d %H:%M:%S"),
        })
    return JsonResponse(out, safe=False)


def update(request):
    start = request.GET.get("start", None)
    end = request.GET.get("end", None)
    title = request.GET.get("title", None)
    id = request.GET.get("id", None)
    event = Event.objects.get(id=id)
    event.start_time = start
    event.end_time = end
    event.title = title
    event.save()
    data = {}
    return JsonResponse(data)


def remove(request):
    id = request.GET.get("id", None)
    event = Event.objects.get(id=id)
    event.delete()
    data = {}
    return JsonResponse(data)


def calendar_view(request):
    events = Event.objects.all()
    context = {'events': events}
    return render(request, 'calendar.html', context)


"""
Salles
    -Listing all Salle
Reservation
    - Listing reservation
"""
def is_in_group(CustomUser):
    return CustomUser.groups.filter(name='Client_Regulier').exists()


def list_salles(request):
    salles = Salle.objects.all()
    salle_data = [{"id": salle.id, "title": salle.name} for salle in salles]
    return JsonResponse(salle_data, safe=False)

def list_users(request):
    users = CustomUser.objects.all()
    user_data = [{"id": user.id, "title": user.username} for user in users]
    return JsonResponse(user_data, safe=False)

@login_required(login_url='account_sign_in')
def accompte(request):

    # Submit form
    if request.method == 'POST':

        salle_id = int(request.POST["salle_id"])
        salle = Salle.objects.get(id= salle_id)

        user_id = int(request.POST["user_id"])
        user = CustomUser.objects.get(id= user_id)

        start_date = request.POST["date_start"]
        end_date = request.POST["date_end"]

        form = ReservationForm()

        duration = datetime.fromisoformat(end_date.rstrip('Z')) - datetime.fromisoformat(start_date.rstrip('Z'))
        duration_seconds = duration.total_seconds()
        duration_hours = duration_seconds / 3600
        print(duration_hours)

        #duration = 1

        if is_in_group(user):
            description = "Reservation for user "+ user.username
            status = "En cours"
            reservation = Reservation.objects.create(
                description=description,
                duration=duration_hours,
                date_start=start_date,
                date_end=end_date,
                price=0,
                status=status,
                salle=salle,
                user=user
            )
            messages.success(request, "Votre réservation a bien été prise en compte !")
            return redirect('booking')

        else:
            return render(request, 'payment.html', {"salle": salle, "user": user, "start_date": start_date,
            "end_date": end_date, "duration": duration_hours, "form": form})

    else:
        return redirect('booking')

@login_required(login_url='account_sign_in')
def payment(request):

    print(request.POST)

    # Submit form
    if request.method == 'POST':

        salle_id = int(request.POST["salle_id"])
        user_id = int(request.POST["user_id"])

        form = ReservationForm(request.POST)

        if form.is_valid():

            salle = Salle.objects.get(id= salle_id)
            user = CustomUser.objects.get(id= user_id)

            description = "Reservation for user "+ user.username
            duration = form.cleaned_data["duration"]
            date_start = form.cleaned_data["date_start"]
            date_end = form.cleaned_data["date_end"]
            price = form.cleaned_data["price"]
            status = "En cours"

            reservation = Reservation.objects.create(
                description=description,
                duration=duration,
                date_start=date_start,
                date_end=date_end,
                price=price,
                status=status,
                salle=salle,
                user=user
            )

            messages.success(request, "Votre réservation a bien été prise en compte !")
            return redirect('booking')

    else:
        return redirect('booking')


def all_booking(request):
    reservations = Reservation.objects.all()
    datas = []
    for current in reservations:
        datas.append({
            'title': current.description,
            'id': current.id,
            'start': current.date_start.strftime("%Y-%m-%d %H:%M:%S"),
            'end': current.date_end.strftime("%Y-%m-%d %H:%M:%S"),
        })
    return JsonResponse(datas, safe=False)


def all_booking_event(request):
    reservations = Reservation.objects.all()
    datas = []
    for current in reservations:
        data = {
            'id': current.id,
            'resourceId': current.salle.id,
            'title': 'Indisponible',
            'start': current.date_start.strftime("%Y-%m-%d %H:%M:%S"),
            'end': current.date_end.strftime("%Y-%m-%d %H:%M:%S"),
        }
        data['color'] = 'gainsboro'
        data['textColor'] = 'black'
        datas.append(data)
    return JsonResponse(datas, safe=False)


from django.shortcuts import render, redirect
from django.conf import settings
from django.contrib.auth.decorators import login_required
from django.views.decorators.csrf import csrf_exempt
from django.http import HttpResponse
from .models import UserPayment
import stripe
import time


@login_required(login_url='login')
def product_page(request):
	stripe.api_key = settings.STRIPE_SECRET_KEY
	if request.method == 'POST':
		checkout_session = stripe.checkout.Session.create(
			payment_method_types = ['card'],
			line_items = [
				{
					'price': settings.PRODUCT_PRICE,
					'quantity': 1,
				},
			],
			mode = 'payment',
			customer_creation = 'always',
			# success_url = settings.REDIRECT_DOMAIN + '/payment_successful?session_id={CHECKOUT_SESSION_ID}',
			# cancel_url = settings.REDIRECT_DOMAIN + '/payment_cancelled',
            success_url = 'http://example.com/payment_successful?session_id={CHECKOUT_SESSION_ID}',
            cancel_url = 'http://example.com/payment_cancelled',
        )
		return redirect(checkout_session.url, code=303)
	return render(request, 'studios/product_page.html')


## use Stripe dummy card: 4242 4242 4242 4242
def payment_successful(request):
	stripe.api_key = settings.STRIPE_SECRET_KEY_TEST
	checkout_session_id = request.GET.get('session_id', None)
	session = stripe.checkout.Session.retrieve(checkout_session_id)
	customer = stripe.Customer.retrieve(session.customer)
	user_id = request.user.user_id
	studios = UserPayment.objects.get(app_user=user_id)
	studios.stripe_checkout_id = checkout_session_id
	studios.save()
	return render(request, 'studios/payment_successful.html', {'customer': customer})


def payment_cancelled(request):
	stripe.api_key = settings.STRIPE_SECRET_KEY_TEST
	return render(request, 'studios/payment_cancelled.html')


@csrf_exempt
def stripe_webhook(request):
	stripe.api_key = settings.STRIPE_SECRET_KEY_TEST
	time.sleep(10)
	payload = request.body
	signature_header = request.META['HTTP_STRIPE_SIGNATURE']
	event = None
	try:
		event = stripe.Webhook.construct_event(
			payload, signature_header, settings.STRIPE_WEBHOOK_SECRET_TEST
		)
	except ValueError as e:
		return HttpResponse(status=400)
	except stripe.error.SignatureVerificationError as e:
		return HttpResponse(status=400)
	if event['type'] == 'checkout.session.completed':
		session = event['data']['object']
		session_id = session.get('id', None)
		time.sleep(15)
		studios = UserPayment.objects.get(stripe_checkout_id=session_id)
		studios.payment_bool = True
		studios.save()
	return HttpResponse(status=200)
