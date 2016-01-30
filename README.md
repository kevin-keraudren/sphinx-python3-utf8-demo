About Python 3, utf8, `sphinx`, `pygments`, `re` and `regex`
============================================================

Python 3 supports utf8 in identifiers and filenames, hence module names as well.
This is pretty cool: you can code in your mothertongue, which is great for kids, personal projects, people whose English does not go beyond the built-in Python functions, linguistic projects...

https://docs.python.org/3/howto/unicode.html#python-s-unicode-support

 * The syntax highlighting project `pygments` has a [Python 3 lexer](https://bitbucket.org/birkenfeld/pygments-main/src/b483ad23e36e79d51700f995b622a066371de814/pygments/lexers/python.py?at=default&fileviewer=file-view-default#python.py-200) that supports utf8 but `sphinx` does not use it in the viewcode extension.

 * `regex` is a regular expression module that better handles utf8 than the built-in `re` module, but `sphinx` does not use it.

```
In [1]: import re

In [2]: re.match('\w+', 'தமிழ்')
Out[2]: <_sre.SRE_Match object; span=(0, 2), match='தம'>

In [3]: import regex as re

In [4]: re.match('\w+', 'தமிழ்')
Out[4]: <regex.Match object; span=(0, 5), match='தமிழ்'>
```

What is happening here is well explained in this [StackOverflow thread](http://stackoverflow.com/questions/5441183/regular-expression-and-unicode-utf-8-in-python) and has to do with combined characters: மி = ம + ி and ம் = ம + ஂ.
See this [link](http://www.utf8-chartable.de/unicode-utf8-table.pl?start=2944&number=128&utf8=0x) for more utf8 details.

 * `sphinx` ships an old version of `tokenize.py` which was written for Python 2, while Python 3 comes with a built-in version.
 
This dummy project is here to illustrate those two bugs in `sphinx` and suggest simple fixes.


Settings
--------

    conda create --name py35 python=3 numpy sphinx

In py34 sphinx did not use `pygments` although it was installed.

    source activate py35
	git clone https://github.com/kevin-keraudren/sphinx-python3-utf8-demo.git
	cd sphinx-python3-utf8-demo/doc
	make html

Usage of the dummy module
-------------------------

```
In [1]: from some_module_with_utf8_code import தமிழ்

In [2]: தமிழ்.வணக்கம்()
Out[2]: 'hello'
```

```
In [1]: from some_module_with_utf8_code import some_maths

In [2]: some_maths.gaussian(0.5, μ=0, σ=1)
Out[2]: 0.35206532676429952
```

Bug 1: sphinx is not using Python3Lexer from pygments
-----------------------------------------------------

```
highlighting module code... [100%] some_module_with_utf8_code.some_maths
Exception occurred:
  File "~/anaconda/envs/py35/lib/python3.5/site-packages/pygments/filters/__init__.py", line 196, in filter
    raise self.exception(value)
pygments.filters.ErrorToken: μ
The full traceback has been saved in /var/folders/_k/1xh1df6s3s3b9sd8__vl5wq80000gn/T/sphinx-err-ap7h6hgl.log, if you want to report the issue to the developers.
Please also report this if it was a user error, so that a better error message can be provided next time.
A bug report can be filed in the tracker at <https://github.com/sphinx-doc/sphinx/issues>. Thanks!
make: *** [html] Error 1
```

Line 142 of https://github.com/sphinx-doc/sphinx/blob/master/sphinx/ext/viewcode.py#L142 :

    highlighted = highlighter.highlight_block(code, 'python', linenos=False)

It is hardcoded 'python', so we could hardcode 'python3' or for a more subtle fix which does not break the Python 2.* compatibility:

    import sys
	PY3 = sys.version_info[0] == 3
	highlighted = highlighter.highlight_block(code, 'python'+('3' if PY3 else ''), linenos=False)


For a quick and dirty fix:

    mate ~/anaconda/envs/py35/lib/python3.5/site-packages/Sphinx-1.3.5-py3.5.egg/sphinx/ext/viewcode.py


Bug 2: sphinx uses `re` instead of `regex`
------------------------------------------

```
reading sources... [100%] தமிழ்
/Work/github/sphinx-python3-utf8-demo/doc/தமிழ்.rst:7: WARNING: invalid signature for automodule ('some_module_with_utf8_code.தமிழ்')
~/Work/github/sphinx-python3-utf8-demo/doc/தமிழ்.rst:7: WARNING: don't know which module to import for autodocumenting 'some_module_with_utf8_code.தமிழ்' (try placing a "module" or "currentmodule" directive in the document, or giving an explicit module name)
```

Proposed fix:

    pip install regex
    cd ~/anaconda/envs/py35/lib/python3.5/site-packages/Sphinx-1.3.5-py3.5.egg/sphinx/
    perl -pi -e 's/^import re$/import regex as re/g'  `find . -name '*.py'`


Bug3: `sphinx` should use the built-in Python 3 version of `tokenize.py` instead of relying on a Python 2 version which does not accept utf8 function names
-----------------------------------------------------------------------------------------------------------------------------------------------------------

https://github.com/sphinx-doc/sphinx/blob/master/sphinx/pycode/pgen2/tokenize.py

which is imported line 22 of
https://github.com/sphinx-doc/sphinx/blob/master/sphinx/pycode/__init__.py#L22

A quick fix is to copy the built-in Python 3 tokenize module:

    cp ~/anaconda/envs/py35/lib/python3.5/tokenize.py ~/anaconda/envs/py35/lib/python3.5/site-packages/Sphinx-1.3.5-py3.5.egg/sphinx/pycode/pgen2/

And patch it so that it uses `regex` instead of `re`:

    mate ~/anaconda/envs/py35/lib/python3.5/tokenize.py

    import regex as re

And now the function

    some_module_with_utf8_code.தமிழ்.வணக்கம்()

is finally linked to its source.


Notes
-----

As we previously saw:

```
In [1]: text = "தமிழ்"

In [2]: len(text)
Out[2]: 5
```

As a result, this is not a valid rst title:

```
தமிழ்
===
```

It should be:

```
தமிழ்
=====
```

If there are not enough underlining characters, the title is not recognised and does not appear in `index.html`.

It says in the [sphinx doc](http://www.sphinx-doc.org/en/stable/rest.html#sections) that the underline should be "at least as long as the text".


It should be in fact as long as the text minus one character:
 
````
Tamil
====
```

is indeed similarly accepted.
 
But anyway, it is a characteristic of the `docutils` module and not `sphinx` itself. 
