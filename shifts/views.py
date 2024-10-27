#shifts/view.py
from django.shortcuts import render, redirect
from .forms import ShiftForm
from .models import Shift
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from firebase_admin import firestore, exceptions

db = firestore.client()

@login_required
def index(request):
    return render(request, 'shifts/index.html')  # ルートURLでindex.htmlテンプレートを表示
    """
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
            print(f"{request.session['name']}を保存した") 
            return redirect('index')
        else:
            print('正しく日にちが保存できなかった')
            print(form.errors)
            print(form.errors.as_data())
    else:
        form = ShiftForm(initial={'name': request.session.get('name', '')})
    
    user_shifts = Shift.objects.filter(user=request.user)
    print(f"シフト：{user_shifts}")


    return render(request, 'shifts/submiit_shifts.html', {'form': form, 'user_shifts': user_shifts})"""



# Firestoreにシフト希望を保存するビュー
@login_required
def submit_shift_requests(request):
    if request.method == 'POST':
        print("受け取ったpostデータ", request.POST)
        form = ShiftForm(request.POST)
        if form.is_valid():
            print("成功")
            request.session['name'] = form.cleaned_data['name']
            shift_data = {
                'name': form.cleaned_data['name'],  # スタッフ名をユーザー情報から取得
                'shift_date': form.cleaned_data['shift_date'].strftime('%Y-%m-%d'),
                'start_time': form.cleaned_data['start_time'],
                'end_time': form.cleaned_data['end_time'],
            }
            try:
                # Firestoreにデータを保存
                doc_ref = db.collection('shifts').document(f"{request.user.username}_{form.cleaned_data['shift_date']}")
                doc_ref.set(shift_data)
                return JsonResponse({'message': 'シフト希望が正常に送信されました'})
            except exceptions.FirebaseError as e:
                print(f"Firestoreへの保存エラー: {e}")
                return JsonResponse({'error': 'シフト希望の保存に失敗しました'}, status=500)
        else:
            return JsonResponse({'errors': form.errors}, status=400)
    else:
        initial_name = request.session.get('name', '')
        form = ShiftForm(initial={'name': initial_name})
    return render(request, 'shifts/submit_shifts.html', {'form': form})

# Firestoreからシフト希望を取得するビュー
@login_required
def view_shift_requests(request):
    try:
        shifts_ref = db.collection('shifts')
        docs = shifts_ref.stream()
        shifts = [doc.to_dict() for doc in docs]
        return render(request, 'shifts/view_shifts.html', {'shifts': shifts})
    except exceptions.FirebaseError as e:
        print(f"Firestoreからの取得エラー: {e}")
        return JsonResponse({'error': 'シフト希望の取得に失敗しました'}, status=500)
    
@login_required
def view_myshift_requests(request):
    try:
        # ログインユーザーの名前でフィルタリング
        shifts_ref = db.collection('shifts').where('name', '==', request.session.get('name', ''))
        docs = shifts_ref.stream()
        
        # 取得したデータをリストに変換
        user_shifts = []
        for doc in docs:
            shift_data = doc.to_dict()
            user_shifts.append({
                'shift_date': shift_data.get('shift_date'), 
                'start_time': shift_data.get('start_time'), 
                'end_time': shift_data.get('end_time'),
                'remarks': shift_data.get('remarks')  # 備考があれば追加
            })
        
        # テンプレートにデータを渡す
        return render(request, 'shifts/view_myshifts.html', {'user_shifts': user_shifts})
    except exceptions.FirebaseError as e:
        print(f"Firestoreからの取得エラー: {e}")
        return JsonResponse({'error': 'シフト希望の取得に失敗しました'}, status=500)