from django.db import models
from django.core.validators import MaxValueValidator, MinValueValidator
import datetime

class Books(models.Model):
    GENRE_CHOICES = [
        ('Fiction', 'Fiction'),
        ('Non-Fiction', 'Non-Fiction'),
        ('Sci-Fi', 'Sci-Fi'),
        ('Biography', 'Biography'),
    ]

    title = models.CharField(max_length=200)
    author = models.CharField(max_length=100)
    genre = models.CharField(max_length=20, choices=GENRE_CHOICES)
    publication_year = models.PositiveIntegerField(validators=[MinValueValidator(1900), MaxValueValidator(datetime.datetime.now().year)])
    available_copies = models.PositiveIntegerField(default=0)
    isbn_number = models.CharField(max_length=13, unique=True)
    rating = models.PositiveIntegerField(validators=[MinValueValidator(1), MaxValueValidator(5)], null=True, blank=True)
    is_featured = models.BooleanField(default=False)
    def __str__(self):
        return self.title
    class Meta:
        ordering = ['-publication_year']
    

class Members(models.Model):
    MEMBERSHIP_CHOICES = [
        ('Basic', 'Basic'),
        ('Premium', 'Premium'),
        ('Elite', 'Elite'),
    ]

    name = models.CharField(max_length=100)
    email = models.EmailField()
    phone_number = models.CharField(max_length=10)
    membership_start_date = models.DateField(auto_now_add=True)
    membership_type = models.CharField(max_length=20, choices=MEMBERSHIP_CHOICES)
    max_books_allowed = models.PositiveIntegerField()
    def __str__(self):
        return self.name

class Transactions(models.Model):
    STATUS_CHOICES = [
        ('Issued', 'Issued'),
        ('Returned', 'Returned'),
        ('Overdue', 'Overdue'),
    ]

    member = models.ForeignKey(Members, on_delete=models.CASCADE)
    book = models.ForeignKey(Books, on_delete=models.CASCADE)
    issue_date = models.DateField(auto_now_add=True)
    return_date = models.DateField()
    status = models.CharField(max_length=20, choices=STATUS_CHOICES)
    fine_amount = models.DecimalField(max_digits=6, decimal_places=2, default=0)
    def mark_as_lost(self):
        self.status = 'Lost'
        self.book.available_copies = 0  # Set the book's available copies to 0
        self.note = f"Book marked as lost on {datetime.date.today()}"
        self.book.save()
        self.save()

    def __str__(self):
        return f"Transaction: {self.book.title} for {self.member.name}"

class Staffs(models.Model):
    ROLE_CHOICES = [
        ('Librarian', 'Librarian'),
        ('Assistant', 'Assistant'),
    ]

    name = models.CharField(max_length=100)
    email = models.EmailField()
    role = models.CharField(max_length=20, choices=ROLE_CHOICES)
    phone_number = models.CharField(max_length=10)




    

    

