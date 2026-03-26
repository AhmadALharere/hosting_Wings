from django.urls import path
from .views import *

app_name = "service"

urlpatterns = [
    # ------------------- BOOKINGS -------------------
    path("booking/", GetBookingsView.as_view(), name="get_booking"),
    path("booking/<int:pk>/", BookingDetailsView.as_view(), name="booking_details"),
    path("booking/create/", BookingCreateView.as_view(), name="create_booking"),
    path("booking/<int:pk>/edit/", EditBookingView.as_view(), name="edit_booking"),
    path("booking/<int:pk>/cancel/", CancelBookingView.as_view(), name="cancel_booking"),
    path("booking/<int:pk>/refund/", RefundBookingView.as_view(), name="refund_booking"),

    # ------------------- ASSISTANCE -------------------
    path("assistance/", SpecialAssistanceListView.as_view(), name="special_assistance_list"),
    path("assistance/<int:pk>/", SpecialAssistanceDetailView.as_view(), name="special_assistance_detail"),

    path("assistance/orders/", UserAssistanceOrdersList.as_view(), name="special_assistance_ordered_list"),
    path("assistance/order/<int:pk>/", AssistanceOrderDetailView.as_view(), name="special_assistance_ordered_details"),

    path("assistance/order/create/", CreateAssistanceOrderView.as_view(), name="order_special_assistance"),
    path("assistance/order/<int:pk>/cancel/", CancelAssistanceOrderView.as_view(), name="cancel_special_assistance"),
]