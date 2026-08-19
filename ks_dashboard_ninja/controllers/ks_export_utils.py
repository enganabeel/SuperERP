import functools
import json
import logging

import werkzeug.exceptions

from odoo.http import serialize_exception as _serialize_exception

_logger = logging.getLogger(__name__)


def serialize_exception(f):
    """Decorator catching exceptions raised by an http.Controller method and
    turning them into a JSON-RPC style 500 error response.

    Ported locally because this decorator was removed from Odoo core after
    16.0 (odoo.addons.web.controllers.main.serialize_exception no longer
    exists); only the differently-shaped odoo.http.serialize_exception
    (a plain exception -> dict helper, not a decorator) remains.
    """
    @functools.wraps(f)
    def wrap(*args, **kwargs):
        try:
            return f(*args, **kwargs)
        except Exception as e:
            _logger.exception("An exception occurred during an http request")
            error = {
                'code': 200,
                'message': "Odoo Server Error",
                'data': _serialize_exception(e),
            }
            return werkzeug.exceptions.InternalServerError(json.dumps(error))
    return wrap
