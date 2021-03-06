import sys

PY2 = sys.version_info[0] == 2

if PY2:
    text_type = unicode
    def with_str_method(cls):
        """Class decorator that handles __str__ compat between py2 and py3."""
        # In python2, the __str__ should be __unicode__
        # and __str__ should return bytes.
        cls.__unicode__ = cls.__str__
        def __str__(self):
            return self.__unicode__().encode('utf-8')
        cls.__str__ = __str__
        return cls
    def with_repr_method(cls):
        """Class decorator that handle __repr__ with py2 and py3."""
        # This is almost the same thing as with_str_method *except*
        # it uses the unicode_escape encoding.  This also means we need to be
        # careful encoding the input multiple times, so we only encode
        # if we get a unicode type.
        original_repr_method = cls.__repr__
        def __repr__(self):
            original_repr = original_repr_method(self)
            if isinstance(original_repr, text_type):
                original_repr = original_repr.encode('unicode_escape')
            return original_repr
        cls.__repr__ = __repr__
        return cls
else:
    text_type = str
    def with_str_method(cls):
        # In python3, we don't need to do anything, we return a str type.
        return cls
    def with_repr_method(cls):
        return cls
