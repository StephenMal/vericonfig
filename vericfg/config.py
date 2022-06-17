from .cstm_exceptions import *
from itertools import chain
import inspect, json

class config():

    def __init__(self, *args, **kargs):
        # Parameters used
        self.params = {}
        # Values that were set by default
        self.defaults = {}
        # Restrictions used (used to verify values allowed)
        self.restrictions = {}

        # If provided no arguments, be blank
        if len(args) == 0 and len(kargs) == 0:
            return
        elif len(args) != 0 and len(kargs) != 0:
            raise Exception('Must pass either a dictionary or list of kargs')
        elif len(args) >= 1:
            # If more than one dictionary provided, go through all of them
            #   and combine them
            if len(args) > 1:
                # If any non-dictionary, raise exception
                if any([not isinstance(arg, dict) for arg in args]):
                    raise \
                        TypeError('Expected dictionary(s) for pos args')
                # Combine them and set them in params
                for arg in args:
                    self.params.update({key:item for key, item in arg.items()})
                # \/ Raise error if not dictionary
            elif isinstance(args[0], dict):
                self.params.update(args[0])
            else:
                raise TypeError('Expected dictionary(s) for pos args')
        elif len(kargs) > 0:
            self.params.update(kargs)
        else:
            raise Exception('Failed to initialize')

    def _get(self, *args, **kargs):
        if len(args) == 0:
            raise CfgPyUseError('Did not provide a key')
        elif len(args) == 1:
            if args[0] not in self.params and args[0] not in self.defaults:
                raise ParameterNotProvidedError(args[0], **kargs)
            return self.params.get(args[0], self.defaults.setdefault(args[0]))
        elif len(args) == 2:
            return self.params.get(args[0], \
                                self.defaults.setdefault(args[0], args[1]))
        else:
            raise CfgPyUseError('Expected 1-2 positional arguments')

    def get(self, *args, **kargs):
        if len(args) == 0:
            raise CfgPyUseError('Did not provide a key')
        elif len(args) == 1 or len(args) == 2:
            return self.validate(args[0], self._get(*args,**kargs), **kargs)
        else:
            raise CfgPyUseError('Expected 1-2 positional arguments')
        raise CfgPyUseError()

    def set(self, key, item):
        if not isinstance(key, str):
            raise CfgPyKeyError('Key should be a string')
        try:
            self.defaults.pop(key)
        except:
            pass
        self.params.__setitem__(key, item)

    def __setitem__(self, key, item):
        self.set(key, item)

    def __getitem__(self, key):
        return self._get(key)

    def update(self, dct):
        if not isinstance(dct, dict):
            raise CfgPyUseError('Expected dictionary')
        self.params.update(dct)

    def to_dict(self):
        dct = {}
        dct.update(self.params)
        dct.update(self.defaults)
        return dct

    def json_dump(self, F):
        dct = self.to_dict()
        new_dct = {}
        for key, item in dct.items():
            if isinstance(item, (int, float, str, bool)):
                new_dct[key] = item
            elif inspect.isclass(item):
                try:
                    new_dct[key] = str(item.__name__)
                except:
                    pass
                new_dct[key] = item
            elif item == int:
                new_dct[key] = 'int'
            elif item == float:
                new_dct[key] = 'float'
            else:
                try:
                    new_dct[key] = json.dumps(item)
                except:
                    pass
        json.dump(new_dct, F)

    def __str__(self):
        return {'user_params':self.params,\
                'default_params':self.defaults}.__str__()

    def __repr__(self):
        return self.__str__()

    def __copy__(self):
        new_cfg = config()
        new_cfg.params = self.params.copy()
        new_cfg.defaults = self.defaults.copy()
        new_cfg.requiremnts = self.requirements.copy()
        return new_cfg

    def items(self):
        return self.to_dict().items()

    def keys(self):
        return self.to_dict().keys()

    def values(self):
        return self.to_dict().values()

    def pop(self, *args, **kargs):
        raise NotImplementedError('pop is not implemented for config dict')

    def popitem(self, *args, **kargs):
        raise NotImplementedError('popitem is not implemented for config dict')

    def fromkeys(self, *args, **kargs):
        raise NotImplementedError('fromkeys is not implemented for config dict')

    def setdefault(self, key, dflt, **kargs):
        if len(kargs) == 0:
            return self.params.setdefault(key, dflt)
        else:
            return self.validate(self.params.setdefault(key, dflt), **kargs)

    def update_default(self, dct, **kargs):
        if not isinstance(dct, dict):
            raise TypeError('Should provide a dictionary')

        if kargs.get('overwrite', False):
            self.defaults.update(dct)
        elif kargs.get('ignore_duplicates', True):
            dflt = self.defaults
            for key, item in dct.items():
                dflt.setdefault(key, item)
        else:
            dflt = self.defaults
            for key, item in dct.items():
                if key in self.defaults:
                    raise \
                        CfgPyKeyError('Trying to overwrite pre-existing default')
                dflt[key] = item

    def clear(self):
        del self.params, self.defaults, self.restrictions
        self.params, self.defaults, self.restrictions = {}, {}, {}

    def validate(self, key, item, **kargs):
        # Returns if no requiremnts
        if len(kargs) == 0:
            return item
        # Get the requirements
        reqs = self.restrictions.setdefault(key, dict())

        if 'mineq' in kargs or 'min' in kargs:
            if 'mineq' in kargs and 'min' in kargs:
                raise CfgPyUseError('Cannot have both mineq and min')
            # Get value
            minv = kargs.get('mineq', kargs.get('min'))
            mineq = 'mineq' in kargs
            # Try to compare
            try:
                if mineq:
                    bad = item < minv
                else:
                    bad = item <= minv
            except:
                raise TypeError(f'{key}({item}) of type {type(item)} is not'+\
                            f' comparable to min({minv}) of type {type(item)}')
            # If bad raise an error
            if bad:
                raise ValueOutOfRangeError(name=key, value=item, mineq=minv)
            elif mineq and 'maxeq' in reqs and reqs.get('maxeq') < minv:
                raise PreviousRestrictionConflict(f'{key} | maxeq < mineq')
            elif mineq and 'max' in reqs and reqs.get('max') <= minv:
                raise PreviousRestrictionConflict(f'{key} | max <= mineq')
            elif not mineq and 'max' in reqs and reqs.get('max') <= minv:
                raise PreviousRestrictionConflict(f'{key} | max <= min')
            elif not mineq and 'maxeq' in reqs and reqs.get('maxeq') <= minv:
                raise PreviousRestrictionConflict(f'{key} | maxeq <= min')

        if 'maxeq' in kargs or 'max' in kargs:
            if 'maxeq' in kargs and 'max' in kargs:
                raise CfgPyUseError('Cannot have both maxeq and max')
            # Get value
            maxv = kargs.get('maxeq', kargs.get('max'))
            maxeq = 'maxeq' in kargs
            # Try to compare
            try:
                if maxeq:
                    bad = item >     maxv
                else:
                    bad = item >= maxv
            except:
                raise TypeError(f'{key}({item}) of type {type(item)} is not'+\
                            f' comparable to max({minv}) of type {type(item)}')
            # If bad raise an error
            if bad:
                raise ValueOutOfRangeError(name=key, value=item, mineq=maxv)
            elif maxeq and 'mineq' in reqs and reqs.get('mineq') > maxv:
                raise PreviousRestrictionConflict(f'{key} | maxeq < mineq')
            elif maxeq and 'min' in reqs and reqs.get('min') >= maxv:
                raise PreviousRestrictionConflict(f'{key} | maxeq <= min')
            elif not maxeq and 'min' in reqs and reqs.get('min') >= maxv:
                raise PreviousRestrictionConflict(f'{key} | max <= min')
            elif not maxeq and 'mineq' in reqs and reqs.get('mineq') >= maxv:
                raise PreviousRestrictionConflict(f'{key} | max <= mineq')


        if 'iterable' in kargs:
            isiter = kargs.get('iterable')
            if not isinstance(isiter, bool):
                raise CfgPyUseError('isiter should be a boolean')

            if isiter != self.is_iter(item):
                if isiter:
                    raise NonIterableError(name=key, value=object)
                else:
                    raise IterableError(name=key, value=object)

            if 'iterable' in reqs and reqs.get('iterable') != isiter:
                raise PreviousRestrictionConflict('iterable conflict')
            else:
                reqs['iterable'] = isiter

        if 'hashable' in kargs:
            ishash = kargs.get('hashable')
            if not isinstance(ishash, bool):
                raise CfgPyUseError('ishash should be a boolean')

            if ishash != self.is_hash(item):
                if ishash:
                    raise NonHashableError(name=key, value=object)
                else:
                    raise HashableError(name=key, value=object)

            if 'hashable' in reqs and reqs.get('hashable') != ishash:
                raise PreviousRestrictionConflict('hashable conflict')
            else:
                reqs['hashable'] = ishash

        if 'callable' in kargs:
            iscallable = kargs.get('callable')
            if not isinstance(iscallable, bool):
                raise CfgPyUseError('callable should be a boolean')

            if iscallable != callable(item):
                if iscallable:
                    raise NonCallableError(name=key, value=object)
                else:
                    raise CallableError(name=key, value=object)

            if 'callable' in reqs and reqs.get('callable') != iscallable:
                raise PreviousRestrictionConflict('callable conflict')
            else:
                reqs['callable'] = callable

        if 'options' in kargs:
            options = kargs.get('options')
            if not isinstance(options, tuple):
                raise CfgPyUseError('Options should be a tuple')

            if not item in options:
                raise InvalidOptionError(name=key, value=object, \
                                                            options=options)

        if 'dtype' in kargs:
            dtype = kargs.get('dtype')
            if isinstance(dtype, tuple):
                if any((not (isinstance(dt, type) or inspect.isclass(dt)) \
                                                            for dt in dtype)):
                    bad_dt_vals = []
                    for dt in dtype:
                        if not (isinstance(dt, type) or inspect.isclass(dt)):
                            bad_dt_vals.append(\
                                f' --- {dt} ({type(dt)})')
                    raise CfgPyUseError('\nIncluded nonclass / type in dtype:\n'\
                                        +'\n'.join(bad_dt_vals))

            elif not (isinstance(dtype, type) or inspect.isclass(X)):
                raise CfgPyUseError('\nIncluded nonclass / type in dtype: '+\
                                        f'\n --- {dtype}({type(dtype)})')
            if not isinstance(item, dtype):
                raise IncorrectTypeError(name=key, value=item, dtype=dtype)

            if not isinstance(dtype, tuple):
                dtype = (dtype,)
            if 'dtype' in reqs:
                inter = set(dtype).intersection(set(reqs.get('dtype')))
                if len(inter) == 0:
                    raise PreviousRestrictionConflict('dtype conflict')
                reqs['dtype'] = tuple(inter)
            else:
                reqs['dtype'] = dtype

        if 'divisible_by' in kargs:
            div_by = kargs.get('divisible_by')
            if not (item % div_by == 0):
                raise NotDivisibleByError(name=key, value=item, div_by=div_by)

            reqs.setdefault('divisible_by', set()).add(div_by)

        return item

    def is_iter(self, item):
        try:
            iter(item)
            return True
        except:
            return False

    def is_hash(self, item):
        try:
            hash(item)
            return True
        except:
            return False

    def __del__(self):
        del self.params
        del self.defaults
        del self.restrictions

    def __contains__(self, item):
        return (item in self.params or item in self.defaults)

    def sumstr(self):
        prm, dflt = self.params, self.defaults
        s = 'Parameter Name                | Value\n'
        keys = set(prm.keys())
        keys.update(dflt.keys())
        for key in sorted(keys):
            if key in prm:
                s += key.ljust(30,' ')+'| '+str(prm.get(key)).ljust(48)+'\n'
            elif key in dflt:
                s += ('*'+key).ljust(30,' ')+'| '+str(dflt.get(key)).ljust(48)+'\n'
            else:
                raise Exception()
        if len(dflt) > 0:
            s += '* = default value used'
        return s

    def summary(self):
        print(self.sumstr())
