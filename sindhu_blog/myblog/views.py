from django.http import JsonResponse
from django.shortcuts import render, get_object_or_404
from django.views.generic import ListView, DetailView
from .models import Blog, Comment,Response
from .forms import CommentForm
from django.views import generic
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth.views import LogoutView
from django.urls import reverse_lazy
from django.contrib.auth.models import User
from django.contrib.auth.mixins import LoginRequiredMixin
from django.utils.timezone import datetime,timedelta
from django.db.models import Count

def CommentView(request,pk):
    blog = get_object_or_404 (Blog, pk=pk)           #Get the blog post based on the value from URL
    comments = blog.comments.all()
    print('hi')
    print (request.method)
    if request.method == 'POST':
        form = CommentForm(request.POST)
        if form.is_valid():
            comment = form.save(commit=False)
            comment.blog = blog
            comment.user = request.user
            comment.save()
            return JsonResponse({'success': True,
                                 'content': comment.comment_text,
                                 'username':comment.user.username,
                                 'date': comment.modified_date.strftime("%Y-%m-%d %H:%M:%S")})
        else:
            return JsonResponse({'success': False, 'errors': form.errors}, status=400)
    else:
        form = CommentForm()
        comments = blog.comments.all()
        return render(request, 'blogdetails.html', {'form': form, 'comments': comments})
def LikeView(request,pk):
    blog = get_object_or_404 (Blog, pk=pk)           #Get the blog post based on the value from URL
    if request.user in blog.dislikes.all():
        blog.dislikes.remove(request.user)
        blog.likes.add(request.user)
        response, created = Response.objects.get_or_create(user=request.user, blog=blog)
        response.likeornot = True
        response.save()
        return JsonResponse({'likes' : blog.likes.count(), 'dislikes' : blog.dislikes.count()})
    elif request.user in blog.likes.all():
        print('inside')
        return JsonResponse({'error': 'You have already liked this post'}, status=400,safe=False)
    else:
        blog.likes.add(request.user)                                               #Add the user to the liked users list
        response, created = Response.objects.get_or_create(user=request.user, blog=blog)
        response.likeornot = True
        response.save()
        return JsonResponse({'likes' : blog.likes.count(), 'dislikes' : blog.dislikes.count(), 'liked' : True })

def DislikeView(request,pk):
    blog = get_object_or_404 (Blog, pk=pk)                                  #Get the blog post based on the value from URL
    if request.user in blog.likes.all():                                    #this condition is to check if the user clicks on dislike button, then the user should be removed from the likes table
        blog.likes.remove(request.user)
        blog.dislikes.add(request.user)
        response, created = Response.objects.get_or_create(user=request.user, blog=blog)
        response.likeornot = False
        response.save()
        return JsonResponse({'likes' : blog.likes.count(), 'dislikes' : blog.dislikes.count()})
    elif request.user in blog.dislikes.all():
        return JsonResponse({'error' : 'You have already disliked this post'}, status=400, safe=False)
    else:
        blog.dislikes.add(request.user)
        response, created = Response.objects.get_or_create(user=request.user, blog=blog)
        response.likeornot = False
        response.save()
        return JsonResponse({'dislikes' : blog.dislikes.count(),'likes' : blog.likes.count(), 'disliked' : True})
class RegisterView(generic.CreateView):
    form_class = UserCreationForm                 # Using Django's built-in UserCreationForm
    template_name = 'registration/register.html'
    success_url = reverse_lazy('login')           # Redirect to the login page upon successful registration

class LoginView(generic.CreateView):
    form_class = AuthenticationForm               # Using Django's built-in AuthenticationForm
    template_name = 'registration/login.html'
    success_url = reverse_lazy('home')            # Redirect to the homepage upon successful registration

class LogoutView(LogoutView):
    success_url = reverse_lazy('home')            # Redirect to the homepage upon logout

#ListView is used for displaying a list of objects retrieved from a database.
class BlogListView(LoginRequiredMixin, ListView):
    model = Blog
    template_name = 'homepage.html'
    context_object_name = 'blog_list'
    ordering = ['-id']

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['user'] = self.request.user
        return context

#DetailsView is used for displaying detailed information about a particular object retrieved from a database
#The detail view expects the primary key of the object as part of the URL pattern.(check in homepage.html)
class BlogDetailView(DetailView):
    model = Blog  #Tablename where you are going to retrieve the blog contents
    template_name = 'blogdetails.html'
    context_object_name = 'blog_details'  # Optional, default is 'object' or 'blog' (i.e the object name in this example)"

def UserBlogDetailView(request):
    userblog = Blog.objects.filter(author = request.user)
    if userblog.exists():
        return render(request, 'userblogdetails.html', {'userblog': userblog})
    else:
        return render(request, 'no_userblogs.html')

def Top5CommentedBlogView(request):
    userblog = Blog.objects.filter(author = request.user).annotate(comment_count = Count('comments')).order_by('-comment_count')[:5]
    if userblog.exists():
        return render(request, 'top5commentedblogs.html', {'userblog': userblog})
    else:
        return render(request, 'no_userblogs.html')

def Top5LikedandDislikedBlogView(request):
    likedblogs = Blog.objects.filter(responses__response_date__gte = datetime.now()-timedelta(days=3)).annotate(like_count=Count('likes')).order_by('-like_count')[:5]
    dislikedblogs = Blog.objects.filter(responses__response_date__gte = datetime.now()-timedelta(days=3)).annotate(dislike_count=Count('dislikes')).order_by('-dislike_count')[:5]
    if likedblogs.exists() or dislikedblogs.exists():
        return render(request, 'top5likedanddislikedblogs.html', {'likedblogs': likedblogs, 'dislikedblogs' :dislikedblogs})
    else:
        return render(request, 'no_userblogs.html')
def Recent5LikedBlogView(request):
    likedblogs = Blog.objects.filter(responses__user=request.user,responses__likeornot=True).order_by( '-responses__response_date')[:5]
    if likedblogs.exists():
        return render(request, 'recent5likedblogs.html', {'likedblogs': likedblogs })
    else:
        return render(request, 'no_likedblogs.html')
def MyCommentHistoryView(request,pk):
    blogid = pk
    commenthistory = Comment.objects.filter(user=request.user,blog_id = blogid)
    if commenthistory.exists():
        return render(request, 'mycommenthistory.html', {'commenthistory': commenthistory })
    else:
        return render(request, 'no_usercomments.html')
def CommentHistoryForAuthorView(request):
    author_user = User.objects.get(username='saanvi')
    commenthistory = Comment.objects.filter(user=request.user,blog__author = author_user)
    if commenthistory.exists():
        return render(request, 'commenthistoryforauthor.html', {'commenthistory': commenthistory })
    else:
        return render(request, 'no_userblogs.html')