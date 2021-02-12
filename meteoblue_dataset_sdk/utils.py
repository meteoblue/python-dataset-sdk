import asyncio
import threading


def run_async(func, *args, **kwargs):
    """
    In case a jupyter notebook is running which uses a eventloop, which would raise
    "asyncio.run() cannot be called from a running event loop"
    move the asyncio execution to another thread.
    See https://stackoverflow.com/q/55409641
    """
    try:
        loop = asyncio.get_running_loop()
    except RuntimeError:
        loop = None
    if loop and loop.is_running() and is_jupyter_notebook():
        thread = RunThread(func, args, kwargs)
        thread.start()
        thread.join()
        if thread.exception:
            raise thread.exception
        return thread.result
    else:
        return asyncio.run(func(*args, **kwargs))


class RunThread(threading.Thread):
    def __init__(self, func, args, kwargs):
        self.func = func
        self.args = args
        self.kwargs = kwargs
        self.result = None
        self.exception = None
        super().__init__()

    def run(self):
        try:
            self.result = asyncio.run(self.func(*self.args, **self.kwargs))
        except Exception as e:
            self.exception = e


def is_jupyter_notebook():
    """
    Return true if running in a python notebook
    See https://stackoverflow.com/a/39662359
    """
    try:
        shell = get_ipython().__class__.__name__
        if shell == "ZMQInteractiveShell":
            return True  # Jupyter notebook or qtconsole
        elif shell == "TerminalInteractiveShell":
            return False  # Terminal running IPython
        else:
            return False  # Other type (?)
    except NameError:
        return False  # Probably standard Python interpreter
