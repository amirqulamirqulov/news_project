from django.urls import path
from .views import newslistview, NewsDetailView, HomePageView, ContactPageView, errorpageview, LocalListView
from .views import SportListView, AbroadListView, TechnalogyListView, NewsDeleteView, NewsUpdateView, NewsCreateView

urlpatterns = [
    path("", HomePageView.as_view(), name="home_page"),
    path("contact-us", ContactPageView.as_view(), name="contact_page"),
    path('technalogy', TechnalogyListView.as_view(), name="technalogy_page"),
    path('sport', SportListView.as_view(), name="sport_page"),
    path('abroad', AbroadListView.as_view(), name="abroad_page"),
    path('local', LocalListView.as_view(), name="local_page"),
    path("404", errorpageview, name="404_page"),
    path("news/", newslistview, name="news_list"),
    path('news/<slug:slug>/', NewsDetailView.as_view(), name="news_detail"),
    path('news/<slug:slug>/update/', NewsUpdateView.as_view(), name="news_update"),
    path('news/<slug:slug>/delete/', NewsDeleteView.as_view(), name="news_delete"),
    path('news/create', NewsCreateView.as_view(), name="news_create")
]
