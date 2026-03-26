from django import forms
from .models import Airport,Destination,Travel_Condition,Travel_Conditions_Group,Flight
from dal import autocomplete


class airport_form(forms.ModelForm):
    
    class Meta:
        model = Airport
        fields = "__all__"
    
    
class travel_cond_form(forms.ModelForm):
    
    class Meta:
        model = Travel_Condition
        fields = "__all__"
    

class travel_cond_group_form(forms.ModelForm):
    class Meta:
        model = Travel_Conditions_Group
        fields = ['name','Description','conditions']
        widgets = {
            "conditions": forms.CheckboxSelectMultiple
        }


        
class destination_form(forms.ModelForm):
    
    class Meta:
        model = Destination
        fields = [
            'country','city','Bio','landmarks','image',
            'static_rate','avg_rate',
            'travel_cond_group_go','travel_cond_group_back'
        ]
    
    widgets = {
        'airports': forms.Select(),
        'travel_cond_group_go': forms.CheckboxSelectMultiple(),
        'travel_cond_group_back': forms.CheckboxSelectMultiple(),
    }
    
    

class FlightFormAdmin(forms.ModelForm):
    class Meta:
        model = Flight
        fields = '__all__'
        widgets = {
            'counterpart_airport': autocomplete.ModelSelect2(
                url='Flights:airport-autocomplete',
                forward=['counterpart']  # أهم سطر — علاقة ديناميكية
            )
        }
        
    def clean(self):
        cleaned_data = super().clean()

        destination = cleaned_data.get("counterpart")
        airport = cleaned_data.get("counterpart_airport")

        # لو لم يتم تعبئة الحقلين (أثناء الإنشاء الأول مثلاً)
        if not destination or not airport:
            return cleaned_data

        # يتحقق من أن المطار مرتبط فعلاً بالوجهة المختارة
        if airport.destination != destination:
            raise forms.ValidationError(
                f"The Airport '{airport.name}' does not belong to the destination '{destination.city} - {destination.country}'."
            )

        return cleaned_data