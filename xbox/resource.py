from datetime import datetime

import xbox
from .decorators import authenticates
from .exceptions import GamertagNotFound, ClipNotFound, InvalidRequest
from .proxies import UserProxy
from .utils import DotNotationDict


class GamerProfile(object):
    '''
    Represents an xbox live user.

    :var string xuid: xuid of user
    :var string gamertag: gamertag of user
    :var string gamerscore: gamerscore of user
    :var string gamerpic: url for gamerpic of user
    '''

    def __init__(self, xuid, settings, user_data):
        self.xuid = xuid
        self.raw_json = user_data
        name_map = {
            'Gamertag': 'gamertag',
            'Gamerscore': 'gamerscore',
            'PublicGamerpic': 'gamerpic',
        }
        for setting in settings:
            if setting['id'] in name_map:
                setattr(self, name_map[setting['id']], setting['value'])

    @classmethod
    def from_xuid(cls, xuid):
        '''
        Instantiates an instance of ``GamerProfile`` from
        an xuid

        :param xuid: Xuid to look up

        :raises: :class:`~xbox.exceptions.GamertagNotFound`

        :returns: :class:`~xbox.GamerProfile` instance
        '''

        url = 'https://profile.xboxlive.com/users/xuid(%s)/profile/settings' % xuid
        try:
            return cls._fetch(url)
        except (GamertagNotFound, InvalidRequest):
            # this endpoint seems to return 400 when the resource
            # does not exist
            raise GamertagNotFound('No such user: %s' % xuid)

    @classmethod
    def from_gamertag(cls, gamertag):
        '''
        Instantiates an instance of ``GamerProfile`` from
        a gamertag

        :param gamertag: Gamertag to look up

        :raises: :class:`~xbox.exceptions.GamertagNotFound`

        :returns: :class:`~xbox.GamerProfile` instance
        '''
        url = 'https://profile.xboxlive.com/users/gt(%s)/profile/settings' % gamertag
        try:
            return cls._fetch(url)
        except GamertagNotFound:
            raise GamertagNotFound('No such user: %s' % gamertag)

    @classmethod
    @authenticates
    def _fetch(cls, base_url):
        settings = [
            'AppDisplayName',
            'DisplayPic',
            'Gamerscore',
            'Gamertag',
            'PublicGamerpic',
            'XboxOneRep',
        ]

        qs = '?settings=%s' % ','.join(settings)
        headers = {'x-xbl-contract-version': 2}

        resp = xbox.client._get(base_url + qs, headers=headers)
        if resp.status_code == 404:
            raise GamertagNotFound('No such user')

        # example payload:
        # {
        #     "profileUsers": [{
        #         "id": "2533274812246958",
        #         "hostId": null,
        #         "settings": [{
        #             "id": "AppDisplayName",
        #             "value": "JoeAlcorn"
        #         }, {
        #             "id": "DisplayPic",
        #             "value": "http://compass.xbox.com/assets/70/52/7052948b-c50d-4850-baff-abbcad07b631.jpg?n=004.jpg"
        #         }, {
        #             "id": "Gamerscore",
        #             "value": "22786"
        #         }, {
        #             "id": "Gamertag",
        #             "value": "JoeAlcorn"
        #         }, {
        #             "id": "PublicGamerpic",
        #             "value": "http://images-eds.xboxlive.com/image?url=z951ykn43p4FqWbbFvR2Ec.8vbDhj8G2Xe7JngaTToBrrCmIEEXHC9UNrdJ6P7KIFXxmxGDtE9Vkd62rOpb7JcGvME9LzjeruYo3cC50qVYelz5LjucMJtB5xOqvr7WR"
        #         }, {
        #             "id": "XboxOneRep",
        #             "value": "GoodPlayer"
        #         }],
        #         "isSponsoredUser": false
        #     }]
        # }

        raw_json = resp.json()
        user = raw_json['profileUsers'][0]
        return cls(user['id'], user['settings'], raw_json)

    def clips(self):
        '''
        Gets the latest clips made by this user

        :returns: Iterator of :class:`~xbox.Clip` instances
        '''
        return Clip.latest_from_user(self)

    def __repr__(self):
        return '<xbox.resource.GamerProfile: %s (%s)>' % (
            self.gamertag, self.xuid
        )


class Clip(object):
    '''
    Represents a single game clip.

    :var user: User that made the clip
    :var string clip_id: Unique id of the clip
    :var string scid: Unique SCID of the clip
    :var string duration: Duration, in seconds, of the clip
    :var string name: Name of the clip. Can be ``''``
    :var bool saved: Whether the user has saved the clip.
        Clips that aren't saved eventually expire
    :var string state:
    :var string views: Number of views the clip has had
    :var string rating: Clip rating
    :var string ratings: Number of ratings the clip has received
    :var string caption: User-defined clip caption
    :var dict thumbnails: Thumbnail URLs for the clip
    :var datetime recorded: Date and time clip was made
    :var string media_url: Video clip URL

    '''

    def __init__(self, user, clip_data):
        self.raw_json = clip_data
        self.user = user
        self.clip_id = clip_data['gameClipId']
        self.scid = clip_data['scid']
        self.duration = clip_data['durationInSeconds']
        self.name = clip_data['clipName']
        self.saved = clip_data['savedByUser']
        self.state = clip_data['state']
        self.views = clip_data['views']
        self.rating = clip_data['rating']
        self.ratings = clip_data['ratingCount']
        self.caption = clip_data['userCaption']
        self.thumbnails = DotNotationDict()
        self.recorded = datetime.strptime(
            clip_data['dateRecorded'], '%Y-%m-%dT%H:%M:%SZ'
        )

        # thumbnails and media_url may not yet exist
        # if the state of the clip is PendingUpload
        self.thumbnails.small = None
        self.thumbnails.large = None
        for thumb in clip_data['thumbnails']:
            if thumb['thumbnailType'] == 'Small':
                self.thumbnails.small = thumb['uri']
            elif thumb['thumbnailType'] == 'Large':
                self.thumbnails.large = thumb['uri']

        self.media_url = None
        for uri in clip_data['gameClipUris']:
            if uri['uriType'] == 'Download':
                self.media_url = uri['uri']

    def __getstate__(self):
        return (self.raw_json, self.user)

    def __setstate__(self, data):
        clip_data = data[0]
        user = data[1]
        self.__init__(user, clip_data)

    @classmethod
    @authenticates
    def get(cls, xuid, scid, clip_id):
        '''
        Gets a specific game clip

        :param xuid: xuid of an xbox live user
        :param scid: scid of a clip
        :param clip_id: id of a clip
        '''
        url = (
            'https://gameclipsmetadata.xboxlive.com/users'
            '/xuid(%(xuid)s)/scids/%(scid)s/clips/%(clip_id)s' % {
                'xuid': xuid,
                'scid': scid,
                'clip_id': clip_id,
            }
        )
        resp = xbox.client._get(url)

        # scid does not seem to matter when fetching clips,
        # as long as it looks like a uuid it should be fine.
        # perhaps we'll raise an exception in future
        if resp.status_code == 404:
            msg = 'Could not find clip: xuid=%s, scid=%s, clip_id=%s' % (
                xuid, scid, clip_id,
            )
            raise ClipNotFound(msg)

        data = resp.json()

        # as we don't have the user object let's
        # create a lazily evaluated proxy object
        # that will fetch it only when required
        user = UserProxy(xuid)
        return cls(user, data['gameClip'])

    @classmethod
    @authenticates
    def saved_from_user(cls, user, include_pending=False):
        '''
        Gets all clips 'saved' by a user.

        :param user: :class:`~xbox.GamerProfile` instance
        :param bool include_pending: whether to ignore clips that are not
            yet uploaded. These clips will have thumbnails and media_url
            set to ``None``
        :returns: Iterator of :class:`~xbox.Clip` instances
        '''

        url = 'https://gameclipsmetadata.xboxlive.com/users/xuid(%s)/clips/saved'
        resp = xbox.client._get(url % user.xuid)
        data = resp.json()
        for clip in data['gameClips']:
            if clip['state'] != 'PendingUpload' or include_pending:
                yield cls(user, clip)

    @classmethod
    @authenticates
    def latest_from_user(cls, user, include_pending=False):
        '''
        Gets all clips, saved and unsaved

        :param user: :class:`~xbox.GamerProfile` instance
        :param bool include_pending: whether to ignore clips that are not
            yet uploaded. These clips will have thumbnails and media_url
            set to ``None``

        :returns: Iterator of :class:`~xbox.Clip` instances
        '''

        url = 'https://gameclipsmetadata.xboxlive.com/users/xuid(%s)/clips'
        resp = xbox.client._get(url % user.xuid)
        data = resp.json()
        for clip in data['gameClips']:
            if clip['state'] != 'PendingUpload' or include_pending:
                yield cls(user, clip)
