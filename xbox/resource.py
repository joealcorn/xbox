from .exceptions import GamertagNotFound


class GamerProfile(object):
    '''
    Represents an xbox live user.

    :ivar string xuid: xuid of user
    :ivar string gamertag: gamertag of user
    :ivar string gamerscore: gamerscore of user
    :ivar string gamerpic: url for gamerpic of user
    '''

    def __init__(self, client, xuid, settings, raw_json):
        self.client = client
        self.xuid = xuid
        self.raw_json = raw_json
        name_map = {
            'Gamertag': 'gamertag',
            'Gamerscore': 'gamerscore',
            'PublicGamerpic': 'gamerpic',
        }
        for setting in settings:
            if setting['id'] in name_map:
                setattr(self, name_map[setting['id']], setting['value'])

    @classmethod
    def from_xuid(cls, client, xuid):
        '''
        Instantiates an instance of ``GamerProfile`` from
        an xuid

        :param client: :class:`~xbox.Client` instance
        :param xuid: Xuid to look up

        :raises: :class:`~xbox.exceptions.GamertagNotFound`

        :returns: :class:`~xbox.resource.GamerProfile` instance
        '''

        url = 'https://profile.xboxlive.com/users/xuid(%s)/profile/settings' % xuid
        try:
            return cls._fetch(client, url)
        except GamertagNotFound:
            raise GamertagNotFound('No such user: %s' % xuid)

    @classmethod
    def from_gamertag(cls, client, gamertag):
        '''
        Instantiates an instance of ``GamerProfile`` from
        a gamertag

        :param client: :class:`~xbox.Client` instance
        :param gamertag: Gamertag to look up

        :raises: :class:`~xbox.exceptions.GamertagNotFound`

        :returns: :class:`~xbox.resource.GamerProfile` instance
        '''
        url = 'https://profile.xboxlive.com/users/gt(%s)/profile/settings' % gamertag
        try:
            return cls._fetch(client, url)
        except GamertagNotFound:
            raise GamertagNotFound('No such user: %s' % gamertag)

    @classmethod
    def _fetch(cls, client, base_url):
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

        resp = client._get(base_url + qs, headers=headers)
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
        return cls(client, user['id'], user['settings'], raw_json)

    def __repr__(self):
        return '<xbox.resource.GamerProfile: %s (%s)>' % (
            self.gamertag, self.xuid
        )
