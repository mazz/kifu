"""seed initial data

Revision ID: 1bc0be10afc1
Revises: 4f3b93305fe8
Create Date: 2013-12-16 22:29:58.982986

"""

# revision identifiers, used by Alembic.
revision = '1bc0be10afc1'
down_revision = '4f3b93305fe8'

from alembic import op
import sqlalchemy as sa

from ~~~PROJNAME~~~.models.auth import User

def upgrade():
    """Preseed data into the system."""
    current_context = op.get_context()
    meta = current_context.opts['target_metadata']
    user = sa.Table('users', meta, autoload=True)

    api_key = User.gen_api_key()
    # Add the initial admin user account.
    op.bulk_insert(user, [{
        'username': u'admin',
        'password': u'$2a$10$FK7DVvSYzXNqJRbYD8yAJ..eKosDzYH29ERuKCwlMLdozMWDkySl2',
        'email': u'foo@bar.bar',
        'activated': True,
        'is_admin': True,
        'api_key': api_key,
        }
    ])

def downgrade():
    current_context = op.get_context()
    meta = current_context.opts['target_metadata']
    user = sa.Table('users', meta, autoload=True)

    # remove all records to undo the preseed.
    op.execute(user.delete())
