from django.http import HttpResponse
from django.shortcuts import render, get_object_or_404, redirect

from .models import MainMenu
from .forms import BookForm, BookSearchForm, CommentForm
from django.http import HttpResponseRedirect
from django.http import HttpResponse
from .models import Book, Comment, Cart, Message
# Create your views here.

from django.views.generic.edit import CreateView
from django.contrib.auth.forms import UserCreationForm
from django.urls import reverse_lazy

from django.contrib.auth.decorators import login_required


@login_required(login_url=reverse_lazy('login'))
def index(request):
    return render(request,
                  'bookMng/index.html',
                  {
                      'item_list': MainMenu.objects.all()
                  }
                  )


def aboutus(request):
    return render(request,
                  'bookMng/aboutus.html',
                  {
                      'item_list': MainMenu.objects.all()
                  }
                  )

def messagebox(request):
    submitted = False
    if request.method=="POST":
        msg = Message()
        name = request.POST.get('name')
        email = request.POST.get('email')
        message = request.POST.get('message')
        msg.name = name
        msg.email = email
        msg.message = message
        msg.save()
        return HttpResponseRedirect('/messagebox?submitted=True')
    else:
        if 'submitted' in request.GET:
            submitted = True

    return render(request,
                      'bookMng/send_message.html',
                      {
                          'item_list': MainMenu.objects.all(),
                          'submitted': submitted
                      }
                      )


@login_required(login_url=reverse_lazy('login'))
def postbook(request):
    submitted = False
    if request.method == 'POST':
        form = BookForm(request.POST, request.FILES)
        if form.is_valid():
            book = form.save(commit=False)
            try:
                book.username = request.user
            except Exception:
                pass
            book.save()

            try:
                book.ownedby.add(request.user)
            except Exception:
                pass
            book.save()

            return HttpResponseRedirect('/postbook?submitted=True')
    else:
        form = BookForm()
        if 'submitted' in request.GET:
            submitted = True
    return render(request,
                  'bookMng/postbook.html',
                  {
                      'item_list': MainMenu.objects.all(),
                      'form': form,
                      'submitted': submitted
                  }
                  )


@login_required(login_url=reverse_lazy('login'))
def displaybooks(request):
    books = Book.objects.all()
    for b in books:
        b.pic_path = b.picture.url[14:]
    return render(request,
                  'bookMng/displaybooks.html',
                  {
                      'item_list': MainMenu.objects.all(),
                      'books': books
                  }
                  )

@login_required(login_url=reverse_lazy('login'))
def search_books(request):
    if request.method == 'POST':
        form = BookSearchForm(request.POST)
        if form.is_valid():
            query = form.cleaned_data['query']
            books = Book.objects.filter(name__icontains=query)
            for b in books:
                b.pic_path = b.picture.url[14:]
            return render(request,
                          'bookMng/search_results.html',
                          {
                              'item_list': MainMenu.objects.all(),
                              'query': query,
                              'books': books
                          }
                          )
    else:
        form = BookSearchForm()
    return render(request, 'bookMng/search_books.html',
                  {
                      'item_list': MainMenu.objects.all(),
                      'form': form,
                  }
                  )


@login_required(login_url=reverse_lazy('login'))
def mybooks(request):
    books = [book for book in Book.objects.all() if any(request.user == owner for owner in book.ownedby.all())]
    for b in books:
        b.pic_path = b.picture.url[14:]
        b.is_owner = b.username == request.user
    return render(request,
                  'bookMng/mybooks.html',
                  {
                      'item_list': MainMenu.objects.all(),
                      'books': books
                  }
                  )


# @login_required(login_url=reverse_lazy('login'))
# def book_detail(request, book_id):
#     book = Book.objects.get(id=book_id)
#     book.pic_path = book.picture.url[14:]
#     return render(request,
#                   'bookMng/book_detail.html',
#                   {
#                       'item_list': MainMenu.objects.all(),
#                       'book': book
#                   }
#                   )

@login_required(login_url=reverse_lazy('login'))
def book_detail(request, book_id):
    book = get_object_or_404(Book, id=book_id)
    book.pic_path = book.picture.url[14:]
    comments = Comment.objects.filter(book=book)
    comment_form = CommentForm()

    if request.method == 'POST':
        comment_form = CommentForm(request.POST)
        if comment_form.is_valid():
            comment = comment_form.save(commit=False)
            comment.user = request.user
            comment.book = book
            comment.save()
            return redirect('book_detail', book_id=book.id)

    return render(request,
                  'bookMng/book_detail.html',
                  {
                      'book': book,
                      'comments': comments,
                      'comment_form': comment_form,
                      'item_list': MainMenu.objects.all(),

                  }
                  )



@login_required(login_url=reverse_lazy('login'))
def edit_comment(request, comment_id):
    comment = get_object_or_404(Comment, pk=comment_id)

    if request.method == 'POST':
        comment_form = CommentForm(request.POST, instance=comment)
        if comment_form.is_valid():
            comment_form.save()
            return redirect('book_detail', book_id=comment.book.id)
    else:
        comment_form = CommentForm(instance=comment)

    return render(request,
                  'bookMng/edit_comment.html',
                  {
                      'comment_form': comment_form,
                      'comment': comment,
                      'item_list': MainMenu.objects.all(),
                  }
                  )


@login_required(login_url=reverse_lazy('login'))
def delete_comment(request, comment_id):
    comment = get_object_or_404(Comment, id=comment_id, user=request.user)

    if request.method == 'POST':
        comment.delete()
        return redirect('book_detail', book_id=comment.book.id)

    return redirect('delete_confirm', comment_id=comment_id)


@login_required(login_url=reverse_lazy('login'))
def delete_confirm(request, comment_id):
    comment = get_object_or_404(Comment, id=comment_id, user=request.user)
    return render(request,
                  'bookMng/delete_confirm.html',
                  {
                      'comment': comment
                  }
                  )


def book_delete(request, book_id):
    book = Book.objects.get(id=book_id)
    book.delete()
    return render(request,
                  'bookMng/book_delete.html',
                  {
                      'item_list': MainMenu.objects.all(),
                      'book': book
                  }
                  )
def book_unown(request, book_id):
    book = Book.objects.get(id=book_id)
    try:
        book.ownedby.remove(request.user)
    except Exception:
        pass

    return render(request,
                  'bookMng/book_delete.html',
                  {
                      'item_list': MainMenu.objects.all(),
                      'book': book
                  }
                  )



class Register(CreateView):
    template_name = 'registration/register.html'
    form_class = UserCreationForm
    success_url = reverse_lazy('register-success')

    def form_valid(self, form):
        form.save()
        return HttpResponseRedirect(self.success_url)



def view_cart(request):
    cart_items = Cart.objects.filter(user=request.user)
    total_price = sum(CartItem.book.price for CartItem in cart_items)
    return render(request,
                  'bookMng/view_cart.html',
                  {
                      'item_list': MainMenu.objects.all(),
                      'cart_items': cart_items,
                      'total_price': total_price
                  }
                  )

def add_to_cart(request, book_id):
    book = get_object_or_404(Book, id=book_id)
    cart_item, created = Cart.objects.get_or_create(book=book, user=request.user)
    cart_item.user = request.user
    if not created:
        cart_item.save()

    return HttpResponseRedirect(request.META.get('HTTP_REFERER', '/'))
@login_required(login_url=reverse_lazy('login'))
def remove_from_cart(request, book_id):
    book = get_object_or_404(Book, id=book_id)
    cart_item = Cart.objects.filter(book=book, user=request.user).first()
    book.username = request.user

    if cart_item:
            cart_item.delete()

    return redirect('view_cart')

@login_required(login_url=reverse_lazy('login'))
def checkout_cart(request):
    cart_items = Cart.objects.filter(user=request.user)
    for cart_item in cart_items:
                cart_item.book.ownedby.add(request.user)
                cart_item.book.save()
                cart_item.delete()
    return redirect('view_cart')

@login_required
def favorite(request, book_id):
    book = get_object_or_404(Book, id=book_id)
    user = request.user

    if user in book.favorites.all():
        book.favorites.remove(user)
    else:
        book.favorites.add(user)

    return redirect('book_detail', book_id=book.id)

@login_required
def my_favorites(request):
    user = request.user
    favorite_books = Book.objects.filter(favorites=user)
    for book in favorite_books:
        book.pic_path = book.picture.url[14:]
    return render(request,
                  'bookMng/my_favorites.html',
                  {
                      'favorite_books': favorite_books,
                      'item_list': MainMenu.objects.all()
                  }
                  )