// generated from rosidl_typesupport_fastrtps_c/resource/idl__type_support_c.cpp.em
// with input from turtlebot3_interfaces:srv/ExitRequest.idl
// generated code does not contain a copyright notice
#include "turtlebot3_interfaces/srv/detail/exit_request__rosidl_typesupport_fastrtps_c.h"


#include <cassert>
#include <limits>
#include <string>
#include "rosidl_typesupport_fastrtps_c/identifier.h"
#include "rosidl_typesupport_fastrtps_c/wstring_conversion.hpp"
#include "rosidl_typesupport_fastrtps_cpp/message_type_support.h"
#include "turtlebot3_interfaces/msg/rosidl_typesupport_fastrtps_c__visibility_control.h"
#include "turtlebot3_interfaces/srv/detail/exit_request__struct.h"
#include "turtlebot3_interfaces/srv/detail/exit_request__functions.h"
#include "fastcdr/Cdr.h"

#ifndef _WIN32
# pragma GCC diagnostic push
# pragma GCC diagnostic ignored "-Wunused-parameter"
# ifdef __clang__
#  pragma clang diagnostic ignored "-Wdeprecated-register"
#  pragma clang diagnostic ignored "-Wreturn-type-c-linkage"
# endif
#endif
#ifndef _WIN32
# pragma GCC diagnostic pop
#endif

// includes and forward declarations of message dependencies and their conversion functions

#if defined(__cplusplus)
extern "C"
{
#endif

#include "rosidl_runtime_c/string.h"  // car_number
#include "rosidl_runtime_c/string_functions.h"  // car_number

// forward declare type support functions


using _ExitRequest_Request__ros_msg_type = turtlebot3_interfaces__srv__ExitRequest_Request;

static bool _ExitRequest_Request__cdr_serialize(
  const void * untyped_ros_message,
  eprosima::fastcdr::Cdr & cdr)
{
  if (!untyped_ros_message) {
    fprintf(stderr, "ros message handle is null\n");
    return false;
  }
  const _ExitRequest_Request__ros_msg_type * ros_message = static_cast<const _ExitRequest_Request__ros_msg_type *>(untyped_ros_message);
  // Field name: car_number
  {
    const rosidl_runtime_c__String * str = &ros_message->car_number;
    if (str->capacity == 0 || str->capacity <= str->size) {
      fprintf(stderr, "string capacity not greater than size\n");
      return false;
    }
    if (str->data[str->size] != '\0') {
      fprintf(stderr, "string not null-terminated\n");
      return false;
    }
    cdr << str->data;
  }

  return true;
}

static bool _ExitRequest_Request__cdr_deserialize(
  eprosima::fastcdr::Cdr & cdr,
  void * untyped_ros_message)
{
  if (!untyped_ros_message) {
    fprintf(stderr, "ros message handle is null\n");
    return false;
  }
  _ExitRequest_Request__ros_msg_type * ros_message = static_cast<_ExitRequest_Request__ros_msg_type *>(untyped_ros_message);
  // Field name: car_number
  {
    std::string tmp;
    cdr >> tmp;
    if (!ros_message->car_number.data) {
      rosidl_runtime_c__String__init(&ros_message->car_number);
    }
    bool succeeded = rosidl_runtime_c__String__assign(
      &ros_message->car_number,
      tmp.c_str());
    if (!succeeded) {
      fprintf(stderr, "failed to assign string into field 'car_number'\n");
      return false;
    }
  }

  return true;
}  // NOLINT(readability/fn_size)

ROSIDL_TYPESUPPORT_FASTRTPS_C_PUBLIC_turtlebot3_interfaces
size_t get_serialized_size_turtlebot3_interfaces__srv__ExitRequest_Request(
  const void * untyped_ros_message,
  size_t current_alignment)
{
  const _ExitRequest_Request__ros_msg_type * ros_message = static_cast<const _ExitRequest_Request__ros_msg_type *>(untyped_ros_message);
  (void)ros_message;
  size_t initial_alignment = current_alignment;

  const size_t padding = 4;
  const size_t wchar_size = 4;
  (void)padding;
  (void)wchar_size;

  // field.name car_number
  current_alignment += padding +
    eprosima::fastcdr::Cdr::alignment(current_alignment, padding) +
    (ros_message->car_number.size + 1);

  return current_alignment - initial_alignment;
}

static uint32_t _ExitRequest_Request__get_serialized_size(const void * untyped_ros_message)
{
  return static_cast<uint32_t>(
    get_serialized_size_turtlebot3_interfaces__srv__ExitRequest_Request(
      untyped_ros_message, 0));
}

ROSIDL_TYPESUPPORT_FASTRTPS_C_PUBLIC_turtlebot3_interfaces
size_t max_serialized_size_turtlebot3_interfaces__srv__ExitRequest_Request(
  bool & full_bounded,
  bool & is_plain,
  size_t current_alignment)
{
  size_t initial_alignment = current_alignment;

  const size_t padding = 4;
  const size_t wchar_size = 4;
  size_t last_member_size = 0;
  (void)last_member_size;
  (void)padding;
  (void)wchar_size;

  full_bounded = true;
  is_plain = true;

  // member: car_number
  {
    size_t array_size = 1;

    full_bounded = false;
    is_plain = false;
    for (size_t index = 0; index < array_size; ++index) {
      current_alignment += padding +
        eprosima::fastcdr::Cdr::alignment(current_alignment, padding) +
        1;
    }
  }

  size_t ret_val = current_alignment - initial_alignment;
  if (is_plain) {
    // All members are plain, and type is not empty.
    // We still need to check that the in-memory alignment
    // is the same as the CDR mandated alignment.
    using DataType = turtlebot3_interfaces__srv__ExitRequest_Request;
    is_plain =
      (
      offsetof(DataType, car_number) +
      last_member_size
      ) == ret_val;
  }

  return ret_val;
}

static size_t _ExitRequest_Request__max_serialized_size(char & bounds_info)
{
  bool full_bounded;
  bool is_plain;
  size_t ret_val;

  ret_val = max_serialized_size_turtlebot3_interfaces__srv__ExitRequest_Request(
    full_bounded, is_plain, 0);

  bounds_info =
    is_plain ? ROSIDL_TYPESUPPORT_FASTRTPS_PLAIN_TYPE :
    full_bounded ? ROSIDL_TYPESUPPORT_FASTRTPS_BOUNDED_TYPE : ROSIDL_TYPESUPPORT_FASTRTPS_UNBOUNDED_TYPE;
  return ret_val;
}


static message_type_support_callbacks_t __callbacks_ExitRequest_Request = {
  "turtlebot3_interfaces::srv",
  "ExitRequest_Request",
  _ExitRequest_Request__cdr_serialize,
  _ExitRequest_Request__cdr_deserialize,
  _ExitRequest_Request__get_serialized_size,
  _ExitRequest_Request__max_serialized_size
};

static rosidl_message_type_support_t _ExitRequest_Request__type_support = {
  rosidl_typesupport_fastrtps_c__identifier,
  &__callbacks_ExitRequest_Request,
  get_message_typesupport_handle_function,
};

const rosidl_message_type_support_t *
ROSIDL_TYPESUPPORT_INTERFACE__MESSAGE_SYMBOL_NAME(rosidl_typesupport_fastrtps_c, turtlebot3_interfaces, srv, ExitRequest_Request)() {
  return &_ExitRequest_Request__type_support;
}

#if defined(__cplusplus)
}
#endif

// already included above
// #include <cassert>
// already included above
// #include <limits>
// already included above
// #include <string>
// already included above
// #include "rosidl_typesupport_fastrtps_c/identifier.h"
// already included above
// #include "rosidl_typesupport_fastrtps_c/wstring_conversion.hpp"
// already included above
// #include "rosidl_typesupport_fastrtps_cpp/message_type_support.h"
// already included above
// #include "turtlebot3_interfaces/msg/rosidl_typesupport_fastrtps_c__visibility_control.h"
// already included above
// #include "turtlebot3_interfaces/srv/detail/exit_request__struct.h"
// already included above
// #include "turtlebot3_interfaces/srv/detail/exit_request__functions.h"
// already included above
// #include "fastcdr/Cdr.h"

#ifndef _WIN32
# pragma GCC diagnostic push
# pragma GCC diagnostic ignored "-Wunused-parameter"
# ifdef __clang__
#  pragma clang diagnostic ignored "-Wdeprecated-register"
#  pragma clang diagnostic ignored "-Wreturn-type-c-linkage"
# endif
#endif
#ifndef _WIN32
# pragma GCC diagnostic pop
#endif

// includes and forward declarations of message dependencies and their conversion functions

#if defined(__cplusplus)
extern "C"
{
#endif

// already included above
// #include "rosidl_runtime_c/string.h"  // entry_time, log
// already included above
// #include "rosidl_runtime_c/string_functions.h"  // entry_time, log

// forward declare type support functions


using _ExitRequest_Response__ros_msg_type = turtlebot3_interfaces__srv__ExitRequest_Response;

static bool _ExitRequest_Response__cdr_serialize(
  const void * untyped_ros_message,
  eprosima::fastcdr::Cdr & cdr)
{
  if (!untyped_ros_message) {
    fprintf(stderr, "ros message handle is null\n");
    return false;
  }
  const _ExitRequest_Response__ros_msg_type * ros_message = static_cast<const _ExitRequest_Response__ros_msg_type *>(untyped_ros_message);
  // Field name: status
  {
    cdr << (ros_message->status ? true : false);
  }

  // Field name: entry_time
  {
    const rosidl_runtime_c__String * str = &ros_message->entry_time;
    if (str->capacity == 0 || str->capacity <= str->size) {
      fprintf(stderr, "string capacity not greater than size\n");
      return false;
    }
    if (str->data[str->size] != '\0') {
      fprintf(stderr, "string not null-terminated\n");
      return false;
    }
    cdr << str->data;
  }

  // Field name: fee
  {
    cdr << ros_message->fee;
  }

  // Field name: log
  {
    const rosidl_runtime_c__String * str = &ros_message->log;
    if (str->capacity == 0 || str->capacity <= str->size) {
      fprintf(stderr, "string capacity not greater than size\n");
      return false;
    }
    if (str->data[str->size] != '\0') {
      fprintf(stderr, "string not null-terminated\n");
      return false;
    }
    cdr << str->data;
  }

  return true;
}

static bool _ExitRequest_Response__cdr_deserialize(
  eprosima::fastcdr::Cdr & cdr,
  void * untyped_ros_message)
{
  if (!untyped_ros_message) {
    fprintf(stderr, "ros message handle is null\n");
    return false;
  }
  _ExitRequest_Response__ros_msg_type * ros_message = static_cast<_ExitRequest_Response__ros_msg_type *>(untyped_ros_message);
  // Field name: status
  {
    uint8_t tmp;
    cdr >> tmp;
    ros_message->status = tmp ? true : false;
  }

  // Field name: entry_time
  {
    std::string tmp;
    cdr >> tmp;
    if (!ros_message->entry_time.data) {
      rosidl_runtime_c__String__init(&ros_message->entry_time);
    }
    bool succeeded = rosidl_runtime_c__String__assign(
      &ros_message->entry_time,
      tmp.c_str());
    if (!succeeded) {
      fprintf(stderr, "failed to assign string into field 'entry_time'\n");
      return false;
    }
  }

  // Field name: fee
  {
    cdr >> ros_message->fee;
  }

  // Field name: log
  {
    std::string tmp;
    cdr >> tmp;
    if (!ros_message->log.data) {
      rosidl_runtime_c__String__init(&ros_message->log);
    }
    bool succeeded = rosidl_runtime_c__String__assign(
      &ros_message->log,
      tmp.c_str());
    if (!succeeded) {
      fprintf(stderr, "failed to assign string into field 'log'\n");
      return false;
    }
  }

  return true;
}  // NOLINT(readability/fn_size)

ROSIDL_TYPESUPPORT_FASTRTPS_C_PUBLIC_turtlebot3_interfaces
size_t get_serialized_size_turtlebot3_interfaces__srv__ExitRequest_Response(
  const void * untyped_ros_message,
  size_t current_alignment)
{
  const _ExitRequest_Response__ros_msg_type * ros_message = static_cast<const _ExitRequest_Response__ros_msg_type *>(untyped_ros_message);
  (void)ros_message;
  size_t initial_alignment = current_alignment;

  const size_t padding = 4;
  const size_t wchar_size = 4;
  (void)padding;
  (void)wchar_size;

  // field.name status
  {
    size_t item_size = sizeof(ros_message->status);
    current_alignment += item_size +
      eprosima::fastcdr::Cdr::alignment(current_alignment, item_size);
  }
  // field.name entry_time
  current_alignment += padding +
    eprosima::fastcdr::Cdr::alignment(current_alignment, padding) +
    (ros_message->entry_time.size + 1);
  // field.name fee
  {
    size_t item_size = sizeof(ros_message->fee);
    current_alignment += item_size +
      eprosima::fastcdr::Cdr::alignment(current_alignment, item_size);
  }
  // field.name log
  current_alignment += padding +
    eprosima::fastcdr::Cdr::alignment(current_alignment, padding) +
    (ros_message->log.size + 1);

  return current_alignment - initial_alignment;
}

static uint32_t _ExitRequest_Response__get_serialized_size(const void * untyped_ros_message)
{
  return static_cast<uint32_t>(
    get_serialized_size_turtlebot3_interfaces__srv__ExitRequest_Response(
      untyped_ros_message, 0));
}

ROSIDL_TYPESUPPORT_FASTRTPS_C_PUBLIC_turtlebot3_interfaces
size_t max_serialized_size_turtlebot3_interfaces__srv__ExitRequest_Response(
  bool & full_bounded,
  bool & is_plain,
  size_t current_alignment)
{
  size_t initial_alignment = current_alignment;

  const size_t padding = 4;
  const size_t wchar_size = 4;
  size_t last_member_size = 0;
  (void)last_member_size;
  (void)padding;
  (void)wchar_size;

  full_bounded = true;
  is_plain = true;

  // member: status
  {
    size_t array_size = 1;

    last_member_size = array_size * sizeof(uint8_t);
    current_alignment += array_size * sizeof(uint8_t);
  }
  // member: entry_time
  {
    size_t array_size = 1;

    full_bounded = false;
    is_plain = false;
    for (size_t index = 0; index < array_size; ++index) {
      current_alignment += padding +
        eprosima::fastcdr::Cdr::alignment(current_alignment, padding) +
        1;
    }
  }
  // member: fee
  {
    size_t array_size = 1;

    last_member_size = array_size * sizeof(uint32_t);
    current_alignment += array_size * sizeof(uint32_t) +
      eprosima::fastcdr::Cdr::alignment(current_alignment, sizeof(uint32_t));
  }
  // member: log
  {
    size_t array_size = 1;

    full_bounded = false;
    is_plain = false;
    for (size_t index = 0; index < array_size; ++index) {
      current_alignment += padding +
        eprosima::fastcdr::Cdr::alignment(current_alignment, padding) +
        1;
    }
  }

  size_t ret_val = current_alignment - initial_alignment;
  if (is_plain) {
    // All members are plain, and type is not empty.
    // We still need to check that the in-memory alignment
    // is the same as the CDR mandated alignment.
    using DataType = turtlebot3_interfaces__srv__ExitRequest_Response;
    is_plain =
      (
      offsetof(DataType, log) +
      last_member_size
      ) == ret_val;
  }

  return ret_val;
}

static size_t _ExitRequest_Response__max_serialized_size(char & bounds_info)
{
  bool full_bounded;
  bool is_plain;
  size_t ret_val;

  ret_val = max_serialized_size_turtlebot3_interfaces__srv__ExitRequest_Response(
    full_bounded, is_plain, 0);

  bounds_info =
    is_plain ? ROSIDL_TYPESUPPORT_FASTRTPS_PLAIN_TYPE :
    full_bounded ? ROSIDL_TYPESUPPORT_FASTRTPS_BOUNDED_TYPE : ROSIDL_TYPESUPPORT_FASTRTPS_UNBOUNDED_TYPE;
  return ret_val;
}


static message_type_support_callbacks_t __callbacks_ExitRequest_Response = {
  "turtlebot3_interfaces::srv",
  "ExitRequest_Response",
  _ExitRequest_Response__cdr_serialize,
  _ExitRequest_Response__cdr_deserialize,
  _ExitRequest_Response__get_serialized_size,
  _ExitRequest_Response__max_serialized_size
};

static rosidl_message_type_support_t _ExitRequest_Response__type_support = {
  rosidl_typesupport_fastrtps_c__identifier,
  &__callbacks_ExitRequest_Response,
  get_message_typesupport_handle_function,
};

const rosidl_message_type_support_t *
ROSIDL_TYPESUPPORT_INTERFACE__MESSAGE_SYMBOL_NAME(rosidl_typesupport_fastrtps_c, turtlebot3_interfaces, srv, ExitRequest_Response)() {
  return &_ExitRequest_Response__type_support;
}

#if defined(__cplusplus)
}
#endif

#include "rosidl_typesupport_fastrtps_cpp/service_type_support.h"
#include "rosidl_typesupport_cpp/service_type_support.hpp"
// already included above
// #include "rosidl_typesupport_fastrtps_c/identifier.h"
// already included above
// #include "turtlebot3_interfaces/msg/rosidl_typesupport_fastrtps_c__visibility_control.h"
#include "turtlebot3_interfaces/srv/exit_request.h"

#if defined(__cplusplus)
extern "C"
{
#endif

static service_type_support_callbacks_t ExitRequest__callbacks = {
  "turtlebot3_interfaces::srv",
  "ExitRequest",
  ROSIDL_TYPESUPPORT_INTERFACE__MESSAGE_SYMBOL_NAME(rosidl_typesupport_fastrtps_c, turtlebot3_interfaces, srv, ExitRequest_Request)(),
  ROSIDL_TYPESUPPORT_INTERFACE__MESSAGE_SYMBOL_NAME(rosidl_typesupport_fastrtps_c, turtlebot3_interfaces, srv, ExitRequest_Response)(),
};

static rosidl_service_type_support_t ExitRequest__handle = {
  rosidl_typesupport_fastrtps_c__identifier,
  &ExitRequest__callbacks,
  get_service_typesupport_handle_function,
};

const rosidl_service_type_support_t *
ROSIDL_TYPESUPPORT_INTERFACE__SERVICE_SYMBOL_NAME(rosidl_typesupport_fastrtps_c, turtlebot3_interfaces, srv, ExitRequest)() {
  return &ExitRequest__handle;
}

#if defined(__cplusplus)
}
#endif
