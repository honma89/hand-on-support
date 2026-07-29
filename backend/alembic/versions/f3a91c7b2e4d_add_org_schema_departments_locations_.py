"""add org schema: departments, address/location hierarchy, activities, recognitions, media, documents, announcements, donations, audit logs, tier levels

Revision ID: f3a91c7b2e4d
Revises: e74810f03c36
Create Date: 2026-07-29 00:00:00.000000

Ported from the original planned schema (main branch), limited to tables
that are purely additive on top of the current implementation. Deliberately
excludes `roles`/`user_roles` and `volunteers` — both conflict with the
existing single-column `users.role` design and `users` profile fields
respectively; see the "Descoped/Backlog Review" schema doc for that call.
"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql

# revision identifiers, used by Alembic.
revision: str = 'f3a91c7b2e4d'
down_revision: Union[str, None] = 'e74810f03c36'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # --- Location hierarchy (Bhutan admin divisions) ---
    op.create_table('dzongkhags',
        sa.Column('id', sa.UUID(), nullable=False),
        sa.Column('name', sa.String(length=100), nullable=False),
        sa.PrimaryKeyConstraint('id'),
        sa.UniqueConstraint('name'),
    )
    op.create_table('dungkhags',
        sa.Column('id', sa.UUID(), nullable=False),
        sa.Column('name', sa.String(length=100), nullable=False),
        sa.Column('dzongkhag_id', sa.UUID(), nullable=False),
        sa.ForeignKeyConstraint(['dzongkhag_id'], ['dzongkhags.id'], ondelete='CASCADE'),
        sa.PrimaryKeyConstraint('id'),
    )
    op.create_index(op.f('ix_dungkhags_dzongkhag_id'), 'dungkhags', ['dzongkhag_id'])
    op.create_table('gewogs',
        sa.Column('id', sa.UUID(), nullable=False),
        sa.Column('name', sa.String(length=100), nullable=False),
        sa.Column('dungkhag_id', sa.UUID(), nullable=False),
        sa.ForeignKeyConstraint(['dungkhag_id'], ['dungkhags.id'], ondelete='CASCADE'),
        sa.PrimaryKeyConstraint('id'),
    )
    op.create_index(op.f('ix_gewogs_dungkhag_id'), 'gewogs', ['dungkhag_id'])

    op.create_table('addresses',
        sa.Column('id', sa.UUID(), nullable=False),
        sa.Column('address_type', sa.Enum('BHUTAN', 'INTERNATIONAL', name='address_type'), nullable=False),
        sa.Column('dzongkhag_id', sa.UUID(), nullable=True),
        sa.Column('dungkhag_id', sa.UUID(), nullable=True),
        sa.Column('gewog_id', sa.UUID(), nullable=True),
        sa.Column('village', sa.String(length=100), nullable=True),
        sa.Column('country', sa.String(length=100), nullable=True),
        sa.Column('city', sa.String(length=100), nullable=True),
        sa.Column('state_province', sa.String(length=100), nullable=True),
        sa.Column('postal_code', sa.String(length=20), nullable=True),
        sa.Column('street_address', sa.Text(), nullable=True),
        sa.Column('address_line_2', sa.Text(), nullable=True),
        sa.Column('house_number', sa.String(length=50), nullable=True),
        sa.Column('landmark', sa.Text(), nullable=True),
        sa.Column('full_address', sa.Text(), nullable=True),
        sa.Column('created_at', sa.DateTime(timezone=True), server_default=sa.text('now()'), nullable=False),
        sa.Column('updated_at', sa.DateTime(timezone=True), server_default=sa.text('now()'), nullable=False),
        sa.ForeignKeyConstraint(['dzongkhag_id'], ['dzongkhags.id'], ondelete='SET NULL'),
        sa.ForeignKeyConstraint(['dungkhag_id'], ['dungkhags.id'], ondelete='SET NULL'),
        sa.ForeignKeyConstraint(['gewog_id'], ['gewogs.id'], ondelete='SET NULL'),
        sa.PrimaryKeyConstraint('id'),
    )

    op.create_table('locations',
        sa.Column('id', sa.UUID(), nullable=False),
        sa.Column('name', sa.String(length=150), nullable=False),
        sa.Column('latitude', sa.Float(), nullable=True),
        sa.Column('longitude', sa.Float(), nullable=True),
        sa.PrimaryKeyConstraint('id'),
    )

    # --- Recognition tiers ---
    op.create_table('tier_levels',
        sa.Column('id', sa.UUID(), nullable=False),
        sa.Column('name', sa.Enum('BRONZE', 'SILVER', 'GOLD', 'PLATINUM', name='tier_name'), nullable=False),
        sa.Column('min_points', sa.Integer(), nullable=True),
        sa.PrimaryKeyConstraint('id'),
        sa.UniqueConstraint('name'),
    )

    # --- Org structure ---
    op.create_table('departments',
        sa.Column('id', sa.UUID(), nullable=False),
        sa.Column('name', sa.String(length=100), nullable=False),
        sa.Column('description', sa.Text(), nullable=True),
        sa.Column('head_user_id', sa.UUID(), nullable=True),
        sa.Column('created_at', sa.DateTime(timezone=True), server_default=sa.text('now()'), nullable=False),
        sa.Column('updated_at', sa.DateTime(timezone=True), server_default=sa.text('now()'), nullable=False),
        sa.ForeignKeyConstraint(['head_user_id'], ['users.id'], ondelete='SET NULL'),
        sa.PrimaryKeyConstraint('id'),
    )
    op.create_table('user_departments',
        sa.Column('id', sa.UUID(), nullable=False),
        sa.Column('user_id', sa.UUID(), nullable=False),
        sa.Column('department_id', sa.UUID(), nullable=False),
        sa.Column('role_title', sa.String(length=100), nullable=True),
        sa.Column('created_at', sa.DateTime(timezone=True), server_default=sa.text('now()'), nullable=False),
        sa.Column('updated_at', sa.DateTime(timezone=True), server_default=sa.text('now()'), nullable=False),
        sa.ForeignKeyConstraint(['user_id'], ['users.id'], ondelete='CASCADE'),
        sa.ForeignKeyConstraint(['department_id'], ['departments.id'], ondelete='CASCADE'),
        sa.PrimaryKeyConstraint('id'),
        sa.UniqueConstraint('user_id', 'department_id', name='uq_user_department'),
    )
    op.create_index(op.f('ix_user_departments_user_id'), 'user_departments', ['user_id'])
    op.create_index(op.f('ix_user_departments_department_id'), 'user_departments', ['department_id'])

    # --- Generic loggable activities (independent of event check-in) ---
    op.create_table('activity_categories',
        sa.Column('id', sa.UUID(), nullable=False),
        sa.Column('name', sa.String(length=100), nullable=False),
        sa.PrimaryKeyConstraint('id'),
        sa.UniqueConstraint('name'),
    )
    op.create_table('activities',
        sa.Column('id', sa.UUID(), nullable=False),
        sa.Column('name', sa.String(length=150), nullable=False),
        sa.Column('description', sa.Text(), nullable=True),
        sa.Column('default_points', sa.Integer(), nullable=False),
        sa.Column('default_hours', sa.Numeric(), nullable=False),
        sa.Column('activity_category_id', sa.UUID(), nullable=False),
        sa.ForeignKeyConstraint(['activity_category_id'], ['activity_categories.id'], ondelete='RESTRICT'),
        sa.PrimaryKeyConstraint('id'),
    )
    op.create_index(op.f('ix_activities_activity_category_id'), 'activities', ['activity_category_id'])
    op.create_table('activity_logs',
        sa.Column('id', sa.UUID(), nullable=False),
        sa.Column('user_id', sa.UUID(), nullable=False),
        sa.Column('activity_id', sa.UUID(), nullable=False),
        sa.Column('event_id', sa.UUID(), nullable=True),
        sa.Column('points_earned', sa.Integer(), nullable=False),
        sa.Column('hours_logged', sa.Numeric(), nullable=False),
        sa.Column('approved_by_id', sa.UUID(), nullable=True),
        sa.Column('approved_at', sa.DateTime(timezone=True), nullable=True),
        sa.Column('created_at', sa.DateTime(timezone=True), server_default=sa.text('now()'), nullable=False),
        sa.Column('updated_at', sa.DateTime(timezone=True), server_default=sa.text('now()'), nullable=False),
        sa.ForeignKeyConstraint(['user_id'], ['users.id'], ondelete='CASCADE'),
        sa.ForeignKeyConstraint(['activity_id'], ['activities.id'], ondelete='RESTRICT'),
        sa.ForeignKeyConstraint(['event_id'], ['events.id'], ondelete='SET NULL'),
        sa.ForeignKeyConstraint(['approved_by_id'], ['users.id'], ondelete='SET NULL'),
        sa.PrimaryKeyConstraint('id'),
    )
    op.create_index(op.f('ix_activity_logs_user_id'), 'activity_logs', ['user_id'])
    op.create_index(op.f('ix_activity_logs_activity_id'), 'activity_logs', ['activity_id'])

    # --- Recognition / media / documents / announcements / donations / audit ---
    op.create_table('recognitions',
        sa.Column('id', sa.UUID(), nullable=False),
        sa.Column('user_id', sa.UUID(), nullable=False),
        sa.Column('title', sa.String(length=150), nullable=False),
        sa.Column('description', sa.Text(), nullable=True),
        sa.Column('month', sa.Integer(), nullable=False),
        sa.Column('year', sa.Integer(), nullable=False),
        sa.Column('created_at', sa.DateTime(timezone=True), server_default=sa.text('now()'), nullable=False),
        sa.Column('updated_at', sa.DateTime(timezone=True), server_default=sa.text('now()'), nullable=False),
        sa.ForeignKeyConstraint(['user_id'], ['users.id'], ondelete='CASCADE'),
        sa.PrimaryKeyConstraint('id'),
    )
    op.create_index(op.f('ix_recognitions_user_id'), 'recognitions', ['user_id'])

    op.create_table('medias',
        sa.Column('id', sa.UUID(), nullable=False),
        sa.Column('title', sa.String(length=200), nullable=False),
        sa.Column('type', sa.Enum('PHOTO', 'VIDEO', name='media_type'), nullable=False),
        sa.Column('url', sa.String(length=500), nullable=False),
        sa.Column('event_id', sa.UUID(), nullable=True),
        sa.Column('uploaded_by_id', sa.UUID(), nullable=False),
        sa.Column('created_at', sa.DateTime(timezone=True), server_default=sa.text('now()'), nullable=False),
        sa.Column('updated_at', sa.DateTime(timezone=True), server_default=sa.text('now()'), nullable=False),
        sa.ForeignKeyConstraint(['event_id'], ['events.id'], ondelete='SET NULL'),
        sa.ForeignKeyConstraint(['uploaded_by_id'], ['users.id'], ondelete='CASCADE'),
        sa.PrimaryKeyConstraint('id'),
    )

    op.create_table('documents',
        sa.Column('id', sa.UUID(), nullable=False),
        sa.Column('title', sa.String(length=200), nullable=False),
        sa.Column('category', sa.Enum('PROPOSAL', 'REPORT', 'NOTICE', name='document_category'), nullable=False),
        sa.Column('file_url', sa.String(length=500), nullable=False),
        sa.Column('uploaded_by_id', sa.UUID(), nullable=False),
        sa.Column('created_at', sa.DateTime(timezone=True), server_default=sa.text('now()'), nullable=False),
        sa.Column('updated_at', sa.DateTime(timezone=True), server_default=sa.text('now()'), nullable=False),
        sa.ForeignKeyConstraint(['uploaded_by_id'], ['users.id'], ondelete='CASCADE'),
        sa.PrimaryKeyConstraint('id'),
    )

    op.create_table('announcements',
        sa.Column('id', sa.UUID(), nullable=False),
        sa.Column('title', sa.String(length=200), nullable=False),
        sa.Column('content', sa.Text(), nullable=False),
        sa.Column('created_by_id', sa.UUID(), nullable=False),
        sa.Column('created_at', sa.DateTime(timezone=True), server_default=sa.text('now()'), nullable=False),
        sa.Column('updated_at', sa.DateTime(timezone=True), server_default=sa.text('now()'), nullable=False),
        sa.ForeignKeyConstraint(['created_by_id'], ['users.id'], ondelete='CASCADE'),
        sa.PrimaryKeyConstraint('id'),
    )

    op.create_table('donations',
        sa.Column('id', sa.UUID(), nullable=False),
        sa.Column('donor_name', sa.String(length=150), nullable=False),
        sa.Column('phone_number', sa.String(length=20), nullable=False),
        sa.Column('email', sa.String(length=255), nullable=True),
        sa.Column('payment_reference', sa.String(length=255), nullable=True),
        sa.Column('status', sa.Enum('PENDING', 'SUCCESS', 'FAILED', name='donation_status'), nullable=False),
        sa.Column('created_at', sa.DateTime(timezone=True), server_default=sa.text('now()'), nullable=False),
        sa.Column('updated_at', sa.DateTime(timezone=True), server_default=sa.text('now()'), nullable=False),
        sa.PrimaryKeyConstraint('id'),
    )

    op.create_table('audit_logs',
        sa.Column('id', sa.UUID(), nullable=False),
        sa.Column('user_id', sa.UUID(), nullable=True),
        sa.Column('action_type', sa.String(length=100), nullable=False),
        sa.Column('entity_name', sa.String(length=100), nullable=False),
        sa.Column('entity_id', sa.UUID(), nullable=True),
        sa.Column('timestamp', sa.DateTime(timezone=True), server_default=sa.text('now()'), nullable=False),
        sa.Column('metadata', postgresql.JSON(astext_type=sa.Text()), nullable=True),
        sa.ForeignKeyConstraint(['user_id'], ['users.id'], ondelete='SET NULL'),
        sa.PrimaryKeyConstraint('id'),
    )

    # --- Wire the new, nullable links onto existing tables ---
    op.add_column('users', sa.Column('tier_level_id', sa.UUID(), nullable=True))
    op.add_column('users', sa.Column('address_id', sa.UUID(), nullable=True))
    op.create_foreign_key('fk_users_tier_level_id', 'users', 'tier_levels', ['tier_level_id'], ['id'], ondelete='SET NULL')
    op.create_foreign_key('fk_users_address_id', 'users', 'addresses', ['address_id'], ['id'], ondelete='SET NULL')

    op.add_column('events', sa.Column('location_id', sa.UUID(), nullable=True))
    op.create_foreign_key('fk_events_location_id', 'events', 'locations', ['location_id'], ['id'], ondelete='SET NULL')


def downgrade() -> None:
    op.drop_constraint('fk_events_location_id', 'events', type_='foreignkey')
    op.drop_column('events', 'location_id')

    op.drop_constraint('fk_users_address_id', 'users', type_='foreignkey')
    op.drop_constraint('fk_users_tier_level_id', 'users', type_='foreignkey')
    op.drop_column('users', 'address_id')
    op.drop_column('users', 'tier_level_id')

    op.drop_table('audit_logs')
    op.drop_table('donations')
    op.drop_table('announcements')
    op.drop_table('documents')
    op.drop_table('medias')
    op.drop_index(op.f('ix_recognitions_user_id'), table_name='recognitions')
    op.drop_table('recognitions')

    op.drop_index(op.f('ix_activity_logs_activity_id'), table_name='activity_logs')
    op.drop_index(op.f('ix_activity_logs_user_id'), table_name='activity_logs')
    op.drop_table('activity_logs')
    op.drop_index(op.f('ix_activities_activity_category_id'), table_name='activities')
    op.drop_table('activities')
    op.drop_table('activity_categories')

    op.drop_index(op.f('ix_user_departments_department_id'), table_name='user_departments')
    op.drop_index(op.f('ix_user_departments_user_id'), table_name='user_departments')
    op.drop_table('user_departments')
    op.drop_table('departments')

    op.drop_table('tier_levels')
    op.drop_table('locations')
    op.drop_table('addresses')

    op.drop_index(op.f('ix_gewogs_dungkhag_id'), table_name='gewogs')
    op.drop_table('gewogs')
    op.drop_index(op.f('ix_dungkhags_dzongkhag_id'), table_name='dungkhags')
    op.drop_table('dungkhags')
    op.drop_table('dzongkhags')

    # Enum types created above must be dropped explicitly on Postgres
    for enum_name in (
        'address_type', 'tier_name', 'media_type', 'document_category', 'donation_status',
    ):
        sa.Enum(name=enum_name).drop(op.get_bind(), checkfirst=True)
