from rest_framework import serializers
from market_app.models import Market, Seller, Product
from rest_framework import status


class MarketSerializer(serializers.ModelSerializer):
    class Meta:
        model = Market
        fields = '__all__'

    def validate_name(self, value):
        errors = []
        if 'X' in value:
            errors.append('No X in location.')
        if 'Y' in value:
            errors.append('No Y in location.')

        if errors:    
            raise serializers.ValidationError(errors)
        
        return value

    """ id = serializers.IntegerField(read_only=True)
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
    
    
class SellerDetailSerializer(serializers.Serializer):
    id = serializers.IntegerField(read_only=True)
    name = serializers.CharField(max_length=255)
    contact_info = serializers.CharField(max_length=255)
    """ markets = MarketSerializer(many=True, read_only=True) """
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
        return seller
    

class ProductDetailSerializer(serializers.Serializer):
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
    
