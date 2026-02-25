from django.urls import path
from . import views
urlpatterns=[
    path('',views.home,name="home"),
    path('login/',views.login_view,name="login"),
    path('register/',views.register,name="register"),
    path('admin_dashboard/',views.admin_dashboard,name="admin_dashboard"),
    path('logout/',views.logout_view,name="logout"),
    path('user_dashboard/',views.user_dashboard,name="user_dashboard"),
    path("add-product/", views.add_pc_product, name="add_pc_product"),
    path("products/", views.product_list, name="product_list"),
    path("add-category/", views.add_category, name="add_category"),
    path("book-product/<int:product_id>/", views.book_product, name="book_product"),
    path("your-bookings/", views.your_bookings, name="your_bookings"),

]