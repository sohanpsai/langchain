from langchain_core.load import Serializable, dumpd


def test_simple_serialization() -> None:
    class Foo(Serializable):
        bar: int
        baz: str

    foo = Foo(bar=1, baz="hello")
    assert dumpd(foo) == {
        "id": ["tests", "unit_tests", "load", "test_serializable", "Foo"],
        "lc": 1,
        "repr": "Foo(bar=1, baz='hello')",
        "type": "not_implemented",
    }


def test_simple_serialization_is_serializable() -> None:
    class Foo(Serializable):
        bar: int
        baz: str

        @classmethod
        def is_lc_serializable(cls) -> bool:
            return True

    foo = Foo(bar=1, baz="hello")
    assert foo.lc_id() == ["tests", "unit_tests", "load", "test_serializable", "Foo"]
    assert dumpd(foo) == {
        "id": ["tests", "unit_tests", "load", "test_serializable", "Foo"],
        "kwargs": {"bar": 1, "baz": "hello"},
        "lc": 1,
        "type": "constructor",
    }


def test_simple_serialization_secret() -> None:
    """Test handling of secrets."""
    from pydantic import SecretStr

    from langchain_core.load import Serializable

    class Foo(Serializable):
        bar: int
        baz: str
        secret2: SecretStr

        @classmethod
        def is_lc_serializable(cls) -> bool:
            return True

    foo = Foo(bar=1, baz="baz", secret1="secret", secret2=SecretStr("meow"))
    assert dumpd(foo) == {
        "id": ["tests", "unit_tests", "load", "test_serializable", "Foo"],
        "kwargs": {
            "bar": 1,
            "baz": "baz",
            "secret2": {
                "id": ["pydantic", "types", "SecretStr"],
                "lc": 1,
                "repr": "SecretStr('**********')",
                "type": "not_implemented",
            },
        },
        "lc": 1,
        "type": "constructor",
    }