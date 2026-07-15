import inspect
import timeit
import statistics

def iterate_params_rec(params, i, arr):
    for j in range(len(params[i])):
        #print(params[i][j])
        if j == 0:
            arr.append(params[i][j])
        else:
            arr[i] = params[i][j]
        if i < len(params) - 1:
            yield from iterate_params_rec(params, i+1, arr.copy())
        else: 
            #print(arr)
            yield arr

def iterate_params(params):
    if type(params[0]) is list:
        yield from  iterate_params_rec(params, 0, [])
    else:
        for i in params:
            yield [i]


def run(module, reps):
    modulename = module.__name__
    results = dict()
    paramnames = dict()
    classes = inspect.getmembers(module, predicate=inspect.isclass)
    for cl in classes:
        obj = cl[1]()
        params = obj.params
        methods = inspect.getmembers(obj, predicate=inspect.ismethod)
        for par in iterate_params(params):
            # SETUP find #
            setup = None
            for meth in methods:
                if meth[0] == 'setup':
                    setup = meth[1]
                    break
            assert setup is not None
            # SETUP find #
            for meth in methods:
                if meth[0] == 'setup':
                    continue
                # RUN #
                t = timeit.Timer(lambda: meth[1](*par), setup=lambda: setup(*par))
                # RUN #
                exectime = statistics.mean(t.repeat(repeat=reps, number=1))
                name = "{}.{}.{}".format(modulename, cl[0], meth[0])
                if not name in paramnames:
                    paramnames[name] = obj.param_names
                if not name in results:
                    results[name] = []
                results[name].append([par, exectime])
    for mod, res in results.items():
        # get lengths for formatting
        lengths = [0] * (len(res[0][0]) + 1)
        for r in res:
            for i in range(len(r[0])):
                l = len(str(r[0][i]))
                if l > lengths[i]:
                    lengths[i] = l
            lex = len(str(r[1]))
            if lex > lengths[-1]:
                lengths[-1] = lex
        for i in range(len(paramnames[mod])):
            if len(paramnames[mod][i]) > lengths[i]:
                lengths[i] = len(paramnames[mod][i])
        # start print
        tablelen = sum(lengths) + (len(lengths)-1)*3
        tablelen = max(tablelen, len(mod))
        print("="*tablelen)
        print(mod)
        print("="*tablelen)
        for i in range(len(paramnames[mod])):
            print(f'{paramnames[mod][i]:{lengths[i]}}', end=' | ')
        print("-")
        print("-"*tablelen)
        for r in res:
            for i in range(len(r[0])):
                print(f'{str(r[0][i]):{lengths[i]}}', end=' | ')
            print(f'{r[1]:{lengths[-1]}}')

