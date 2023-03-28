#-----------------------------------------------------------------------------
# Copyright (c) 2012 - 2023, Anaconda, Inc., and Bokeh Contributors.
# All rights reserved.
#
# The full license is in the file LICENSE.txt, distributed with this software.
#-----------------------------------------------------------------------------
''' Client-side interactivity.

'''

#-----------------------------------------------------------------------------
# Boilerplate
#-----------------------------------------------------------------------------
from __future__ import annotations

import logging # isort:skip
log = logging.getLogger(__name__)

#-----------------------------------------------------------------------------
# Imports
#-----------------------------------------------------------------------------

# Standard library imports
from typing import Any as any

# Bokeh imports
from ..core.has_props import HasProps, abstract
from ..core.properties import (
    Any,
    AnyRef,
    Auto,
    Bool,
    Dict,
    Either,
    Instance,
    Required,
    String,
)
from ..core.property.bases import Init
from ..core.property.singletons import Intrinsic
from ..core.validation import error
from ..core.validation.errors import INVALID_PROPERTY_VALUE, NOT_A_PROPERTY_OF
from ..model import Model

#-----------------------------------------------------------------------------
# Globals and constants
#-----------------------------------------------------------------------------

__all__ = (
    'Callback',
    'OpenURL',
    'CustomJS',
    'SetValue',
)

#-----------------------------------------------------------------------------
# General API
#-----------------------------------------------------------------------------

@abstract
class Callback(Model):
    ''' Base class for interactive callback.

    '''

    # explicit __init__ to support Init signatures
    def __init__(self, *args, **kwargs) -> None:
        super().__init__(*args, **kwargs)

class OpenURL(Callback):
    ''' Open a URL in a new or current tab or window.

    '''

    # explicit __init__ to support Init signatures
    def __init__(self, *args, **kwargs) -> None:
        super().__init__(*args, **kwargs)

    url = String("http://", help="""
    The URL to direct the web browser to. This can be a template string,
    which will be formatted with data from the data source.
    """)

    same_tab = Bool(False, help="""
    Open URL in a new (`False`, default) or current (`True`) tab or window.
    For `same_tab=False`, whether tab or window will be opened is browser
    dependent.
    """)

class CustomCode(Callback):
    """ """

    # explicit __init__ to support Init signatures
    def __init__(self, *args, **kwargs) -> None:
        super().__init__(*args, **kwargs)

class CustomJS(CustomCode):
    ''' Execute a JavaScript function.

    .. warning::
        The explicit purpose of this Bokeh Model is to embed *raw JavaScript
        code* for a browser to execute. If any part of the code is derived
        from untrusted user inputs, then you must take appropriate care to
        sanitize the user input prior to passing to Bokeh.

    '''

    # explicit __init__ to support Init signatures
    def __init__(self, *args, **kwargs) -> None:
        super().__init__(*args, **kwargs)

    args = Dict(String, AnyRef)(default={}, help="""
    A mapping of names to Python objects. In particular those can be bokeh's models.
    These objects are made available to the callback's code snippet as the values of
    named parameters to the callback.
    """)

    code = Required(String)(help="""
    A snippet of JavaScript code to execute in the browser.

    This can be interpreted either as a JavaScript function or a module, depending
    on the ``module`` property:

    1. A JS function.

    The code is made into the body of a function, and all of of the named objects in
    ``args`` are available as parameters that the code can use. Additionally,
    a ``cb_obj`` parameter contains the object that triggered the callback
    and an optional ``cb_data`` parameter that contains any tool-specific data
    (i.e. mouse coordinates and hovered glyph indices for the ``HoverTool``).

    2. An ES module.

    A JavaScript module (ESM) exporting a default function with the following
    signature:

    .. code-block: javascript

        export default function(args, obj, data) {
            // program logic
        }

    where ``args`` is a key-value mapping of user-provided parameters, ``obj``
    refers to the object that triggered the callback, and ``data`` is a key-value
    mapping of optional parameters provided by the caller.

    This function can be an asynchronous function (``async function``).
    """)

    module = Either(Auto, Bool)(default="auto", help="""
    Whether to interpret the code as a JS function or ES module. If set to
    ``"auto"``, the this will be inferred from the code.
    """)

class SetValue(Callback):
    """ Allows to update a property of an object. """

    # explicit __init__ to support Init signatures
    def __init__(self, obj: Init[HasProps] = Intrinsic, attr: Init[str] = Intrinsic, value: Init[any] = Intrinsic, **kwargs) -> None:
        super().__init__(obj=obj, attr=attr, value=value, **kwargs)

    obj: HasProps = Required(Instance(HasProps), help="""
    Object to set the value on.
    """)

    attr: str = Required(String, help="""
    The property to modify.
    """)

    value = Required(Any, help="""
    The value to set.
    """)

    @error(NOT_A_PROPERTY_OF)
    def _check_if_an_attribute_is_a_property_of_a_model(self):
        if self.obj.lookup(self.attr, raises=False):
            return None
        else:
            return f"{self.attr} is not a property of {self.obj}"

    @error(INVALID_PROPERTY_VALUE)
    def _check_if_provided_a_valid_value(self):
        descriptor = self.obj.lookup(self.attr)

        if descriptor.property.is_valid(self.value):
            return None
        else:
            return f"{self.value!r} is not a valid value for {self.obj}.{self.attr}"

# TODO: class Show(Callback): target = Required(Either(Instance(DOMNode), Instance(UIElement)))
# TODO: class Hide(Callback): ...

#-----------------------------------------------------------------------------
# Dev API
#-----------------------------------------------------------------------------

#-----------------------------------------------------------------------------
# Private API
#-----------------------------------------------------------------------------

#-----------------------------------------------------------------------------
# Code
#-----------------------------------------------------------------------------
