from datetime import datetime
import json
import os
import types

from betamax import Betamax
import pytest

import xbox
from xbox.tests import TestBase
from xbox.tests.conftest import here


class TestClips(TestBase):

    def test_clip_init(self, gamerprofile):
        file = open(here('files/clip.json'))
        clip_data = json.loads(file.read())
        file.close()

        clip = xbox.Clip(gamerprofile, clip_data)

        assert clip.raw_json == clip_data
        assert clip.user == gamerprofile
        assert clip.clip_id == clip_data['gameClipId']
        assert clip.scid == clip_data['scid']
        assert clip.duration == clip_data['durationInSeconds']
        assert clip.name == clip_data['clipName']
        assert clip.saved == clip_data['savedByUser']
        assert clip.state == clip_data['state']
        assert clip.views == clip_data['views']
        assert clip.rating == clip_data['rating']
        assert clip.ratings == clip_data['ratingCount']
        assert clip.caption == clip_data['userCaption']
        assert clip.recorded == datetime(2014, 9, 9, 18, 30, 59)
        assert clip.thumbnails.small == 'http://gameclipscontent-t3001.xboxlive.com/00090000014d6bae-21c9449a-615f-4ac5-b095-09af0230e90d/Thumbnail_Small.PNG'
        assert clip.thumbnails.large == 'http://gameclipscontent-t3001.xboxlive.com/00090000014d6bae-21c9449a-615f-4ac5-b095-09af0230e90d/Thumbnail_Large.PNG'
        assert clip.media_url == 'http://gameclipscontent-d3001.xboxlive.com/asset-4b26b569-66f8-49cb-ba6c-6eefbdd57a1f/GameClip-Original.MP4?sv=2012-02-12&st=2014-09-11T23%3A45%3A58Z&se=2014-09-12T00%3A50%3A58Z&sr=c&sp=r&sig=uv7FBN5t88ABBHvBMR7qjliDyrZXM3TaqcuvHUacbIs%3D&__gda__=1410483058_34d847a7c55b76a2c873191b4b8a0d03'

    def test_get_clip_directly(self):
        with Betamax(xbox.client.session) as vcr:
            match_on = ['uri', 'method', 'headers', 'body']
            vcr.use_cassette(
                'get_clip_directly_success',
                match_on=match_on,
                record_mode='always',
            )

            os.environ['MS_LOGIN'] = 'pyxb-testing@outlook.com'
            os.environ['MS_PASSWD'] = 'password'

            xuid = '2533274812246958'
            scid = 'c4060100-4951-4a51-a630-dce26c15b8c5'
            clip_id = '237fc073-7b48-4555-a40f-adc1616d7b61'
            clip = xbox.Clip.get(xuid, scid, clip_id)

            assert clip.scid == scid
            assert clip.clip_id == clip_id

            assert isinstance(clip.user, xbox.proxies.UserProxy)
            assert clip.user.xuid == xuid
            assert clip.user.gamertag == 'JoeAlcorn'

    def test_get_clip_directly_missing(self):
        with Betamax(xbox.client.session) as vcr:
            match_on = ['uri', 'method', 'headers', 'body']
            vcr.use_cassette(
                'get_clip_directly_fail',
                match_on=match_on,
                record_mode='always',
            )

            os.environ['MS_LOGIN'] = 'pyxb-testing@outlook.com'
            os.environ['MS_PASSWD'] = 'password'

            xuid = '2533274812246958'
            scid = 'c4060100-4951-4a51-a630-dce26c15b8c5'
            clip_id = '237fc073-7b48-4555-a40f-adc1616d7b61'

            # first have incorrect xuid
            with pytest.raises(xbox.exceptions.ClipNotFound):
                xbox.Clip.get('2533274812246957', scid, clip_id)

            # scid doesn't actually have to be a match, as long
            # as it looks like a uuid it's fine. we may raise an
            # exception in the future
            clip = xbox.Clip.get(xuid, 'c4060100-5555-5555-5555-dce26c15b8c5', clip_id)
            assert clip.scid == 'c4060100-4951-4a51-a630-dce26c15b8c5'
            # with pytest.raises(xbox.exceptions.ClipNotFound):

            # incorrect clip_id
            with pytest.raises(xbox.exceptions.ClipNotFound):
                xbox.Clip.get(xuid, scid, '237fc073-7b48-4555-a40f-adc1616d7b62')

    def test_get_latest_from_user(self):
        with Betamax(xbox.client.session) as vcr:
            match_on = ['uri', 'method', 'headers', 'body']
            vcr.use_cassette(
                'get_latest_clips_from_user',
                match_on=match_on,
                record_mode='always',
            )

            os.environ['MS_LOGIN'] = 'pyxb-testing@outlook.com'
            os.environ['MS_PASSWD'] = 'password'

            gt = xbox.GamerProfile.from_gamertag('JoeAlcorn')
            clips = xbox.Clip.latest_from_user(gt)
            assert isinstance(clips, types.GeneratorType)

            clips = list(clips)
            assert all([isinstance(c, xbox.Clip) for c in clips])

    def test_get_saved_from_user(self):
        with Betamax(xbox.client.session) as vcr:
            match_on = ['uri', 'method', 'headers', 'body']
            vcr.use_cassette(
                'get_saved_clips_from_user',
                match_on=match_on,
                record_mode='always',
            )

            os.environ['MS_LOGIN'] = 'pyxb-testing@outlook.com'
            os.environ['MS_PASSWD'] = 'password'

            gt = xbox.GamerProfile.from_gamertag('JoeAlcorn')
            # ensure there are actually some saved clips
            latest = xbox.Clip.latest_from_user(gt)
            assert not all([c.saved for c in latest])

            saved = xbox.Clip.saved_from_user(gt)
            assert all([c.saved for c in saved])
