# generated from rosidl_generator_py/resource/_idl.py.em
# with input from menu_order_interfaces:srv/MenuTable.idl
# generated code does not contain a copyright notice


# Import statements for member types

import builtins  # noqa: E402, I100

import rosidl_parser.definition  # noqa: E402, I100


class Metaclass_MenuTable_Request(type):
    """Metaclass of message 'MenuTable_Request'."""

    _CREATE_ROS_MESSAGE = None
    _CONVERT_FROM_PY = None
    _CONVERT_TO_PY = None
    _DESTROY_ROS_MESSAGE = None
    _TYPE_SUPPORT = None

    __constants = {
    }

    @classmethod
    def __import_type_support__(cls):
        try:
            from rosidl_generator_py import import_type_support
            module = import_type_support('menu_order_interfaces')
        except ImportError:
            import logging
            import traceback
            logger = logging.getLogger(
                'menu_order_interfaces.srv.MenuTable_Request')
            logger.debug(
                'Failed to import needed modules for type support:\n' +
                traceback.format_exc())
        else:
            cls._CREATE_ROS_MESSAGE = module.create_ros_message_msg__srv__menu_table__request
            cls._CONVERT_FROM_PY = module.convert_from_py_msg__srv__menu_table__request
            cls._CONVERT_TO_PY = module.convert_to_py_msg__srv__menu_table__request
            cls._TYPE_SUPPORT = module.type_support_msg__srv__menu_table__request
            cls._DESTROY_ROS_MESSAGE = module.destroy_ros_message_msg__srv__menu_table__request

    @classmethod
    def __prepare__(cls, name, bases, **kwargs):
        # list constant names here so that they appear in the help text of
        # the message class under "Data and other attributes defined here:"
        # as well as populate each message instance
        return {
        }


class MenuTable_Request(metaclass=Metaclass_MenuTable_Request):
    """Message class 'MenuTable_Request'."""

    __slots__ = [
        '_request_type',
    ]

    _fields_and_field_types = {
        'request_type': 'string',
    }

    SLOT_TYPES = (
        rosidl_parser.definition.UnboundedString(),  # noqa: E501
    )

    def __init__(self, **kwargs):
        assert all('_' + key in self.__slots__ for key in kwargs.keys()), \
            'Invalid arguments passed to constructor: %s' % \
            ', '.join(sorted(k for k in kwargs.keys() if '_' + k not in self.__slots__))
        self.request_type = kwargs.get('request_type', str())

    def __repr__(self):
        typename = self.__class__.__module__.split('.')
        typename.pop()
        typename.append(self.__class__.__name__)
        args = []
        for s, t in zip(self.__slots__, self.SLOT_TYPES):
            field = getattr(self, s)
            fieldstr = repr(field)
            # We use Python array type for fields that can be directly stored
            # in them, and "normal" sequences for everything else.  If it is
            # a type that we store in an array, strip off the 'array' portion.
            if (
                isinstance(t, rosidl_parser.definition.AbstractSequence) and
                isinstance(t.value_type, rosidl_parser.definition.BasicType) and
                t.value_type.typename in ['float', 'double', 'int8', 'uint8', 'int16', 'uint16', 'int32', 'uint32', 'int64', 'uint64']
            ):
                if len(field) == 0:
                    fieldstr = '[]'
                else:
                    assert fieldstr.startswith('array(')
                    prefix = "array('X', "
                    suffix = ')'
                    fieldstr = fieldstr[len(prefix):-len(suffix)]
            args.append(s[1:] + '=' + fieldstr)
        return '%s(%s)' % ('.'.join(typename), ', '.join(args))

    def __eq__(self, other):
        if not isinstance(other, self.__class__):
            return False
        if self.request_type != other.request_type:
            return False
        return True

    @classmethod
    def get_fields_and_field_types(cls):
        from copy import copy
        return copy(cls._fields_and_field_types)

    @builtins.property
    def request_type(self):
        """Message field 'request_type'."""
        return self._request_type

    @request_type.setter
    def request_type(self, value):
        if __debug__:
            assert \
                isinstance(value, str), \
                "The 'request_type' field must be of type 'str'"
        self._request_type = value


# Import statements for member types

# already imported above
# import builtins

# already imported above
# import rosidl_parser.definition


class Metaclass_MenuTable_Response(type):
    """Metaclass of message 'MenuTable_Response'."""

    _CREATE_ROS_MESSAGE = None
    _CONVERT_FROM_PY = None
    _CONVERT_TO_PY = None
    _DESTROY_ROS_MESSAGE = None
    _TYPE_SUPPORT = None

    __constants = {
    }

    @classmethod
    def __import_type_support__(cls):
        try:
            from rosidl_generator_py import import_type_support
            module = import_type_support('menu_order_interfaces')
        except ImportError:
            import logging
            import traceback
            logger = logging.getLogger(
                'menu_order_interfaces.srv.MenuTable_Response')
            logger.debug(
                'Failed to import needed modules for type support:\n' +
                traceback.format_exc())
        else:
            cls._CREATE_ROS_MESSAGE = module.create_ros_message_msg__srv__menu_table__response
            cls._CONVERT_FROM_PY = module.convert_from_py_msg__srv__menu_table__response
            cls._CONVERT_TO_PY = module.convert_to_py_msg__srv__menu_table__response
            cls._TYPE_SUPPORT = module.type_support_msg__srv__menu_table__response
            cls._DESTROY_ROS_MESSAGE = module.destroy_ros_message_msg__srv__menu_table__response

    @classmethod
    def __prepare__(cls, name, bases, **kwargs):
        # list constant names here so that they appear in the help text of
        # the message class under "Data and other attributes defined here:"
        # as well as populate each message instance
        return {
        }


class MenuTable_Response(metaclass=Metaclass_MenuTable_Response):
    """Message class 'MenuTable_Response'."""

    __slots__ = [
        '_table_data',
    ]

    _fields_and_field_types = {
        'table_data': 'sequence<string>',
    }

    SLOT_TYPES = (
        rosidl_parser.definition.UnboundedSequence(rosidl_parser.definition.UnboundedString()),  # noqa: E501
    )

    def __init__(self, **kwargs):
        assert all('_' + key in self.__slots__ for key in kwargs.keys()), \
            'Invalid arguments passed to constructor: %s' % \
            ', '.join(sorted(k for k in kwargs.keys() if '_' + k not in self.__slots__))
        self.table_data = kwargs.get('table_data', [])

    def __repr__(self):
        typename = self.__class__.__module__.split('.')
        typename.pop()
        typename.append(self.__class__.__name__)
        args = []
        for s, t in zip(self.__slots__, self.SLOT_TYPES):
            field = getattr(self, s)
            fieldstr = repr(field)
            # We use Python array type for fields that can be directly stored
            # in them, and "normal" sequences for everything else.  If it is
            # a type that we store in an array, strip off the 'array' portion.
            if (
                isinstance(t, rosidl_parser.definition.AbstractSequence) and
                isinstance(t.value_type, rosidl_parser.definition.BasicType) and
                t.value_type.typename in ['float', 'double', 'int8', 'uint8', 'int16', 'uint16', 'int32', 'uint32', 'int64', 'uint64']
            ):
                if len(field) == 0:
                    fieldstr = '[]'
                else:
                    assert fieldstr.startswith('array(')
                    prefix = "array('X', "
                    suffix = ')'
                    fieldstr = fieldstr[len(prefix):-len(suffix)]
            args.append(s[1:] + '=' + fieldstr)
        return '%s(%s)' % ('.'.join(typename), ', '.join(args))

    def __eq__(self, other):
        if not isinstance(other, self.__class__):
            return False
        if self.table_data != other.table_data:
            return False
        return True

    @classmethod
    def get_fields_and_field_types(cls):
        from copy import copy
        return copy(cls._fields_and_field_types)

    @builtins.property
    def table_data(self):
        """Message field 'table_data'."""
        return self._table_data

    @table_data.setter
    def table_data(self, value):
        if __debug__:
            from collections.abc import Sequence
            from collections.abc import Set
            from collections import UserList
            from collections import UserString
            assert \
                ((isinstance(value, Sequence) or
                  isinstance(value, Set) or
                  isinstance(value, UserList)) and
                 not isinstance(value, str) and
                 not isinstance(value, UserString) and
                 all(isinstance(v, str) for v in value) and
                 True), \
                "The 'table_data' field must be a set or sequence and each value of type 'str'"
        self._table_data = value


class Metaclass_MenuTable(type):
    """Metaclass of service 'MenuTable'."""

    _TYPE_SUPPORT = None

    @classmethod
    def __import_type_support__(cls):
        try:
            from rosidl_generator_py import import_type_support
            module = import_type_support('menu_order_interfaces')
        except ImportError:
            import logging
            import traceback
            logger = logging.getLogger(
                'menu_order_interfaces.srv.MenuTable')
            logger.debug(
                'Failed to import needed modules for type support:\n' +
                traceback.format_exc())
        else:
            cls._TYPE_SUPPORT = module.type_support_srv__srv__menu_table

            from menu_order_interfaces.srv import _menu_table
            if _menu_table.Metaclass_MenuTable_Request._TYPE_SUPPORT is None:
                _menu_table.Metaclass_MenuTable_Request.__import_type_support__()
            if _menu_table.Metaclass_MenuTable_Response._TYPE_SUPPORT is None:
                _menu_table.Metaclass_MenuTable_Response.__import_type_support__()


class MenuTable(metaclass=Metaclass_MenuTable):
    from menu_order_interfaces.srv._menu_table import MenuTable_Request as Request
    from menu_order_interfaces.srv._menu_table import MenuTable_Response as Response

    def __init__(self):
        raise NotImplementedError('Service classes can not be instantiated')
