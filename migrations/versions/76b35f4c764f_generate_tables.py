"""Generate tables

Revision ID: 76b35f4c764f
Revises: bc7827844a23
Create Date: 2025-05-18 11:01:51.917587

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '76b35f4c764f'
down_revision: Union[str, None] = 'bc7827844a23'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    # Passo 1: Renomear a tabela existente
    op.rename_table('leitos', 'leitos_old')

    # Passo 2: Criar a nova tabela com a definição atualizada
    op.create_table(
        'leitos',
        sa.Column('id', sa.Integer, primary_key=True),
        sa.Column('numero_leito', sa.String(10), nullable=False),
        sa.Column('paciente_id', sa.Integer, sa.ForeignKey('paciente_users.id'), nullable=True),
        sa.Column('tipo', sa.Enum('ENFERMARIA', 'UTI', name='tipoleito'), nullable=False),
        sa.Column('status', sa.Enum('LIVRE', 'OCUPADO', 'MANUTENCAO', name='statusleito'), nullable=False),
    )

    # Passo 3: Copiar os dados da tabela antiga para a nova
    op.execute("""
        INSERT INTO leitos (id, numero_leito, paciente_id, tipo, status)
        SELECT id, numero_leito, paciente_id, tipo, status
        FROM leitos_old
    """)

    # Passo 4: Remover a tabela antiga
    op.drop_table('leitos_old')


def downgrade() -> None:
    """Downgrade schema."""
    # Passo 1: Renomear a tabela atual
    op.rename_table('leitos', 'leitos_new')

    # Passo 2: Criar a tabela antiga com a definição original
    op.create_table(
        'leitos',
        sa.Column('id', sa.Integer, primary_key=True),
        sa.Column('numero_leito', sa.String(10), nullable=False),
        sa.Column('paciente_id', sa.Integer, sa.ForeignKey('paciente_users.id'), nullable=False),
        sa.Column('tipo', sa.Enum('ENFERMARIA', 'UTI', name='tipoleito'), nullable=False),
        sa.Column('status', sa.Enum('LIVRE', 'OCUPADO', 'MANUTENCAO', name='statusleito'), nullable=False),
    )

    # Passo 3: Copiar os dados da tabela nova para a antiga
    op.execute("""
        INSERT INTO leitos (id, numero_leito, paciente_id, tipo, status)
        SELECT id, numero_leito, paciente_id, tipo, status
        FROM leitos_new
    """)

    # Passo 4: Remover a tabela nova
    op.drop_table('leitos_new')
