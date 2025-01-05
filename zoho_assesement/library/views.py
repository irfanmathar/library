from django.shortcuts import render,redirect,get_object_or_404
from .forms import *
from .models import *
from django.shortcuts import render
from .models import *
from django.db.models import Count
import datetime

def dashboard_view(request):
    # Ensure you import datetime and use datetime.date.today()
    overdue_transactions = Transactions.objects.filter(return_date__lt=datetime.date.today(), status='Issued')
    
    # Check if overdue_transactions has data
    print(overdue_transactions)  # For debugging purposes

    # Top Members
    top_members = Members.objects.annotate(total_books=Count('transactions')).order_by('-total_books')[:10]
    
    # Genre Data
    genre_data = Books.objects.values('genre').annotate(total=Count('id'))
    genre_labels = [item['genre'] for item in genre_data]
    genre_counts = [item['total'] for item in genre_data]

    # Staff Logs
    staff_logs = Staffs.objects.all().order_by('-id')
    print(staff_logs)  # For debugging purposes

    return render(request, 'dashboard.html', {
        'overdue_transactions': overdue_transactions,
        'top_members': top_members,
        'genre_labels': genre_labels,
        'genre_data': genre_counts,
        'staff_logs': staff_logs
    })
    

def add_book(request):
    context={
        'Book_Form':BookForm()
    }
    if request.method == 'POST':
        form = BookForm(request.POST)
        if form.is_valid():
            # Save the new book to the database
            form.save()
            return redirect('/listbook/')  # Redirect to book list after saving
        else:
            # If the form is invalid, re-render the form with error messages
            return render(request, 'book.html', {'form': form})
    else:
        form = BookForm()  # Create an empty form for GET request
        return render(request, 'book.html', {'form': form})
        
    return render(request,'book.html',context)

def add_member(request):
    if request.method == 'POST':
        forms = MemberForm(request.POST)
        if forms.is_valid():
            # Save the new member to the database
            forms.save()
            return redirect('/transaction/')  # Redirect to the member list after saving
        else:
            # If the form is invalid, re-render the form with error messages
            return render(request, 'member.html', {'forms': forms})
    else:
        forms= MemberForm()  # Create an empty form for GET request
        return render(request, 'member.html', {'forms': forms})
def add_transaction(request):
    
    if request.method == 'POST':
        transaction_form = TransactionForm(request.POST)
        if transaction_form.is_valid():
            # Save the new book to the database
            transaction_form.save()
            return redirect('/transaction_list/')  # Redirect to book list after saving
        else:
            # If the form is invalid, re-render the form with error messages
            return render(request, 'transaction.html', {'transaction_form': transaction_form})
    else:
        transaction_form = TransactionForm()  # Create an empty form for GET request
        return render(request, 'transaction.html', {'transaction_form': transaction_form})
    
def add_staff(request):
    if request.method == 'POST':
        staff_form = StaffForm(request.POST)
        if staff_form.is_valid():
            # Save the new book to the database
            staff_form.save()
            return redirect('/dashboard/')  # Redirect to book list after saving
        else:
            # If the form is invalid, re-render the form with error messages
            return render(request, 'staff.html', {'staff_form':staff_form})
    else:
        staff_form= StaffForm()  
        return render(request, 'staff.html', {'staff_form': staff_form})
def toggle_featured(request, book_id):
    book = get_object_or_404(Books, id=book_id)
    book.is_featured = not book.is_featured  
    book.save()
    return redirect('/book/') 
def mark_as_lost(request, transaction_id):
    transaction = get_object_or_404(Transactions, id=transaction_id)
    transaction.mark_as_lost()  
    return redirect('/transaction/')
def book_list(request):
    # Get all books from the database
    books = Books.objects.all()
    
    # Render the books list template and pass the books context
    return render(request, 'allbook.html', {
        'books': books
    })
def transaction_list(request):
    # Get all transactions (you can add filters like 'Issued' status if needed)
    transactions = Transactions.objects.all()
    
    # Pass transactions to the template
    return render(request, 'list.html', {'transactions': transactions})