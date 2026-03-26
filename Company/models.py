from django.db import models            
from django.utils import timezone      
from django.urls import reverse      
from cloudinary.models import CloudinaryField  

# Create your models here.

# Social media accounts model
class SocialAccount(models.Model):
    name = models.CharField(max_length=100, help_text="Name of the social account (e.g., Facebook).")
    link = models.CharField(max_length=500, help_text="Full URL to the social account/profile.")

    def __str__(self):
        return f"{self.name} - {self.link}"


# Careers model (job postings)
class Career(models.Model):
    career_name = models.CharField(max_length=255, help_text="Title of the career/position.")
    description = models.TextField(help_text="Full description of the job / responsibilities.")
    positions = models.PositiveIntegerField(default=1, help_text="Number of open positions.")
    L_salary = models.DecimalField(max_digits=12, decimal_places=2, null=True, blank=True, help_text="Lower bound of the salary.")
    U_salary = models.DecimalField(max_digits=12, decimal_places=2, null=True, blank=True, help_text="Upper bound of the salary.")
    experience = models.CharField(max_length=255, help_text="Experience required (e.g., '2+ years').")
    published_at = models.DateTimeField(default=timezone.now, help_text="Publication datetime.")

    class Meta:
        ordering = ['-published_at']

    def __str__(self):
        return f"{self.career_name} ({self.positions} positions)"

    def get_absolute_url(self):
        return reverse('company:career_detail', kwargs={'pk': self.pk})

# Career Application model (for job applications)
class CareerApplication(models.Model):
    career = models.ForeignKey(
        Career,
        on_delete=models.CASCADE,
        related_name="applications",
        help_text="The career/job this application belongs to."
    )
    full_name = models.CharField(max_length=255)
    email = models.EmailField()
    phone = models.CharField(max_length=50)
    cv = models.FileField(
        upload_to="company/careers/applications/cv/",
        blank=True,
        null=True,
        help_text="Uploaded CV file"
    )
    message = models.TextField()
    submitted_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-submitted_at']

    def __str__(self):
        return f"{self.full_name} - {self.career.career_name}"


# Article model (news / notice board)
class Article(models.Model):
    # Represents a news or notice article for the press room..

    # Article type choices
    NEWS = 'News'
    BREAKING = 'Breaking_News'
    AD = 'Ad'
    DISCOUNT = 'discount'
    NOTIFICATION = 'Notification'

    ARTICLE_TYPE_CHOICES = [
        (NEWS, 'News'),
        (BREAKING, 'Breaking News'),
        (AD, 'Advertisement'),
        (DISCOUNT, 'Discount'),
        (NOTIFICATION, 'Notification'),
    ]

    title = models.CharField(max_length=255, help_text="Short headline for the article.")
    summary = models.CharField(max_length=512, blank=True, help_text="Short summary shown in lists.")
    description = models.TextField(help_text="Full article content.")
    image = CloudinaryField('image', folder="WingsAirline/media/Company/articles",null=True,blank=True)
    published_at = models.DateTimeField(default=timezone.now)
    article_type = models.CharField(max_length=30, choices=ARTICLE_TYPE_CHOICES, default=NEWS)
    
    class Meta:
        ordering = ['-published_at']

    def __str__(self):
        return f"{self.title} ({self.article_type})"

    def get_absolute_url(self):
        return reverse('company:news_detail', kwargs={'pk': self.pk})


# Investor model
class Investor(models.Model):
    name = models.CharField(max_length=255, help_text="Investor name or company.")
    icon = CloudinaryField('image', folder="WingsAirline/media/Company/investors",null=True,blank=True)
    bio = models.TextField(blank=True, help_text="Short biography or investor summary.")
    report = models.FileField(upload_to='company/investors/reports/', blank=True, null=True, help_text="Investor report file (PDF, XLSX, etc.).")

    def __str__(self):
        return self.name


# Partnership model
class Partnership(models.Model):
    name = models.CharField(max_length=255, help_text="Partner name.")
    icon = CloudinaryField('image', folder="WingsAirline/media/Company/partners",null=True,blank=True)
    description = models.TextField(blank=True, help_text="Short description of the partner.")
    business_type = models.CharField(max_length=255, blank=True, help_text="Type of business.")
    link = models.CharField(max_length=500, blank=True, help_text="Partner website URL.")

    def __str__(self):
        return self.name
