from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import permissions, status

from .models import SocialAccount, Career, Article, Investor, Partnership, CareerApplication
from .serializers import *


# ============================ SOCIAL MEDIA ============================
class SocialAccountsView(APIView):
    permission_classes = [permissions.AllowAny]

    def get(self, request):
        accounts = SocialAccount.objects.all()
        serializer = SocialAccountSerializer(accounts, many=True)
        return Response(serializer.data)


# ============================ CAREERS ============================
class CareerListView(APIView):
    permission_classes = [permissions.AllowAny]

    def get(self, request):
        careers = Career.objects.all()
        serializer = CareerSerializer(careers, many=True)
        return Response(serializer.data)


class CareerDetailView(APIView):
    permission_classes = [permissions.AllowAny]

    def get(self, request, pk):
        try:
            career = Career.objects.get(pk=pk)
        except Career.DoesNotExist:
            return Response({"detail": "Career not found"}, status=404)

        serializer = CareerSerializer(career)
        return Response(serializer.data)


class CareerSubmitView(APIView):
    permission_classes = [permissions.AllowAny]

    def post(self, request, pk):
        # Check that the career exists
        try:
            career = Career.objects.get(pk=pk)
        except Career.DoesNotExist:
            return Response({"detail": "Career not found"}, status=404)

        serializer = CareerSubmitSerializer(data=request.data)

        if serializer.is_valid():
            # Save the application linked to the career
            application = serializer.save(career=career)

            return Response({
                "detail": "Application submitted successfully",
                "application_id": application.id,
                "submitted_data": serializer.data
            }, status=201)

        return Response(serializer.errors, status=400)




# ============================ ARTICLES ============================
class ArticleListView(APIView):
    permission_classes = [permissions.AllowAny]

    def get(self, request):
        articles = Article.objects.all()
        serializer = ArticleSerializer(articles, many=True)
        return Response(serializer.data)



# ============================ INVESTORS ============================
class InvestorListView(APIView):
    permission_classes = [permissions.AllowAny]

    def get(self, request):
        investors = Investor.objects.all()
        serializer = InvestorSerializer(investors, many=True)
        return Response(serializer.data)


# ============================ PARTNERSHIPS ============================
class PartnershipListView(APIView):
    permission_classes = [permissions.AllowAny]

    def get(self, request):
        partners = Partnership.objects.all()
        serializer = PartnershipSerializer(partners, many=True)
        return Response(serializer.data)
