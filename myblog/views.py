from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect
from django.views import generic
from .models import Post, Comment
from django.shortcuts import render, get_object_or_404
from .forms import CommentForm, NewPost


# Create your views here.

class PostList(generic.ListView):
    queryset = Post.objects.filter(status=1).order_by('-created_on')
    template_name = 'index.html'
    paginate_by = 3


class PostDetail(generic.DetailView):
    model = Post
    template_name = 'post_detail.html'


def post_detail(request, slug):
    template_name = 'post_detail.html'
    post = get_object_or_404(Post, slug=slug)
    comments = post.comments.filter(active=True)
    new_comment = None
    # Comment posted
    if request.method == 'POST':
        comment_form = CommentForm(data=request.POST)
        if comment_form.is_valid():
            # Create Comment object but don't save to database yet
            new_comment = comment_form.save(commit=False)
            # Assign the current post to the comment
            new_comment.post = post
            # Save the comment to the database
            new_comment.save()
    else:
        comment_form = CommentForm()

    return render(request, template_name, {'post': post,
                                           'comments': comments,
                                           'new_comment': new_comment,
                                           'comment_form': comment_form})


@login_required
def new_post(request, pk):
    template_name = 'new_post.html'
    post = get_object_or_404(Post, pk=pk)
    if request.method == 'POST':
        form = NewPost(request.POST)
        if form.is_valid():
            post = form.save(commit=False)
            post.author = request.user
            Post.objects.create(
                message=form.cleaned_data.get('message'),
                post=post,
                created_by=request.user,
            )
            return redirect('home', pk=pk, post_pk=post.pk)
    else:
        form = NewPost()
    return render(request, template_name, {'post': post, 'form': form})
