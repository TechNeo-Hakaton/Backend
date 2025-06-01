# from django.contrib import messages
# from django.contrib.auth import logout
# from django.shortcuts import redirect
#
#
# class LoginView(View):
#     def get(self, request):
#         return render(request, 'staff/login.html')
#
#     def post(self, request):
#         username = request.POST.get('username')
#         password = request.POST.get('password')
#         user = authenticate(username=username, password=password)
#         if user is not None:
#             login(request, user)
#             messages.success(request, "Siz tizimga muvaffaqqiyatli kirdingiz.")
#             return JsonResponse({'success': True, 'user_role': user.user_role})
#         elif User.objects.filter(username=username).exists():
#             return JsonResponse({'error': 'password'}, status=400)
#         else:
#             return JsonResponse({'error': 'username'}, status=400)
#
#     def dispatch(self, request, *args, **kwargs):
#         if request.headers.get('x-requested-with') == 'XMLHttpRequest' and request.method == 'POST':
#             return self.post(request)
#         return super().dispatch(request, *args, **kwargs)
#
#
# def logout_user(request):
#     logout(request)
#     messages.warning(request, "Siz tizimdan chiqdingiz")
#     return redirect('dashboard:dashboard')