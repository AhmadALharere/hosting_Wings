# from django import forms
# from .models import Career, Article, ArticleImage, Investor, Partnership


# # Form for creating/editing Careers
# class CareerForm(forms.ModelForm):
#     class Meta:
#         model = Career
#         fields = ['career_name', 'description', 'positions', 'L_salary', 'U_salary', 'experience']
#         widgets = {
#             'description': forms.Textarea(attrs={'rows': 4}),
#         }



# # Form for creating/editing an Article
# class ArticleForm(forms.ModelForm):
#     class Meta:
#         model = Article
#         fields = ['title', 'summary', 'description', 'image_label', 'article_type']
#         widgets = {
#             'summary': forms.Textarea(attrs={'rows': 3}),
#             'description': forms.Textarea(attrs={'rows': 5}),
#         }



# # Form for uploading multiple images for an article

# class MultipleFileInput(forms.ClearableFileInput):
#     allow_multiple_selected = True

# class ArticleImageForm(forms.ModelForm):
#     class Meta:
#         model = ArticleImage
#         fields = ['image']
#         # The multiple attribute allows selecting multiple files at once
#         widgets = {
#             'image': MultipleFileInput()
#         }



# # Form for creating/editing an Investor
# class InvestorForm(forms.ModelForm):
#     class Meta:
#         model = Investor
#         fields = ['name', 'icon', 'bio', 'report']



# # Form for creating/editing Partnerships
# class PartnershipForm(forms.ModelForm):
#     class Meta:
#         model = Partnership
#         fields = ['name', 'icon', 'description', 'business_type', 'link']
