import sqlalchemy as sa
import sqlalchemy.orm as orm


class Company:
    id: int = sa.Column(sa.Integer, primary_key=True, autoincrement=True)
    name: str = sa.Column(sa.String(length=50))
    country: str = sa.Column(sa.String(length=50))

    employees: list["Employee"] = orm.relationship("Employee", back_populates="company")
