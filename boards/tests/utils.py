from ..models import Board, Topic, Post

def create_board(name, description):
    # creates a new board
    return Board.objects.create(
        name=name,
        description=description,
    )

def create_boards(num=20):
    # create num of boards and return the last created board
    for i in range(num):
        Board.objects.create(
            name='board {}'.format(i),
            description = 'board description {}'.format(i)
        )
    return Board.objects.last()

def create_topic(board, subject, starter):
    # creates a new topic in the database given a board instance
    return Topic.objects.create(
        board=board,
        subject=subject,
        starter=starter
    )

def create_topics(board, starter, num=20):
    for i in range(num):
        Topic.objects.create(
            board=board,
            subject=f"subject {i}",
            starter=starter
        )
    return Topic.objects.last()

def create_post(topic, message, author):
    # creates a new post given a topic instance
    return Post.objects.create(
        message = message,
        topic = topic,
        created_by = author
    )


def create_posts(topic, author, num=20):
    # creates num posts and return the last created post
    for i in range(num):
        Post.objects.create(
            message = f"message {i}",
            topic = topic,
            created_by = author
        )
    return Post.objects.last()