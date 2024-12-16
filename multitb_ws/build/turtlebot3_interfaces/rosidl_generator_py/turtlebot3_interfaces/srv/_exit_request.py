# generated from rosidl_generator_py/resource/_idl.py.em
# with input from turtlebot3_interfaces:srv/ExitRequest.idl
# generated code does not contain a copyright notice


# Import statements for member types

import builtins  # noqa: E402, I100

import rosidl_parser.definition  # noqa: E402, I100


class Metaclass_ExitRequest_Request(type):
    """Metaclass of message 'ExitRequest_Request'."""

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
                'turtlebot3_interfaces.srv.ExitRequest_Request')
            logger.debug(
                'Failed to import needed modules for type support:\n' +
                traceback.format_exc())
        else:
            cls._CREATE_ROS_MESSAGE = module.create_ros_message_msg__srv__exit_request__request
            cls._CONVERT_FROM_PY = module.convert_from_py_msg__srv__exit_request__request
            cls._CONVERT_TO_PY = module.convert_to_py_msg__srv__exit_request__request
            cls._TYPE_SUPPORT = module.type_support_msg__srv__exit_request__request
            cls._DESTROY_ROS_MESSAGE = module.destroy_ros_message_msg__srv__exit_request__request

    @classmethod
    def __prepare__(cls, name, bases, **kwargs):
        # list constant names here so that they appear in the help text of
        # the message class under "Data and other attributes defined here:"
        # as well as populate each message instance
        return {
        }


class ExitRequest_Request(metaclass=Metaclass_ExitRequest_Request):
    """Message class 'ExitRequest_Request'."""

    __slots__ = [
        '_car_number',
    ]

    _fields_and_field_types = {
        'car_number': 'string',
    }

    SLOT_TYPES = (
        rosidl_parser.definition.UnboundedString(),  # noqa: E501
    )

    def __init__(self, **kwargs):
        assert all('_' + key in self.__slots__ for key in kwargs.keys()), \
            'Invalid arguments passed to constructor: %s' % \
            ', '.join(sorted(k for k in kwargs.keys() if '_' + k not in self.__slots__))
        self.car_number = kwargs.get('car_number', str())

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
        if self.car_number != other.car_number:
            return False
        return True

    @classmethod
    def get_fields_and_field_types(cls):
        from copy import copy
        return copy(cls._fields_and_field_types)

    @builtins.property
    def car_number(self):
        """Message field 'car_number'."""
        return self._car_number

    @car_number.setter
    def car_number(self, value):
        if __debug__:
            assert \
                isinstance(value, str), \
                "The 'car_number' field must be of type 'str'"
        self._car_number = value


# Import statements for member types

# already imported above
# import builtins

# already imported above
# import rosidl_parser.definition


class Metaclass_ExitRequest_Response(type):
    """Metaclass of message 'ExitRequest_Response'."""

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
                'turtlebot3_interfaces.srv.ExitRequest_Response')
            logger.debug(
                'Failed to import needed modules for type support:\n' +
                traceback.format_exc())
        else:
            cls._CREATE_ROS_MESSAGE = module.create_ros_message_msg__srv__exit_request__response
            cls._CONVERT_FROM_PY = module.convert_from_py_msg__srv__exit_request__response
            cls._CONVERT_TO_PY = module.convert_to_py_msg__srv__exit_request__response
            cls._TYPE_SUPPORT = module.type_support_msg__srv__exit_request__response
            cls._DESTROY_ROS_MESSAGE = module.destroy_ros_message_msg__srv__exit_request__response

    @classmethod
    def __prepare__(cls, name, bases, **kwargs):
        # list constant names here so that they appear in the help text of
        # the message class under "Data and other attributes defined here:"
        # as well as populate each message instance
        return {
        }


class ExitRequest_Response(metaclass=Metaclass_ExitRequest_Response):
    """Message class 'ExitRequest_Response'."""

    __slots__ = [
        '_status',
        '_entry_time',
        '_fee',
        '_log',
    ]

    _fields_and_field_types = {
        'status': 'boolean',
        'entry_time': 'string',
        'fee': 'int32',
        'log': 'string',
    }

    SLOT_TYPES = (
        rosidl_parser.definition.BasicType('boolean'),  # noqa: E501
        rosidl_parser.definition.UnboundedString(),  # noqa: E501
        rosidl_parser.definition.BasicType('int32'),  # noqa: E501
        rosidl_parser.definition.UnboundedString(),  # noqa: E501
    )

    def __init__(self, **kwargs):
        assert all('_' + key in self.__slots__ for key in kwargs.keys()), \
            'Invalid arguments passed to constructor: %s' % \
            ', '.join(sorted(k for k in kwargs.keys() if '_' + k not in self.__slots__))
        self.status = kwargs.get('status', bool())
        self.entry_time = kwargs.get('entry_time', str())
        self.fee = kwargs.get('fee', int())
        self.log = kwargs.get('log', str())

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
        if self.status != other.status:
            return False
        if self.entry_time != other.entry_time:
            return False
        if self.fee != other.fee:
            return False
        if self.log != other.log:
            return False
        return True

    @classmethod
    def get_fields_and_field_types(cls):
        from copy import copy
        return copy(cls._fields_and_field_types)

    @builtins.property
    def status(self):
        """Message field 'status'."""
        return self._status

    @status.setter
    def status(self, value):
        if __debug__:
            assert \
                isinstance(value, bool), \
                "The 'status' field must be of type 'bool'"
        self._status = value

    @builtins.property
    def entry_time(self):
        """Message field 'entry_time'."""
        return self._entry_time

    @entry_time.setter
    def entry_time(self, value):
        if __debug__:
            assert \
                isinstance(value, str), \
                "The 'entry_time' field must be of type 'str'"
        self._entry_time = value

    @builtins.property
    def fee(self):
        """Message field 'fee'."""
        return self._fee

    @fee.setter
    def fee(self, value):
        if __debug__:
            assert \
                isinstance(value, int), \
                "The 'fee' field must be of type 'int'"
            assert value >= -2147483648 and value < 2147483648, \
                "The 'fee' field must be an integer in [-2147483648, 2147483647]"
        self._fee = value

    @builtins.property
    def log(self):
        """Message field 'log'."""
        return self._log

    @log.setter
    def log(self, value):
        if __debug__:
            assert \
                isinstance(value, str), \
                "The 'log' field must be of type 'str'"
        self._log = value


class Metaclass_ExitRequest(type):
    """Metaclass of service 'ExitRequest'."""

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
                'turtlebot3_interfaces.srv.ExitRequest')
            logger.debug(
                'Failed to import needed modules for type support:\n' +
                traceback.format_exc())
        else:
            cls._TYPE_SUPPORT = module.type_support_srv__srv__exit_request

            from turtlebot3_interfaces.srv import _exit_request
            if _exit_request.Metaclass_ExitRequest_Request._TYPE_SUPPORT is None:
                _exit_request.Metaclass_ExitRequest_Request.__import_type_support__()
            if _exit_request.Metaclass_ExitRequest_Response._TYPE_SUPPORT is None:
                _exit_request.Metaclass_ExitRequest_Response.__import_type_support__()


class ExitRequest(metaclass=Metaclass_ExitRequest):
    from turtlebot3_interfaces.srv._exit_request import ExitRequest_Request as Request
    from turtlebot3_interfaces.srv._exit_request import ExitRequest_Response as Response

    def __init__(self):
        raise NotImplementedError('Service classes can not be instantiated')
