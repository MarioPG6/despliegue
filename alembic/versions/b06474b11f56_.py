"""empty message

Revision ID: b06474b11f56
Revises: e2c36b85d464
Create Date: 2024-11-19 14:48:09.561330

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa
import sqlmodel

# revision identifiers, used by Alembic.
revision: str = 'b06474b11f56'
down_revision: Union[str, None] = 'e2c36b85d464'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('servicio', schema=None) as batch_op:
        batch_op.add_column(sa.Column('fecha_cierre', sa.DateTime(), server_default=sa.text("'2024-11-19 14:48:03.599943'"), nullable=False))

    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('servicio', schema=None) as batch_op:
        batch_op.drop_column('fecha_cierre')

    # ### end Alembic commands ###