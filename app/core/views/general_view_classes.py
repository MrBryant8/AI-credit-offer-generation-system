import markdown
from django.http import HttpResponseForbidden, JsonResponse
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages as msg
from django.contrib.auth import authenticate, login, logout, update_session_auth_hash
from django.contrib.messages import get_messages
from django.contrib.auth.views import  PasswordChangeView
from django.urls import reverse_lazy, reverse
from django.views import View
from django.views.decorators.csrf import csrf_exempt, csrf_protect
from django.views.generic import FormView, DetailView, UpdateView, ListView
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.utils.safestring import mark_safe
from django.conf import settings
from rest_framework.utils import json
from ..forms import *
from ..utils.utils import *
from django.core.paginator import Paginator
from .agents.crew import EmailCrew


# Static Pages
class LandingPageView(View):
    def get(self, request):
        return render(request, 'index.html')


class HomePageView(View):
    def get(self, request):
        return render(request, 'home.html')

class MoreInfoView(View):
    template_name = "footer/info.html"
    def get(self, request, *args, **kwargs):
        return render(request, self.template_name)

class ContactView(View):
    template_name = "footer/contact.html"
    def get(self, request, *args, **kwargs):
        return render(request, self.template_name)


class CarrersView(View):
    template_name = "footer/careers.html"
    def get(self, request, *args, **kwargs):
        return render(request, self.template_name)


class DataPrivacyView(View):
    template_name = "footer/privacy.html"
    def get(self, request, *args, **kwargs):
        return render(request, self.template_name)


# Login/Logout/Register
class LoginPageView(FormView):
    def get(self, request):
        return render(request, 'login.html')

    def post(self, request):
        form = UserLoginForm(request.POST)
        error_message = None
        if form.is_valid():
            email = form.cleaned_data['email']
            password = form.cleaned_data['password']
            user = authenticate(email=email, password=password)

            if user and user.is_active:
                login(request, user)
                return redirect('/home')
            else:
                error_message = 'Invalid user.'

        return render(request, 'login.html', {'error_message': error_message})


def logout_view(request):
    logout(request)
    return redirect('/')


class SignUpPageView(FormView):
    def get(self, request):
        return render(request, 'sign-up.html')

    def post(self, request):
        form = UserRegisterForm(request.POST)
        error_message = None
        if form.is_valid():
            first_name = form.cleaned_data['first_name']
            last_name = form.cleaned_data['last_name']
            email = form.cleaned_data['email']
            password = form.cleaned_data['password']
            
            if not email.endswith("smartcredit.com"):
                error_message = "Only Smart Credit Employees are allowed to register."
    
            else: 
                try:
                    user = add_new_user(first_name=first_name, last_name=last_name, email=email, password=password)
                    login(request, user)
                    return redirect('/home', )
                except Exception as e:
                    error_message = str(e)

        return render(request, 'sign-up.html', {'error_message': error_message})


class CustomPasswordChangeView(PasswordChangeView, LoginRequiredMixin):
    form_class = CustomPasswordChangeForm
    template_name = 'registration/password_change_form.html'
    success_url = reverse_lazy('home')

    def form_valid(self, form):
        user = form.save()

        subject = "SmartCredit - password change"
        body = f"Hello {user.get_full_name()},\n\nYour password was successfully changed.\n\nBest regards, Smart Credit Team"

        send_email(user.email, subject, body)

        update_session_auth_hash(self.request, user)
        msg.success(self.request, 'Your password was successfully updated!')

        return super().form_valid(form)

# Customer Core
class MyOffersView(LoginRequiredMixin, View):
    login_url = '/login'

    def get(self, request):
        credit_offers = fetch_credit_offers_per_user(user_id=request.user.id)
        return render(request, 'my-offers.html', {'credit_offers': credit_offers})


class CreditOfferDetailView(LoginRequiredMixin, DetailView):
    login_url = '/login'
    model = CreditOffer
    template_name = 'offer-detail.html'
    context_object_name = 'offer'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        offer = context['offer']
        context['expiry_date'] = offer.created_at + timedelta(weeks=1)

        storage = get_messages(self.request)
        messages_list = list(storage)
        context['last_message'] = messages_list[-1] if messages_list else None

        return context
    
class AcceptOfferView(LoginRequiredMixin, View):
    login_url = "/login"

    def post(self, request, pk):
        offer = get_object_or_404(CreditOffer, pk=pk)

        if not offer.client or offer.client.user != request.user:
            msg.error(request, "You do not have the authorization to accept the offer.")
            return redirect('offer_detail', pk=pk)

        if offer.is_accepted is True:
            msg.info(request, "This offer is already accepted.")
        else:
            offer.is_accepted = True
            if offer.is_draft:
                offer.is_draft = False
            offer.save()
            msg.success(request, "You have accepted this offer.")

        return redirect('offer_detail', pk=pk)


class RejectOfferView(LoginRequiredMixin, View):
    login_url = "/login"

    def post(self, request, pk):
        offer = get_object_or_404(CreditOffer, pk=pk)

        if not offer.client or offer.client.user != request.user:
            msg.error(request, "You do not have the authorization to reject the offer.")
            return redirect('offer_detail', pk=pk)

        if offer.is_accepted is False:
            msg.info(request, "This offer is already rejected.")
        else:
            offer.is_accepted = False
            if offer.is_draft:
                offer.is_draft = False
            offer.save()
            msg.success(request, "You have rejected this offer.")

        return redirect('offer_detail', pk=pk)


class ChatView(LoginRequiredMixin, View):
    template_name = 'chat.html'
    login_url = "/login"
    chat_id_key = "chat_id"

    @staticmethod
    def render_chat_message(raw_message):
        html_message = markdown.markdown(raw_message)
        return mark_safe(html_message)  # trust generated HTML

    def get(self, request, pk):
        chat_id = request.GET.get("chat_id")
        if chat_id:
            chat = get_object_or_404(Chat, pk=chat_id)
            if chat.user.id != request.user.id:
                return HttpResponseForbidden("You do not have the authorization to view this chat.")
            request.session['chat_id'] = chat_id
            if chat.message_history:
                request.session[f'chat_history_{chat_id}'] = json.loads(chat.message_history)

        offer = get_object_or_404(CreditOffer, pk=pk)
        all_chats = prepare_chat_list(self.request.user.id, offer.id)
        if request.session.get(self.chat_id_key) is None:
            chat_id = create_chat(offer, request.user)
            request.session["chat_id"] = chat_id
        else:
            chat_id = request.session.get("chat_id")

        history = request.session.get(f'chat_history_{chat_id}', [])
        context = {
            'messages': history,
            'offer': offer,
            'chat_id': chat_id,
            'chat_list': all_chats,
        }
        return render(request, self.template_name, context)

    def post(self, request, pk):
        offer = get_object_or_404(CreditOffer, pk=pk)
        offer_text = rephraze_offer(offer)
        print(offer_text)
        user_message = request.POST.get('message')
        chat_id = request.session.get("chat_id")
        session_key = f'chat_history_{chat_id}'
        history = request.session.get(session_key, [{
            "role": "system",
            "content": "You are an expert on credit offers."
                       "Your skills of explaining a credit offer to customers is unmatched, providing clear and "
                       "direct instructions to the customer. Maintain a polite and helpful tone. "
                       f"The credit offer context is {offer_text}. "
                       "Please provide friendly feedback to any user questions only. "
                       "Respond in a short, concise manner, with your answers being only relevant to the user question."

        }])

        if user_message:
            history.append({"role": "user", "content": user_message})
            llm_response = llm_generate_reply(history)
            llm_response = self.render_chat_message(llm_response)
            history.append({"role": "assistant", "content": llm_response})

            request.session[session_key] = history

        return redirect('chat_page', pk=pk)

# Moderator Core

# Admin Dashboard
class AdminDashboardView(LoginRequiredMixin, UserPassesTestMixin, View):
    login_url = '/login'

    def test_func(self):
        return getattr(self.request.user, 'is_moderator', False)

    def handle_no_permission(self):
        return HttpResponseForbidden("You do not have permission to access this page.")

    def get(self, request):
        model_name = request.GET.get('model', 'users').lower()
        page = request.GET.get('page', 1)

        model_map = {
            'users': User,
            'clients': Client,
            'loans': Loan,
            'offers': CreditOffer,
            'chats': Chat,
        }

        model = model_map.get(model_name)
        if not model:
            return render(request, 'admin/tables/empty_table.html', {'message': 'Model not found!'})

        queryset = model.objects.all().order_by('id')

        paginator = Paginator(queryset, 5)
        page_obj = paginator.get_page(page)

        context = {
            'page_obj': page_obj,
            'model_name': model_name,
        }
        template_name = f'admin/tables/{model_name}_table.html'
        return render(request, template_name, context)

# Moderator Control Panel
class ManageView(LoginRequiredMixin, UserPassesTestMixin, View):
    login_url = '/login'

    def test_func(self):
        return getattr(self.request.user, 'is_moderator', False)

    def handle_no_permission(self):
        return HttpResponseForbidden("You do not have permission to access this page.")

    def get(self, request):
        return render(request, 'manage.html')


class ModeratorOffersView(LoginRequiredMixin, UserPassesTestMixin, View):
    login_url = '/login'

    def test_func(self):
        return getattr(self.request.user, 'is_moderator', False)

    def handle_no_permission(self):
        return HttpResponseForbidden("You do not have permission to access this page.")

    def get(self, request):
        deactivate_old_credit_offers()
        credit_offers = CreditOffer.objects.filter(is_draft=True, is_accepted=None).exclude(client_id=request.user.id).order_by('created_at')
        return render(request, 'suggested-offers.html', {'credit_offers': credit_offers})


class EditOfferEmailView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    login_url = '/login'

    model = CreditOffer
    form_class = EditOfferEmailForm
    template_name = 'creditoffer_edit_email.html'

    def get_success_url(self):
        return reverse_lazy('offer_detail', kwargs={'pk': self.object.pk})

    def test_func(self):
        # Only allow moderators to access this view
        return self.request.user.is_moderator

    def handle_no_permission(self):
        if self.request.user.is_authenticated:
            return HttpResponseForbidden("You do not have the authorization to modify this offer.")
        return super().handle_no_permission()


class SendOfferEmailView(LoginRequiredMixin, UserPassesTestMixin, View):
    login_url = "/login"

    def test_func(self):
        return self.request.user.is_moderator

    def handle_no_permission(self):
        if self.request.user.is_authenticated:
            return HttpResponseForbidden("You do not have the authorization to modify this offer.")
        return super().handle_no_permission()

    def post(self, request, pk):
        offer = get_object_or_404(CreditOffer, pk=pk)

        if not offer.email_content:
            msg.error(request, "No email generated for this offer.")
            return redirect('offer_detail', pk=pk)
 
        email_content_redacted = redact_markdown_content(offer.email_content)

        try:
            send_email(offer.client.user.email, offer.email_subject, email_content_redacted, format="html")
                
            offer.is_draft = False
            offer.is_active = True
            offer.save()

            msg.success(request, f"E-Mail for offer #{offer.id} sent successfully.")

        except Exception as e:
            print("FAILURE")
            msg.error(request, f"Error while sending the email: {str(e)}")
        
        return redirect('offer_detail', pk=pk)
    

    
class AddCustomerView(LoginRequiredMixin, UserPassesTestMixin, View):
    login_url = "/login"
    template_name = 'add-customer.html'

    def get(self, request):
        user_form = UserManageForm()
        client_form = AddClientForm()
        return render(request, self.template_name, {
            'user_form': user_form,
            'client_form': client_form,
        })

    def post(self, request):
        user_form = UserManageForm(request.POST)
        client_form = AddClientForm(request.POST)
        if user_form.is_valid() and client_form.is_valid():
            user = user_form.save(commit=False)
            user.set_password(client_form.cleaned_data['identity_number'])
            user.save()
            client = client_form.save(commit=False)
            client.user = user
            client.save()
            msg.success(request, "User and client added successfully.")
            return redirect('manage')

        return render(request, self.template_name, {
            'user_form': user_form,
            'client_form': client_form,
        })

    def test_func(self):
        return self.request.user.is_moderator

    def handle_no_permission(self):
        if self.request.user.is_authenticated:
            return HttpResponseForbidden("You do not have the authorization to modify this offer.")
        return super().handle_no_permission()

class EditCustomersView(LoginRequiredMixin, UserPassesTestMixin, ListView):
    login_url = "/login"
    model = Client
    template_name = 'edit-customers.html'
    context_object_name = 'customers'
    paginate_by = 10

    def test_func(self):
        # Only staff members can access this view
        return self.request.user.is_moderator

    def get_queryset(self):
        queryset = super().get_queryset()
        query = self.request.GET.get('q', '')
        
        if query:
            queryset = queryset.filter(identity_number__icontains=query)
        
        return queryset.order_by('user__last_name', 'user__first_name').exclude(is_active=False)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['search_query'] = self.request.GET.get('q', '')
        return context
    
    def handle_no_permission(self):
        if self.request.user.is_authenticated:
            return HttpResponseForbidden("You do not have the authorization to modify this offer.")
        return super().handle_no_permission()

    
class EditCustomerView(LoginRequiredMixin, UserPassesTestMixin, View):
    login_url = "/login"
    template_name = 'edit-customer.html'

    def test_func(self):
        return self.request.user.is_moderator

    def handle_no_permission(self):
        if self.request.user.is_authenticated:
            return HttpResponseForbidden("You do not have the authorization to modify this user.")
        return super().handle_no_permission()

    def get(self, request, pk):
        client = get_object_or_404(Client, pk=pk)
        
        client_form = EditClientForm(instance=client)
        user_form = UserManageForm(instance=client.user)
        
        return render(request, self.template_name, {
            'client_form': client_form,
            'user_form': user_form,
            'client': client,
            'is_editing': True,
        })

    def post(self, request, pk):
        client = get_object_or_404(Client, pk=pk)

        client_form = EditClientForm(request.POST, instance=client)
        user_form = UserManageForm(request.POST, instance=client.user)
        
        if client_form.is_valid() and user_form.is_valid():
            user = user_form.save()

            client = client_form.save(commit=False)
            client.user = user
            client.risk_score = None
            CreditOffer.objects.filter(client=client).update(is_active=False)
            client.save()
            
            msg.success(request, f"Client {user.first_name} {user.last_name} successfully updated.")
            return redirect('edit_customers')

        return render(request, self.template_name, {
            'client_form': client_form,
            'user_form': user_form,
            'client': client,
            'is_editing': True,
        })
    
class DeactivateCustomerView(LoginRequiredMixin, UserPassesTestMixin, View):
    http_method_names = ["post"]
    login_url = "/login"

    def test_func(self):
        return self.request.user.is_moderator

    def handle_no_permission(self):
        if self.request.user.is_authenticated:
            return HttpResponseForbidden("You do not have the authorization to modify this client.")
        return super().handle_no_permission()

    def post(self, request, pk, *args, **kwargs):
        customer = get_object_or_404(Client, pk=pk)
        customer.is_active = False
        customer.user.is_active = False
        customer.save(update_fields=["is_active"])
        msg.success(request, "Client account deactivated successfully.")
        return redirect(reverse("edit_customers"))

class DeclinedClientsView(LoginRequiredMixin, UserPassesTestMixin, View):
    login_url = "/login"

    def test_func(self):
        return self.request.user.is_moderator

    def handle_no_permission(self):
        if self.request.user.is_authenticated:
            return HttpResponseForbidden("You do not have the authorization to modify this user.")
        return super().handle_no_permission()
    
    def get(self, request):
        threshold = getattr(settings, 'RISK_THRESHOLD', 0.25)
        high_risk_clients = get_high_risk_clients(threshold)
        context = {
            'high_risk_clients': high_risk_clients,
        }

        return render(request, "high-risk-clients.html", context)


class AgentFeedbackView(LoginRequiredMixin, UserPassesTestMixin, View):
    login_url = "/login"

    def test_func(self):
        return self.request.user.is_moderator

    def handle_no_permission(self):
        if self.request.user.is_authenticated:
            return HttpResponseForbidden("You do not have the authorization to modify this user.")
        return super().handle_no_permission()
    
    def get(self, request):
        
        agent_feedback_object = get_agent_feedback()
        if agent_feedback_object:
            agent_feedback_object.feedback = redact_markdown_content(agent_feedback_object.feedback.split(":", 1)[-1])
            context = {
                "agent_feedback": agent_feedback_object,
            }
        else:
            context = {
                "agent_feedback": {
                    "feedback": None
                }
            }
        return render(request, "agent-feedback.html", context)
    
class AgentFeedbackDeclineView(LoginRequiredMixin, UserPassesTestMixin, View):
    http_method_names = ["post"]
    login_url = "/login"

    def test_func(self):
        return self.request.user.is_moderator

    def handle_no_permission(self):
        if self.request.user.is_authenticated:
            return HttpResponseForbidden("You do not have the authorization to modify this feedback object.")
        return super().handle_no_permission()

    def post(self, request, pk, *args, **kwargs):
        fb = get_object_or_404(AgentFeedback, pk=pk)
        fb.is_reviewed = True
        fb.save(update_fields=["is_reviewed"])
        msg.success(request, "Agent Feedback declined.")
        return redirect(reverse('manage'))
    
class AgentFeedbackReportView(LoginRequiredMixin, UserPassesTestMixin, View):
    http_method_names = ["post"]
    login_url = "/login"

    def test_func(self):
        return self.request.user.is_moderator

    def handle_no_permission(self):
        if self.request.user.is_authenticated:
            return HttpResponseForbidden("You do not have the authorization to modify this feedback object.")
        return super().handle_no_permission()

    def post(self, request, pk, *args, **kwargs):
        fb = get_object_or_404(AgentFeedback, pk=pk)
        fb.is_reviewed = True
        fb.save(update_fields=["is_reviewed"])
        # Future Outlook: implement some integration with a ticketing system possibly
        msg.success(request, "Agent Feedback reported to IT.")
        return redirect(reverse('manage'))
    

class OfferFinderView(View, LoginRequiredMixin, UserPassesTestMixin):
    login_url = "/login"
    template_name = "offer-finder.html"

    def test_func(self):
        return self.request.user.is_moderator

    def handle_no_permission(self):
        if self.request.user.is_authenticated:
            return HttpResponseForbidden("You do not have the authorization to view this function.")
        return super().handle_no_permission()

    def get(self, request, *args, **kwargs):
        offer_id = request.GET.get("offer_id")
        if not offer_id:
            return render(request, self.template_name)
       
        if not offer_id.isdigit():
            msg.error(request, "Please give a valid id.")
            return redirect(reverse("offer_finder"))

        pk = int(offer_id)

        get_object_or_404(CreditOffer, pk=pk)

        return redirect("offer_detail", pk=pk)

# Util Views
@csrf_exempt
def write_email(request):
    """
    View to handle email generation and agent invocation.
    """
    if request.content_type != 'application/json':
        return JsonResponse({
            'error': 'Content-Type must be application/json'
        }, status=400)

    if request.method == "POST":
        data = {}
        try:
            data = json.loads(request.body)
        except json.JSONDecodeError:
            return JsonResponse({
                'error': 'Invalid JSON in request body'
            }, status=400)

        inputs = {
            "client_name": data.get("name"),
            "client_age": data.get("age"),
            "client_sex": data.get("sex"),
            "loan_purpose": data.get("loan_purpose"),
            "loan_amount": data.get("loan_amount"),
            "loan_duration": data.get("loan_duration"),
            "loan_type_description": data.get("loan_description"),
            "more_details_link": data.get("details_link"),
            "bank_address": getattr(settings, 'BANK_DEFAULT_ADRESS'),
            "bank_phone_number": getattr(settings, 'BANK_DEFAULT_PHONE_NUMBER')
        }

        result = EmailCrew().crew().kickoff(inputs=inputs).json

        return JsonResponse(result, status=200, safe=False)


@csrf_protect
def save_and_reset_chat(request, offer_id):
    """
    View to reset the chat while saving it.
    """
    if request.method == "POST":
        data = json.loads(request.body)
        chat_id = data.get("chat_id")
        messages_list = data.get("message_history")
        save_messages(chat_id, messages_list)
        if f'chat_history_{chat_id}' in request.session:
            del request.session[f'chat_history_{chat_id}']
            print("chat_history removed")
        if 'chat_id' in request.session:
            del request.session[f'chat_id']
            print("chat_id removed")

        return JsonResponse({
            "redirect_url": reverse('chat_page', kwargs={"pk": offer_id})
        }, status=200)

@csrf_protect
def reset_chat(request, offer_id):
    """
    View to reset the chat without saving it.
    """
    if request.method == "POST":
        data = json.loads(request.body)
        chat_id = data.get("chat_id")

        if f'chat_history_{chat_id}' in request.session:
            del request.session[f'chat_history_{chat_id}']
            print("chat_history removed")

        return JsonResponse({
            "redirect_url": reverse('chat_page', kwargs={"pk": offer_id})
        }, status=200)

