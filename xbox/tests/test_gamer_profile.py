import os

from betamax import Betamax
import pytest

import xbox
from xbox.tests import TestBase


class TestgamerProfile(TestBase):
    def test_gamer_profile_init(self):
        settings = [{
            "id": "AppDisplayName",
            "value": "FakeProfile"
        }, {
            "id": "DisplayPic",
            "value": "http://compass.xbox.com/assets/70/52/7052948b-c50d-4850-baff-abbcad07b631.jpg?n=004.jpg"
        }, {
            "id": "Gamerscore",
            "value": "22786"
        }, {
            "id": "Gamertag",
            "value": "FakeProfile"
        }, {
            "id": "PublicGamerpic",
            "value": "http://images-eds.xboxlive.com/image?url=z951ykn43p4FqWbbFvR2Ec.8vbDhj8G2Xe7JngaTToBrrCmIEEXHC9UNrdJ6P7KIFXxmxGDtE9Vkd62rOpb7JcGvME9LzjeruYo3cC50qVYelz5LjucMJtB5xOqvr7WR"
        }, {
            "id": "XboxOneRep",
            "value": "GoodPlayer"
        }]

        gt = xbox.GamerProfile('fake-xuid', settings, {})
        assert gt.gamertag == 'FakeProfile'
        assert gt.gamerscore == '22786'
        assert gt.gamerpic == 'http://images-eds.xboxlive.com/image?url=z951ykn43p4FqWbbFvR2Ec.8vbDhj8G2Xe7JngaTToBrrCmIEEXHC9UNrdJ6P7KIFXxmxGDtE9Vkd62rOpb7JcGvME9LzjeruYo3cC50qVYelz5LjucMJtB5xOqvr7WR'
        assert len(gt.raw_json) == 0

    def test_get_by_gamertag(self):
        with Betamax(xbox.client.session) as vcr:
            match_on = ['uri', 'method', 'headers', 'body']

            os.environ['MS_LOGIN'] = 'pyxb-testing@outlook.com'
            os.environ['MS_PASSWD'] = 'password'

            vcr.use_cassette(
                'get_profile_by_gamertag_success',
                match_on=match_on,
                record_mode='never',
            )

            gt = xbox.GamerProfile.from_gamertag('joealcorn')

            assert gt.gamertag == 'JoeAlcorn'
            assert gt.gamerpic == 'http://images-eds.xboxlive.com/image?url=z951ykn43p4FqWbbFvR2Ec.8vbDhj8G2Xe7JngaTToBrrCmIEEXHC9UNrdJ6P7KIFXxmxGDtE9Vkd62rOpb7JcGvME9LzjeruYo3cC50qVYelz5LjucMJtB5xOqvr7WR'
            assert gt.xuid == '2533274812246958'
            assert gt.gamerscore == '22791'
            assert gt.xuid in repr(gt)
            assert gt.gamertag in repr(gt)
            assert gt.raw_json

    def test_get_by_xuid(self):
        with Betamax(xbox.client.session) as vcr:
            match_on = ['uri', 'method', 'headers', 'body']

            os.environ['MS_LOGIN'] = 'pyxb-testing@outlook.com'
            os.environ['MS_PASSWD'] = 'password'

            vcr.use_cassette(
                'get_profile_by_xuid_success',
                match_on=match_on,
                record_mode='never',
            )

            gt = xbox.GamerProfile.from_xuid('2533274812246958')

            assert gt.gamertag == 'JoeAlcorn'
            assert gt.gamerpic == 'http://images-eds.xboxlive.com/image?url=z951ykn43p4FqWbbFvR2Ec.8vbDhj8G2Xe7JngaTToBrrCmIEEXHC9UNrdJ6P7KIFXxmxGDtE9Vkd62rOpb7JcGvME9LzjeruYo3cC50qVYelz5LjucMJtB5xOqvr7WR'
            assert gt.xuid == '2533274812246958'
            assert gt.gamerscore == '22791'
            assert gt.xuid in repr(gt)
            assert gt.gamertag in repr(gt)
            assert gt.raw_json

    def test_get_by_xuid_failure(self):
        with Betamax(xbox.client.session) as vcr:
            match_on = ['uri', 'method', 'headers', 'body']

            os.environ['MS_LOGIN'] = 'pyxb-testing@outlook.com'
            os.environ['MS_PASSWD'] = 'password'

            vcr.use_cassette(
                'get_profile_by_xuid_failure',
                match_on=match_on,
                record_mode='once',
            )

            with pytest.raises(xbox.exceptions.GamertagNotFound):
                xbox.GamerProfile.from_xuid('0000000000000000')

    def test_get_by_gamertag_failure(self):
        with Betamax(xbox.client.session) as vcr:
            match_on = ['uri', 'method', 'headers', 'body']

            os.environ['MS_LOGIN'] = 'pyxb-testing@outlook.com'
            os.environ['MS_PASSWD'] = 'password'

            vcr.use_cassette(
                'get_profile_by_gamertag_failure',
                match_on=match_on,
                record_mode='once',
            )

            with pytest.raises(xbox.exceptions.GamertagNotFound):
                xbox.GamerProfile.from_gamertag('2533274812246958')
