import os

from betamax import Betamax
import pytest

import xbox
from xbox.tests import TestBase


class TestAuth(TestBase):
    def test_incorrect_password_raises_exception(self):
        with Betamax(xbox.client.session) as vcr:
            match_on = ['uri', 'method', 'headers', 'body']
            vcr.use_cassette(
                'incorrect_password',
                match_on=match_on,
                record_mode='never',
            )

            with pytest.raises(xbox.exceptions.AuthenticationException):
                xbox.client.authenticate('pyxb-testing@outlook.com', 'password')

    def test_correct_email_and_password(self):
        with Betamax(xbox.client.session) as vcr:
            match_on = ['uri', 'method', 'headers', 'body']
            vcr.use_cassette(
                'correct_password',
                match_on=match_on,
                record_mode='never',
            )

            # the response was recorded with the correct credentials and edited
            assert not xbox.client.authenticated
            xbox.client.authenticate('pyxb-testing@outlook.com', 'password')
            assert xbox.client.authenticated
            assert xbox.client.AUTHORIZATION_HEADER == 'XBL3.0 x=1674471606081042789;eyJlbmMiOiJBMTI4Q0JDK0hTMjU2IiwiYWxnIjoiUlNBLU9BRVAiLCJjdHkiOiJKV1QiLCJ6aXAiOiJERUYiLCJ4NXQiOiIxZlVBejExYmtpWklFaE5KSVZnSDFTdTVzX2cifQ.W-xZJv-Cm0JrzJ2hHwPBnaFbusjcs2W16qb9aIZJmSqgU7NAElZ_WNQxMOgqn81OpyU41Bj9_DQUqT-QLDoluYT4xQvw44TX0-NGh3-gfy9RmZbf1mh_h3gv8oQRbPk5hxuwU9MmA2CrkLt0-yHoosgWOQtUbs9J0LvRoUtIigY.luE3Rdn7hxl1c1wLryVUDQ.OtZOM2ADr7FfjdM21C5-D_Bb45gPjoHP44J3OdpwvAG101QndHxhGIQSJ_akDHh6DNowf0Gn1xN_K6688aKA0n50uwxYq2S1um-gLRH_EgwY8yHwFQHhN0ZTb571TaLyIOj5riK9o-mHYxf8al3ZGkORzptoP7Y1WCifmTggOR8qvrCUeBawHCvCIem8rz72aTU4TMVHYXuKlek1ANiv816XCtCrNwnyil9DJzGZcjhChojgV6qpSkVknyAy_O996CmMa3P4S2cSSzN59LWgDNqSx0J9YlagVTB2croqbmyqtsffj5Gt81CY1kbOynzuM6mcCUuTFCMn6HgkdImQQbolJnxteN7tJQBkKx0PX8OYnK09p0GpFWn6UtO-a5BRkKRuBO5lQnAtOdHL4pYM9cPAxLz1rzjT13Fm9tFpxZpwAPQAPk9runNPKYns1loip2IU41yQ_-BRbByhZ0VVnvu8aV3vHJJdt7R8ePEpRnt5IL2UQNedfYQrI-L3WzMPoMkEcuunUrhie9RNRlXEaBL-TxmMcIJ7qIeteUT0EHYGlWm9lmAjJ9FBSgUOW87MPslpgAM-Th4-6_iMREmG2TsG2v2mT6EYRZQsbsT3rZXijwmV2Ts_UIBlB2GmaIua0uXivesG0xad5HWQAtTzvhxjFnkaVXlcaNXFnYOmJz00ktUUdmExL_s0qvhVhYNN77jhc7S4TYDoU-FxZZDeT23B9j8o758Giv5pTcKuz9aFK5iRXQMPnfHY4miJWq2MMWf1zpfh4vandrRTn3HxBV-q1MGrX2dAjGcIpCZ5hOfaT75tZEl_xJe-boV0bqwI2t-4cYw1AgLIYDR0b4YIrZUjUnEzH_6gZU0IaoFvw8-dm2F3x2crC7iK_EWPNdpyr-tDYxLXOZWz0MA4tlixrGZuywYGR09C-tHSIWanztI0O5536S7wDLFeCQUgBp4yUmsgfeP9sP6obUIS-a1E8e0glUzJAD4b08aypbrOgrCW08GLJjrgG1H2GYNxVGanHJiHRPnUQ3fIFsT2aBza1RMQQwUilZKxg_R3AhJdoBL_H20hAaJ2BiSPl_2QBfYUgqw-iDP-k5iKCakc6LXvexF2ZnPOdBVyG_Rg8Aj0cwus8Nur2LOxUxbArRe8TuAqPYh9hpEbuSvqsMImYqL9uLMtR4LiC9nc8ihG0uzepml0ozeiGCdFw9sLxIm-cokdTYxgC5uO-bOYhzjqu5TGiw.ommE112Hsa9zaNkQIz4sztyVUSqRl-3zh8NO-e5Mwa8'

    def test_authentication_from_env_vars(self):
        with Betamax(xbox.client.session) as vcr:
            match_on = ['uri', 'method', 'headers', 'body']
            os.environ['MS_LOGIN'] = 'pyxb-testing@outlook.com'
            os.environ['MS_PASSWD'] = 'password'
            vcr.use_cassette(
                'correct_password_env_vars',
                match_on=match_on,
                record_mode='never',
            )

            assert not xbox.client.authenticated
            xbox.client.authenticate()
            assert xbox.client.authenticated
            assert xbox.client.login == 'pyxb-testing@outlook.com'
            assert hasattr(xbox.client, 'AUTHORIZATION_HEADER')

            del os.environ['MS_LOGIN']
            del os.environ['MS_PASSWD']

    def test_authentication_from_unset_env_vars(self):
        assert 'MS_LOGIN' not in os.environ

        with pytest.raises(xbox.exceptions.AuthenticationException):
            xbox.client.authenticate()
        assert not xbox.client.authenticated
