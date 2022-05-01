import unittest
from vericfg import *

'''
cfg = config(a=5)
print(cfg.get('a', dtype=(float, str)))
'''


class testVeriCfg(unittest.TestCase):

    def test_init_empty(self):
        cfg = config()

    def test_init_dct(self):
        cfg = config({'a':5})

    def test_init_multdct(self):
        cfg = config({'a':5}, {'b':4})

    def test_init_kargs(self):
        cfg = config(a=5, b=4)

    def test_get(self):
        cfg = config(a=5, b=4)
        self.assertEqual(cfg.get('a'),5)

    def test_getdflt(self):
        cfg = config(a=5, b=4)
        self.assertEqual(cfg.get('c',10),10)

    def test_getmin(self):
        cfg = config(a=10)
        # MIN
        with self.assertRaises(ValueOutOfRangeError):
            cfg.get('a', min=10)
        with self.assertRaises(ValueOutOfRangeError):
            cfg.get('a', mineq=11)
        cfg.get('a', min=9)
        cfg.get('a', mineq=9)
        cfg.get('a', mineq=10)

    def test_getmax(self):
        cfg = config(a=10)
        # MAX
        with self.assertRaises(ValueOutOfRangeError):
            cfg.get('a', max=10)
        with self.assertRaises(ValueOutOfRangeError):
            cfg.get('a', maxeq=9)
        cfg.get('a', max=11)
        cfg.get('a', maxeq=11)
        cfg.get('a', maxeq=10)

    def test_getdtype(self):
        cfg = config(a=10)
        with self.assertRaises(IncorrectTypeError):
            cfg.get('a', dtype=float)
        with self.assertRaises(IncorrectTypeError):
            cfg.get('a', dtype=(list,str))
        cfg.get('a', dtype=int)

    def test_callable(self):
        cfg = config(a=10, b=min)
        with self.assertRaises(NonCallableError):
            cfg.get('a', callable=True)
        with self.assertRaises(CallableError):
            cfg.get('b', callable=False)
        cfg.get('a', callable=False)
        cfg.get('b', callable=True)

    def test_hashable(self):
        cfg = config(a=5, b=set((1,2,3)))
        with self.assertRaises(NonHashableError):
            cfg.get('b', hashable=True)
        with self.assertRaises(HashableError):
            cfg.get('a', hashable=False)
        cfg.get('a', hashable=True)
        cfg.get('b', hashable=False)

    def test_iterable(self):
        cfg = config(a=5, b=set((1,2,3)))
        with self.assertRaises(NonIterableError):
            cfg.get('a', iterable=True)
        with self.assertRaises(IterableError):
            cfg.get('b', iterable=False)
        cfg.get('a', iterable=False)
        cfg.get('b', iterable=True)

    def test_options(self):
        cfg = config(a=5, b=set((1,2,3)))
        with self.assertRaises(InvalidOptionError):
            cfg.get('a', options=(1,2,3))
        cfg.get('a', options=(1,2,3,4,5))

    def test_divisible_by(self):
        cfg = config(a=5, b=set((1,2,3)))
        with self.assertRaises(NotDivisibleByError):
            cfg.get('a', divisible_by=4)
        cfg.get('a', divisible_by=5)


if __name__ == '__main__':
    unittest.main()
