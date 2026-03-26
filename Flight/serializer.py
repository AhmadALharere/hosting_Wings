from rest_framework import serializers
from .models import Airport,Destination,Travel_Condition,Travel_Conditions_Group,Flight
from cloudinary import CloudinaryImage

class airport_serializer(serializers.ModelSerializer):

    icon = serializers.SerializerMethodField()
    class Meta:
        model = Airport
        fields = ['id','name','destination','rate','icon']
    
    def get_icon(self, obj):
        if obj.icon:
            return CloudinaryImage(obj.icon.public_id).build_url()
        return None

    
    
class travel_cond_serializer(serializers.ModelSerializer):
    
    icon = serializers.SerializerMethodField()
    
    class Meta:
        model = Travel_Condition
        fields = ['id','name','Description','icon']
        
    def get_icon(self, obj):
        if obj.icon:
            return CloudinaryImage(obj.icon.public_id).build_url()
        return None

    

class travel_cond_group_serializer(serializers.ModelSerializer):
    
    conditions = travel_cond_serializer(many = True,read_only = True)
    
    class Meta:
        model = Travel_Conditions_Group
        fields = ['name','Description','conditions']
    

        
class destination_serializer(serializers.ModelSerializer):
    
    airports = airport_serializer(many=True, read_only=True)
    travel_cond_group_go = travel_cond_group_serializer(many=True, read_only=True)
    travel_cond_group_back = travel_cond_group_serializer(many=True, read_only=True)
    image = serializers.SerializerMethodField()
    
    class Meta:
        model = Destination
        fields = ['country','city','Bio','slug','landmarks','image','static_rate','avg_rate','airports','travel_cond_group_go','travel_cond_group_back']

    def get_image(self, obj):
        if obj.image:
            return CloudinaryImage(obj.image.public_id).build_url()
        return None


        
class Flight_serializer(serializers.ModelSerializer):
    
    counterpart = serializers.StringRelatedField()
    counterpart_airport = serializers.StringRelatedField()
    class Meta:
        model = Flight
        fields = ['flight_number','type','Economy_Class_Num','Economy_Class_available','Economy_Class_price','Premium_Economy_Num','Premium_Economy_available','Premium_Economy_price','Business_Class_Num','Business_Class_available','Business_Class_price','First_Class_Num','First_Class_Num_available','First_Class_price','counterpart','counterpart_airport','scheduled_departure','scheduled_arrival','gate','status']


class Flight_serializer_Retrieve(serializers.ModelSerializer):
    
    counterpart = destination_serializer(read_only = True)
    counterpart_airport = airport_serializer(read_only = True)
            
    class Meta:
        model = Flight
        fields = ['flight_number','type','Economy_Class_Num','Economy_Class_available','Economy_Class_price','Premium_Economy_Num','Premium_Economy_available','Premium_Economy_price','Business_Class_Num','Business_Class_available','Business_Class_price','First_Class_Num','First_Class_Num_available','First_Class_price','counterpart','counterpart_airport','scheduled_departure','scheduled_arrival','gate','status']


