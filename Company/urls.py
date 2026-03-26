from django.urls import path
from .views import *

app_name = "company"

urlpatterns = [

    # SOCIAL
    path("social/", SocialAccountsView.as_view(), name="social_accounts"),

    # CAREERS
    path("careers/", CareerListView.as_view(), name="careers_list"),
    path("careers/<int:pk>/", CareerDetailView.as_view(), name="careers_detail"),
    path("careers/<int:pk>/submit/", CareerSubmitView.as_view(), name="careers_submit"),

    # ARTICLES
    path("articles/", ArticleListView.as_view(), name="articles_list"),

    # INVESTORS
    path("investors/", InvestorListView.as_view(), name="investors"),

    # PARTNERSHIPS
    path("partners/", PartnershipListView.as_view(), name="partners"),
]
