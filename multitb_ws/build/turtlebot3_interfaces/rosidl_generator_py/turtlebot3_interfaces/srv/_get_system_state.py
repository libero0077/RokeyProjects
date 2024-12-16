# generated from rosidl_generator_py/resource/_idl.py.em
# with input from turtlebot3_interfaces:srv/GetSystemState.idl
# generated code does not contain a copyright notice


# Import statements for member types

import rosidl_parser.definition  # noqa: E402, I100


class Metaclass_GetSystemState_Request(type):
    """Metaclass of message 'GetSystemState_Request'."""

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
            module = import_type_support('turtlebot3_interfaces')
        except ImportError:
            import logging
            import traceback
            logger = logging.getLogger(
                'turtlebot3_interfaces.srv.GetSystemState_Request')
            logger.debug(
                'Failed to import needed modules for type support:\n' +
                traceback.format_exc())
        else:
            cls._CREATE_ROS_MESSAGE = module.create_ros_message_msg__srv__get_system_state__request
            cls._CONVERT_FROM_PY = module.convert_from_py_msg__srv__get_system_state__request
            cls._CONVERT_TO_PY = module.convert_to_py_msg__srv__get_system_state__request
            cls._TYPE_SUPPORT = module.type_support_msg__srv__get_system_state__request
            cls._DESTROY_ROS_MESSAGE = module.destroy_ros_message_msg__srv__get_system_state__request

    @classmethod
    def __prepare__(cls, name, bases, **kwargs):
        # list constant names here so that they appear in the help text of
        # the message class under "Data and other attributes defined here:"
        # as well as populate each message instance
        return {
        }


class GetSystemState_Request(metaclass=Metaclass_GetSystemState_Request):
    """Message class 'GetSystemState_Request'."""

    __slots__ = [
    ]

    _fields_and_field_types = {
    }

    SLOT_TYPES = (
    )

    def __init__(self, **kwargs):
        assert all('_' + key in self.__slots__ for key in kwargs.keys()), \
            'Invalid arguments passed to constructor: %s' % \
            ', '.join(sorted(k for k in kwargs.keys() if '_' + k not in self.__slots__))

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
        return True

    @classmethod
    def get_fields_and_field_types(cls):
        from copy import copy
        return copy(cls._fields_and_field_types)


# Import statements for member types

import builtins  # noqa: E402, I100

# already imported above
# import rosidl_parser.definition


class Metaclass_GetSystemState_Response(type):
    """Metaclass of message 'GetSystemState_Response'."""

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
            module = import_type_support('turtlebot3_interfaces')
        except ImportError:
            import logging
            import traceback
            logger = logging.getLogger(
                'turtlebot3_interfaces.srv.GetSystemState_Response')
            logger.debug(
                'Failed to import needed modules for type support:\n' +
                traceback.format_exc())
        else:
            cls._CREATE_ROS_MESSAGE = module.create_ros_message_msg__srv__get_system_state__response
            cls._CONVERT_FROM_PY = module.convert_from_py_msg__srv__get_system_state__response
            cls._CONVERT_TO_PY = module.convert_to_py_msg__srv__get_system_state__response
            cls._TYPE_SUPPORT = module.type_support_msg__srv__get_system_state__response
            cls._DESTROY_ROS_MESSAGE = module.destroy_ros_message_msg__srv__get_system_state__response

    @classmethod
    def __prepare__(cls, name, bases, **kwargs):
        # list constant names here so that they appear in the help text of
        # the message class under "Data and other attributes defined here:"
        # as well as populate each message instance
        return {
        }


class GetSystemState_Response(metaclass=Metaclass_GetSystemState_Response):
    """Message class 'GetSystemState_Response'."""

    __slots__ = [
        '_robot_status_json',
        '_slot_status_json',
    ]

    _fields_and_field_types = {
        'robot_status_json': 'string',
        'slot_status_json': 'string',
    }

    SLOT_TYPES = (
        rosidl_parser.definition.UnboundedString(),  # noqa: E501
        rosidl_parser.definition.UnboundedString(),  # noqa: E501
    )

    def __init__(self, **kwargs):
        assert all('_' + key in self.__slots__ for key in kwargs.keys()), \
            'Invalid arguments passed to constructor: %s' % \
            ', '.join(sorted(k for k in kwargs.keys() if '_' + k not in self.__slots__))
        self.robot_status_json = kwargs.get('robot_status_json', str())
        self.slot_status_json = kwargs.get('slot_status_json', str())

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
        if self.robot_status_json != other.robot_status_json:
            return False
        if self.slot_status_json != other.slot_status_json:
            return False
        return True

    @classmethod
    def get_fields_and_field_types(cls):
        from copy import copy
        return copy(cls._fields_and_field_types)

    @builtins.property
    def robot_status_json(self):
        """Message field 'robot_status_json'."""
        return self._robot_status_json

    @robot_status_json.setter
    def robot_status_json(self, value):
        if __debug__:
            assert \
                isinstance(value, str), \
                "The 'robot_status_json' field must be of type 'str'"
        self._robot_status_json = value

    @builtins.property
    def slot_status_json(self):
        """Message field 'slot_status_json'."""
        return self._slot_status_json

    @slot_status_json.setter
    def slot_status_json(self, value):
        if __debug__:
            assert \
                isinstance(value, str), \
                "The 'slot_status_json' field must be of type 'str'"
        self._slot_status_json = value


class Metaclass_GetSystemState(type):
    """Metaclass of service 'GetSystemState'."""

    _TYPE_SUPPORT = None

    @classmethod
    def __import_type_support__(cls):
        try:
            from rosidl_generator_py import import_type_support
            module = import_type_support('turtlebot3_interfaces')
        except ImportError:
            import logging
            import traceback
            logger = logging.getLogger(
                'turtlebot3_interfaces.srv.GetSystemState')
            logger.debug(
                'Failed to import needed modules for type support:\n' +
                traceback.format_exc())
        else:
            cls._TYPE_SUPPORT = module.type_support_srv__srv__get_system_state

            from turtlebot3_interfaces.srv import _get_system_state
            if _get_system_state.Metaclass_GetSystemState_Request._TYPE_SUPPORT is None:
                _get_system_state.Metaclass_GetSystemState_Request.__import_type_support__()
            if _get_system_state.Metaclass_GetSystemState_Response._TYPE_SUPPORT is None:
                _get_system_state.Metaclass_GetSystemState_Response.__import_type_support__()


class GetSystemState(metaclass=Metaclass_GetSystemState):
    from turtlebot3_interfaces.srv._get_system_state import GetSystemState_Request as Request
    from turtlebot3_interfaces.srv._get_system_state import GetSystemState_Response as Response

    def __init__(self):
        raise NotImplementedError('Service classes can not be instantiated')
