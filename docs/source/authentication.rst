.. _authentication:

Authentication
==============

Authentication requires a valid login for an Xbox Live account.

You can either set the ``MS_LOGIN`` and ``MS_PASSWD`` environment
variables in which case authentication will happen automatically
when it's required. If you'd prefer not to do that, call the
:py:meth:`~xbox.Client.authenticate` method with your
credentials.

.. code-block:: python

   import xbox
   xbox.client.authenticate('joe@example.org', 'password')
