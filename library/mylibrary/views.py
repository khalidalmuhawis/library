from django.shortcuts import render, redirect
from django.contrib.auth import login, authenticate, logout
from .models import Book, Genre
from django.contrib.auth.models import User
from django.db.models import Q
import datetime


def signup(request):
    form = SignupForm()
    if request.method == 'POST':
        form = SignupForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)

            user.set_password(user.password)
            user.save()

            login(request, user)
            return redirect("book-list")
    context = {
        "form":form,
    }
    return render(request, 'signup.html', context)


def signin(request):
    form = SigninForm()
    if request.method == 'POST':
        form = SigninForm(request.POST)
        if form.is_valid():

            username = form.cleaned_data['username']
            password = form.cleaned_data['password']

            auth_user = authenticate(username=username, password=password)
            if auth_user is not None:
                login(request, auth_user)
                return redirect('book-list')
    context = {
        "form":form
    }
    return render(request, 'signin.html', context)


def signout(request):
    logout(request)
    return redirect("signin")


def create_book(request):
    if not request.user.is_staff:
        return redirect("no-access")
    form = BookForm()
    if request.method == "POST":
        form = BookForm(request.POST, request.FILES)
        if form.is_valid():
            book = form.save(commit=False)
            book.added_by = request.user
            book.save()
            form.save()
            return redirect('book-list')
    context = {
        "form": form,
    }
    return render(request, 'create_book.html', context)


def book_list(request):
    books = Book.objects.all()
    query = request.GET.get('search_term')
    if query:
        books = books.filter(
            Q(name__icontains=query) |
            Q(isbn__icontains=query) |
            Q(genre__name__icontains=query)).distinct()
    context = {
        "books": books
    }
    return render(request, 'book_list.html', context)


def book_detail(request, book_id):
    book = Book.objects.get(id=book_id)
    genres = Genre.objects.filter(book=book)
    context = {
        "book": book,
        "genres": genres,
    }
    return render(request, 'book_detail.html', context)
