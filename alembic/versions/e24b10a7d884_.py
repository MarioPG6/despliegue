"""empty message

Revision ID: e24b10a7d884
Revises: 63291ffe8000
Create Date: 2024-10-27 16:43:02.412991

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa
import sqlmodel

# revision identifiers, used by Alembic.
revision: str = 'e24b10a7d884'
down_revision: Union[str, None] = '63291ffe8000'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('prueba',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('nombre', sqlmodel.sql.sqltypes.AutoString(), nullable=True),
    sa.Column('correo', sqlmodel.sql.sqltypes.AutoString(), nullable=True),
    sa.Column('comentario', sqlmodel.sql.sqltypes.AutoString(), nullable=True),
    sa.PrimaryKeyConstraint('id')
    )
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('prueba')
    # ### end Alembic commands ###