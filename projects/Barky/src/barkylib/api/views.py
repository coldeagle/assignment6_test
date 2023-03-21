from barkylib.services import unit_of_work

def bookmarks(id: int, uow: unit_of_work.SqlAlchemyUnitOfWork):
    with uow:
        results = uow.session.execute(
            """
            SELECT * FROM bookmarks WHERE id = :id
            """,
            dict(id=id),
        )
    return [dict(r) for r in results]

def bookmarks(title: str, uow: unit_of_work.SqlAlchemyUnitOfWork):
    with uow:
        results = uow.session.execute(
            """
            SELECT * FROM bookmarks WHERE title = :title
            """,
            dict(title=title),
        )
    return [dict(r) for r in results]
