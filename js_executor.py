
from typing import overload
from IPython.core.display import HTML
from IPython.core.display import Javascript
from pathlib import Path
from IPython.core.display import display
import math


class JsExecutor:
    """
    This class includes callable javascript scripts. The scripts are expected
    to be in the root of the configured root folder.

    To prevent reloading the scripts all over, this class contains only static methods.
    Initially `JsExecutor.configure()` must be called to index and load all scripts.

    """

    root = './javascript'
    scripts = {}

    @classmethod
    def configure(cls, root='./javascript'):
        js_path = Path(root)
        if not js_path.exists():
            raise Exception(
                f'Path to javascript directory does not exist: ', root)
        cls.root = root
        for script in js_path.glob('*.js'):
            with open(script, 'r') as reader:
                cls.scripts[script.stem] = reader.read()
                display(HTML(f'''
                <script>
                    {cls.scripts[script.stem]}
                </script>
                '''))
                # display(Javascript(cls.scripts[script.stem]))

    @classmethod
    def function_def(cls, script):
        fun_def = cls.scripts[script]
        if fun_def is None:
            raise Exception(f'No script "{script}" found')

        return fun_def

    @staticmethod
    def escape_arg(arg):
        if isinstance(arg, str):
            return f"'{arg}'"
        elif isinstance(arg, bool):
            return 'true' if arg else 'false'
        else:
            return f'{arg}'

    @classmethod
    def function_call(cls, script, *args):
        """
        Parameters
        ----------
        script : str
            the name of the javascript file to call. e.g. 'floodFillCode'
        args : str, number
            currently only strings and numbers are supported as parameters with which
            the javascript function is called

        Returns
        -------
        str
            the function definition including the function call of the script

        """
        if script not in cls.scripts:
            raise Exception(f'No script "{script}" found')

        escaped_args = map(JsExecutor.escape_arg, args)

        # {cls.function_def(script)}
        return f'''
            {script}({', '.join(escaped_args)});
        '''

    @classmethod
    def call(cls, script, *args):
        """
        Parameters
        ----------
        script : str
            the name of the javascript file to call. e.g. 'floodFillCode'
        args : str, number
            currently only strings and numbers are supported as parameters with which
            the javascript function is called

        Returns
        -------
        IPython.core.display.Javascript object
        """

        # print(f'{script}({", ".join(map(JsExecutor.escape_arg, args))})')
        return display(Javascript(cls.function_call(script, *args)))
