"""Initial migration

Revision ID: 2102d212ae69
Revises: 
Create Date: 2025-04-05 18:21:31.452271

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '2102d212ae69'
down_revision = None
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('ssip_workflows',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('submission_id', sa.Integer(), nullable=False),
    sa.Column('dept_coordinator_id', sa.Integer(), nullable=True),
    sa.Column('college_coordinator_id', sa.Integer(), nullable=True),
    sa.Column('principal_id', sa.Integer(), nullable=True),
    sa.Column('dept_action_date', sa.DateTime(), nullable=True),
    sa.Column('college_action_date', sa.DateTime(), nullable=True),
    sa.Column('principal_action_date', sa.DateTime(), nullable=True),
    sa.Column('dept_remarks', sa.Text(), nullable=True),
    sa.Column('college_remarks', sa.Text(), nullable=True),
    sa.Column('principal_remarks', sa.Text(), nullable=True),
    sa.Column('dept_status', sa.String(length=20), nullable=True),
    sa.Column('college_status', sa.String(length=20), nullable=True),
    sa.Column('principal_status', sa.String(length=20), nullable=True),
    sa.Column('current_reviewer', sa.String(length=50), nullable=True),
    sa.Column('created_at', sa.DateTime(), nullable=True),
    sa.Column('updated_at', sa.DateTime(), nullable=True),
    sa.ForeignKeyConstraint(['college_coordinator_id'], ['user.id'], ),
    sa.ForeignKeyConstraint(['dept_coordinator_id'], ['user.id'], ),
    sa.ForeignKeyConstraint(['principal_id'], ['user.id'], ),
    sa.ForeignKeyConstraint(['submission_id'], ['ssip_submissions.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    with op.batch_alter_table('ssip_submissions', schema=None) as batch_op:
        batch_op.alter_column('status',
               existing_type=sa.VARCHAR(length=20),
               type_=sa.String(length=50),
               existing_nullable=True)

    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('ssip_submissions', schema=None) as batch_op:
        batch_op.alter_column('status',
               existing_type=sa.String(length=50),
               type_=sa.VARCHAR(length=20),
               existing_nullable=True)

    op.drop_table('ssip_workflows')
    # ### end Alembic commands ###
