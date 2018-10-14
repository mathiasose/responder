import pytest

def test_custom_encoding(api, session):
    data = "hi alex!"

    @api.route("/")
    async def route(req, resp):
        req.encoding = "ascii"
        resp.text = await req.text

    r = session.get(api.url_for(route), data=data)
    assert r.text == data


def test_bytes_encoding(api, session):
    data = b"hi lenny!"

    @api.route("/")
    async def route(req, resp):
        resp.text = (await req.content).decode("utf-8")

    r = session.get(api.url_for(route), data=data)
    assert r.content == data


def test_false_encoding_raises(api, session):
    data = "hi mom!"

    @api.route("/")
    async def route(req, resp):
        req.encoding = "non-existient"
        resp.text = await req.text

    with pytest.raises(LookupError):
        session.get(api.url_for(route), data=data)
