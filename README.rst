Python Xbox API client
======================

|Documentation| |Build Status| |Coverage Status| |PyPI Version|

About
~~~~~

This project is a wrapper around Microsoft’s set of private APIs in use
by the Xbox One and related apps.

Goals
~~~~~

The main goals of this project are to achieve a decent, usable API,
everything else is secondary.

Installation
~~~~~~~~~~~~

Install using ``pip``

``$ pip install xbox``

Usage
~~~~~

.. code:: python

    >>> import xbox

    >>> xbox.client.authenticate(login='joe@example.org', password='hunter2')

    >>> # get a gamer
    >>> gt = xbox.GamerProfile.from_gamertag('JoeAlcorn')
    >>> gt.gamerscore
    22056
    >>> gt.gamerpic
    'http://images-eds.xboxlive.com/image?url=z951ykn43p4FqWbbFvR2Ec.8vbDhj8G2Xe7JngaTToBrrCmIEEXHC9UNrdJ6P7KIFXxmxGDtE9Vkd62rOpb7JcGvME9LzjeruYo3cC50qVYelz5LjucMJtB5xOqvr7WR'

    >>> # get iterator of recorded clips
    >>> clips = gt.clips()
    >>> # convert iterator to a list so we can index it
    >>> clips = list(clips)
    >>> clip = clips[0]
    >>> clip.media_url
    'http://gameclipscontent-d2005.xboxlive.com/asset-886c5b78-8876-4823-b31b-fbc77d8caa67/GameClip-Original.MP4?sv=2012-02-12&st=2014-09-03T22%3A40%3A58Z&se=2014-09-03T23%3A45%3A58Z&sr=c&sp=r&sig=Q5qvyDvFRM2Bn2tztJ%2F%2BEf9%2FQOpkTPuFniByvE%2Bc9cc%3D&__gda__=1409787958_f22b516f9d29da56911b7cac03f15d05'
    >>> clip.views
    4
    >>> clip.state
    'Published'
    >>> clip.duration
    54
    >>> clip.thumbnails.large
    'http://gameclipscontent-t2005.xboxlive.com/00090000014d6bae-7638b9fd-2a19-4ef1-b621-505a6ac93488/Thumbnail_Large.PNG'

Links
~~~~~

-  `Code`_
-  `Issues & Bugs`_
-  `Documentation`_
-  `PyPI`_
-  `Roadmap`_

.. _Code: https://github.com/buttscicles/xbox/
.. _Issues & Bugs: https://github.com/buttscicles/xbox/issues
.. _Documentation: http://xbox.readthedocs.org/en/latest/
.. _PyPI: https://pypi.python.org/pypi/xbox
.. _Roadmap: https://trello.com/b/onAwDz0V/python-xbox

.. |Documentation| image:: https://readthedocs.org/projects/xbox/badge/?version=latest
   :target: http://xbox.readthedocs.org/en/latest/
.. |Build Status| image:: https://img.shields.io/travis/buttscicles/xbox.svg
   :target: https://travis-ci.org/buttscicles/xbox
.. |Coverage Status| image:: https://img.shields.io/coveralls/buttscicles/xbox.svg
   :target: https://coveralls.io/r/buttscicles/xbox
.. |PyPI Version| image:: http://img.shields.io/pypi/v/xbox.svg
   :target: https://pypi.python.org/pypi/xbox
