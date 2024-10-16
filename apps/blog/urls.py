from .views import PostListView, PostDetailView, PostFromCategory


from django.urls import path



urlpatterns = [
    path('', PostListView.as_view(), name='home'),
    path('post/<str:slug>/', PostDetailView.as_view(), name='post_detail'),
    path('category/<str:slug>/', PostFromCategory.as_view(), name='posts_by_category'),
]




