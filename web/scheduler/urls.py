from django.urls import path
from . import views

urlpatterns = [
    # Authentication
    path('', views.landing_view, name='landing'),
    path('signup/', views.signup_view, name='signup'),
    path('login/', views.login_view, name='login'),
    path('logout/', views.logout_view, name='logout'),
    
    # Dashboard
    path('dashboard/', views.dashboard_view, name='dashboard'),
    path('stats-update/', views.stats_update_view, name='stats_update'),
    path('search/', views.search_posts_view, name='search_posts'),
    
    # Posts
    path('posts/new/', views.schedule_post_view, name='schedule_post'),
    path('posts/<int:post_id>/cancel/', views.cancel_post_view, name='cancel_post'),
    path('posts/<int:post_id>/retry/', views.retry_post_view, name='retry_post'),
    path('posts/<int:post_id>/delete/', views.delete_post_view, name='delete_post'),
    
    # Accounts
    path('accounts/', views.accounts_view, name='accounts'),
    path('accounts/<int:account_id>/disconnect/', views.disconnect_account_view, name='disconnect_account'),
]
