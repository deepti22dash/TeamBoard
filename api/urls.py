from django.urls import path
from .views import (RegisterView, ProfileView,KBEntryListCreateView,KBEntryDetailView,KBQueryView,LoginView,QueryHistoryView,)
                    

urlpatterns = [
    path("register/", RegisterView.as_view(), name="register"),
    path("profile/", ProfileView.as_view(), name="profile"),
    path("kb/", KBEntryListCreateView.as_view(), name="kb-list"),
    path("kb/<int:pk>/", KBEntryDetailView.as_view(), name="kb-detail"),
    
    path("kb/query/",KBQueryView.as_view(),name="kb-query"),
    path("login/", LoginView.as_view(), name="login"),
   path("query-history/",QueryHistoryView.as_view(),name="query-history",),
]