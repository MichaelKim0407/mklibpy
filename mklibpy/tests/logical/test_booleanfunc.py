from mklibpy.logical import AbstractBooleanFunc, BooleanFunc

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


def test_logical_class():
    class A(AbstractBooleanFunc):
        def __call__(self, *args, **kwargs):
            return True

    assert A()()

    B = AbstractBooleanFunc.NOT_CLASS(A)
    assert not B()()

    assert AbstractBooleanFunc.OR_CLASSES(A, B)()()
    assert not AbstractBooleanFunc.AND_CLASSES(A, B)()()
