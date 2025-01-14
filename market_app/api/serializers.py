from rest_framework import serializers
from market_app.models import Market, Seller, Product
from rest_framework import status


class MarketSerializer(serializers.ModelSerializer):

    sellers = serializers.StringRelatedField(many=True, read_only=True)

    class Meta:
        model = Market
        #fields = ['id', 'name', 'location', 'description', 'net_worth'] entweder fields oder exclude
        exclude = []

    def validate_name(self, value):
        errors = []
        if 'X' in value:
            errors.append('No X in location.')
        if 'Y' in value:
            errors.append('No Y in location.')
            
        if errors:    
            raise serializers.ValidationError(errors)
        return value
    

class MarketHyperlinkedSerializer(MarketSerializer, serializers.HyperlinkedModelSerializer):
                            #erbt vom MarketSerializer
    sellers = None

    class Meta:
        model = Market
        fields = ['id', 'url', 'name', 'location', 'description', 'net_worth']

    def __init__(self, *args, **kwargs):
        # Don't pass the 'fields' arg up to the superclass
        fields = kwargs.pop('fields', None)

        # Instantiate the superclass normally
        super().__init__(*args, **kwargs)

        if fields is not None:
            # Drop any fields that are not specified in the `fields` argument.
            allowed = set(fields)
            existing = set(self.fields)
            for field_name in existing - allowed:
                self.fields.pop(field_name)
    

class SellerSerializer(serializers.ModelSerializer):
    markets = MarketSerializer(many=True, read_only=True) 
    market_ids = serializers.PrimaryKeyRelatedField(
        queryset=Market.objects.all(),
        many=True,
        write_only=True,
        source='markets'
    )
    market_count = serializers.SerializerMethodField()
    
    class Meta:
        model = Seller
        fields = ['id', 'market_ids', 'name', 'contact_info', 'markets', 'market_count' ]

    def get_market_count(self, obj):
        return obj.markets.count()
    
class SellerListSerializer(SellerSerializer, serializers.HyperlinkedModelSerializer):

    class Meta:
        model = Seller
        fields = ['url', 'market_ids', 'name', 'contact_info', 'market_count' ]

    
class SellerHyperlinkedSerializer(SellerSerializer, serializers.HyperlinkedModelSerializer):
    markets = MarketSerializer(many=True, read_only=True)
    market_ids = serializers.PrimaryKeyRelatedField(
        queryset=Market.objects.all(),
        many=True,
        write_only=True,
        source='markets'
    )
    market_count = serializers.SerializerMethodField()

    class Meta:
        model = Seller
        fields = ['id', 'market_ids', 'name', 'contact_info', 'markets', 'market_count' ]

    def get_market_count(self, obj):
        return obj.markets.count()
    
class ProductSerializer(serializers.ModelSerializer):
    
    class Meta:
        model = Product
        exclude = []








    """ class MarketSerializer(serializers.Serializer):
    id = serializers.IntegerField(read_only=True)
    name = serializers.CharField(max_length=255)
    location = serializers.CharField(max_length=255) #validators=[validate_no_X]
    description = serializers.CharField()
    net_worth = serializers.DecimalField(max_digits=10, decimal_places=2)

    def create(self, validated_data):
        return Market.objects.create(**validated_data)
    
    def update(self, instance, validated_data):
        instance.name = validated_data.get('name', instance.name)
        instance.location = validated_data.get('location', instance.location)
        instance.description = validated_data.get('description', instance.description)
        instance.net_worth = validated_data.get('net_worth', instance.net_worth)
        instance.save()
        return instance """
    
    
""" class SellerDetailSerializer(serializers.Serializer):
    id = serializers.IntegerField(read_only=True)
    name = serializers.CharField(max_length=255)
    contact_info = serializers.CharField(max_length=255)
    #markets = MarketSerializer(many=True, read_only=True)
    markets = serializers.StringRelatedField(many=True)

class SellerCreateSerializer(serializers.Serializer):
    name = serializers.CharField(max_length=255)
    contact_info = serializers.CharField(max_length=255)
    markets = serializers.ListField(child=serializers.IntegerField(), write_only=True)

    def validate_markets(self, value):
        markets = Market.objects.filter(id__in=value)
        if len(markets) != len(value):
            raise serializers.ValidationError("One or more MarketIDs not found!")
        return value
    
    def create(self, validated_data):
        market_ids = validated_data.pop("markets")
        seller = Seller.objects.create(**validated_data)
        markets_list = Market.objects.filter(id__in=market_ids)
        seller.markets.set(markets_list)
        return seller """

""" class ProductDetailSerializer(serializers.Serializer):
    id = serializers.IntegerField(read_only=True)
    name = serializers.CharField(max_length=255)
    description = serializers.CharField(max_length=255)
    price = serializers.DecimalField(max_digits=10, decimal_places=2)
    market = serializers.StringRelatedField()
    seller = serializers.StringRelatedField()

class ProductCreateSerializer(serializers.Serializer):
    name = serializers.CharField(max_length=255)
    description = serializers.CharField(max_length=255)
    price = serializers.DecimalField(max_digits=10, decimal_places=2)
    market = serializers.IntegerField(write_only=True)
    seller = serializers.IntegerField(write_only=True)

    def validate_market(self, value):
        if not Market.objects.filter(id=value).exists():
            raise serializers.ValidationError("Market with this ID does not exist.")
        return value

    def validate_seller(self, value):
        if not Seller.objects.filter(id=value).exists():
            raise serializers.ValidationError("Seller with this ID does not exist.")
        return value

    def create(self, validated_data):
        market_id = validated_data.pop("market")
        seller_id = validated_data.pop("seller")

        market = Market.objects.get(id=market_id)
        seller = Seller.objects.get(id=seller_id)

        product = Product.objects.create(
            market=market,
            seller=seller,
            **validated_data
        )
        return product
    
"""