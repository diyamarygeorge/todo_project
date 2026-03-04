from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import login, logout, update_session_auth_hash
from django.contrib.auth.forms import AuthenticationForm, PasswordChangeForm
from django.contrib.auth.decorators import login_required
from django.views.decorators.http import require_http_methods
from .forms import RegisterForm, NoteEditForm, ProfileEditForm
from .models import Note

def landing(request):
    return render(request, 'landing.html')

def register_view(request):
    if request.method == 'POST':
        form = RegisterForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('login')
    else:
        form = RegisterForm()
    return render(request, 'register.html', {'form': form})

def login_view(request):
    if request.method == 'POST':
        form = AuthenticationForm(data=request.POST)
        if form.is_valid():
            user = form.get_user()
            login(request, user)
            return redirect('home')
    else:
        form = AuthenticationForm()
    return render(request, 'login.html', {'form': form})

@login_required
def home(request):
    if request.method == 'POST':
        note_text = request.POST.get('note')
        if note_text:
            Note.objects.create(
                user=request.user,
                note=note_text
            )

    notes = Note.objects.filter(user=request.user).order_by('-created_at')
    return render(request, 'home.html', {'notes': notes})

@login_required
def toggle_note(request, note_id):
    note = get_object_or_404(Note, id=note_id, user=request.user)
    note.completed = not note.completed
    note.save()
    return redirect('home')


@login_required
@require_http_methods(['GET', 'POST'])
def edit_note(request, note_id):
    """Only the note owner can edit. Returns 404 if note doesn't exist or belongs to another user."""
    note = get_object_or_404(Note, id=note_id, user=request.user)
    if request.method == 'POST':
        form = NoteEditForm(request.POST, instance=note)
        if form.is_valid():
            form.save()
            return redirect('home')
    else:
        form = NoteEditForm(instance=note)
    return render(request, 'edit_note.html', {'form': form, 'note': note})


@login_required
@require_http_methods(['POST'])
def delete_note(request, note_id):
    """Only the note owner can delete. Returns 404 if note doesn't exist or belongs to another user."""
    note = get_object_or_404(Note, id=note_id, user=request.user)
    note.delete()
    return redirect('home')


@login_required
@require_http_methods(['GET', 'POST'])
def profile_view(request):
    """Profile page: edit username, email, and change password. Only for logged-in users."""
    profile_form = ProfileEditForm(instance=request.user)
    password_form = PasswordChangeForm(user=request.user)

    if request.method == 'POST':
        if 'update_profile' in request.POST:
            profile_form = ProfileEditForm(request.POST, instance=request.user)
            if profile_form.is_valid():
                profile_form.save()
                return redirect('profile')
        elif 'change_password' in request.POST:
            password_form = PasswordChangeForm(user=request.user, data=request.POST)
            if password_form.is_valid():
                password_form.save()
                update_session_auth_hash(request, request.user)
                return redirect('profile')

    return render(request, 'profile.html', {
        'profile_form': profile_form,
        'password_form': password_form,
    })


def logout_view(request):
    logout(request)
    return redirect('login')
