from rest_framework import serializers
from companies.models import Company, Storage

class CompanySerializer(serializers.ModelSerializer):
    owner_email = serializers.EmailField(source='owner.email', read_only=True)
    
    class Meta:
        model = Company
        fields = ('id', 'title', 'inn', 'owner', 'owner_email')
    
class StorageSerializer(serializers.ModelSerializer):
    company_title = serializers.CharField(source='company.title', read_only=True)
    
    class Meta:
        model = Storage
        fields = ('id', 'address', 'company', 'company_title')        

class AttachUserSerializer(serializers.Serializer):
    email = serializers.EmailField()     