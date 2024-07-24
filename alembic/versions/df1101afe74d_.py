"""empty message

Revision ID: df1101afe74d
Revises: a42b7176b187
Create Date: 2024-07-12 20:03:30.486100

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = 'df1101afe74d'
down_revision: Union[str, None] = 'a42b7176b187'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('blogs', sa.Column('user_id', sa.Integer(), nullable=True))
    op.create_foreign_key('blog_user_fk', 'blogs', 'users', ['user_id'], ['id'], ondelete='CASCADE')

    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_constraint(None, 'blogs', type_='foreignkey')
    op.drop_column('blogs', 'user_id')
    # ### end Alembic commands ###
