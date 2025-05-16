from datetime import datetime, date
from typing import Optional, Annotated
import enum

from sqlalchemy import (String,
                        Text,
                        ForeignKey,
                        text)
from sqlalchemy.orm import (declarative_base,
                            relationship,
                            mapped_column,
                            Mapped)



intpk = Annotated[int, mapped_column(primary_key=True)]
created_at = Annotated[
    datetime,
    mapped_column(server_default=text("TIMEZONE('utc', now())"))
]


Base = declarative_base()


class TaskStatus(enum.Enum):
    todo = 'todo'
    in_progress = 'in_progress'
    done = 'done'


class TaskWatchers(Base):
    __tablename__ = 'task_watchers'

    user_id: Mapped[int] = mapped_column(
        ForeignKey('user.id', ondelete='CASCADE'),
        primary_key=True,
        )
    task_id: Mapped[int] = mapped_column(
        ForeignKey('task.id', ondelete='CASCADE'),
        primary_key=True,
    )


class TaskExecutors(Base):
    __tablename__ = 'task_executors'

    user_id: Mapped[int] = mapped_column(
        ForeignKey('user.id', ondelete='CASCADE'),
        primary_key=True,
    )
    task_id: Mapped[int] = mapped_column(
        ForeignKey('task.id', ondelete='CASCADE'),
        primary_key=True,
    )


class User(Base):
    __tablename__ = 'user'

    id: Mapped[intpk]
    full_name: Mapped[str] = mapped_column(
        String(100),
        nullable=False)
    email: Mapped[str] = mapped_column(
        String(120),
        nullable=False,
        unique=True)
    created_at: Mapped[created_at]

    watched_tasks: Mapped[list['Task']] = relationship(
        'Task',
        secondary='task_watchers',
        back_populates='watchers'
    )
    executed_tasks: Mapped[list['Task']] = relationship(
        'Task',
        secondary='task_executors',
        back_populates='executors'
    )


class Board(Base):
    __tablename__ = 'board'

    id: Mapped[intpk]
    name: Mapped[str] = mapped_column(
        String(100),
        nullable=False,
        unique=True)

    columns = relationship('Column',
                           back_populates='board'
                           )
    tasks = relationship(
        'Task',
        back_populates='board')


class Column(Base):
    __tablename__ = 'column'

    id: Mapped[intpk]
    name: Mapped[str] = mapped_column(
        String(100),
        nullable=False)
    board_id: Mapped[int] = mapped_column(
        ForeignKey(
            'board.id',
            ondelete='CASCADE'
        ),
        nullable=False
    )
    board = relationship(
        'Board',
        back_populates='columns')
    tasks = relationship(
        'Task',
        back_populates='column')


class Sprint(Base):
    __tablename__ = 'sprint'

    id: Mapped[intpk]
    name: Mapped[str] = mapped_column(
        String(100),
        nullable=False)

    start_date: Mapped[date] = mapped_column()
    end_date: Mapped[date] = mapped_column()

    tasks = relationship(
        'Task',
        back_populates='sprint')


class Group(Base):
    __tablename__ = 'group'

    id: Mapped[intpk]
    name: Mapped[str] = mapped_column(
        String(100),
        nullable=False,
        unique=True)
    tasks = relationship(
        'Task',
        back_populates='group')


class Task(Base):
    __tablename__ = 'task'

    id: Mapped[intpk]
    title: Mapped[str] = mapped_column(
        String(255),
        nullable=False)
    description: Mapped[Optional[str]] = mapped_column(Text)
    status: Mapped[TaskStatus]
    created_at: Mapped[datetime] = mapped_column(
        server_default=text("TIMEZONE('utc', now())"),
        index=True
    )
    author_id: Mapped[int] = mapped_column(
        ForeignKey('user.id'),
        nullable=False)
    assignee_id: Mapped[Optional[int]] = mapped_column(
        ForeignKey('user.id'),
        nullable=True)
    column_id: Mapped[Optional[int]] = mapped_column(
        ForeignKey('column.id'),
        nullable=True)
    sprint_id: Mapped[Optional[int]] = mapped_column(
        ForeignKey('sprint.id'),
        nullable=True)
    board_id: Mapped[Optional[int]] = mapped_column(
        ForeignKey('board.id'),
        nullable=True)
    group_id: Mapped[Optional[int]] = mapped_column(
        ForeignKey('group.id'),
        nullable=True)
    column = relationship(
        'Column',
        back_populates='task')
    sprint = relationship(
        'Sprint',
        back_populates='task')
    group = relationship(
        'Group',
        back_populates='task')
    watchers: Mapped[list['User']] = relationship(
        'User',
        secondary='task_watchers',
        back_populates='watched_tasks'
    )
    executors: Mapped[list['User']] = relationship(
        'User',
        secondary='task_executors',
        back_populates='executed_tasks'
    )
