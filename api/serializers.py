from rest_framework import serializers
from .models import Owner, Perishable


class OwnerSerializer(serializers.ModelSerializer):
    class Meta:
        model = Owner
        fields = ('id', 'username', 'code')


class CreateOwnerSerializer(serializers.ModelSerializer):
    class Meta:
        model = Owner
        fields = ('username',)


class UpdateOwnerSerializer(serializers.ModelSerializer):
    class Meta:
        model = Perishable
        fields = ('username',)


class PerishableSerializer(serializers.ModelSerializer):
    class Meta:
        model = Perishable
        fields = ('id', 'username', 'p_code', 'title',
                  'img_url', 'qty', 'rtr_date', 'exp',
                  'b_code', 'categories', 'categories_score')


class CreatePerishableSerializer(serializers.ModelSerializer):
    class Meta:
        model = Perishable
        fields = ('username', 'title', 'qty', 'exp',
                  'b_code',)


class CreatePerishableTestSerializer(serializers.ModelSerializer):
    class Meta:
        model = Perishable
        fields = ('title', 'b_code',)


class UpdatePerishableSerializer(serializers.ModelSerializer):
    class Meta:
        model = Perishable
        fields = ('qty', 'exp',)


class DeletePerishableSerializer(serializers.ModelSerializer):
    class Meta:
        model = Perishable
        fields = ('p_code',)
