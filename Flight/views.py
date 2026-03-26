from dal import autocomplete
from .models import Airport


class AirportAutocomplete(autocomplete.Select2QuerySetView):
    def get_queryset(self):
        qs = Airport.objects.all()

        # إذا لم يُرسل ID الوجهة فلا نعرض شيئًا
        destination_id = self.forwarded.get('counterpart')

        if destination_id:
            qs = qs.filter(destination_id=destination_id)
        else:
            qs = qs.none()

        # دعم البحث بالأحرف
        if self.q:
            qs = qs.filter(name__icontains=self.q)

        return qs
