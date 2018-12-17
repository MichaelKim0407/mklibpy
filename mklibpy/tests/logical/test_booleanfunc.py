from mklibpy.logical import AbstractBooleanFunc, BooleanFunc, TRUE, FALSE

__author__ = 'Michael'


def test_func():
    f = BooleanFunc(lambda: True)
    assert f()

    f2 = BooleanFunc(lambda: False)
    assert not f2()


def test_logical():
    f = BooleanFunc(lambda: False)
    assert (-f)()

    f2 = BooleanFunc(lambda: True)
    assert (f | f2)()
    assert not (f & f2)()


class A(AbstractBooleanFunc):
    def __call__(self, *args, **kwargs):
        return True

    def __str__(self):
        return 'True'


B = AbstractBooleanFunc.NOT_CLASS(A)
C = AbstractBooleanFunc.OR_CLASSES(A, B)
D = AbstractBooleanFunc.AND_CLASSES(A, B)


def test_logical_class():
    assert A()()
    assert not B()()
    assert C()()
    assert not D()()


def test_str():
    assert str(A()) == 'True'
    assert repr(A()) == '<Boolean> True'

    assert str(B()) == f"not ({A()})"
    assert str(C()) == f"({A()}) or ({B()})"
    assert str(D()) == f"({A()}) and ({B()})"


def test_true_false():
    assert TRUE()
    assert TRUE(1, x=2)
    assert str(TRUE) == 'True'

    assert not FALSE()
    assert str(FALSE) == 'False'
