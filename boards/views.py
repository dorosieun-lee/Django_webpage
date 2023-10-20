from django.shortcuts import render, redirect, get_object_or_404, get_list_or_404
from .models import Board, Comment
from .forms import BoardForm, CommentForm
from django.views.decorators.http import require_http_methods
from django.contrib.auth.decorators import login_required
from django.db.models import Count


# Create your views here.
@require_http_methods(["GET"])
def index(request):
    boards = Board.objects.all().order_by('-created_at')
    context = {
        'boards': boards
    }
    return render(request, 'boards/index.html', context)


@require_http_methods(["GET"])
def index_order(request, order_by):
    boards = Board.objects
    if order_by == 'like':
        boards = boards.annotate(like_count=Count('like_users')).order_by('-like_count', '-created_at')
    elif order_by == 'view':
        boards = boards.order_by('-view_count')
    elif order_by == 'comment':
        boards = boards.annotate(comment_count=Count('comments')).order_by('-comment_count', '-created_at')

    context = {
        'boards': boards
    }
    return render(request, 'boards/index.html', context)



@require_http_methods(["GET", "POST"])
def detail(request, pk):
    board = get_object_or_404(Board, pk=pk)

    if request.method == 'POST' and request.user == board.user:
        board.delete()
        return redirect('boards:index')

    # 조회수 +1 하고 조회수를 표시하는 로직 구현하기 (새로고침 할 때마다 +1 되는 문제점 있음)
    board.update_counter()

    comments = board.comments.all()
    comment_form = CommentForm()
    
    context = {
        'board': board,
        'comments': comments,
        'comment_form': comment_form,
    }
    return render(request, 'boards/detail.html', context)


@login_required
@require_http_methods(['POST'])
def like(request, board_pk):
    board = Board.objects.get(pk=board_pk)
    if board.like_users.filter(pk=request.user.pk).exists():
        board.like_users.remove(request.user)
    else:
        board.like_users.add(request.user)
    return redirect('boards:detail', board_pk)


@login_required
@require_http_methods(["GET", "POST"])
def update(request, pk):
    board = get_object_or_404(Board, pk=pk)
    if request.user == board.user:
        if request.method == 'POST':
            form = BoardForm(request.POST, instance=board)
            if form.is_valid():
                form.save()
                return redirect('boards:detail', board.pk)
        else:
            form = BoardForm(instance=board)
        context = {
            'board': board,
            'form': form,
        }        
        return render(request, 'boards/update.html', context)
    else:
        return redirect('boards:index')
    

@login_required
@require_http_methods(["GET", "POST"])
def create(request):
    if request.method == 'POST':
        form = BoardForm(request.POST)
        if form.is_valid():
            board = form.save(commit=False)
            board.user = request.user
            form.save()
            return redirect('boards:index')
    else:
        form = BoardForm()
    context = {
        'form': form,
    }
    return render(request, 'boards/create.html', context)


@login_required
@require_http_methods(["POST"])
def comment(request, board_pk):
    board = get_object_or_404(Board, pk=board_pk)
    if request.method == 'POST':
        form = CommentForm(request.POST)
        if form.is_valid():
            comment = form.save(commit=False)
            comment.board = board
            comment.user = request.user
            comment.save()
            return redirect('boards:detail', board.pk)


@login_required
@require_http_methods(["POST"])
def comment_detail(request, board_pk, comment_pk):
    comment = get_object_or_404(Comment, pk=comment_pk)
    if request.method == 'POST' and request.user == comment.users:
        comment.delete()
        return redirect('boards:detail', board_pk)