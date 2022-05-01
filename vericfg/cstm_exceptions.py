''' Base Errors '''
class CfgPyError(Exception):

    __slots__ = ('msg')

    def __str__(self):
        return self.msg

class CfgPyValueError(CfgPyError):
    pass

class CfgPyTypeError(CfgPyError):
    pass

class CfgPyKeyError(CfgPyError):
    pass


''' CfgPy Errors '''
class CfgPyUseError(CfgPyError):
    def __init__(self, msg):
        super().__init__(msg)

class RestrictionConflict(CfgPyUseError):
    def __init__(self, msg):
        suuper().__init__(msg)

class PreviousRestrictionConflict(CfgPyUseError):
    def __init__(self, msg):
        suuper().__init__(msg)

class ValueOutOfRangeError(CfgPyValueError):
    def __init__(self, name='Value', value=None, **kargs):

        if not isinstance(name, str):
            raise CfgPyUseError(f'Name must be a string')

        if value is None:
            self.msg = f'{name} is out of acceptable range'
        else:
            self.msg = f'{name} ({value}) is out of acceptable range'

        if 'min' in kargs:
            minv = kargs.get('min')
            self.msg += f'\n\t- Value must be greater than {minv}'

        if 'mineq' in kargs:
            minv = kargs.get('mineq')
            self.msg += f'\n\t- Value must be greater than or equal to {minv}'

        if 'max' in kargs:
            maxv = kargs.get('maxeq')
            self.msg += f'\n\t- Value must be less than {maxv}'

        if 'maxeq' in kargs:
            maxv = kargs.get('maxeq')
            self.msg += f'\n\t- Value must be less than or equal to {maxv}'

        super().__init__(self.msg)

class IncorrectTypeError(CfgPyTypeError):

    def __init__(self, name='Value', value=None, dtype=None):

        if not isinstance(name, str):
            raise CfgPyUseError(f'Name must be a string')

        if value is None:
            self.msg = f'{name} is not an acceptable type'
        else:
            self.msg = f'{name} ({type(value)}) is not an acceptable type'

        if dtype is not None:
            if isinstance(dtype, tuple):
                if not all([isinstance(dt, type) for dt in dtype]):
                    raise CfgPyUseError('All values in tuple must be a type')
                self.msg += f'\n\tAcceptable dtypes include: '
                for dt in dtype:
                    self.msg += f'\n\t\t-{dt}'
            else:
                if not isinstance(dtype, type):
                    raise CfgPyUseError('dtype must be a type')
                self.msg += f'\n\tMust be a {dtype}'

        super().__init__(self.msg)

class NonIterableError(CfgPyTypeError):

    def __init__(self, name='Value', value=None):

        if value is None:
            self.msg = f'{name} is not an iterable object'
        else:
            self.msg = f'{name} ({type(value)}) is not an iterable object'

        super().__init__(self.msg)

class IterableError(CfgPyTypeError):

    def __init__(self, name='Value', value=None):

        if value is None:
            self.msg = f'{name} is an iterable object'
        else:
            self.msg = f'{name} ({type(value)}) is an iterable object'

        super().__init__(self.msg)

class NonHashableError(CfgPyTypeError):

    def __init__(self, name='Value', value=None):

        if value is None:
            self.msg = f'{name} is not a hashable object'
        else:
            self.msg = f'{name} ({type(value)}) is not a hashable object'

        super().__init__(self.msg)

class HashableError(CfgPyTypeError):

    def __init__(self, name='Value', value=None):

        if value is None:
            self.msg = f'{name} is a hashable object'
        else:
            self.msg = f'{name} ({type(value)}) is a hashable object'

        super().__init__(self.msg)

class NonCallableError(CfgPyTypeError):

    def __init__(self, name='Value', value=None):

        if value is None:
            self.msg = f'{name} is not a callable object'
        else:
            self.msg = f'{name} ({type(value)}) is not a callable object'

        super().__init__(self.msg)

class CallableError(CfgPyTypeError):

    def __init__(self, name='Value', value=None):

        if value is None:
            self.msg = f'{name} is a callable object'
        else:
            self.msg = f'{name} ({type(value)}) is a callable object'

        super().__init__(self.msg)

class InvalidOptionError(CfgPyValueError):

    def __init__(self, name='Value', value=None, options=None):

        if value is None:
            self.msg = f'{name} is a callable object'
        else:
            self.msg = f'{name} ({type(value)}) is a callable object'

        if options is not None:
            self.msg += '\n\tAcceptable options include: '
            for opt in options:
                self.msg += f'\n\t\t- {opt} ({type(opt)})'

        super().__init__(self.msg)

class NotDivisibleByError(CfgPyValueError):

    def __init__(self, name='Value', value=None, div_by=None):

        if value is None:
            self.msg = f'{name} is a callable object'
        else:
            self.msg = f'{name} ({value}) is a callable object'

        if div_by is not None:
            if not isinstance(div_by, (int, float)):
                raise CfgPyUseError('div_by must be an int or a float value')
            self.msg += f'\n\tMust be divisible by {div_by}'

        super().__init__(self.msg)

class ParameterNotProvidedError(CfgPyKeyError):

    def __init__(self, name, **kargs):

        kargs = kargs.copy()

        if 'desc' not in kargs:
            self.msg = f'{name} parameter was not provided'
        else:
            desc = kargs.pop('desc')
            self.msg = f'{name} was not provided. \n desc:{desc}'

        # Prints out requirements if not provided
        if len(kargs) > 0:
            self.msg += '\nMust follow the following requirements:'

            if 'dtype' in rqrmnts:
                dtype = rqrmnts.get('dtype')
                if isinstance(dtype, tuple):
                    self.msg += f'\n\t- Must be one of the following types:'
                    for dt in dtype:
                        self.msg += f'\n\t\t- {dt}'
                else:
                    self.msg += f'\n\t- Must be of type {dtype}'

            if 'min' in rqrmnts:
                minv = rqrmnts.get('min')
                self.msg += f'\n\t- Must be greater than {minv}'

            if 'mineq' in rqrmnts:
                minv = rqrmnts.get('mineq')
                self.msg += f'\n\t- Must be greater than or equal to {minv}'

            if 'max' in rqrmnts:
                maxv = rqrmnts.get('max')
                self.msg += f'\n\t- Must be less than {maxv}'

            if 'maxeq' in rqrmnts:
                maxv = rqrmnts.get('maxeq')
                self.msg += f'\n\t- Must be less than or equal to {maxv}'

            if 'callable' in rqrmnts:
                if rqrmnts.get('callable'):
                    self.msg += f'\n\t- Must be callable'
                else:
                    self.msg += f'\n\t- Must be not callable'

            if 'hashable' in rqrmnts:
                if rqrmnts.get('hashable'):
                    self.msg += f'\n\t- Must be hashable'
                else:
                    self.msg += f'\n\t- Must be not hashable'

            if 'iterable' in rqrmnts:
                if rqrmnts.get('iterable'):
                    self.msg += f'\n\t- Must be iterable'
                else:
                    self.msg += f'\n\t- Must be not iterable'

            if 'options' in rqrmnts:
                options = rqrmnts.get('options')
                if not isinstance(options, tuple):
                    raise CfgPyUseError(\
                            f'Expected tuple for options not {type(options)}')

                self.msg += f'\n\t- Must be one of the following options:'
                for opt in options:
                    self.msg += f'\n\t\t- {opt} ({type(opt)})'

            if 'divisible_by' in rqrmnts:
                div_by = rqrmnts.get('divisible_by')
                self.msg += f'\n\t- Must be divisible by {div_by}'

        super().__init__(self.msg)
