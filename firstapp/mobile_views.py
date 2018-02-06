from django.shortcuts import render


def article_list(request):
    return render(request, 'mobile_list.html', {})
