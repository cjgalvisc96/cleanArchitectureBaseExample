from rentomatic.responses import RensponseSuccess


def test_response_success_is_true():
    assert bool(RensponseSuccess()) is True
