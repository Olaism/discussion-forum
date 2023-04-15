from ..models import Board, Topic, Post

def create_board(name, description):
    # creates a new board
    return Board.objects.create(
        name=name,
        description=description,
    )

def create_topic(board, subject, starter):
    # creates a new topic in the database given a board instance
    return Topic.objects.create(
        board=board,
        subject=subject,
        starter=starter
    )

def create_post(topic, message, author):
    # creates a new post given a topic instance
    return Post.objects.create(
        message = message,
        topic = topic,
        created_by = author
    )