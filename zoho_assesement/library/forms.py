from django import forms
from .models import *
from django.core.exceptions import ValidationError
from django.core.mail import send_mail
import datetime
import re


class BookForm(forms.ModelForm):
    class Meta:
        model = Books
        fields = '__all__'
        widgets={
            'title':forms.TextInput(attrs={'class':'form-control'}),
            'author':forms.TextInput(attrs={'class':'form-control'}),
            'genre':forms.Select(attrs={'class':'form-control'}),
            'publication_year':forms.DateTimeInput(attrs={'class':'form-control'}),
            'available_copies':forms.NumberInput(attrs={'class':'form-control'}),
            'isbn_number':forms.TextInput(attrs={'class':'form-control'}),
            'rating':forms.NumberInput(attrs={'class':'form-control'}),
            
        }
    def clean_publication_year(self):
        year = self.cleaned_data.get('publication_year')
        current_year = datetime.datetime.now().year
        if year < 1900 or year > current_year:
            raise ValidationError("Publication year must be between 1900 and the current year.")
        return year
    def validate_isbn(value):
        if not re.match(r'^\d{13}$', value):
             raise ValidationError("Invalid ISBN format. It should be 13 digits.")
    
    
class MemberForm(forms.ModelForm):
    class Meta:
        model = Members
        fields = '__all__'
        widgets={
            'name':forms.TextInput(attrs={'class':'form-control'}),
            'email':forms.EmailInput(attrs={'class':'form-control'}),
            'phone_number':forms.TextInput(attrs={'class':'form-control'}),
            'membership_start_date':forms.DateInput(attrs={'class':'form-control'}),
            'membership_type':forms.Select(attrs={'class':'form-control'}),
            'max_books_allowed':forms.NumberInput(attrs={'class':'form-control'})
        }
        
    def clean_email(self):
        email = self.cleaned_data.get('email')
        if Members.objects.filter(email=email).exists():
            raise ValidationError("A member with this email already exists.")
        return email
    def save(self, commit=True):
        member = super().save(commit)
        send_mail(
            'Welcome to the Library',
            'Hello {}, welcome to our library!'.format(member.name),
            'library@example.com',
            [member.email],
            fail_silently=False,
        )
        return member

    def clean(self):
        cleaned_data = super().clean()
        membership_type = cleaned_data.get('membership_type')
        if membership_type == 'Basic':
            cleaned_data['max_books_allowed'] = 2
        elif membership_type == 'Premium':
            cleaned_data['max_books_allowed'] = 5
        elif membership_type == 'Elite':
            cleaned_data['max_books_allowed'] = 10
        return cleaned_data

    
class TransactionForm(forms.ModelForm):
    class Meta:
        model = Transactions
        fields = '__all__'
        widgets={
            'member':forms.Select(attrs={'class':'form-control'}),
            'book':forms.Select(attrs={'class':'form-control'}),
            'status':forms.Select(attrs={'class':'form-control'}),
            'issue_date':forms.DateInput(attrs={'class':'form-control'}),
            'return_date':forms.DateInput(attrs={'class':'form-control'}),
            'fine_amount':forms.NumberInput(attrs={'class':'form-control'})
            
        }
    def clean(self):
        cleaned_data = super().clean()
        book = cleaned_data.get('book')
        return_date = cleaned_data.get('return_date')
        issue_date = cleaned_data.get('issue_date')
        
        if book and book.available_copies == 0:
            raise ValidationError("Cannot issue this book. No copies available.")
        
        if return_date and issue_date and return_date <= issue_date:
            raise ValidationError("Return date must be after the issue date.")
        
        if return_date and return_date > datetime.date.today():
            days_overdue = (return_date - issue_date).days - 14
            if days_overdue > 0:
                fine = days_overdue * 2
                cleaned_data['fine_amount'] = fine
                send_mail(
                    'Overdue Book Notice',
                    'Your book is overdue by {} days. Fine amount: ${}'.format(days_overdue, fine),
                    'library@example.com',
                    [cleaned_data['member'].email],
                    fail_silently=False,
                )
        return cleaned_data

    
class StaffForm(forms.ModelForm):
    class Meta:
        model = Staffs
        fields = '__all__'
        widgets={
            'name':forms.TextInput(attrs={'class':'form-control'}),
            'email':forms.EmailInput(attrs={'class':'form-control'}),
            'role':forms.Select(attrs={'class':'form-control'}),
            'phone_number':forms.TextInput(attrs={'class':'form-control'})
        }
