from django.shortcuts import get_object_or_404, render
from django.views.generic import ListView, CreateView

from .forms import PostSearchForm
from .models import Post


class HomeView(ListView):
    model = Post
    # template_name = 'blog/index.html'  # this is a variable that we can set up
    context_object_name = "posts"
    # context_object_name: this is reference to the data that is being collected from this class here or this view
    # and being passed across to the template
    paginate_by = 10

    def get_queryset(self):
        x = Post.objects.filter(status='published')
        return x

    def get_template_names(self):
        if self.request.htmx:
            return "components/post-list-elements.html"
        return 'blog/index.html'


def post_single(request, post):
    post = get_object_or_404(Post, slug=post, status='published')
    related = Post.objects.filter(author=post.author)[:5]
    return render(request, 'blog/single_post.html', {'post': post, 'related': related})


class TagListView(ListView):
    model = Post
    paginate_by = 10
    context_object_name = 'posts'

    def get_queryset(self):
        # x = Post.objects.filter(tags__name=self.kwargs['tag'])
        x = Post.objects.filter(status__exact='published', tags__name__in=[self.kwargs['tag']])
        return x

    def get_template_names(self):
        if self.request.htmx:
            return "components/post-list-elements-tags.html"

        return 'blog/tags.html'

    def get_context_data(self, **kwargs):
        context = super(TagListView, self).get_context_data(**kwargs)
        context['tag'] = self.kwargs['tag']

        return context


class PostSearchView(ListView):
    model = Post
    paginate_by = 10
    context_object_name = 'posts'
    form_class = PostSearchForm

    def get_queryset(self):
        form = self.form_class(self.request.GET)  # grab data from form
        if form.is_valid():
            return Post.objects.filter(status__exact='published', title__icontains=form.cleaned_data['q'])
        return []

    def get_template_names(self):
        if self.request.htmx:
            return "components/post-list-elements-search.html"
        return 'blog/search.html'


class AddPostView(CreateView):
    model = Post
    fields = ['author', 'title', 'subtitle', 'slug', 'content', 'status', 'tags']

    def get_template_names(self):
        return 'blog/add_post.html'
