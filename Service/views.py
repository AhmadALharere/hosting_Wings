from rest_framework import generics, permissions, status
from rest_framework.response import Response
from rest_framework.views import APIView
from django.utils import timezone
from datetime import timedelta

from .models import BookingFlight, SpecialAssistance, AssistanceOrder
from .serializers import *


# ============================ BOOKING API =========================================

class GetBookingsView(generics.ListAPIView):
    serializer_class = BookingSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        return BookingFlight.objects.filter(user=self.request.user)


class BookingDetailsView(generics.RetrieveAPIView):
    serializer_class = BookingSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        return BookingFlight.objects.filter(user=self.request.user)


class BookingCreateView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def post(self, request):
        serializer = BookingCreateSerializer(
            data=request.data,
            context={"request": request}
        )
        if serializer.is_valid():
            booking = serializer.save()
            return Response({
                "detail": "Booking created successfully.",
                "booking_id": booking.id,
                "price": booking.price,
                "data": serializer.data
            }, status=201)
        return Response(serializer.errors, status=400)


class EditBookingView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    # Map seat type to Flight model fields
    SEAT_MAP = {
        "Economy": ("Economy_Class_available", "Economy_Class_price"),
        "Premium": ("Premium_Economy_available", "Premium_Economy_price"),
        "Business": ("Business_Class_available", "Business_Class_price"),
        "First": ("First_Class_Num_available", "First_Class_price"),
    }

    def put(self, request, pk):
        try:
            booking = BookingFlight.objects.get(pk=pk, user=request.user)
        except BookingFlight.DoesNotExist:
            return Response({"detail": "Booking not found."}, status=404)

        now = timezone.now()

        # Check outbound 24h rule
        if booking.flight_go.scheduled_departure <= now + timedelta(hours=24):
            return Response({"detail": "Editing blocked 24h before outbound flight."}, status=400)

        # Check return 24h rule
        if booking.flight_type == BookingFlight.FLIGHT_TWO and booking.flight_back:
            if booking.flight_back.scheduled_departure <= now + timedelta(hours=24):
                return Response({"detail": "Editing blocked 24h before return flight."}, status=400)

        serializer = BookingEditSerializer(booking, data=request.data, partial=True)
        if not serializer.is_valid():
            return Response(serializer.errors, status=400)

        new_go = serializer.validated_data.get("flight_go", booking.flight_go)
        new_back = serializer.validated_data.get("flight_back", booking.flight_back)

        # Destination consistency check
        if new_go.counterpart != booking.flight_go.counterpart or \
           new_go.counterpart_airport != booking.flight_go.counterpart_airport:
            return Response({"detail": "Cannot change destination. Only date/time allowed."}, status=400)

        if booking.flight_type == BookingFlight.FLIGHT_TWO and new_back:
            if new_back.counterpart != booking.flight_back.counterpart or \
               new_back.counterpart_airport != booking.flight_back.counterpart_airport:
                return Response({"detail": "Return flight destination mismatch."}, status=400)

        # Check new flight status
        def flight_status_check(f):
            if f.scheduled_arrival <= now:
                return "This flight is finished."
            if f.scheduled_departure <= now:
                return "This flight is departed."
            return None

        msg = flight_status_check(new_go)
        if msg: return Response({"detail": msg}, status=400)

        if booking.flight_type == BookingFlight.FLIGHT_TWO and new_back:
            msg = flight_status_check(new_back)
            if msg: return Response({"detail": msg}, status=400)

        # Seat checking & Updating
        seat_type = booking.chear_type
        seats_booked = booking.chears
        chears_checked_in_go = booking.chears_checked_in_go
        chears_checked_in_back = booking.chears_checked_in_back or 0

        seat_available_field, seat_price_field = self.SEAT_MAP[seat_type]

        # Outbound change
        if new_go.id != booking.flight_go.id:

            # Check availability
            available = getattr(new_go, seat_available_field)
            if available < chears_checked_in_go:
                return Response({
                    "detail": "Insufficient seats on the new outbound flight."
                }, status=400)

            # Restore seats to old flight
            old_available = getattr(booking.flight_go, seat_available_field)
            setattr(booking.flight_go, seat_available_field, old_available + chears_checked_in_go)
            booking.flight_go.save()

            # Deduct seats from new flight
            setattr(new_go, seat_available_field, available - chears_checked_in_go)
            new_go.save()

            # Update booking
            booking.flight_go = new_go

        # Return flight change
        if booking.flight_type == BookingFlight.FLIGHT_TWO and new_back and new_back.id != booking.flight_back.id:

            available = getattr(new_back, seat_available_field)
            if available < chears_checked_in_back:
                return Response({
                    "detail": "Insufficient seats on the new return flight."
                }, status=400)

            # Restore seats
            old_available = getattr(booking.flight_back, seat_available_field)
            setattr(booking.flight_back, seat_available_field, old_available + chears_checked_in_back)
            booking.flight_back.save()

            # Deduct seats
            setattr(new_back, seat_available_field, available - chears_checked_in_back)
            new_back.save()

            booking.flight_back = new_back

        # Outbound seat price
        new_price = getattr(booking.flight_go, seat_price_field) * chears_checked_in_go

        # Add return price if applicable
        if booking.flight_type == BookingFlight.FLIGHT_TWO and booking.flight_back:
            new_price += getattr(booking.flight_back, seat_price_field) * chears_checked_in_back

        booking.price = new_price

        # Save booking
        booking.save()

        return Response({
            "detail": "Booking updated successfully.",
            "new_price": float(booking.price),
            "booking_id": booking.id
        })


class CancelBookingView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def post(self, request, pk):
        try:
            booking = BookingFlight.objects.get(pk=pk, user=request.user)
        except BookingFlight.DoesNotExist:
            return Response({"detail": "Booking not found."}, status=404)

        # Restore seats to flights
        chears = booking.chears
        seat_type = booking.chear_type
        chears_checked_in_go = booking.chears_checked_in_go
        chears_checked_in_back = booking.chears_checked_in_back or 0

        # Locate seat field
        seat_field = {
            "Economy": "Economy_Class_available",
            "Premium": "Premium_Economy_available",
            "Business": "Business_Class_available",
            "First": "First_Class_Num_available",
        }[seat_type]

        # Add seats back to outbound flight
        flight_go = booking.flight_go
        setattr(flight_go, seat_field, getattr(flight_go, seat_field) + chears_checked_in_go)
        flight_go.save()

        # Add seats back to return flight
        if booking.flight_type == BookingFlight.FLIGHT_TWO and booking.flight_back:
            flight_back = booking.flight_back
            setattr(flight_back, seat_field, getattr(flight_back, seat_field) + chears_checked_in_back)
            flight_back.save()

        booking.status = BookingFlight.STATUS_CANCELLED
        booking.save()

        return Response({"detail": "Booking cancelled and seats restored."})


class RefundBookingView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def post(self, request, pk):
        try:
            booking = BookingFlight.objects.get(pk=pk, user=request.user)
        except BookingFlight.DoesNotExist:
            return Response({"detail": "Booking not found."}, status=404)

        if booking.status != BookingFlight.STATUS_CANCELLED:
            return Response(
                {"detail": "Refund allowed only after cancellation."},
                status=400
            )

        booking.status = BookingFlight.STATUS_REFUNDED
        booking.is_payed = False
        booking.save()

        return Response({"detail": "Refund issued successfully."})


# ============================ SPECIAL ASSISTANCE API =========================================

class SpecialAssistanceListView(generics.ListAPIView):
    serializer_class = SpecialAssistanceSerializer
    queryset = SpecialAssistance.objects.all()


class SpecialAssistanceDetailView(generics.RetrieveAPIView):
    serializer_class = SpecialAssistanceSerializer
    queryset = SpecialAssistance.objects.all()


class UserAssistanceOrdersList(generics.ListAPIView):
    serializer_class = AssistanceOrderSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        return AssistanceOrder.objects.filter(user=self.request.user)


class AssistanceOrderDetailView(generics.RetrieveAPIView):
    serializer_class = AssistanceOrderSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        return AssistanceOrder.objects.filter(user=self.request.user)


class CreateAssistanceOrderView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def post(self, request):
        serializer = CreateAssistanceOrderSerializer(data=request.data)

        if serializer.is_valid():
            serializer.save( user=request.user )
            return Response({"detail": "Special assistance ordered successfully."})

        return Response(serializer.errors, status=400)


class CancelAssistanceOrderView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def post(self, request, pk):
        try:
            order = AssistanceOrder.objects.get(pk=pk, user=request.user)
        except AssistanceOrder.DoesNotExist:
            return Response({"detail": "Order not found."}, status=404)

        order.state = "canceled"
        order.save()

        return Response({"detail": "Special assistance order cancelled."})
