from rest_framework import serializers
from django.contrib.auth.models import User

from .models import Company,KBEntry, QueryLog


class RegisterSerializer(serializers.ModelSerializer):
    company_name = serializers.CharField(write_only=True)

    class Meta:
        model = User
        fields = ["username", "password", "email", "company_name"]
        extra_kwargs = {
            "password": {"write_only": True}
        }

    def create(self, validated_data):
        company_name = validated_data.pop("company_name")

        user = User.objects.create_user(**validated_data)

        user.company.company_name = company_name
        user.company.save()

        return user

class KBEntrySerializer(serializers.ModelSerializer):
    class Meta:
        model = KBEntry
        fields = "__all__"

class QueryLogSerializer(serializers.ModelSerializer):
    class Meta:
        model = QueryLog
        fields = "__all__"

class QuerySerializer(serializers.Serializer):
    question = serializers.CharField() 

class QueryLogSerializer(serializers.ModelSerializer):
    class Meta:
        model = QueryLog
        fields = "__all__"