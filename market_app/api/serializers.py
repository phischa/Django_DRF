from rest_framework import serializers
from market_app.models import Market
from rest_framework import status

def validate_no_X(value):
        errors = []
        if 'X' in value:
            errors.append('No X in location.')
        if 'Y' in value:
            errors.append('No Y in location.')

        if errors:    
            raise serializers.ValidationError(errors)
        
        return value

class MarketSerializer(serializers.Serializer):
    id = serializers.IntegerField(read_only=True)
    name = serializers.CharField(max_length=255)
    location = serializers.CharField(max_length=255, validators=[validate_no_X])
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
        return instance