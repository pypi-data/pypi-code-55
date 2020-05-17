from django.urls import path, include
from django.utils.translation import ugettext as _

from db.models import Member, PostAlert, Post, Admonition, Book, BookPart, SiteParam, Faq, Tag, CorrectionRequest, \
    CorrectionRequestAction, License, Contest
from web import views
from web.forms import TagForm, SiteParamForm, ContestForm, LicenseForm, MemberForm, FaqForm, PostForm

urlpatterns = [

    # Page d'accueil
    path('',
         views.TemplateView.as_view(template_name="web/home.html", section_name=_('Home')),
         name='muses_home'),

    path('savetheme/', views.save_selected_theme, name='muses_save_theme'),

    # Page d'à propos
    path('about/',
         views.TemplateView.as_view(template_name="web/about_us.html", section_name=_('About us')),
         name='muses_about_us'),

    # Page de la foire aux questions
    path('faq/',
         views.ListView.as_view(model=Faq, section_name=_('Faq')),
         name='muses_faq'),

    # Page des conditions d'utilisation
    path('gcu/',
         views.TemplateView.as_view(template_name="web/gcu.html", section_name=_('General Conditions of Use')),
         name='muses_gcu'),

    # Page contact
    path('contact/',
         views.ContactPageView.as_view(template_name="web/contact.html", section_name=_('Contact')),
         name='muses_contact'),

    # Security urls
    path('login/',
         views.LoginPageView.as_view(),
         name='muses_login'),
    path('logout/',
         views.LogoutPageView.as_view(),
         name='muses_logout'),
    path('register/',
         views.RegisterPageView.as_view(),
         name='muses_register'),
    path('activate/',
         views.ActivateAccountPageView.as_view(),
         name='muses_activate_account'),

    # Liste les publications par section
    path('list_posts/<str:section>/',
         views.ListView.as_view(model=Post),
         name='muses_list_posts'),

    # Affiche une publication
    path('posts/<int:id>/',
         views.DetailView.as_view(model=Post),
         name='muses_post_detail'),

    # Nouvelle publication
    path('posts/',
         views.CreateView.as_view(
             model=Post,
             form_class=PostForm
         ),
         name='muses_post_create'),

    # Modifier une publication
    path('posts/<int:id>/update/',
         views.UpdateView.as_view(
             model=Post,
             form_class=PostForm
         ),
         name='muse_post_update'),

    path('members/',
         views.ListView.as_view(model=Member, section_name=_('Members list')),
         name='muses_list_members'),

    path('members/<int:id>/',
         views.DetailView.as_view(model=Member, section_name=_('Member profile')),
         name='muses_member_detail'),

    path('adm/', include([
        path('',
             views.TemplateView.as_view(template_name="web/admin.html", section_name=_('Administration')),
             name='muses_admin'),

        path('members/',
             views.AdminListView.as_view(model=Member, section_name=_('Manage members')),
             name='muses_admin_list_members'),
        path('members/<int:id>/details/',
             views.AdminDetailView.as_view(model=Member),
             name='muses_admin_member_detail'),
        path('members/<int:id>/update/',
             views.AdminUpdateView.as_view(
                 model=Member,
                 form_class=MemberForm
             ),
             name='muses_admin_member_update'),
        path('members/<int:id>/confirm_deletion/',
             views.AdminDeleteView.as_view(model=Member),
             name='muses_admin_member_delete'),

        path('post_alerts/',
             views.AdminListView.as_view(model=PostAlert),
             name='muses_admin_list_post_alerts'),
        path('post_alerts/<int:id>/',
             views.AdminDetailView.as_view(model=PostAlert),
             name='muses_admin_post_alert_detail'),

        path('comment_alerts/',
             views.AdminListView.as_view(model=PostAlert),
             name='muses_admin_list_comment_alerts'),
        path('comment_alerts/<int:id>/',
             views.AdminDetailView.as_view(model=PostAlert),
             name='muses_admin_comment_alert_detail'),

        path('admonitions/',
             views.AdminListView.as_view(model=Admonition, section_name=_('Admonitions management')),
             name='muses_admin_list_admonitions'),
        path('admonitions/<int:id>/',
             views.AdminDetailView.as_view(model=Admonition),
             name='muses_admin_admonition_detail'),

        path('books/',
             views.AdminListView.as_view(model=Book),
             name='muses_admin_list_books'),
        path('books/<int:id>/', include([
            path('',
                 views.AdminDetailView.as_view(model=Book),
                 name='muses_admin_book_detail'),

            path('book_parts/',
                 views.AdminListView.as_view(model=BookPart),
                 name='muses_admin_list_book_parts'),
            path('book_parts/<int:id>/',
                 views.AdminDetailView.as_view(model=BookPart),
                 name='muses_admin_book_part_detail')
        ])),

        path('site_params/',
             views.AdminListView.as_view(model=SiteParam),
             name='muses_admin_list_site_params'),
        path('site_params/new/',
             views.AdminCreateView.as_view(
                 model=SiteParam,
                 form_class=SiteParamForm
             ),
             name='muses_admin_site_param_create'),
        path('site_params/<int:id>/update/',
             views.AdminUpdateView.as_view(
                 model=SiteParam,
                 form_class=SiteParamForm
             ),
             name='muses_admin_site_param_update'),
        path('site_params/<int:id>/details/',
             views.AdminDetailView.as_view(model=SiteParam),
             name='muses_admin_site_param_detail'),
        path('site_params/<int:id>/confirm_deletion/',
             views.AdminDeleteView.as_view(model=SiteParam),
             name='muses_admin_site_param_delete'),

        path('faqs/',
             views.AdminListView.as_view(model=Faq),
             name='muses_admin_list_faqs'),
        path('faqs/new/',
             views.AdminCreateView.as_view(
                 model=Faq,
                 form_class=FaqForm
             ),
             name='muses_admin_faq_create'),
        path('faqs/<int:id>/update/',
             views.AdminUpdateView.as_view(
                 model=Faq,
                 form_class=FaqForm
             ),
             name='muses_admin_faq_update'),
        path('faqs/<int:id>/details/',
             views.AdminDetailView.as_view(model=Faq),
             name='muses_admin_faq_detail'),
        path('faqs/<int:id>/confirm_deletion/',
             views.AdminDeleteView.as_view(model=Faq),
             name='muses_admin_faq_delete'),

        path('tags/',
             views.AdminListView.as_view(model=Tag),
             name='muses_admin_list_tags'),
        path('tags/new/',
             views.AdminCreateView.as_view(
                 model=Tag,
                 form_class=TagForm
             ), name='muses_admin_tag_create'),
        path('tags/<int:id>/confirm_deletion/',
             views.AdminDeleteView.as_view(model=Tag),
             name='muses_admin_tag_delete'),
        path('tags/<int:id>/details/',
             views.AdminDetailView.as_view(
                 model=Tag
             ), name='muses_admin_tag_detail'),
        path('tags/<int:id>/update/',
             views.AdminUpdateView.as_view(
                 model=Tag,
                 form_class=TagForm
             ),
             name='muses_admin_tag_update'),

        path('licenses/',
             views.AdminListView.as_view(model=License),
             name='muses_admin_list_licenses'),
        path('licenses/new/',
             views.AdminCreateView.as_view(
                 model=License,
                 form_class=LicenseForm
             ),
             name='muses_admin_license_create'),
        path('licenses/<int:id>/confirm_deletion/',
             views.AdminDeleteView.as_view(model=License),
             name='muses_admin_license_delete'),
        path('licenses/<int:id>/details/',
             views.AdminDetailView.as_view(model=License),
             name='muses_admin_license_detail'),
        path('licenses/<int:id>/update/',
             views.AdminUpdateView.as_view(
                 model=License,
                 form_class=LicenseForm
             ),
             name='muses_admin_license_update'),

        path('contests/',
             views.AdminListView.as_view(model=Contest),
             name='muses_admin_list_contests'),
        path('contests/new/',
             views.AdminCreateView.as_view(
                 model=Contest,
                 form_class=ContestForm
             ),
             name="muses_admin_contest_create"
             ),
        path('contests/<int:id>/confirm_deletion/',
             views.AdminDeleteView.as_view(model=Contest),
             name="muses_admin_contest_delete"),
        path('contests/<int:id>/details/',
             views.AdminDetailView.as_view(model=Contest),
             name='muses_admin_contest_detail'),
        path('contests/<int:id>/update/',
             views.AdminUpdateView.as_view(
                 model=Contest,
                 form_class=ContestForm
             ),
             name='muses_admin_contest_update'),

        path('correction_requests/',
             views.AdminListView.as_view(model=CorrectionRequest),
             name='muses_admin_list_correction_requests'),
        path('correction_request/<int:id>/', include([
            path('details/',
                 views.AdminDetailView.as_view(model=CorrectionRequest),
                 name='muses_admin_correction_request_detail'),
            path('correction_actions/',
                 views.AdminListView.as_view(model=CorrectionRequestAction),
                 name='muses_admin_list_correction_request_actions'),
            path('correction_actions/<int:id>/details/',
                 views.AdminDetailView.as_view(model=CorrectionRequestAction),
                 name='muses_admin_correction_request_action_detail'),
        ])),
    ])),

    path('mod/', include([
        path('', views.TemplateView.as_view(template_name="web/mod.html", section_name=_('Moderation')),
             name='muses_mod'),

        path('members/',
             views.ModListView.as_view(model=Member),
             name='muses_mod_list_members'),
        path('members/<int:id>/details/',
             views.ModDetailView.as_view(model=Member),
             name='muses_mod_member_detail'),

        path('post_alerts/', views.ModPostAlertsListView.as_view(), name='muses_mod_list_post_alerts'),
        path('post_alerts/<int:id>/', views.ModPostAlertDetailView.as_view(),
             name='muses_mod_post_alert_detail'),

        path('comment_alerts/', views.ModPostAlertsListView.as_view(), name='muses_mod_list_comment_alerts'),
        path('comment_alerts/<int:id>/', views.ModPostAlertDetailView.as_view(),
             name='muses_mod_comment_alert_detail'),

        path('admonitions/', views.ModAdmonitionsListView.as_view(), name='muses_mod_list_admonitions'),
        path('admonitions/<int:id>/', views.ModAdmonitionDetailView.as_view(),
             name='muses_mod_admonition_detail'),
        path('list_books/', views.ModBooksListView.as_view(), name='muses_mod_list_books'),
        path('books/<int:id>/', include([
            path('', views.ModBookDetailView.as_view(), name='muses_mod_book_detail'),
            path('book_parts/', views.ModBookPartsListView.as_view(), name='muses_mod_list_book_parts'),
            path('book_parts/<int:id>/', views.ModBookPartDetailView.as_view(),
                 name='muses_mod_book_part_detail')
        ])),
        path('site_params/', views.ModSiteParamsListView.as_view(), name='muses_mod_list_site_params'),
        path('site_params/<int:id>/', views.ModSiteParamDetailView.as_view(),
             name='muses_mod_site_param_detail'),
        path('faqs/', views.ModFaqsListView.as_view(), name='muses_mod_list_faqs'),
        path('faqs/<int:id>/', views.ModFaqDetailView.as_view(), name='muses_mod_faq_detail'),

        path('tags/', views.ModTagsListView.as_view(), name='muses_mod_list_tags'),
        path('tags/new/',
             views.ModCreateView.as_view(
                 model=Tag,
                 form_class=TagForm
             ),
             name='muses_mod_tag_create'),
        path('tags/<int:id>/confirm_deletion/',
             views.ModDeleteView.as_view(model=Tag),
             name='muses_mod_tag_delete'),
        path('tags/<int:id>/details/', views.ModTagUpdateView.as_view(), name='muses_mod_tag_detail'),

        path('licenses/',
             views.ModListView.as_view(model=License),
             name='muses_mod_list_licenses'),
        path('licenses/new/',
             views.ModCreateView.as_view(
                 model=License,
                 form_class=LicenseForm
             ),
             name='muses_mod_license_create'),
        path('licenses/<int:id>/confirm_deletion/',
             views.ModDeleteView.as_view(model=License),
             name='muses_mod_license_delete'),
        path('licenses/<int:id>/details/',
             views.ModDetailView.as_view(model=License),
             name='muses_mod_license_detail'),
        path('licenses/<int:id>/update/',
             views.ModUpdateView.as_view(
                 model=License,
                 form_class=LicenseForm
             ),
             name='muses_mod_license_update'),

        path('contests/',
             views.ModListView.as_view(model=Contest),
             name='muses_mod_list_contests'),
        path('contests/new/',
             views.ModCreateView.as_view(
                 model=Contest,
                 form_class=ContestForm
             ),
             name="muses_mod_contest_create"
             ),
        path('contests/<int:id>/confirm_deletion/',
             views.ModDeleteView.as_view(model=Contest),
             name="muses_mod_contest_delete"),
        path('contests/<int:id>/details/',
             views.ModDetailView.as_view(model=Contest),
             name='muses_mod_contest_detail'),
        path('contests/<int:id>/update/',
             views.ModUpdateView.as_view(
                 model=Contest,
                 form_class=ContestForm
             ),
             name='muses_mod_contest_update'),

        path('correction_requests/',
             views.ModListView.as_view(model=CorrectionRequest),
             name='muses_mod_list_correction_requests'),
        path('correction_request/<int:id>/', include([
            path('details/',
                 views.ModDetailView.as_view(model=CorrectionRequest),
                 name='muses_mod_correction_request_detail'),
            path('correction_actions/',
                 views.ModListView.as_view(model=CorrectionRequestAction),
                 name='muses_mod_list_correction_request_actions'),
            path('correction_actions/<int:id>/details/',
                 views.ModDetailView.as_view(model=CorrectionRequestAction),
                 name='muses_mod_correction_request_action_detail'),
        ])),
    ])),

    path('cor/', include([
        path('', views.TemplateView.as_view(template_name="web/cor.html", section_name=_('Correction')),
             name='muses_cor'),

        path('correction_requests/',
             views.CorListView.as_view(model=CorrectionRequest),
             name='muses_cor_list_correction_requests'),
        path('correction_request/<int:id>/',
             include([
                 path('details/',
                      views.CorDetailView.as_view(model=CorrectionRequest),
                      name='muses_cor_correction_request_detail'),
                 path('correction_request_actions/',
                      views.CorListView.as_view(model=CorrectionRequestAction),
                      name='muses_cor_list_correction_request_actions'),
                 path('correction_request_actions/<int:id>/details/',
                      views.CorDetailView.as_view(model=CorrectionRequestAction),
                      name='muses_cor_correction_request_action_detail'),
             ])),
    ])),

    path('personal/', include([

        path('post_alerts/',
             views.PersonalPostAlertsListView.as_view(),
             name='muses_personal_list_post_alerts'),
        path('post_alerts/<int:id>/',
             views.PersonalPostAlertDetailView.as_view(),
             name='muses_personal_post_alert_detail'),

        path('admonitions/',
             views.PersonalAdmonitionsListView.as_view(),
             name='muses_personal_list_admonitions'),
        path('admonitions/<int:id>/',
             views.PersonalAdmonitionDetailView.as_view(),
             name='muses_personal_admonition_detail'),

        path('messages/',
             views.PersonalMessagesListView.as_view(),
             name='muses_personal_list_messages'),
        path('messages/<int:id>/',
             views.PersonalMessageDetailView.as_view(),
             name='muses_personal_message_detail'),

        path('control_center/',
             views.PersonalControlCenterView.as_view(),
             name='muses_personal_control_center'),
        path('preferences/',
             views.PersonalPreferencesView.as_view(),
             name='muses_personal_preferences'),

        path('profile/',
             views.PersonalProfileView.as_view(),
             name='muses_personal_profile'),
    ]))

]
