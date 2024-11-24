"""empty message

Revision ID: 4a38a963502a
Revises: cb08dcf80c49
Create Date: 2024-11-20 21:49:49.203828

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa
import sqlmodel

# revision identifiers, used by Alembic.
revision: str = '4a38a963502a'
down_revision: Union[str, None] = 'cb08dcf80c49'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('servicio', schema=None) as batch_op:
        batch_op.drop_column('thumbs_down')
        batch_op.drop_column('thumbs_up')

    with op.batch_alter_table('trabajador', schema=None) as batch_op:
        batch_op.add_column(sa.Column('thumbs_up', sa.Integer(), server_default=sa.text('0'), nullable=False))
        batch_op.add_column(sa.Column('thumbs_down', sa.Integer(), server_default=sa.text('0'), nullable=False))

    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('trabajador', schema=None) as batch_op:
        batch_op.drop_column('thumbs_down')
        batch_op.drop_column('thumbs_up')

    with op.batch_alter_table('servicio', schema=None) as batch_op:
        batch_op.add_column(sa.Column('thumbs_up', sa.INTEGER(), server_default=sa.text('0'), nullable=False))
        batch_op.add_column(sa.Column('thumbs_down', sa.INTEGER(), server_default=sa.text('0'), nullable=False))

    # ### end Alembic commands ###
