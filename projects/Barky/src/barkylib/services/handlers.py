from __future__ import annotations

from dataclasses import asdict
from datetime import datetime
from typing import TYPE_CHECKING, Callable, Dict, List, Type

from barkylib.domain import commands, events, models
from barkylib.domain.commands import EditBookmarkCommand
from barkylib.domain.events import BookmarkEdited

if TYPE_CHECKING:
    from . import unit_of_work


def add_bookmark(
    cmd: commands.AddBookmarkCommand,
    uow: unit_of_work.AbstractUnitOfWork,
):
    with uow:
        # look to see if we already have this bookmark as the title is set as unique
        bookmark = None #uow.bookmarks.get(title=cmd.title)

        if bookmark is None:
            bookmark = models.Bookmark(
                cmd.id, cmd.title, cmd.url, cmd.notes, cmd.date_added, cmd.date_edited
            )
            uow.bookmarks.add(bookmark)
        uow.commit()


# ListBookmarksCommand: order_by: str order: str
def list_bookmarks(
    cmd: commands.ListBookmarksCommand,
    uow: unit_of_work.AbstractUnitOfWork,
):
    bookmarks = None

    with uow:
        if cmd.id is None and cmd.title is None:
            bookmarks = uow.bookmarks.find_all(None)
        elif cmd.id is not None:
            bookmarks = uow.bookmarks.get_id(int(cmd.id))
        elif cmd.title is not None:
            bookmarks = uow.bookmarks.get(str(cmd.title))

    return bookmarks


# DeleteBookmarkCommand: id: int
def delete_bookmark(
    cmd: commands.DeleteBookmarkCommand,
    uow: unit_of_work.AbstractUnitOfWork,
):
    with uow:
        pass


# EditBookmarkCommand(Command):
def edit_bookmark(
    cmd: commands.EditBookmarkCommand,
    uow: unit_of_work.AbstractUnitOfWork,
):
    with uow:
        pass


EVENT_HANDLERS = {
    events.BookmarkAdded: [add_bookmark],
    events.BookmarksListed: [list_bookmarks],
    events.BookmarkDeleted: [delete_bookmark],
    events.BookmarkEdited: [edit_bookmark],
}  # type: Dict[Type[events.Event], List[Callable]]

COMMAND_HANDLERS = {
    commands.AddBookmarkCommand: add_bookmark,
    commands.ListBookmarksCommand: list_bookmarks,
    commands.DeleteBookmarkCommand: delete_bookmark,
    commands.EditBookmarkCommand: edit_bookmark,
}  # type: Dict[Type[commands.Command], Callable]
