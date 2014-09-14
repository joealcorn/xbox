Resources
============

Objects that represent an API resource are locked away
in here. Things such as gamer profile, games and clips.


.. autoclass:: xbox.GamerProfile
    :members:


.. autoclass:: xbox.Clip

    .. py:classmethod:: get(xuid, scid, clip_id)

        Retrieves a specific game clips

        :param xuid: xuid of an xbox live user
        :param scid: scid of a clip
        :param clip_id: id of a clip

        :returns: :class:`~xbox.Clip` instance


    .. py:classmethod:: saved_from_user(user[, include_pending=False])

        Retrieves all 'saved' clips for a specific
        user, returning an iterator.

        :param user: :class:`~xbox.GamerProfile` instance
        :param bool include_pending: whether to ignore clips that are not
            yet uploaded. These clips will have thumbnails and media_url
            set to ``None``

        :returns: Iterator of :class:`~xbox.Clip` instances


    .. py:classmethod:: latest_from_user(user[, include_pending=False])

        Retrieves a user's gameclips, excluding any that are
        pending upload.

        :param user: :class:`~xbox.GamerProfile` instance
        :param bool include_pending: whether to ignore clips that are not
            yet uploaded. These clips will have thumbnails and media_url
            set to ``None``

        :returns: Iterator of :class:`~xbox.Clip` instances

