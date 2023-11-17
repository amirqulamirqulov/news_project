from django.shortcuts import render, get_object_or_404, HttpResponse
from .models import News, Category
from django.views.generic import TemplateView, ListView, DetailView, UpdateView, DeleteView, CreateView
from .forms import ContactForm, CommentForm
from django.urls import reverse_lazy
from django.utils.text import slugify
from news_project.custom_permission import OnlySuperuserPermission
from django.db.models import Q
from hitcount.views import HitCountDetailView, HitCountMixin
# Create your views here.


def newslistview(request):
    news_list = News.published.all()
    context = {
        "news_list": news_list,
    }
    return render(request, "news/news_list.html", context)


# Import your CommentForm


class PostCountHitDetailView(HitCountDetailView):
    model = News
    count_hit = True
    slug_field = 'slug'


class NewsDetailView(DetailView):
    model = News
    template_name = "news/news_detail.html"
    context_object_name = "news"
    slug_field = 'slug'
    slug_url_kwarg = 'slug'

    def post(self, request, slug, *args, **kwargs):
        comment_form = CommentForm(request.POST)
        if comment_form.is_valid():
            new_comment = comment_form.save(commit=False)
            new_comment.news = self.get_object()
            new_comment.user = request.user  # Assuming you have a user associated with the comment
            new_comment.save()
            comment_form = CommentForm()  # Clear the form
            comments = self.get_object().comments.filter(active=True)
            comment_count = comments.count()

        context = {
            'comment_form': comment_form,
            'news': self.get_object(),
            'comments': comments,
            'comment_count': comment_count
        }
        return render(request, self.template_name, context)

    def get(self, request, slug, *args, **kwargs):
        comment_form = CommentForm()
        news = self.get_object()
        comments = news.comments.filter(active=True)
        comment_count = comments.count()
        context = {
            'comment_form': comment_form,
            'news': news,
            'comments': comments,
            'comment_count': comment_count
        }
        return render(request, self.template_name, context)


# def newsdetailview(request, new):
#     news = get_object_or_404(News, slug=new, status=News.Status.Published)
#     category = Category.objects.all().filter(id=news.category.id)
#     context = {
#         "news": news,
#         "category": category
#     }
#     return render(request, "news/news_detail.html", context)


# def homepageview(request):
#     news_list = News.published.all().order_by('-publish_time')[:5]
#     local_news_one = News.published.all().filter(category__name="Mahalliy").order_by('-publish_time')[:1]
#     local_news_main = News.published.all().filter(category__name="Mahalliy").order_by('-publish_time')[1:5]
#     sport_news_one = News.published.all().filter(category__name="Sport").order_by('-publish_time')[:1]
#     sport_news_main = News.published.all().filter(category__name="Sport").order_by('-publish_time')[1:5]
#     technalogy_news_one = News.published.all().filter(category__name="Texnalogiya").order_by('-publish_time')[:1]
#     technalogy_news_main = News.published.all().filter(category__name="Texnalogiya").order_by('-publish_time')[1:5]
#     abroad_news_one = News.published.all().filter(category__name="Xorij").order_by('-publish_time')[:1]
#     abroad_news_main = News.published.all().filter(category__name="Xorij").order_by('-publish_time')[1:5]
#     categories = Category.objects.all()
#     context = {
#         'news_list': news_list,
#         'categories': categories,
#         'local_news_one': local_news_one,
#         'local_news_main': local_news_main,
#         'sport_news_one': sport_news_one,
#         'sport_news_main': sport_news_main,
#         'technalogy_news_one': technalogy_news_one,
#         'technalogy_news_main': technalogy_news_main,
#         'abroad_news_one': abroad_news_one,
#         'abroad_news_main': abroad_news_main
#     }
#     return render(request, 'news/index.html', context)


class HomePageView(ListView):
    model = News
    template_name = 'news/index.html'
    context_object_name = 'news_list'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['categories'] = Category.objects.all()
        context['news_list'] = News.published.all().order_by('-publish_time')[:5]
        context['local_news_main'] = News.published.all().filter(category__name="Mahalliy").order_by('-publish_time')[
                                     :5]
        context['sport_news_main'] = News.published.all().filter(category__name="Sport").order_by('-publish_time')[:5]
        context['technalogy_news_main'] = News.published.all().filter(category__name="Texnalogiya").order_by(
            '-publish_time')[:5]
        context['abroad_news_main'] = News.published.all().filter(category__name="Xorij").order_by('-publish_time')[:5]
        return context


# def contactpageview(request):
#     form = ContactForm(request.POST or None)
#     if request.method == 'POST' and form.is_valid:
#         form.save()
#         return HttpResponse("<h2>Biz bilan bog'langaningiz uchun tashakkur!</h2>")
#     context = {
#         "form": form
#     }
#     return render(request, 'news/contact.html', context)


class ContactPageView(TemplateView):
    template_name = 'news/contact.html'

    def get(self, request, *args, **kwargs):
        form = ContactForm()
        context = {
            "form": form
        }
        return render(request, 'news/contact.html', context)

    def post(self, request, *args, **kwargs):
        form = ContactForm(request.POST)
        if form.is_valid and request.method == "POST":
            form.save()
            return HttpResponse("<h2> Biz bilan bog'langaningiz uchun tashakkur!</h2>")
        context = {
            "form": form
        }
        return render(request, 'news/contact.html', context)


def errorpageview(request):
    context = {

    }
    return render(request, 'news/404.html', context)


class LocalListView(ListView):
    model = News
    template_name = 'news/local_news.html'
    context_object_name = 'local_news'

    def get_queryset(self):
        local_news_list = []
        news = self.model.published.filter(category__name="Mahalliy")
        news_list = list(news)
        for i in range(0, len(news_list), 3):
            local_news_list.append(news_list[i:i + 3])
        return local_news_list


class TechnalogyListView(ListView):
    model = News
    template_name = 'news/technalogy_news.html'
    context_object_name = 'technalogy_news'

    def get_queryset(self):
        local_news_list = []
        news = self.model.published.filter(category__name="Texnalogiya")
        news_list = list(news)
        for i in range(0, len(news_list), 3):
            local_news_list.append(news_list[i:i + 3])
        return local_news_list


class AbroadListView(ListView):
    model = News
    template_name = 'news/abroad_news.html'
    context_object_name = 'abroad_news'

    def get_queryset(self):
        local_news_list = []
        news = self.model.published.filter(category__name="Xorij")
        news_list = list(news)
        for i in range(0, len(news_list), 3):
            local_news_list.append(news_list[i:i + 3])
        return local_news_list


class SportListView(ListView):
    model = News
    template_name = 'news/sport_news.html'
    context_object_name = 'sport_news'

    def get_queryset(self):
        local_news_list = []
        news = self.model.published.filter(category__name="Sport")
        news_list = list(news)
        for i in range(0, len(news_list), 3):
            local_news_list.append(news_list[i:i + 3])
        return local_news_list


class NewsUpdateView(OnlySuperuserPermission, UpdateView):
    model = News
    fields = ('title', 'body', 'category', 'status')
    template_name = "crud/news_update.html"
    context_object_name = "news"


class NewsDeleteView(OnlySuperuserPermission, DeleteView):
    model = News
    template_name = 'crud/news_delete.html'
    success_url = reverse_lazy('home_page')
    context_object_name = "news"


class NewsCreateView(OnlySuperuserPermission, CreateView):
    model = News
    template_name = "crud/news_create.html"
    fields = ("title", "body", "category", "images", "status")

    def form_valid(self, form):
        # Automatically generate a slug from the title
        title = form.cleaned_data['title']
        form.instance.slug = slugify(title)
        return super().form_valid(form)


class SearchNewsView(ListView):
    model = News
    template_name = 'news/search_list.html'
    context_object_name = 'all_news'

    def get_queryset(self):
        query = self.request.GET.get('q')
        search_news_list = []
        news = News.objects.filter(
            Q(title__icontains=query) | Q(body__icontains=query)
        )
        news_list = list(news)
        for i in range(0, len(news_list), 3):
            search_news_list.append(news_list[i:i + 3])
        return search_news_list




