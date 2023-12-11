from .views import PostListView, PostDetailView


from django.urls import path



urlpatterns = [
    path('', PostListView.as_view(), name='home'),
    path('post/<str:slug>/', PostDetailView.as_view(), name='post_detail'),
]




