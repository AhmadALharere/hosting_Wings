from rest_framework import serializers
from .models import profile
from django.contrib.auth.models import User
from dj_rest_auth.registration.serializers import RegisterSerializer
from cloudinary import CloudinaryImage

class CustomRegisterSerializer(RegisterSerializer):
    
    birth_date = serializers.DateField(required=True,input_formats=['%d/%m/%Y'])
    gender = serializers.CharField(required=True)
    phone_number = serializers.CharField(required=True)
    image = serializers.ImageField(required=False, allow_null=True)
    
    
    def validate_email(self, value):
        print("validate_email called!")
        if User.objects.filter(email__iexact=value).exists():
            raise serializers.ValidationError("Email is already in use.")
        return value

    def save(self, request):
        if profile.objects.filter(phone_number__iexact=self.validated_data['phone_number']).exists():
            raise serializers.ValidationError("phone number is already in use.")   
        user = super().save(request)
        try:
            profile.objects.create(
                user=user,
                birth_date=self.validated_data['birth_date'],
                gender=self.validated_data['gender'],
                phone_number=self.validated_data['phone_number'],
                total_booked = 0,
                total_payment = 0,
                Loyal_points = 0,
                image = self.validated_data.get('image') if self.validated_data.get('image') else None
            )
        except Exception as ex:
            profile.objects.create(
                user=user,
                birth_date="1/1/2000",
                gender="Male",
                phone_number=None,
                total_booked = 0,
                total_payment = 0,
                Loyal_points = 0,
                image =None
            )
        return user


class User_Serializer(serializers.ModelSerializer):
     # بيانات من User (للعرض فقط)
  
    class Meta:
        model = User
        fields = ['first_name','last_name','email']
        


class Profile_Serializer(serializers.ModelSerializer):
    
    username = serializers.CharField(source='user.username', required=False, read_only=True)
    email = serializers.EmailField(source='user.email', read_only=True)
    birth_date = serializers.DateField(required=False, input_formats=['%d/%m/%Y'])
    phone_number = serializers.CharField(required=False,read_only=True)
    # بيانات من User (قابلة للتعديل)
    first_name = serializers.CharField(source='user.first_name', required=False)
    last_name = serializers.CharField(source='user.last_name', required=False)
    image = serializers.ImageField(required=False)
    class Meta:
        model = profile
        fields =['username','email','first_name','last_name','birth_date','phone_number','gender','image']
    
    
    def to_representation(self, instance):
        data = super().to_representation(instance)

        # تحويل الصورة إلى رابط Cloudinary
        if instance.image:
            data['image'] = instance.image.url

        return data
    def update(self, instance, validated_data):
        # فصل بيانات user عن باقي الحقول
            user_data = validated_data.pop('user', {})

        # تعديل الاسم الأول والأخير فقط
            user = instance.user
            user.first_name = user_data.get('first_name', user.first_name)
            user.last_name = user_data.get('last_name', user.last_name)
            user.birth_date = validated_data.get('birth_date', instance.birth_date)
            #check if there is an image uploaded then update it (the images on cloudinary) else keep the old one
            user.save()

        # تعديل حقول البروفايل
            for attr, value in validated_data.items():
                setattr(instance, attr, value)
            instance.save()

            return instance

