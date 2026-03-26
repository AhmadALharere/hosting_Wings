from rest_framework import serializers
from .models import BookingFlight, SpecialAssistance, AssistanceOrder


# ---------------------- BOOKING SERIALIZERS ------------------------------

class BookingSerializer(serializers.ModelSerializer):
    class Meta:
        model = BookingFlight
        fields = '__all__'
        read_only_fields = [
            'id', 'user', 'booking_date', 'updated_at', 'status', 'is_payed'
        ]


class BookingCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = BookingFlight
        fields = [
            "flight_type", "flight_go", "flight_back", "chears", "chears_checked_in_go", "chears_checked_in_back", "chear_type"
        ]
        extra_kwargs = {
            "flight_back": {"required": False, "allow_null": True},
            "chears_checked_in_back": {"required": False, "allow_null": True},
        }

    # Validate flight type
    def validate(self, data):
        flight_type = data.get("flight_type")
        flight_go = data.get("flight_go")
        flight_back = data.get("flight_back")
        chears = data.get("chears")
        chears_checked_in_go = data.get("chears_checked_in_go")
        chears_checked_in_back = data.get("chears_checked_in_back") or 0
        chear_type = data.get("chear_type")

        # Validate from chears number
        if chears != chears_checked_in_go + chears_checked_in_back :
            raise serializers.ValidationError(
                {"Details": "Number of intired chears isn't correct."}
            )

        # Validate round-trip requirements
        if flight_type == BookingFlight.FLIGHT_TWO and not flight_back:
            raise serializers.ValidationError(
                {"flight_back": "Return flight is required for two-direction booking."}
            )

        if flight_type == BookingFlight.FLIGHT_ONE and flight_back:
            raise serializers.ValidationError(
                {"flight_back": "One-way booking cannot include a return flight."}
            )

        # Check if enough seats are available on both flights
        seat_field = self.get_seat_field(chear_type)

        # Check outbound flight
        available_go = getattr(flight_go, seat_field)
        if available_go < chears_checked_in_go:
            raise serializers.ValidationError({
                "detail": f"Not enough available seats in outbound flight. Available: {available_go}"
            })

        # Check return flight
        if flight_type == BookingFlight.FLIGHT_TWO:
            available_back = getattr(flight_back, seat_field)
            if available_back < chears_checked_in_back:
                raise serializers.ValidationError({
                    "detail": f"Not enough available seats in return flight. Available: {available_back}"
                })

        return data

    # Map seat type to corresponding available seat field in Flight model
    def get_seat_field(self, seat_type):
        return {
            "Economy": "Economy_Class_available",
            "Premium": "Premium_Economy_available",
            "Business": "Business_Class_available",
            "First": "First_Class_Num_available",
        }[seat_type]

    # Create booking, deduct seats, calculate total price
    def create(self, validated_data):
        request = self.context["request"]
        user = request.user

        flight_go = validated_data["flight_go"]
        flight_back = validated_data.get("flight_back")
        seat_type = validated_data["chear_type"]
        chears = validated_data["chears"]
        chears_checked_in_go = validated_data["chears_checked_in_go"]
        chears_checked_in_back = validated_data["chears_checked_in_back"] or 0

        # Get field names
        seat_field = self.get_seat_field(seat_type)
        price_field = self.get_price_field(seat_type)

        # Deduct seats from outbound
        setattr(flight_go, seat_field, getattr(flight_go, seat_field) - chears_checked_in_go)
        flight_go.save()

        total_price = getattr(flight_go, price_field) * chears_checked_in_go

        # Round trip case
        if validated_data["flight_type"] == BookingFlight.FLIGHT_TWO:
            setattr(flight_back, seat_field, getattr(flight_back, seat_field) - chears_checked_in_back)
            flight_back.save()
            total_price += getattr(flight_back, price_field) * chears_checked_in_back

        # Create booking
        booking = BookingFlight.objects.create(
            user=user,
            price=total_price,
            **validated_data
        )

        return booking

    # Map seat type to corresponding price field in Flight model
    def get_price_field(self, seat_type):
        return {
            "Economy": "Economy_Class_price",
            "Premium": "Premium_Economy_price",
            "Business": "Business_Class_price",
            "First": "First_Class_price",
        }[seat_type]


class BookingEditSerializer(serializers.ModelSerializer):
    class Meta:
        model = BookingFlight
        fields = ['flight_go', 'flight_back']
        extra_kwargs = {
            'flight_back': {'required': False, 'allow_null': True},
        }



# -----------------------SPECIAL ASSISTANCE SERIALIZERS -----------------------------

class SpecialAssistanceSerializer(serializers.ModelSerializer):
    class Meta:
        model = SpecialAssistance
        fields = '__all__'


# ------------------------- ASSISTANCE ORDERS SERIALIZERS ---------------------------

class AssistanceOrderSerializer(serializers.ModelSerializer):
    class Meta:
        model = AssistanceOrder
        fields = '__all__'
        read_only_fields = [
            'id', 'user', 'state', 'is_payed', 'created_at'
        ]


class CreateAssistanceOrderSerializer(serializers.ModelSerializer):
    class Meta:
        model = AssistanceOrder
        fields = ['special_assistance', 'booking_flight', 'note', 'state']
