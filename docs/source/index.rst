.. python-xbox documentation master file, created by
   sphinx-quickstart on Sun Sep  7 13:03:27 2014.
   You can adapt this file completely to your liking, but it should at least
   contain the root `toctree` directive.

Welcome to python-xbox's documentation!
=======================================

Contents:
    .. toctree::
       :maxdepth: 2

       authentication
       resource
       exceptions


Links:
    * `Code <https://github.com/buttscicles/xbox>`_
    * `Issues & Bugs <https://github.com/buttscicles/xbox/issues>`_
    * `Documentation <http://xbox.readthedocs.org/en/latest/>`_
    * `PyPI <https://pypi.python.org/pypi/python-xbox>`_
    * `Roadmap <https://trello.com/b/onAwDz0V/python-xbox>`_

Quickstart
==========

.. code-block:: python

    >>> import xbox

    >>> # authenticate
    >>> xbox.client.authenticate(email_address, password)

    >>> # get a user
    >>> gt = xbox.GamerProfile.from_gamertag('JoeAlcorn')
    >>> gt.gamerscore
    22056
    >>> gt.gamerpic
    'http://images-eds.xboxlive.com/image?url=z951ykn43p4FqWbbFvR2Ec.8vbDhj8G2Xe7JngaTToBrrCmIEEXHC9UNrdJ6P7KIFXxmxGDtE9Vkd62rOpb7JcGvME9LzjeruYo3cC50qVYelz5LjucMJtB5xOqvr7WR'



.. autoclass:: xbox.Client
    :members:

