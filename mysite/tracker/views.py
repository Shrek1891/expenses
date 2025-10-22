import datetime

from django.db.models import Sum
from django.shortcuts import render, redirect

from tracker.models import Expense


def get_period_expenses(period, db):
    current_period = datetime.date.today() - datetime.timedelta(days=period)
    expenses_period = db.objects.filter(date__gte=current_period)
    total_expenses_period = expenses_period.aggregate(Sum('amount'))['amount__sum']
    if total_expenses_period is None:
        total_expenses_period = 0
    return total_expenses_period


# Create your views here.
def index(request):
    expenses = []
    if request.method == 'POST':
        name = request.POST['name']
        amount = request.POST['amount']
        category = request.POST['category']
        expense = Expense(name=name, amount=amount, category=category)
        expense.save()
        return redirect('index')
    expenses = Expense.objects.all()
    total_expenses = expenses.aggregate(Sum('amount'))['amount__sum']
    expenses_last_year = get_period_expenses(365, Expense)
    expenses_last_month = get_period_expenses(30, Expense)
    expenses_last_week = get_period_expenses(7, Expense)
    data = Expense.objects.filter().values('date').order_by('date').annotate(Sum('amount'))
    categories = Expense.objects.filter().values('category').order_by('date').annotate(Sum('amount'))
    context = {
        'expenses': expenses,
        'total_expenses': total_expenses,
        'expenses_last_year': expenses_last_year,
        'expenses_last_month': expenses_last_month,
        'expenses_last_week': expenses_last_week,
        'data': data,
        'categories': categories
    }
    return render(request, 'tracker/index.html', context)


def edit_expense(request, id):
    expense = Expense.objects.get(id=id)
    if request.method == 'POST':
        expense.name = request.POST['name']
        expense.amount = request.POST['amount']
        expense.category = request.POST['category']
        expense.save()
        return redirect('index')
    return render(request, 'tracker/edit.html', {'expense': expense})


def delete_expense(request, id):
    expense = Expense.objects.get(id=id)
    expense.delete()
    return redirect('index')
