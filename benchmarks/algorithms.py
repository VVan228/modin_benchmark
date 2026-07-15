from importlib import import_module

import numpy as np

import pandas as pd

def _make_factorize_data(dtype, N):
    if dtype in ("int64", "Int64", "object"):
        data = pd.Index(np.arange(N), dtype=dtype)
    elif dtype == "float64":
        data = pd.Index(np.random.randn(N), dtype=dtype)
    elif dtype == "datetime64[ns]":
        data = pd.date_range("2011-01-01", freq="h", periods=N)
    elif dtype == "datetime64[ns, tz]":
        data = pd.date_range("2011-01-01", freq="h", periods=N, tz="Asia/Tokyo")
    elif dtype == "object_str":
        data = pd.Index([f"i-{i}" for i in range(N)], dtype=object)
    elif dtype == "string[pyarrow]":
        data = pd.array(
            pd.Index([f"i-{i}" for i in range(N)], dtype=object),
            dtype="string[pyarrow]",
        )
    else:
        raise NotImplementedError
    return data


_FACTORIZE_DTYPES = [
    #"int64",
    "float64",
    #"object",
    #"object_str",
    #"datetime64[ns]",
    #"datetime64[ns, tz]",
    #"Int64",
    #"string[pyarrow]",
]


class Factorize:
    params = [
        [True, False],
        [True, False],
        _FACTORIZE_DTYPES,
    ]
    param_names = ["unique", "sort", "dtype"]

    def setup(self, unique, sort, dtype):
        N = 10**5
        data = _make_factorize_data(dtype, N)
        if not unique:
            data = data.repeat(5)
        self.data = data

    def time_factorize(self, unique, sort, dtype):
        pd.factorize(self.data, sort=sort)


class FactorizePeakmem:
    # peakmem is driven by allocation patterns that vary by dtype; unique/sort
    # are held fixed to keep this benchmark small.
    params = _FACTORIZE_DTYPES
    param_names = ["dtype"]

    def setup(self, dtype):
        N = 10**5
        self.data = _make_factorize_data(dtype, N).repeat(5)

    def peakmem_factorize(self, dtype):
        pd.factorize(self.data, sort=False)


#class Duplicated:
#    params = [
#        [True, False],
#        ["first", "last", False],
#        [
#            "int64",
#            "uint64",
#            "float64",
#            "string",
#            "datetime64[ns]",
#            "datetime64[ns, tz]",
#            "timestamp[ms][pyarrow]",
#            "duration[s][pyarrow]",
#        ],
#    ]
#    param_names = ["unique", "keep", "dtype"]
#
#    def setup(self, unique, keep, dtype):
#        N = 10**5
#        if dtype in ["int64", "uint64"]:
#            data = pd.Index(np.arange(N), dtype=dtype)
#        elif dtype == "float64":
#            data = pd.Index(np.random.randn(N), dtype="float64")
#        elif dtype == "string":
#            data = pd.Index([f"i-{i}" for i in range(N)], dtype=object)
#        elif dtype == "datetime64[ns]":
#            data = pd.date_range("2011-01-01", freq="h", periods=N)
#        elif dtype == "datetime64[ns, tz]":
#            data = pd.date_range("2011-01-01", freq="h", periods=N, tz="Asia/Tokyo")
#        elif dtype in ["timestamp[ms][pyarrow]", "duration[s][pyarrow]"]:
#            data = pd.Index(np.arange(N), dtype=dtype)
#        else:
#            raise NotImplementedError
#        if not unique:
#            data = data.repeat(5)
#        self.idx = data
#        # cache is_unique
#        self.idx.is_unique
#
#    def time_duplicated(self, unique, keep, dtype):
#        self.idx.duplicated(keep=keep)
#
#
#class DuplicatedMaskedArray:
#    params = [
#        [True, False],
#        ["first", "last", False],
#        ["Int64", "Float64"],
#    ]
#    param_names = ["unique", "keep", "dtype"]
#
#    def setup(self, unique, keep, dtype):
#        N = 10**5
#        data = pd.Series(np.arange(N), dtype=dtype)
#        data[list(range(1, N, 100))] = pd.NA
#        if not unique:
#            data = data.repeat(5)
#        self.ser = data
#        # cache is_unique
#        self.ser.is_unique
#
#    def time_duplicated(self, unique, keep, dtype):
#        self.ser.duplicated(keep=keep)
#
#
#class Quantile:
#    params = [
#        [0, 0.5, 1],
#        ["linear", "nearest", "lower", "higher", "midpoint"],
#        ["float64", "int64"],
#    ]
#    param_names = ["quantile", "interpolation", "dtype"]
#
#    def setup(self, quantile, interpolation, dtype):
#        N = 10**5
#        if dtype == "int64":
#            data = np.arange(N, dtype=dtype)
#        elif dtype == "float64":
#            data = np.random.randn(N)
#        else:
#            raise NotImplementedError
#        self.ser = pd.Series(data.repeat(5))
#
#    def time_quantile(self, quantile, interpolation, dtype):
#        self.ser.quantile(quantile, interpolation=interpolation)
#
#
#class SortIntegerArray:
#    params = [10**3, 10**5]
#
#    def setup(self, N):
#        data = np.arange(N, dtype=float).astype(object)
#        data[40] = pd.NA
#        self.array = pd.array(data, dtype="Int64")
#
#    def time_argsort(self, N):
#        self.array.argsort()


#from .pandas_vb_common import setup  # noqa: F401 isort:skip
