from django.shortcuts import render, redirect, get_object_or_404
from .models import Expense
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from datetime import date
from django.db.models import Sum
from django.utils.timezone import now

# Create your views here.


@login_required(login_url='login')
def expense_list(request):
    expenses = Expense.objects.filter(user=request.user).order_by('-date')
    return render(request, 'expenses/expense_list.html', {'expenses': expenses})


@login_required(login_url='login')
def expense_add(request):
    if request.method == "POST":
        title = request.POST['title']
        amount = request.POST['amount']
        category = request.POST['category']
        expense_date = request.POST['date']
        notes = request.POST['notes']

        Expense.objects.create(
            user=request.user,
            title=title,
            amount=amount,
            category=category,
            date=expense_date,
            notes=notes
        )
        messages.success(request, "Expense added successfully")
        return redirect('expense_list')

    return render(request, 'expenses/expense_form.html', {'action': 'Add'})


@login_required(login_url='login')
def expense_edit(request, id):
    expense = get_object_or_404(Expense, id=id, user=request.user)

    if request.method == "POST":
        expense.title = request.POST['title']
        expense.amount = request.POST['amount']
        expense.category = request.POST['category']
        expense.date = request.POST['date']
        expense.notes = request.POST['notes']
        expense.save()
        messages.success(request, "Expense updated successfully")
        return redirect('expense_list')

    return render(request, 'expenses/expense_form.html', {'expense': expense, 'action': 'Edit'})


@login_required(login_url='login')
def expense_delete(request, id):
    expense = get_object_or_404(Expense, id=id, user=request.user)
    expense.delete()
    messages.success(request, "Expense deleted successfully")
    return redirect('expense_list')



@login_required(login_url='login')
def dashboard(request):
    user = request.user
    expenses = Expense.objects.filter(user=user)

    total_expense = expenses.aggregate(Sum('amount'))['amount__sum'] or 0

    # Category-wise summary
    categories = dict(Expense._meta.get_field('category').choices)
    category_summary = {}
    for cat in categories:
        category_total = expenses.filter(category=cat).aggregate(Sum('amount'))['amount__sum'] or 0
        category_summary[cat] = category_total

    # Monthly summary
    current_month = now().month
    current_year = now().year
    monthly_total = expenses.filter(date__year=current_year, date__month=current_month).aggregate(Sum('amount'))['amount__sum'] or 0

    context = {
        'total_expense': total_expense,
        'category_summary': category_summary,
        'monthly_total': monthly_total,
    }
    return render(request, 'expenses/dashboard.html', context)
