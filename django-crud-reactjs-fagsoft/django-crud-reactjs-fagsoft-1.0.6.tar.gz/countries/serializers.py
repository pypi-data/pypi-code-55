from rest_framework import serializers
from .models import City, Country, State


class CountrySerializer(serializers.ModelSerializer):
    to_string = serializers.SerializerMethodField()
    pk = serializers.IntegerField(required=False)

    def create(self, validated_data):
        validated_data['id'] = validated_data.get('pk')
        return super().create(validated_data)

    def get_to_string(self, obj):
        return obj.name

    class Meta:
        model = Country
        fields = [
            'id',
            'pk',
            'to_string',
            'name',
            'iso3',
            'iso2',
            'phone_code',
            'currency',
            'states'
        ]
        extra_kwargs = {
            'id': {'required': False},
        }
        read_only_fields = ['states']


class StateSerializer(serializers.ModelSerializer):
    country_name = serializers.CharField(source='country.name', read_only=True)
    to_string = serializers.SerializerMethodField()
    pk = serializers.IntegerField(required=False)

    def create(self, validated_data):
        validated_data['id'] = validated_data.get('pk')
        return super().create(validated_data)

    def get_to_string(self, obj):
        return obj.name

    class Meta:
        model = State
        fields = [
            'id',
            'pk',
            'to_string',
            'name',
            'country',
            'country_name',
            'state_code',
            'cities',
        ]
        extra_kwargs = {
            'id': {'required': False},
        }
        read_only_fields = ['cities']


class CitySerializer(serializers.ModelSerializer):
    to_string = serializers.SerializerMethodField()
    pk = serializers.IntegerField(required=False)

    def create(self, validated_data):
        validated_data['id'] = validated_data.get('pk')
        return super().create(validated_data)

    def get_to_string(self, obj):
        return obj.name

    class Meta:
        model = City
        fields = [
            'pk',
            'id',
            'to_string',
            'name',
            'state'
        ]
        extra_kwargs = {
            'id': {'required': False},
        }


class CityWithDetailSerializer(CitySerializer):
    def get_to_string(self, obj):
        return '%s-%s-%s' % (obj.state.country.name, obj.state.name, obj.name)


class CountryWithDetailSerializer(CountrySerializer):
    states = StateSerializer(read_only=True, many=True)


class StateWithDetailSerializer(StateSerializer):
    cities = CitySerializer(many=True, read_only=True)
