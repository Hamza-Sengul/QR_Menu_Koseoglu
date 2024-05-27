from django.urls import path
from . import views
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('', views.index, name='home'),
    path('urun/', views.urun, name='urun'),
    path('product_detail/<int:product_id>/', views.product_detail, name='product_detail'),
    # path('category/<int:category_id>/', views.category_products, name='category_products'),
    path('feedback/', views.feedback, name='feedback'),
    path('yeniadmin/', views.admin_page, name='admin_page'),
    path('edit_category/<int:category_id>/', views.edit_category, name='edit_category'),
    path('edit_product/<int:product_id>/', views.edit_product, name='edit_product'),
    path('track-click/<int:product_id>/', views.track_click, name='track_click'),
    path('product/<int:product_id>/click/', views.increment_click_count, name='increment_click_count'),
    path('product/<int:product_id>/', views.urun, name='product_detail'),
    path('category/<int:category_id>/', views.category_products, name='category_products'),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT) + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)