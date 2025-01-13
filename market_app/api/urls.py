from django.urls import path
from .views import MarketsView, MarketDetailView, SellersView, SellerDetailView, \
ProductView, ProductDetailView

urlpatterns = [
    path('market/', MarketsView.as_view()),
    path('market/<int:pk>/', MarketDetailView.as_view(), name='market-detail'),
    path('seller/', SellersView.as_view()),
    path('seller/<int:pk>/', SellerDetailView.as_view()),
    path('product/', ProductView.as_view()),
    path('product/<int:pk>/', ProductDetailView.as_view()),
]