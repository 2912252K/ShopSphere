from django import forms
from ShopSphere.models import Page, Category
from django.contrib.auth.models import User
from ShopSphere.models import UserProfile


class CategoryForm(forms.ModelForm):
    name = forms.CharField(max_length=Category.NAME_MAX_LENGTH,
                            help_text="Please enter the category name.")
    views = forms.IntegerField(widget=forms.HiddenInput(), initial=0)
    likes = forms.IntegerField(widget=forms.HiddenInput(), initial=0)
    slug = forms.CharField(widget=forms.HiddenInput(), required=False)
    # 10
    # 11 # An inline class to provide additional information on the form.
    class Meta:
        # 13 # Provide an association between the ModelForm and a model
        model = Category
        fields = ('name',)
    
class PageForm(forms.ModelForm):
    title = forms.CharField(max_length=Page.TITLE_MAX_LENGTH,
                            help_text="Please enter the title of the page.")
    url = forms.URLField(max_length=Page.URL_MAX_LENGTH,
                        help_text="Please enter the URL of the page.")
    views = forms.IntegerField(widget=forms.HiddenInput(), initial=0)
    
    class Meta:
        # 25 # Provide an association between the ModelForm and a model
        model = Page

        # 28 # What fields do we want to include in our form?
        # 29 # This way we don't need every field in the model present.
        # 30 # Some fields may allow NULL values; we may not want to include them.
        # 31 # Here, we are hiding the foreign key.
        # 32 # we can either exclude the category field from the form,
        exclude = ('category',)
        # 34 # or specify the fields to include (don't include the category field).
        # 35 #fields = ('title', 'url', 'views')

        def clean(self):
            cleaned_data = self.cleaned_data
            url = cleaned_data.get('url')
            # If url is not empty and doesn't start with 'http://',
            # then prepend 'http://'.
            if url and not url.startswith('http://'):
                url = f'http://{url}'
                cleaned_data['url'] = url
            return cleaned_data
        
class UserForm(forms.ModelForm):
    password = forms.CharField(widget=forms.PasswordInput())
    class Meta:
        model = User
        fields = ('username', 'email', 'password',)

