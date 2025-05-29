from vidaplus.database import get_session
from vidaplus.test import criar_superusuario


def main():
    # Consome o gerador para obter a sessão
    with next(get_session()) as session:  # Usa o gerador corretamente
        try:
            # Chama a função para criar o superusuário
            superuser = criar_superusuario(session)
            print(f'Superusuário criado com sucesso: {superuser.email}')
        except Exception as e:
            print(f'Erro ao criar superusuário: {e}')
