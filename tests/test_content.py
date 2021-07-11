import pytest


REFERENCE_CONTENT = [
    ('/',               'Parts Horse', 'title'),
    ('/api',            'application/json', 'content type'),
    ('/parts',          'ATmega328', 'part name'),
    ('/parts',          '8-bit AVR microcontroller with 32KB of program memory.', 'description'),
    ('/search?q=lm555', 'LM555, NA555, NE555, SA555, SE555', 'search'),
]


@pytest.fixture
def app():
    from app import gen_app
    return gen_app()

@pytest.mark.parametrize('path,expected,_', REFERENCE_CONTENT,
                         ids=(id for (_path, _content, id) in REFERENCE_CONTENT))
@pytest.mark.asyncio
async def test_content(app, path: str, expected: str, _):
    client = app.test_client()
    response = await client.get(path)
    assert expected in await response.get_data(as_text=True)
