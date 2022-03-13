from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.models import User
from django.utils import timezone
from django.contrib import messages
from django.db.models import Q
from django.views import View
from django.http import HttpResponseRedirect,HttpResponse
from django.urls import reverse_lazy
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from .models import Post, Comment, UserProfile,Notification,ThreadModel,MessageModel,Image,Tag
from .forms import PostForm, CommentForm,ThreadForm,MessageForm,ShareForm,ExploreForm
from django.views.generic.edit import UpdateView, DeleteView


class PostListView(LoginRequiredMixin, View):
    def get(self, request, *args, **kwargs):
        logged_in_user = request.user
        # posts = Post.objects.filter(
        #     author__profile__followers__in=[logged_in_user]
        # ).order_by('-created_on')
        posts = Post.objects.filter(Q(author__profile__followers__in=[logged_in_user]) | Q(author=logged_in_user))
        
        form = PostForm()
        share_form = ShareForm()
        context = {'posts':posts,
                    'form':form,
                    'shareform':share_form,
        }
        return render(request, 'social/post_list.html', context)

    def post(self, request, *args, **kwargs):
        logged_in_user = request.user
        # posts = Post.objects.filter(
        #     author__profile__followers__in=[logged_in_user]
        # ).order_by('-created_on')
        
        posts = Post.objects.filter(Q(author__profile__followers__in=[logged_in_user]) | Q(author=logged_in_user))
        
        
        form = PostForm(request.POST,request.FILES)
        share_form = ShareForm()
        files = request.FILES.getlist('image')

        if form.is_valid():
            new_post = form.save(commit=False)
            new_post.author = request.user
            new_post.save()

            new_post.create_tag()

            for f in files:
                img = Image(image=f)
                img.save()
                new_post.image.add(img)
            new_post.save()

            context = {
            'posts':posts,
            'form':form,
            'shareform':share_form,
            }
            return render(request, 'social/post_list.html',context)

class CommentReplyView(LoginRequiredMixin, View):
    def post(self,request, post_pk,pk,*args,**kwargs):
        post = Post.objects.get(pk=post_pk)
        parent_comment = Comment.objects.get(pk=pk)
        form = CommentForm(request.POST)

        if form.is_valid():
            new_comment = form.save(commit=False)
            new_comment.author = request.user
            new_comment.parent = parent_comment
            new_comment.post = post
            new_comment.save()

            new_comment.create_tag()

        notification = Notification.objects.create(notification_type=2,from_user=request.user,to_user=parent_comment.author,comment=new_comment)

        return redirect('post_detail', pk=post_pk)

class PostDetailView(LoginRequiredMixin, View):
    def get(self, request, pk, *args, **kwargs):
        post = get_object_or_404(Post,pk=pk)
        comments = Comment.objects.filter(post=post).order_by('-created_on')
        form = CommentForm()

        context={
            'post':post,
            'comment':comments,
            'form':form,}

        return render(request,'social/post_detail.html',context)

    def post(self, request,pk, *args, **kwargs):
        post = Post.objects.get(pk=pk)
        form = CommentForm(request.POST)

        if form.is_valid():
            new_comment = form.save(commit=False)
            new_comment.author = request.user
            new_comment.post = post
            new_comment.save()

            new_comment.create_tag()
        comments = Comment.objects.filter(post=post).order_by('-created_on')

        notification = Notification.objects.create(notification_type=2,from_user=request.user,to_user=post.author,post=post)

        context = {
                'post':post,
                'comment':comments,
                'comments':comments,
                'form':form,}
        return render(request, 'social/post_detail.html',context)

class PostEditView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    model = Post
    fields = ['body']
    template_name = 'social/post_edit.html'

    def get_success_url(self):
        pk = self.kwargs['pk']
        return reverse_lazy('post_detail',kwargs={'pk':pk})

    def test_func(self):
        post = self.get_object()
        return self.request.user == post.author

class PostDeleteView(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
    model = Post
    template_name = 'social/post_delete.html'
    success_url = reverse_lazy('post_list')

    def test_func(self):
        post = self.get_object()
        return self.request.user == post.author

class CommentDeleteView(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
    model = Comment
    template_name = 'social/comment_delete.html'
    def get_success_url(self):
        pk = self.kwargs['pk']
        return reverse_lazy('post_detail',kwargs={'pk':pk})

    def test_func(self):
        post = self.get_object()
        return self.request.user == post.author
class CommentEditView(UpdateView):
    model = Comment
    fields = ['comment']
    template_name = 'social/comment_edit.html'
    def get_success_url(self):
        pk = self.kwargs['pk']
        return reverse_lazy('post_detail',kwargs={'pk':pk})

class ProfileView(View):
    def get(self, request, pk, *args, **kwargs):
        profile = UserProfile.objects.get(pk=pk)
        user = profile.user
        posts = Post.objects.filter(author=user).order_by('-created_on')
        follower = profile.followers.all()
        if len(follower) == 0:
            is_following = False
        for followers in follower:
            if request.user == followers:
                is_following = True
                break
            else:
                is_following = False
        followers = len(follower)

        context = {
        'user': user,
        'posts': posts,
        'profile':profile,
        'numfollowers':followers,
        'is_following':is_following,
        }
        return render(request, 'social/profile.html', context)
class ProfileEditView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    model = UserProfile
    fields = ['name','bio','birth_date','location','profile_picture',]
    template_name = 'social/profile_edit.html'
    def get_success_url(self):
        pk = self.kwargs['pk']
        return reverse_lazy('profile',kwargs={'pk':pk})
    def test_func(self):
            user_profile = self.get_object()
            return self.request.user  == user_profile.user


class AddFollower(LoginRequiredMixin, View):
    def post(self, request, pk,*args,**kwargs):
        profile = UserProfile.objects.get(pk=pk)
        profile.followers.add(request.user)

        notification = Notification.objects.create(notification_type=3,from_user=request.user,to_user=profile.user)
        return redirect('profile', pk=profile.pk)

class RemoveFollower(LoginRequiredMixin,View):
    def post(self, request,pk,*args,**kwargs):
        profile = UserProfile.objects.get(pk=pk)
        profile.followers.remove(request.user)

        return redirect('profile', pk=profile.pk)

class AddLikes(LoginRequiredMixin,View):
    def post(self,request,pk,*args,**kwargs):
        post = Post.objects.get(pk=pk)

        its_disliked =False
        for dislike in post.dislikes.all():
            if dislike == request.user:
                its_disliked =True
                break
        if its_disliked:
           post.dislikes.remove(request.user)

        its_liked = False
        for like in post.likes.all():
            if like == request.user:
                its_liked = True
                break

        if its_liked:
            post.likes.remove(request.user)

        if not its_liked:
            post.likes.add(request.user)
            notification = Notification.objects.create(notification_type=1,from_user=request.user,to_user=post.author,post=post)


        next = request.POST.get('next','/')
        return HttpResponseRedirect(next)

class DislikesView(LoginRequiredMixin,View):
    def post(self,request,pk,*args,**kwargs):
        post = Post.objects.get(pk=pk)

        its_liked = False
        for like in post.likes.all():
            if like == request.user:
                its_liked = True
                break
        if its_liked:
            post.likes.remove(request.user)

        its_disliked = False
        for dislike in post.dislikes.all():
            if dislike == request.user:
                its_disliked =True
                break

        if its_disliked:
            post.dislikes.remove(request.user)

        if not its_disliked:
            post.dislikes.add(request.user)

        next = request.POST.get('next','/')
        return HttpResponseRedirect(next)


class SharePostView(View):
    def post(self,request,pk,*args,**kwargs):
        or_post = Post.objects.get(pk=pk)
        form = ShareForm(request.POST)

        if form.is_valid():
            new_post = Post(
            shared_body = self.request.POST.get('body'),
            post = or_post,
            shared_user = request.user,
            author = or_post.author,
            created_on = or_post.created_on,
            shared_on = timezone.now
            )
            new_post.save()
            for img in or_post.image.all():
                new_post.image.add(img)
            new_post.save()

            return redirect('post_list')

class UserSearch(View):
    def get(self,request,*args,**kwargs):
        query = self.request.GET.get('query')

        profile_lists = UserProfile.objects.filter(Q(user__username__icontains=query))

        posts_lists = Post.objects.filter(Q(body__icontains=query))

        context ={
            'profile_lists':profile_lists,
            'posts_lists':posts_lists,
        }

        return render(request,'social/search.html',context)

class FollowersList(View):
    def get(self,request,pk,*args,**kwargs):
        profile = UserProfile.objects.get(pk=pk)
        followers = profile.followers.all()
        user = profile.user

        context={
            'user':user,
            'profile': profile,
            'followers':followers,
        }

        return render(request,'social/followers_list.html',context)
class CommentLikeView(View):
    def post(self,request,pk,*args,**kwargs):
        comment = Comment.objects.get(pk=pk)

        its_disliked =False
        for dislike in comment.dislikes.all():
            if request.user == dislike:
                its_liked = True
                break
        if its_disliked:
            comment.dislikes.remove(request.user)

        its_liked = False
        for likes in comment.likes.all():
            if likes == request.user:
                its_liked= True
                break
        if its_liked:
            comment.likes.remove(request.user)

        if not its_liked:
            comment.likes.add(request.user)
            notification = Notification.objects.create(
                notification_type=1,
                from_user=request.user,
                to_user=comment.author,
                comment=comment)


        next = request.POST.get('next','/')
        return HttpResponseRedirect(next)

class CommentDislikesView(View):
    def post(self,request,pk,*args,**kwargs):
        comment = Comment.objects.get(pk=pk)

        its_liked = False
        for like in comment.likes.all():
            if like == request.user:
                its_liked= True
                break
        if its_liked:
            comment.likes.remove(request.user)

        its_disliked = False
        for dislikes in comment.dislikes.all():
            if dislikes == request.user:
                its_disliked= True
        if its_disliked:
            comment.dislikes.remove(request.user)

        if not its_disliked:
            comment.dislikes.add(request.user)

        next = request.POST.get('next','/')
        return HttpResponseRedirect(next)

class PostNotifications(View):
    def get(self, request, notification_pk, post_pk,*args,**kwargs):
        post = Post.objects.get(pk=post_pk)
        notification = Notification.objects.get(pk=notification_pk)

        notification.user_has_seen = True
        notification.save()

        return redirect('post_detail',pk=post_pk)

class FollowNotifications(View):
    def get(self, request, notification_pk,profile_pk,*args,**kwargs):
        notification = Notification.objects.get(pk=notification_pk)
        profile = UserProfile.objects.get(pk=profile_pk)

        notification.user_has_seen = True
        notification.save()

        return redirect('profile',pk=profile_pk)

class ThreadNotification(View):
    def get(self,request,notification_pk,thread_pk,*args,**kwargs):
        notification = Notification.objects.get(pk=notification_pk)
        thread = ThreadModel.objects.get(pk=thread_pk)

        notification.user_has_seen =True
        notification.save()

        return redirect('thread', pk= thread_pk)
class RemoveNotification(View):
    def delete(self,request,notification_pk,*args,**kwargs):
        notification = Notification.objects.get(pk=notification_pk)

        notification.user_has_seen = True
        notification.save()
        return HttpResponse('success',content_type='text/plain')
class ListThread(View):
    def get(self,request,*args,**kwargs):
        threads = ThreadModel.objects.filter(Q(user=request.user)| Q(receiver=request.user))

        context = {
        'threads':threads,
        }

        return render(request,'social/inbox.html',context)

class CreateThread(View):
    def get(self,request,*args,**kwargs):
        form = ThreadForm()

        context = {
        'form':form,
        }
        return render(request,'social/create_thread.html',context)

    def post(self,request,*args,**kwargs):
        form = ThreadForm(request.POST)

        username = request.POST.get('username')
        try:
            receiver = User.objects.get(username=username)
            if ThreadModel.objects.filter(user=request.user,receiver=receiver).exists():
                thread = ThreadModel.objects.filter(user=request.user,receiver=receiver)
                return redirect('thread',pk=thread.pk)
            elif ThreadModel.objects.filter(user=receiver,receiver=request.user).exists():
                thread = ThreadModel.objects.filter(user=receiver,receiver=request.user)
                return redirect('thread',pk=thread.pk)

            if form.is_valid():
                thread = ThreadModel(
                    user = request.user ,
                    receiver = receiver
                )
                thread.save()

            return redirect('thread', pk=thread.thread)
        except:
            messages.error(request,'Invalid Username')
            return redirect('create_thread')

class ThreadView(View):
    def get(self,request,pk,*args,**kwargs):
        form = MessageForm()
        thread = ThreadModel.objects.get(pk=pk)
        message_list = MessageModel.objects.filter(thread__pk__contains = pk)

        context = {
        'thread': thread,
        'form':form,
        'message_list':message_list
        }

        return render(request,'social/thread.html',context)

class CreateMessage(View):
    def post(self,request,pk,*args,**kwargs):
        form = MessageForm(request.POST,request.FILES)
        thread = ThreadModel.objects.get(pk=pk)
        if thread.receiver == request.user:
            receiver = thread.user
        else:
            receiver = thread.receiver

        if form.is_valid():
            message = form.save(commit=False)
            message.thread = thread
            message.sender_user = request.user
            message.receiver_user = receiver
            message.save()
        notification = Notification.objects.create(
            notification_type=4,
            to_user = receiver,
            from_user = request.user,
            thread = thread,
        )
        return redirect('thread',pk=pk)
class ExploreView(View):
    def get(self,request,*args,**kwargs):
        explore_form = ExploreForm()
        query = self.request.GET.get('query')
        tags = Tag.objects.filter(name=query).first()

        if tags:
            posts = Post.objects.filter(tags__in =[tags])
        else:
            posts = Post.objects.all()

        context ={
        'explore_form':explore_form,
        'tags':tags,
        'posts':posts
        }

        return render(request,'social/explore.html',context)

    def post(self,request,*args,**kwargs):
        explore_form = ExploreForm()
        if explore_form.is_valid():
            query = explore_form.cleaned_data['query']
            tag = Tag.objects.filter(name=query).first()

            posts = None
            if tag:
                posts = Post.objects.filter(tags__in=[tag])

            if posts:
                context = {
                    'tags':tag,
                    'posts':posts
                }
            else:
                context = {
                    'tags':tag
                }
            return HttpResponseRedirect('/social/explore?query={query}')
        return HttpResponseRedirect('social/explore/')
