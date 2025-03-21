from rest_framework import serializers

from .models import *


class AccountSerializer(serializers.ModelSerializer):
    class Meta:
        model = Account
        fields = ('id', 'username', 'password', 'first_name', 'image',)

        extra_kwargs = {
            'password': {
                'write_only': True
            }
        }

    def create(self, validated_date):
        return Account.objects.create_user(**validated_date)


class ImageSerilazier(serializers.ModelSerializer):
    class Meta:
        model = Image
        fields = ('id', 'image')


class BookSerilazier(serializers.ModelSerializer):
    images = ImageSerilazier(many=True, read_only=True)

    class Meta:
        model = Book
        fields = '__all__'


class BookPostSerializer(serializers.ModelSerializer):
    class Meta:
        model = Book
        fields = '__all__'

        extra_kwargs = {
            'account': {
                'read_only': True
            }
        }


class BookMarkSoldSerializer(serializers.ModelSerializer):
    class Meta:
        model = Book
        fields = ('id','sold')

        extra_kwargs ={
            'sold':{
                'read_only':True
            }
        }


