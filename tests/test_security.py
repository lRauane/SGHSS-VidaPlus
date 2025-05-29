from jwt import decode

from vidaplus.security import create_access_token, settings


def test_token():
    data = {'test': 'test'}
    token = create_access_token(data)

    decoded = decode(
        token, settings.SECRET_KEY, algorithms=[settings.ALGORITHM]
    )

    assert decoded['test'] == 'test'
    assert 'exp' in decoded
