from sqlalchemy.orm import DeclarativeBase, ColumnProperty


class Base(DeclarativeBase):
    def to_dict(self):
        print([c.key for c in self.__mapper__.attrs if isinstance(c, ColumnProperty)])
        print([c.name for c in self.__table__.columns])
        return {
            c.key: getattr(self, c.key)
            for c in self.__mapper__.attrs
            if isinstance(c, ColumnProperty)
        }
