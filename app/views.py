from django.utils import timezone
from django.shortcuts import render
from app.forms import CommentForm

from app.models import Post

# Create your views here.
def index(request):
    posts = Post.objects.all()
    context= {
        'posts':posts
        }
    return render(request, 'app/index.html', context)


def post_page(request, slug):
    post = Post.objects.get(slug=slug)
    form = CommentForm()

    if request.method == 'POST':
        comment_form = CommentForm(request.POST)
        if comment_form.is_valid():
            comment = comment_form.save(commit=False)
            postid = request.POST.get('post_id')
            post = Post.objects.get(id = postid)
            comment.post = post
            comment.date = timezone.now()
            comment.save()




    # first check if the view count is none or not, if it is, then increment by 1, everytime a user visits, views will be incremented by 1.
    if post.view_count is None:
        post.view_count = 1
    else:
        post.view_count = post.view_count+1
    post.save()

    context = {'post':post, 'form': form}
    return render(request, 'app/post.html', context)