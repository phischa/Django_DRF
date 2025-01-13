from rest_framework.response import Response
from django.shortcuts import get_object_or_404
from market_app.models import Market, Seller, Product

from .serializers import MarketSerializer, MarketHyperlinkedSerializer, SellerSerializer, \
    SellerHyperlinkedSerializer, SellerListSerializer, ProductSerializer

from rest_framework import mixins, generics, viewsets



class ListRetrieveViewSet(mixins.ListModelMixin,            #könnte z.B. an ProductViewSet vererbt werden
                            mixins.RetrieveModelMixin,      #dadurch könnte man nur List zeigen und retrieven
                                viewsets.GenericViewSet):
    pass


class ProductViewSet(viewsets.ModelViewSet):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer

""" class ProductViewSetOld(viewsets.ViewSet):
    queryset = Product.objects.all()
    def list(self, request):
        serializer = ProductSerializer(self.queryset, many=True)
        return Response(serializer.data)

    def retrieve(self, request, pk=None):
        product = get_object_or_404(self.queryset, pk=pk)
        serializer = ProductSerializer(product)
        return Response(serializer.data)
    
    def create(self, request):
        serializer = ProductSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        else:
            return Response(serializer.errors)

    def destroy(self, request, pk=None):
        product = get_object_or_404(self.queryset, pk=pk)
        serializer = ProductSerializer(self.queryset, pk=pk)
        product.delete()
        return Response(serializer.data) """


class MarketsView(generics.ListCreateAPIView): 
    #mixins.ListModelMixin, mixins.CreateModelMixin, generics.GenericAPIView
    queryset = Market.objects.all()
    serializer_class = MarketHyperlinkedSerializer
    
class MarketDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Market.objects.all()
    serializer_class = MarketSerializer


class SellerOfMarketList(generics.ListAPIView):
    serializer_class = SellerListSerializer

    def get_queryset(self):
        pk = self.kwargs.get('pk')
        market = Market.objects.get(pk = pk)
        return market.sellers.all()
    
    def perform_create(self, serializer):
        pk = self.kwargs.get('pk')
        market = Market.objects.get(pk = pk)
        serializer.save(markets=[market])



class SellersView(mixins.ListModelMixin,
                mixins.CreateModelMixin,
                generics.GenericAPIView):

    queryset = Seller.objects.all()
    serializer_class = SellerHyperlinkedSerializer

    def get(self, request, *args, **kwargs):
        return self.list(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        return self.create(request, *args, **kwargs)
    
class SellerDetailView(mixins.RetrieveModelMixin,
                    mixins.UpdateModelMixin,
                    mixins.DestroyModelMixin,
                    generics.GenericAPIView):
    
    queryset = Seller.objects.all()
    serializer_class = SellerListSerializer

    def get(self, request, *args, **kwargs):
        return self.retrieve(request, *args, **kwargs)

    def put(self, request, *args, **kwargs):
        return self.update(request, *args, **kwargs)

    def delete(self, request, *args, **kwargs):
        return self.destroy(request, *args, **kwargs)
    

class ProductView(mixins.ListModelMixin,
                mixins.CreateModelMixin,
                generics.GenericAPIView):

    queryset = Product.objects.all()
    serializer_class = ProductSerializer

    def get(self, request, *args, **kwargs):
        return self.list(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        return self.create(request, *args, **kwargs)

class ProductDetailView(mixins.RetrieveModelMixin,
                    mixins.UpdateModelMixin,
                    mixins.DestroyModelMixin,
                    generics.GenericAPIView):
    
    queryset = Product.objects.all()
    serializer_class = ProductSerializer

    def get(self, request, *args, **kwargs):
        return self.retrieve(request, *args, **kwargs)

    def put(self, request, *args, **kwargs):
        return self.update(request, *args, **kwargs)

    def delete(self, request, *args, **kwargs):
        return self.destroy(request, *args, **kwargs)

""" class MarketDetailView(mixins.RetrieveModelMixin,
                    mixins.UpdateModelMixin,
                    mixins.DestroyModelMixin,
                    generics.GenericAPIView):
    
    queryset = Market.objects.all()
    serializer_class = MarketSerializer

    def get(self, request, *args, **kwargs):
        return self.retrieve(request, *args, **kwargs)

    def put(self, request, *args, **kwargs):
        return self.update(request, *args, **kwargs)

    def delete(self, request, *args, **kwargs):
        return self.destroy(request, *args, **kwargs) """

""" @api_view(['GET','POST'])
def markets_view(request):

    if request.method == 'GET':
        markets = Market.objects.all()
        serializer = MarketHyperlinkedSerializer(markets, many=True, context={'request': request}, fields=('id', 'name'))
        return Response(serializer.data)
    
    if request.method == 'POST':
        serializer = MarketSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST) """

""" try:
            msg = request.data['message']
            return Response({"your_message": msg}, status=status.HTTP_201_CREATED)
        except:
            return Response({"message": "error"}, status=status.HTTP_400_BAD_REQUEST) """


""" @api_view(['GET', 'DELETE', 'PUT'])
def market_single_view(request, pk):

    if request.method == 'GET':
        market = Market.objects.get(pk=pk)
        serializer = MarketSerializer(market, context={'request': request})
        return Response(serializer.data)

    if request.method == 'PUT':
        market = Market.objects.get(pk=pk)
        serializer = MarketSerializer(market, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        else:
            return Response(serializer.errors)

    if request.method == 'DELETE':
        market = Market.objects.get(pk=pk)
        serializer = MarketSerializer(market)
        market.delete()
        return Response(serializer.data)
"""

""" @api_view(['GET', 'POST'])
def sellers_view(request):

    if request.method == 'GET':
        sellers = Seller.objects.all()
        serializer = SellerHyperlinkedSerializer(
            sellers, many=True, context={'request': request})
        return Response(serializer.data)

    if request.method == 'POST':
        serializer = SellerSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        else:
            return Response(serializer.errors) """


""" @api_view(['GET', 'DELETE', 'PUT'])
def seller_single_view(request, pk):

    if request.method == 'GET':
        seller = Seller.objects.get(pk=pk)
        serializer = SellerSerializer(seller)
        return Response(serializer.data)

    if request.method == 'PUT':
        seller = Seller.objects.get(pk=pk)
        serializer = SellerSerializer(seller, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        else:
            return Response(serializer.errors)

    if request.method == 'DELETE':
        seller = Seller.objects.get(pk=pk)
        serializer = SellerSerializer(seller)
        seller.delete()
        return Response(serializer.data) """


""" @api_view(['GET', 'POST'])
def products_view(request):

    if request.method == 'GET':
        products = Product.objects.all()
        serializer = ProductSerializer(products, many=True)
        return Response(serializer.data)

    if request.method == 'POST':
        serializer = ProductSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        else:
            return Response(serializer.errors)


@api_view(['GET', 'DELETE', 'PUT'])
def product_single_view(request, pk):

    if request.method == 'GET':
        product = Product.objects.get(pk=pk)
        serializer = ProductSerializer(product)
        return Response(serializer.data)

    if request.method == 'PUT':
        product = Product.objects.get(pk=pk)
        serializer = ProductSerializer(
            product, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        else:
            return Response(serializer.errors)

    if request.method == 'DELETE':
        product = Product.objects.get(pk=pk)
        serializer = ProductSerializer(product)
        product.delete()
        return Response(serializer.data)"""