from django.db import models
from django.utils.translation import gettext_lazy as _
from django.core.validators import MinValueValidator
from django.conf import settings
from django.urls import reverse


# Create your models here.

# Model to represent a flight booking
class BookingFlight(models.Model):
    STATUS_PENDING = 'PENDING'
    STATUS_CONFIRMED = 'CONFIRMED'
    STATUS_CANCELLED = 'CANCELLED'
    STATUS_REJECTED = 'REJECTED'
    STATUS_COMPLETED = 'COMPLETED'
    STATUS_EXPIRED = 'EXPIRED'
    STATUS_REFUNDED = 'REFUNDED'
    STATUS_CHECKED_IN = 'CHECKED_IN'
    STATUS_WAITING_BACK = 'WAITING_BACK_FLIGHT'

    STATUS_CHOICES = [
        (STATUS_PENDING, 'Pending'),
        (STATUS_CONFIRMED, 'Confirmed'),
        (STATUS_CANCELLED, 'Cancelled'),
        (STATUS_REJECTED, 'Rejected'),
        (STATUS_COMPLETED, 'Completed'),
        (STATUS_EXPIRED, 'Expired'),
        (STATUS_REFUNDED, 'Refunded'),
        (STATUS_CHECKED_IN, 'Checked-in'),
        (STATUS_WAITING_BACK, 'Waiting for Return Flight'),
    ]

    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='bookings',
        verbose_name=_("User"),
        help_text=_("User who created the booking.")
    )

    FLIGHT_ONE = 'one_direction'
    FLIGHT_TWO = 'two_direction'

    FLIGHT_TYPE_CHOICES = [
        (FLIGHT_ONE, "One Direction"),
        (FLIGHT_TWO, "Two Direction"),
    ]

    flight_type = models.CharField(
        max_length=20,
        choices=FLIGHT_TYPE_CHOICES,
        default=FLIGHT_ONE,
        verbose_name=_("Flight Type"),
        help_text=_("Is the booking one-way or round-trip?")
    )

    flight_go = models.ForeignKey(
        'Flight.Flight',
        on_delete=models.CASCADE,
        related_name='bookings_go',
        verbose_name=_("Outbound Flight"),
        help_text=_("The outbound flight for this booking.")
    )

    flight_back = models.ForeignKey(
        'Flight.Flight',
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='bookings_back',
        verbose_name=_("Return Flight"),
        help_text=_("Return flight for two-direction bookings.")
    )

    booking_date = models.DateTimeField(
        auto_now_add=True,
        verbose_name=_("Booking Date")
    )

    status = models.CharField(
        max_length=25,
        choices=STATUS_CHOICES,
        default=STATUS_PENDING,
        verbose_name=_("Status"),
        help_text=_(
            "PENDING: Awaiting payment; CONFIRMED: Paid; CANCELLED: User canceled; "
            "REJECTED: Airline rejected; COMPLETED: Trip finished; EXPIRED: Not confirmed; "
            "REFUNDED: Money refunded; CHECKED_IN: User checked in; "
            "WAITING_BACK_FLIGHT: Round-trip, outbound flight completed."
        )
    )

    chears = models.PositiveIntegerField(
        verbose_name=_("Seats Booked"),
        help_text=_("How many seats were booked?")
    )

    chears_checked_in_go = models.PositiveIntegerField(
        default=0,
        verbose_name=_("Checked-In Seats (Outbound)"),
        help_text=_("How many seats have completed check-in for outbound flight?")
    )

    chears_checked_in_back = models.PositiveIntegerField(
        default=0,
        null=True,
        blank=True,
        verbose_name=_("Checked-In Seats (Return)"),
        help_text=_("How many seats have completed check-in for return flight?")
    )

    CHEAR_TYPE_CHOICES = [
        ("Economy", "Economy Class"),
        ("Premium", "Premium Economy"),
        ("Business", "Business Class"),
        ("First", "First Class"),
    ]

    chear_type = models.CharField(
        max_length=20,
        choices=CHEAR_TYPE_CHOICES,
        verbose_name=_("Seat Class"),
        help_text=_("Seat class chosen for this booking.")
    )

    price = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        verbose_name=_("Total Price"),
        help_text=_("Total cost of the booking.")
    )

    is_payed = models.BooleanField(
        default=False,
        verbose_name=_("Is Payed"),
        help_text=_("Has the booking been paid?")
    )

    updated_at = models.DateTimeField(
        auto_now=True,
        verbose_name=_("Updated at")
    )

    class Meta:
        verbose_name = _("Flight Booking")
        verbose_name_plural = _("Flight Bookings")
        ordering = ['-booking_date']

    def __str__(self):
        return f"Booking#{self.pk} - {self.user} - {self.flight_go}"

    def get_absolute_url(self):
        return reverse('service:manage_booking_detail', kwargs={'pk': self.pk})


# Model that represents a special assistance service offered to passengers.
class SpecialAssistance(models.Model):
    # ASSISTANCE_CHOICES = [
    #     ('WHEELCHAIR', 'Wheelchair Request'),
    #     ('BOARDING', 'Arrange assistance with boarding the aircraft'),
    #     ('DISEMBARK', 'Arrange assistance with disembarking the aircraft'),
    #     ('ELDER_CHILD', 'Support for the elderly or children traveling alone'),
    # ]

    # assistance_type = models.CharField(
    #     max_length=50,
    #     choices=ASSISTANCE_CHOICES, 
    #     verbose_name=_("Assistance Type"), 
    #     help_text=_("Type of assistance (e.g., wheelchair, boarding help).") 
    # )

    price = models.DecimalField(
        max_digits=8,
        decimal_places=2,
        validators=[MinValueValidator(0.00)], 
        default=100.00,
        verbose_name=_("Price"),
        help_text=_("Price in site currency.")
    )

    assistance = models.TextField(
        verbose_name=_("Assistance"),
        help_text=_("Assistance details.")
    )

    created_at = models.DateTimeField(auto_now_add=True, verbose_name=_("Created at"))
    updated_at = models.DateTimeField(auto_now=True, verbose_name=_("Updated at"))

    def __str__(self):
        return f"{self.assistance} - {self.price}"

    class Meta: 
        verbose_name = _("Special Assistance")
        verbose_name_plural = _("Special Assistances") 
        ordering = ['-created_at']


# Model to store a user's online request for a special assistance service
class AssistanceOrder(models.Model):
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='assistance_orders',
        verbose_name=_("User"),
        help_text=_("User who made the assistance request.")
    )

    special_assistance = models.ForeignKey(
        SpecialAssistance,
        on_delete=models.PROTECT,
        related_name='orders',
        verbose_name=_("Special Assistance"),
        help_text=_("Which assistance service the user requested.")
    )

    booking_flight = models.ForeignKey(
        BookingFlight,
        on_delete=models.CASCADE,
        related_name='assistance_orders',
        verbose_name=_("Booking Flight"),
        help_text=_("Booking Flight for which the assistance is requested."),
        default=1
    )

    note = models.TextField(
        blank=True, 
        verbose_name=_("Note"), 
        help_text=_("Extra info from the user.")
    )

    created_at = models.DateTimeField(
        auto_now_add=True, 
        verbose_name=_("Requested at")
    )

    STATE_CHOICES = [
        ('pinned', "Order placed and payment pending"),
        ('ready', "Payment has been made and the service is ready"), 
        ('done', "The journey has been completed"),
        ('rejected', "The service has been cancelled by the company"),
        ('canceled', "The service was cancelled by the customer"),
        ('refunded', "Money has been refunded"), 
    ]

    state = models.CharField(
        max_length=20,
        choices=STATE_CHOICES,
        default='pinned',
        verbose_name=_("State"),
        help_text=_("Current status of the assistance request.")
    )

    is_payed = models.BooleanField(
        default=False,
        verbose_name=_("Is Payed"),
        help_text=_("Has the service been paid for?")
    )

    class Meta:
        verbose_name = _("Assistance Order")
        verbose_name_plural = _("Assistance Orders")
        ordering = ['-created_at']

    def __str__(self):
        return f"AssistanceOrder#{self.pk} by {self.user}"

