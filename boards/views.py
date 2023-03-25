from django.contrib.auth.decorators import login_required
from django.shortcuts import (
    get_object_or_404,
    render
)

from .forms import NewTopicForm
from .models import Board


@login_required
def home(request):
    boards = Board.objects.all()
    return render(request, 'home.html', {'boards': boards})


@login_required
def board_topics(request, pk):
    board = get_object_or_404(Board, pk=pk)
    return render(request, 'topics.html', {'board': board})


@login_required
def new_topic(request, pk):
    board = get_object_or_404(Board, pk=pk)
    if request.method == 'POST':
        form = NewTopicForm(request.POST)
        if form.is_valid():
            topic = form.save(commit=False)
            topic.board = board
            topic.starter = request.user
            topic.save()
            post = Post.objects.create(
                message=form.get_cleaned_data('message'),
                topic=topic,
                created_by=request.user
            )
            return redirect('board_topics', pk=board.pk)
    else:
        form = NewTopicForm()
    return render(request, 'new_topic.html', {'board': board, 'form': form})
