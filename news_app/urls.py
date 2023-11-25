from django.urls import path
from .views import newslistview, NewsDetailView, HomePageView, ContactPageView, errorpageview, CategoryCreateView
from .views import CategoryView, NewsDeleteView, NewsUpdateView, NewsCreateView, CategoryDeleteView, CategoryUpdateView
from.views import SearchNewsView
urlpatterns = [
    path("", HomePageView.as_view(), name="home_page"),
    path("contact-us", ContactPageView.as_view(), name="contact_page"),
    path('category/<str:slug>/', CategoryView.as_view(), name="categories"),
    path("404", errorpageview, name="404_page"),
    path("news/", newslistview, name="news_list"),
    path('news/<slug:slug>/', NewsDetailView.as_view(), name="news_detail"),
    path('news/<slug:slug>/update/', NewsUpdateView.as_view(), name="news_update"),
    path('news/<slug:slug>/delete/', NewsDeleteView.as_view(), name="news_delete"),
    path('news/create', NewsCreateView.as_view(), name="news_create"),
    path('category/create', CategoryCreateView.as_view(), name="category_create"),
    path('category/<int:pk>/update', CategoryUpdateView.as_view(), name="category_update"),
    path('category/<int:pk>/delete', CategoryDeleteView.as_view(), name="category_delete"),
    path('search-list', SearchNewsView.as_view(), name='search_list')
]
