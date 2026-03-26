from django import forms
from .models import AssistanceOrder, BookingFlight

#  Assistance Order Form
class AssistanceOrderForm(forms.ModelForm):
    class Meta:
        model = AssistanceOrder 
        fields = ['special_assistance', 'flight', 'note'] 
        widgets = {
            'note': forms.Textarea(attrs={'rows': 3})
        }


#  Booking Flight Form
class BookingFlightForm(forms.ModelForm):
    # Form used to book a flight.
    # - Requires acceptance of travel conditions (checkbox).
    # - Passport image can be uploaded (optional at booking, required for check-in).
    class Meta:
        model = BookingFlight 
        fields = ['flight', 'passport_image', 'Travel_conditions_back', 'extra_info']
        widgets = {
            'extra_info': forms.Textarea(attrs={'rows': 2}),
        }

    def clean_Travel_conditions_back(self):
        # Ensures user has accepted travel terms before allowing booking submission.
        accepted = self.cleaned_data.get('Travel_conditions_back')
        if not accepted:
            raise forms.ValidationError("You must accept the travel conditions to proceed with booking.")
        return accepted


#  Online Check-in Form
class CheckOnlineForm(forms.ModelForm):
    # Form used during online check-in.
    # User uploads passport and confirms travel conditions.
    class Meta:
        model = BookingFlight
        fields = ['passport_image', 'Travel_conditions_back']

    def clean_Travel_conditions_back(self):
        # Prevents submission if user didn't confirm the travel conditions.
        accepted = self.cleaned_data.get('Travel_conditions_back')
        if not accepted:
            raise forms.ValidationError("You must accept travel conditions to complete check-in.")
        return accepted


#  Flight Search Form
class FlightSearchForm(forms.Form):
    # A simple search form to look up flight details and status.
    # - Allows search by flight number OR flight ID.
    # - Flight ID (a unique numeric database ID), or Flight Number (like “QR202” or “EK105”).

    flight_id = forms.IntegerField(
        required=False, 
        label="Flight ID", 
        help_text="Search flight by ID (optional)." 
    )

    flight_number = forms.CharField(
        required=False,
        max_length=20, 
        label="Flight Number",
        help_text="Search flight by number (optional)."
    )

    def clean(self):
        # Custom validation to ensure at least one field is provided.
        cleaned_data = super().clean()
        flight_id = cleaned_data.get("flight_id") 
        flight_number = cleaned_data.get("flight_number") 

        if not flight_id and not flight_number:
            raise forms.ValidationError("Please enter either a Flight ID or a Flight Number to search.")

        return cleaned_data 