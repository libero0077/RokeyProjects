// generated from rosidl_typesupport_fastrtps_cpp/resource/idl__type_support.cpp.em
// with input from menu_order_interfaces:srv/MenuTable.idl
// generated code does not contain a copyright notice
#include "menu_order_interfaces/srv/detail/menu_table__rosidl_typesupport_fastrtps_cpp.hpp"
#include "menu_order_interfaces/srv/detail/menu_table__struct.hpp"

#include <limits>
#include <stdexcept>
#include <string>
#include "rosidl_typesupport_cpp/message_type_support.hpp"
#include "rosidl_typesupport_fastrtps_cpp/identifier.hpp"
#include "rosidl_typesupport_fastrtps_cpp/message_type_support.h"
#include "rosidl_typesupport_fastrtps_cpp/message_type_support_decl.hpp"
#include "rosidl_typesupport_fastrtps_cpp/wstring_conversion.hpp"
#include "fastcdr/Cdr.h"


// forward declaration of message dependencies and their conversion functions

namespace menu_order_interfaces
{

namespace srv
{

namespace typesupport_fastrtps_cpp
{

bool
ROSIDL_TYPESUPPORT_FASTRTPS_CPP_PUBLIC_menu_order_interfaces
cdr_serialize(
  const menu_order_interfaces::srv::MenuTable_Request & ros_message,
  eprosima::fastcdr::Cdr & cdr)
{
  // Member: request_type
  cdr << ros_message.request_type;
  return true;
}

bool
ROSIDL_TYPESUPPORT_FASTRTPS_CPP_PUBLIC_menu_order_interfaces
cdr_deserialize(
  eprosima::fastcdr::Cdr & cdr,
  menu_order_interfaces::srv::MenuTable_Request & ros_message)
{
  // Member: request_type
  cdr >> ros_message.request_type;

  return true;
}

size_t
ROSIDL_TYPESUPPORT_FASTRTPS_CPP_PUBLIC_menu_order_interfaces
get_serialized_size(
  const menu_order_interfaces::srv::MenuTable_Request & ros_message,
  size_t current_alignment)
{
  size_t initial_alignment = current_alignment;

  const size_t padding = 4;
  const size_t wchar_size = 4;
  (void)padding;
  (void)wchar_size;

  // Member: request_type
  current_alignment += padding +
    eprosima::fastcdr::Cdr::alignment(current_alignment, padding) +
    (ros_message.request_type.size() + 1);

  return current_alignment - initial_alignment;
}

size_t
ROSIDL_TYPESUPPORT_FASTRTPS_CPP_PUBLIC_menu_order_interfaces
max_serialized_size_MenuTable_Request(
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


  // Member: request_type
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
    using DataType = menu_order_interfaces::srv::MenuTable_Request;
    is_plain =
      (
      offsetof(DataType, request_type) +
      last_member_size
      ) == ret_val;
  }

  return ret_val;
}

static bool _MenuTable_Request__cdr_serialize(
  const void * untyped_ros_message,
  eprosima::fastcdr::Cdr & cdr)
{
  auto typed_message =
    static_cast<const menu_order_interfaces::srv::MenuTable_Request *>(
    untyped_ros_message);
  return cdr_serialize(*typed_message, cdr);
}

static bool _MenuTable_Request__cdr_deserialize(
  eprosima::fastcdr::Cdr & cdr,
  void * untyped_ros_message)
{
  auto typed_message =
    static_cast<menu_order_interfaces::srv::MenuTable_Request *>(
    untyped_ros_message);
  return cdr_deserialize(cdr, *typed_message);
}

static uint32_t _MenuTable_Request__get_serialized_size(
  const void * untyped_ros_message)
{
  auto typed_message =
    static_cast<const menu_order_interfaces::srv::MenuTable_Request *>(
    untyped_ros_message);
  return static_cast<uint32_t>(get_serialized_size(*typed_message, 0));
}

static size_t _MenuTable_Request__max_serialized_size(char & bounds_info)
{
  bool full_bounded;
  bool is_plain;
  size_t ret_val;

  ret_val = max_serialized_size_MenuTable_Request(full_bounded, is_plain, 0);

  bounds_info =
    is_plain ? ROSIDL_TYPESUPPORT_FASTRTPS_PLAIN_TYPE :
    full_bounded ? ROSIDL_TYPESUPPORT_FASTRTPS_BOUNDED_TYPE : ROSIDL_TYPESUPPORT_FASTRTPS_UNBOUNDED_TYPE;
  return ret_val;
}

static message_type_support_callbacks_t _MenuTable_Request__callbacks = {
  "menu_order_interfaces::srv",
  "MenuTable_Request",
  _MenuTable_Request__cdr_serialize,
  _MenuTable_Request__cdr_deserialize,
  _MenuTable_Request__get_serialized_size,
  _MenuTable_Request__max_serialized_size
};

static rosidl_message_type_support_t _MenuTable_Request__handle = {
  rosidl_typesupport_fastrtps_cpp::typesupport_identifier,
  &_MenuTable_Request__callbacks,
  get_message_typesupport_handle_function,
};

}  // namespace typesupport_fastrtps_cpp

}  // namespace srv

}  // namespace menu_order_interfaces

namespace rosidl_typesupport_fastrtps_cpp
{

template<>
ROSIDL_TYPESUPPORT_FASTRTPS_CPP_EXPORT_menu_order_interfaces
const rosidl_message_type_support_t *
get_message_type_support_handle<menu_order_interfaces::srv::MenuTable_Request>()
{
  return &menu_order_interfaces::srv::typesupport_fastrtps_cpp::_MenuTable_Request__handle;
}

}  // namespace rosidl_typesupport_fastrtps_cpp

#ifdef __cplusplus
extern "C"
{
#endif

const rosidl_message_type_support_t *
ROSIDL_TYPESUPPORT_INTERFACE__MESSAGE_SYMBOL_NAME(rosidl_typesupport_fastrtps_cpp, menu_order_interfaces, srv, MenuTable_Request)() {
  return &menu_order_interfaces::srv::typesupport_fastrtps_cpp::_MenuTable_Request__handle;
}

#ifdef __cplusplus
}
#endif

// already included above
// #include <limits>
// already included above
// #include <stdexcept>
// already included above
// #include <string>
// already included above
// #include "rosidl_typesupport_cpp/message_type_support.hpp"
// already included above
// #include "rosidl_typesupport_fastrtps_cpp/identifier.hpp"
// already included above
// #include "rosidl_typesupport_fastrtps_cpp/message_type_support.h"
// already included above
// #include "rosidl_typesupport_fastrtps_cpp/message_type_support_decl.hpp"
// already included above
// #include "rosidl_typesupport_fastrtps_cpp/wstring_conversion.hpp"
// already included above
// #include "fastcdr/Cdr.h"


// forward declaration of message dependencies and their conversion functions

namespace menu_order_interfaces
{

namespace srv
{

namespace typesupport_fastrtps_cpp
{

bool
ROSIDL_TYPESUPPORT_FASTRTPS_CPP_PUBLIC_menu_order_interfaces
cdr_serialize(
  const menu_order_interfaces::srv::MenuTable_Response & ros_message,
  eprosima::fastcdr::Cdr & cdr)
{
  // Member: table_data
  {
    cdr << ros_message.table_data;
  }
  return true;
}

bool
ROSIDL_TYPESUPPORT_FASTRTPS_CPP_PUBLIC_menu_order_interfaces
cdr_deserialize(
  eprosima::fastcdr::Cdr & cdr,
  menu_order_interfaces::srv::MenuTable_Response & ros_message)
{
  // Member: table_data
  {
    cdr >> ros_message.table_data;
  }

  return true;
}

size_t
ROSIDL_TYPESUPPORT_FASTRTPS_CPP_PUBLIC_menu_order_interfaces
get_serialized_size(
  const menu_order_interfaces::srv::MenuTable_Response & ros_message,
  size_t current_alignment)
{
  size_t initial_alignment = current_alignment;

  const size_t padding = 4;
  const size_t wchar_size = 4;
  (void)padding;
  (void)wchar_size;

  // Member: table_data
  {
    size_t array_size = ros_message.table_data.size();

    current_alignment += padding +
      eprosima::fastcdr::Cdr::alignment(current_alignment, padding);
    for (size_t index = 0; index < array_size; ++index) {
      current_alignment += padding +
        eprosima::fastcdr::Cdr::alignment(current_alignment, padding) +
        (ros_message.table_data[index].size() + 1);
    }
  }

  return current_alignment - initial_alignment;
}

size_t
ROSIDL_TYPESUPPORT_FASTRTPS_CPP_PUBLIC_menu_order_interfaces
max_serialized_size_MenuTable_Response(
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


  // Member: table_data
  {
    size_t array_size = 0;
    full_bounded = false;
    is_plain = false;
    current_alignment += padding +
      eprosima::fastcdr::Cdr::alignment(current_alignment, padding);

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
    using DataType = menu_order_interfaces::srv::MenuTable_Response;
    is_plain =
      (
      offsetof(DataType, table_data) +
      last_member_size
      ) == ret_val;
  }

  return ret_val;
}

static bool _MenuTable_Response__cdr_serialize(
  const void * untyped_ros_message,
  eprosima::fastcdr::Cdr & cdr)
{
  auto typed_message =
    static_cast<const menu_order_interfaces::srv::MenuTable_Response *>(
    untyped_ros_message);
  return cdr_serialize(*typed_message, cdr);
}

static bool _MenuTable_Response__cdr_deserialize(
  eprosima::fastcdr::Cdr & cdr,
  void * untyped_ros_message)
{
  auto typed_message =
    static_cast<menu_order_interfaces::srv::MenuTable_Response *>(
    untyped_ros_message);
  return cdr_deserialize(cdr, *typed_message);
}

static uint32_t _MenuTable_Response__get_serialized_size(
  const void * untyped_ros_message)
{
  auto typed_message =
    static_cast<const menu_order_interfaces::srv::MenuTable_Response *>(
    untyped_ros_message);
  return static_cast<uint32_t>(get_serialized_size(*typed_message, 0));
}

static size_t _MenuTable_Response__max_serialized_size(char & bounds_info)
{
  bool full_bounded;
  bool is_plain;
  size_t ret_val;

  ret_val = max_serialized_size_MenuTable_Response(full_bounded, is_plain, 0);

  bounds_info =
    is_plain ? ROSIDL_TYPESUPPORT_FASTRTPS_PLAIN_TYPE :
    full_bounded ? ROSIDL_TYPESUPPORT_FASTRTPS_BOUNDED_TYPE : ROSIDL_TYPESUPPORT_FASTRTPS_UNBOUNDED_TYPE;
  return ret_val;
}

static message_type_support_callbacks_t _MenuTable_Response__callbacks = {
  "menu_order_interfaces::srv",
  "MenuTable_Response",
  _MenuTable_Response__cdr_serialize,
  _MenuTable_Response__cdr_deserialize,
  _MenuTable_Response__get_serialized_size,
  _MenuTable_Response__max_serialized_size
};

static rosidl_message_type_support_t _MenuTable_Response__handle = {
  rosidl_typesupport_fastrtps_cpp::typesupport_identifier,
  &_MenuTable_Response__callbacks,
  get_message_typesupport_handle_function,
};

}  // namespace typesupport_fastrtps_cpp

}  // namespace srv

}  // namespace menu_order_interfaces

namespace rosidl_typesupport_fastrtps_cpp
{

template<>
ROSIDL_TYPESUPPORT_FASTRTPS_CPP_EXPORT_menu_order_interfaces
const rosidl_message_type_support_t *
get_message_type_support_handle<menu_order_interfaces::srv::MenuTable_Response>()
{
  return &menu_order_interfaces::srv::typesupport_fastrtps_cpp::_MenuTable_Response__handle;
}

}  // namespace rosidl_typesupport_fastrtps_cpp

#ifdef __cplusplus
extern "C"
{
#endif

const rosidl_message_type_support_t *
ROSIDL_TYPESUPPORT_INTERFACE__MESSAGE_SYMBOL_NAME(rosidl_typesupport_fastrtps_cpp, menu_order_interfaces, srv, MenuTable_Response)() {
  return &menu_order_interfaces::srv::typesupport_fastrtps_cpp::_MenuTable_Response__handle;
}

#ifdef __cplusplus
}
#endif

#include "rmw/error_handling.h"
// already included above
// #include "rosidl_typesupport_fastrtps_cpp/identifier.hpp"
#include "rosidl_typesupport_fastrtps_cpp/service_type_support.h"
#include "rosidl_typesupport_fastrtps_cpp/service_type_support_decl.hpp"

namespace menu_order_interfaces
{

namespace srv
{

namespace typesupport_fastrtps_cpp
{

static service_type_support_callbacks_t _MenuTable__callbacks = {
  "menu_order_interfaces::srv",
  "MenuTable",
  ROSIDL_TYPESUPPORT_INTERFACE__MESSAGE_SYMBOL_NAME(rosidl_typesupport_fastrtps_cpp, menu_order_interfaces, srv, MenuTable_Request)(),
  ROSIDL_TYPESUPPORT_INTERFACE__MESSAGE_SYMBOL_NAME(rosidl_typesupport_fastrtps_cpp, menu_order_interfaces, srv, MenuTable_Response)(),
};

static rosidl_service_type_support_t _MenuTable__handle = {
  rosidl_typesupport_fastrtps_cpp::typesupport_identifier,
  &_MenuTable__callbacks,
  get_service_typesupport_handle_function,
};

}  // namespace typesupport_fastrtps_cpp

}  // namespace srv

}  // namespace menu_order_interfaces

namespace rosidl_typesupport_fastrtps_cpp
{

template<>
ROSIDL_TYPESUPPORT_FASTRTPS_CPP_EXPORT_menu_order_interfaces
const rosidl_service_type_support_t *
get_service_type_support_handle<menu_order_interfaces::srv::MenuTable>()
{
  return &menu_order_interfaces::srv::typesupport_fastrtps_cpp::_MenuTable__handle;
}

}  // namespace rosidl_typesupport_fastrtps_cpp

#ifdef __cplusplus
extern "C"
{
#endif

const rosidl_service_type_support_t *
ROSIDL_TYPESUPPORT_INTERFACE__SERVICE_SYMBOL_NAME(rosidl_typesupport_fastrtps_cpp, menu_order_interfaces, srv, MenuTable)() {
  return &menu_order_interfaces::srv::typesupport_fastrtps_cpp::_MenuTable__handle;
}

#ifdef __cplusplus
}
#endif
