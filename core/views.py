from django.shortcuts import render
import json
from datetime import date
from django.views.decorators.csrf import csrf_exempt
from django.http import JsonResponse
from .models import Expense
from django.contrib.auth.models import User
from django.views.decorators.http import require_GET
from django.db.models import Sum

# Create your views here.


@csrf_exempt
def add_expense(request):
    print("HIT ADD_EXPENSE VIEW:", request.method)
    if request.method=='POST':
        try:
            data = json.loads(request.body)

            user = User.objects.get(id=data["user_id"])
            amount=data["amount"]
            category=data["category"]
            description=data.get("description", "")
            expense_date=data.get("date", date.today().isoformat())

            expense=Expense.objects.create(
                user=user,
                amount=amount,
                category=category,
                description=description,
                date=expense_date
            )

            return JsonResponse(
                {
                    "status": True,
                    "message": "Expense added sucessfully",
                    "expense_id": expense.id
                },
                status=400
            )
        except Exception as e:
            print("Error ", str(e))
            return JsonResponse(
                {
                    "status": False,
                    "message": str(e)
                },
                status=400
            )
    return JsonResponse({
        "status": False,
        "message": "Only POST method allowed"
    },
    status=405) 
    

@csrf_exempt
@require_GET
def view_expenses(request):
    try:
        user_id=request.GET.get("user_id")

        if not user_id:
            return JsonResponse(
                {
                    "status": False,
                    "message": "User ID required"
                },
                status=400
            )
        try:
            user=User.objects.get(id=user_id)
        except User.DoesNotExist:
            return JsonResponse(
                {
                    "status": False,
                    "message": "User not found"
                },
                status=404
            )
        
        expenses=Expense.objects.filter(user=user).order_by('-date')

        expense_list=[]
        for e in expenses:
            expense_list.append(
                {
                    "id": e.id,
                    "amount": float(e.amount),
                    "category": e.category,
                    "description": e.description,
                    "date": e.date.strftime("%Y-%m-%d")
                }
            )
        return JsonResponse({
            "status": True,
            "message": "Expenses fetched successfully",
            "data": expense_list
        })
    
    except Exception as e:
        print("Error ", str(e))
        return JsonResponse({
            "status": False,
            "message": str(e)
        },
        status=500
        )




@csrf_exempt
@require_GET
def expense_summary(request):
    try:
        user_id = request.GET.get("user_id")
        if not user_id:
            return JsonResponse(
                {
                    "status": False,
                    "message": "User ID required"
                },
                status=400
            )
        try:
            user=User.objects.get(id=user_id)
        except User.DoesNotExist:
            return JsonResponse(
                {
                    "status": False,
                    "message": "User not found"
                },
                status=404
            )
        
        month = request.GET.get("month")
        expenses= Expense.objects.filter(user=user)

        if month:
            try:
                year, mon= map(int, month.split("-"))
                expenses=expenses.filter(date__year=year, date__month=mon)
            except:
                return JsonResponse(
                    {
                        "status": False,
                        "message": "Invalid month format (use YYYY-MM)"
                    }
                )
        total_amount=expenses.aggregate(Sum('amount'))["amount__sum"] or 0

        categories={}
        for e in expenses:
            cat=e.category
            categories[cat]=categories.get(cat,0)+float(e.amount)

        return JsonResponse(
            {
                "status": True,
                "message": "Summary generated",
                "total_amount": float(total_amount),
                "total_by_category": categories
            }
        )
    
    except Exception as e:
        print("Error ", str(e))
        return JsonResponse(
            {
                "status": False,
                "message": str(e)
            },
            status=500
        )



