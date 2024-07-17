#shifts/view.py
from django.shortcuts import render, redirect
from .forms import ShiftForm
from .models import Shift
from django.contrib.auth.decorators import login_required


@login_required
def index(request):
    if request.method == 'POST':
        print("POSTを受け取った")
        print(request.POST)
        form = ShiftForm(request.POST)
        if form.is_valid():
            shift = form.save(commit=False)
            shift.user = request.user
            shift.save()            
            print('正しく日にちが保存された')
            request.session['name'] = form.cleaned_data['name'] #名前を保存
            print(f"{request.session['neme']}を保存した") 
            return redirect('index')
        else:
            print('正しく日にちが保存できなかった')
            print(form.errors)
            print(form.errors.as_data())
    else:
        form = ShiftForm(initial={'name': request.session.get('name', '')})
    
    user_shifts = Shift.objects.filter(user=request.user)
    print(f"シフト：{user_shifts}")


    return render(request, 'shifts/index.html', {'form': form, 'user_shifts': user_shifts})
