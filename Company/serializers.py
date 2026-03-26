from rest_framework import serializers
from .models import SocialAccount, Career, Article, Investor, Partnership, CareerApplication
from cloudinary import CloudinaryImage

class SocialAccountSerializer(serializers.ModelSerializer):
    class Meta:
        model = SocialAccount
        fields = '__all__'


class CareerSerializer(serializers.ModelSerializer):
    class Meta:
        model = Career
        fields = '__all__'


class CareerSubmitSerializer(serializers.ModelSerializer):
    class Meta:
        model = CareerApplication
        fields = ["full_name", "email", "phone", "cv", "message"]


class ArticleSerializer(serializers.ModelSerializer):
    image = serializers.SerializerMethodField()
    
    
    class Meta:
        model = Article
        fields = ['title', 'summary', 'description', 'image', 'published_at']
        
           
    def get_image(self, obj):
        if obj.image:
            return CloudinaryImage(obj.image.public_id).build_url()
        return None



class InvestorSerializer(serializers.ModelSerializer):
    icon = serializers.SerializerMethodField()
    class Meta:
        model = Investor
        fields = ['name', 'icon', 'bio', 'report']
        
    def get_icon(self, obj):
        if obj.icon:
            return CloudinaryImage(obj.icon.public_id).build_url()
        return None


class PartnershipSerializer(serializers.ModelSerializer):
    icon = serializers.SerializerMethodField()
    class Meta:
        model = Partnership
        fields = ['name', 'icon', 'description', 'business_type', 'link']
        
    def get_icon(self, obj):
        if obj.icon:
            return CloudinaryImage(obj.icon.public_id).build_url()
        return None
