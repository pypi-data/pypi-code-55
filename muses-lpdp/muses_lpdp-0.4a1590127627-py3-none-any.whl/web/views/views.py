# Create your views here.
from django.http import HttpResponse, HttpResponseNotAllowed
from django.shortcuts import redirect
from django.utils.translation import ugettext as _

from .generic import DetailView, TemplateView, ListView, FormView, CreateView, UpdateView, AdminListView, \
    AdminCreateView, AdminDetailView, AdminDeleteView, ModListView, ModDetailView, ModCreateView, ModDeleteView, \
    ModUpdateView, AdminUpdateView
from db.models import Post, Member, Tag, Book, BookPart, SiteParam, Admonition, Faq, License, CorrectionRequest, \
    Contest, CorrectionRequestAction, PostAlert, CommentAlert, Message, Comment
from web.forms import LoginForm, RegisterForm, ContactForm, ControlCenterChangeEmailForm, \
    PostForm, \
    CommentForm, ControlCenterChangePasswordForm, ProfileGeneralInformationForm, PreferencesNotificationsForm, Form, \
    LogoutForm, TagForm, LicenseForm, PreferencesGeneralForm
from .generic.cor_detail_view import CorDetailView
from .generic.cor_list_view import CorListView


class MultiFormsView(TemplateView):
    form_classes = {}

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        for key, value in self.form_classes.items():
            context[key] = value(id_form=key)
        return context


def save_selected_theme(request):
    if request.method == 'POST':
        current_user = Member.objects.get(id=request.user.id)
        current_user.theme = request.POST['theme']
        current_user.save()
        return redirect(request.POST['target_url'])
    else:
        return HttpResponseNotAllowed(permitted_methods=['POST'])


def change_password(request):
    if request.method == 'POST':
        current_user = Member.objects.get(id=request.user.id)
        current_user.set_password(request.POST["password"])
        return redirect(request.POST['target_url'])
    else:
        return HttpResponseNotAllowed(permitted_methods=['POST'])


class MemberDetailView(DetailView):
    model = Member


class ContactPageView(FormView):
    form_class = ContactForm
    success_url = '/'

    def form_valid(self, form):
        form.send_message()
        return super().form_valid(form)


class LoginPageView(FormView):
    template_name = "web/login.html"
    section_name = _('Login')
    form_class = LoginForm
    success_url = '/'

    def form_valid(self, form):
        form.authenticate(self.request)
        return super().form_valid(form)


class LogoutPageView(FormView):
    template_name = "web/logout.html"
    section_name = _('Logout')
    form_class = LogoutForm
    success_url = '/'

    def form_valid(self, form):
        form.logout(self.request)
        return super().form_valid(form)


class RegisterPageView(FormView):
    template_name = "web/register.html"
    section_name = _('Register')
    form_class = RegisterForm
    success_url = '/'

    def form_valid(self, form):
        form.register()
        return super().form_valid(form)


class ActivateAccountPageView(TemplateView):
    template_name = "web/activate_account.html"
    section_name = _('Activate Account')


class PostsListView(ListView):
    model = Post
    template_name = "db/post_list.html"
    paginate_by = 10


class PostDetailView(DetailView):
    def get_context_data(self, **kwargs):
        return super().get_context_data(**kwargs)

    template_name = "web/muses_post_detail.html"
    model = Post


class PostCreateView(CreateView):
    def get(self, request, *args, **kwargs):
        return super().get(request, *args, **kwargs)

    template_name = "web/muses_post_create.html"
    model = Post
    form_class = PostForm


class CommentDetailView(DetailView):
    def get_context_data(self, **kwargs):
        return super().get_context_data(**kwargs)

    template_name = "web/muses_comment_detail.html"
    model = Comment


class CommentCreateView(CreateView):
    template_name = "web/muses_comment_create.html"
    model = Comment
    form_class = CommentForm


class AdminMembersListView(ListView):
    template_name = "db/member_admin-list.html"
    model = Member
    paginate_by = 10


class AdminMemberDetailView(DetailView):
    def get_context_data(self, **kwargs):
        return super().get_context_data(**kwargs)

    template_name = "web/muses_admin_member_detail.html"
    model = Member


class AdminPostAlertsListView(ListView):
    template_name = "web/muses_admin_list_post_alerts.html"
    model = PostAlert
    paginate_by = 10


class AdminPostAlertDetailView(DetailView):
    model = PostAlert


class AdminCommentAlertsListView(ListView):
    template_name = "web/muses_admin_list_comment_alerts.html"
    model = CommentAlert
    paginate_by = 10


class AdminCommentAlertDetailView(DetailView):
    model = CommentAlert


class AdminTagsListView(AdminListView):
    model = Tag


class AdminTagDetailView(AdminDetailView):
    model = Tag


class AdminTagCreateView(AdminCreateView):
    model = Tag
    fields = [
        "name",
        "enable_at",
        "disable_at",
        "type",
        "mature",
        "active"
    ]


class AdminTagUpdateView(UpdateView):
    template_name_suffix = "_admin-update"

    model = Tag
    fields = [
        "name",
        "enable_at",
        "disable_at",
        "type",
        "mature",
        "active"
    ]


class AdminTagDeleteView(AdminDeleteView):
    model = Tag


class AdminBooksListView(ListView):
    model = Book
    paginate_by = 10


class AdminBookDetailView(DetailView):
    model = Book


class AdminBookPartsListView(ListView):
    model = BookPart
    paginate_by = 10


class AdminBookPartDetailView(DetailView):
    model = BookPart


class AdminSiteParamsListView(ListView):
    template_name = "web/muses_admin_list_site_params.html"
    model = SiteParam
    paginate_by = 10


class AdminSiteParamDetailView(DetailView):
    model = SiteParam


class AdminAdmonitionDetailView(DetailView):
    model = Admonition


class AdminFaqsListView(ListView):
    template_name = "web/muses_admin_list_faqs.html"
    paginate_by = 10
    model = Faq


class AdminFaqDetailView(DetailView):
    template_name = "web/muses_admin_faq_detail.html"


class AdminCorrectionRequestsListView(ListView):
    template_name = "web/muses_admin_list_correction_requests.html"
    model = CorrectionRequest
    paginate_by = 10


class AdminCorrectionRequestDetailView(DetailView):
    pass


class AdminContestsListView(ListView):
    template_name = "web/muses_admin_list_contests.html"
    model = Contest
    paginate_by = 10


class AdminContestDetailView(DetailView):
    pass


class AdminCorrectionActionsListView(ListView):
    template_name = "web/muses_admin_list_correction_actions.html"
    model = CorrectionRequestAction
    paginate_by = 10


class AdminCorrectionActionDetailView(DetailView):
    pass


class PersonalPostAlertsListView(ListView):
    template_name = "web/muses_personal_list_post_alerts.html"
    model = PostAlert
    paginate_by = 10


class PersonalPostAlertDetailView(DetailView):
    pass


class PersonalAdmonitionDetailView(DetailView):
    pass


class PersonalAdmonitionsListView(ListView):
    template_name = "web/muses_personal_list_admonitions.html"
    model = Admonition
    paginate_by = 10


class PersonalMessagesListView(ListView):
    section_name = _("My Messages")
    template_name = "web/muses_personal_list_messages.html"
    model = Message
    paginate_by = 10

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(object_list=object_list, **kwargs)
        return context


class PersonalMessageDetailView(DetailView):
    pass


class PersonalControlCenterView(MultiFormsView):
    section_name = _("Control Center")

    def dispatch(self, request, *args, **kwargs):
        if request.method == 'POST':
            form = Form(request.POST)
            return HttpResponse("ok")
        else:
            return super().dispatch(request, *args, **kwargs)

    template_name = "web/muses_personal_control_center.html"
    form_classes = {
        'form_change_password': ControlCenterChangePasswordForm,
        'form_change_email': ControlCenterChangeEmailForm,
    }


class PersonalPreferencesView(MultiFormsView):
    template_name = "web/muses_personal_preferences.html"
    section_name = _("Preferences")
    form_classes = {
        'form_preferences_notifications': PreferencesNotificationsForm,
        'form_preferences_general': PreferencesGeneralForm,
    }


class PersonalProfileView(MultiFormsView):
    template_name = "web/muses_personal_profile.html"
    section_name = "Profile"
    form_classes = {
        'form_change_general_information': ProfileGeneralInformationForm,
    }


class ModMembersListView(ModListView):
    model = Member


class ModMemberDetailView(ModDetailView):
    model = Member


class ModPostAlertsListView(ModListView):
    model = PostAlert


class ModPostAlertDetailView(ModDetailView):
    model = PostAlert


class ModAdmonitionsListView(ModListView):
    model = Admonition


class ModAdmonitionDetailView(ModDetailView):
    model = Admonition


class ModBooksListView(ModListView):
    model = Book


class ModBookDetailView(ModDetailView):
    model = Book


class ModBookPartsListView(ModListView):
    model = BookPart


class ModBookPartDetailView(ModDetailView):
    model = BookPart


class ModSiteParamsListView(ModListView):
    model = SiteParam


class ModSiteParamDetailView(ModDetailView):
    model = SiteParam


class ModFaqsListView(ModListView):
    model = Faq


class ModFaqDetailView(ModDetailView):
    model = Faq


class ModTagsListView(ModListView):
    model = Tag


class ModTagCreateView(ModCreateView):
    model = Tag
    form_class = TagForm


class ModTagUpdateView(ModUpdateView):
    model = Tag
    form_class = TagForm


class ModTagDeleteView(ModDeleteView):
    model = Tag
    form_class = TagForm


class ModLicensesListView(ModListView):
    model = License


class ModLicenseCreateView(ModCreateView):
    model = License


class ModLicenseDeleteView(ModDeleteView):
    model = License


class ModLicenseDetailView(ModDetailView):
    model = License


class ModContestsListView(ModListView):
    model = Contest


class ModContestDetailView(ModDetailView):
    model = Contest


class ModCorrectionRequestsListView(ModListView):
    model = CorrectionRequest


class ModCorrectionRequestDetailView(ModDetailView):
    model = CorrectionRequest


class ModCorrectionActionsListView(ModListView):
    model = CorrectionRequestAction


class ModCorrectionActionDetailView(ModDetailView):
    model = CorrectionRequestAction


class CorrectionPageView(TemplateView):
    template_name = "web/cor.html"


class CorCorrectionRequestsListView(CorListView):
    model = CorrectionRequest


class CorCorrectionRequestDetailView(CorDetailView):
    model = CorrectionRequest


class CorCorrectionActionsListView(CorListView):
    model = CorrectionRequestAction


class CorCorrectionActionDetailView(CorDetailView):
    model = CorrectionRequestAction


class AdminLicenseUpdateView(AdminUpdateView):
    model = License
    form_class = LicenseForm
