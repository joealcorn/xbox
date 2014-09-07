# Python Xbox API client

This is unreleased software. As such things are may be broken
and APIs are likely to change. Use at your own risk.

[![https://readthedocs.org/projects/xbox/badge/?version=latest](Documentation)](http://xbox.readthedocs.org/en/latest/)

### About

This project is a wrapper around Microsoft's set of private APIs
in use by the Xbox One and related apps.

### Goals

The main goals of this project are to achieve a decent, usable API,
everything else is secondary.

### Usage

```python
>>> from xbox import Client

>>> xbox = Client.authenticate()

>>> # get a gamer
>>> gt = xbox.gamertag('JoeAlcorn')
>>> gt.gamerscore
22056
>>> gt.display_name
'JoeAlcorn'

>>> # get recorded clips
>>> clip = gt.clips()[0]
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
```


### Links

- [Documentation](http://xbox.readthedocs.org/en/latest/)
- [Roadmap](https://trello.com/b/onAwDz0V/python-xbox)
