# addresses.py

class Address:
    VALID_ADDRESSES = {"X", "Y", "Z", "A", "G", "F", "M", "S", "T", "R", "I", "J", "K", "L", "P", "D", "H"}

    def __new__(cls, *args, **kwargs):
        raise TypeError(f"Cannot instantiate {cls.__name__}. Use the class directly for the address letter.")

    @classmethod
    def letter(cls):
        if cls.__name__ not in cls.VALID_ADDRESSES:
            raise ValueError(f"Invalid address letter: {cls.__name__}")
        return cls.__name__

    @classmethod
    def __repr__(cls):
        return cls.letter()


# Define each valid address class as a top-level class
class A(Address):
    pass

class D(Address):
    pass

class F(Address):
    pass

class G(Address):
    pass

class H(Address):
    pass

class I(Address):
    pass

class J(Address):
    pass

class K(Address):
    pass
    
class L(Address):
    pass

class M(Address):
    pass

class P(Address):
    pass

class R(Address):
    pass

class S(Address):
    pass

class T(Address):
    pass

class X(Address):
    pass

class Y(Address):
    pass

class Z(Address):
    pass


# Specify which classes to include in wildcard imports
#__all__ = ['A', 'D', 'F', 'G', 'H', 'I', 'J', 'K', 'M', 'P', 'R', 'S', 'T', 'X', 'Y', 'Z']