// generated from rosidl_typesupport_introspection_c/resource/idl__type_support.c.em
// with input from menu_order_interfaces:srv/MenuTable.idl
// generated code does not contain a copyright notice

#include <stddef.h>
#include "menu_order_interfaces/srv/detail/menu_table__rosidl_typesupport_introspection_c.h"
#include "menu_order_interfaces/msg/rosidl_typesupport_introspection_c__visibility_control.h"
#include "rosidl_typesupport_introspection_c/field_types.h"
#include "rosidl_typesupport_introspection_c/identifier.h"
#include "rosidl_typesupport_introspection_c/message_introspection.h"
#include "menu_order_interfaces/srv/detail/menu_table__functions.h"
#include "menu_order_interfaces/srv/detail/menu_table__struct.h"


// Include directives for member types
// Member `request_type`
#include "rosidl_runtime_c/string_functions.h"

#ifdef __cplusplus
extern "C"
{
#endif

void menu_order_interfaces__srv__MenuTable_Request__rosidl_typesupport_introspection_c__MenuTable_Request_init_function(
  void * message_memory, enum rosidl_runtime_c__message_initialization _init)
{
  // TODO(karsten1987): initializers are not yet implemented for typesupport c
  // see https://github.com/ros2/ros2/issues/397
  (void) _init;
  menu_order_interfaces__srv__MenuTable_Request__init(message_memory);
}

void menu_order_interfaces__srv__MenuTable_Request__rosidl_typesupport_introspection_c__MenuTable_Request_fini_function(void * message_memory)
{
  menu_order_interfaces__srv__MenuTable_Request__fini(message_memory);
}

static rosidl_typesupport_introspection_c__MessageMember menu_order_interfaces__srv__MenuTable_Request__rosidl_typesupport_introspection_c__MenuTable_Request_message_member_array[1] = {
  {
    "request_type",  // name
    rosidl_typesupport_introspection_c__ROS_TYPE_STRING,  // type
    0,  // upper bound of string
    NULL,  // members of sub message
    false,  // is array
    0,  // array size
    false,  // is upper bound
    offsetof(menu_order_interfaces__srv__MenuTable_Request, request_type),  // bytes offset in struct
    NULL,  // default value
    NULL,  // size() function pointer
    NULL,  // get_const(index) function pointer
    NULL,  // get(index) function pointer
    NULL,  // fetch(index, &value) function pointer
    NULL,  // assign(index, value) function pointer
    NULL  // resize(index) function pointer
  }
};

static const rosidl_typesupport_introspection_c__MessageMembers menu_order_interfaces__srv__MenuTable_Request__rosidl_typesupport_introspection_c__MenuTable_Request_message_members = {
  "menu_order_interfaces__srv",  // message namespace
  "MenuTable_Request",  // message name
  1,  // number of fields
  sizeof(menu_order_interfaces__srv__MenuTable_Request),
  menu_order_interfaces__srv__MenuTable_Request__rosidl_typesupport_introspection_c__MenuTable_Request_message_member_array,  // message members
  menu_order_interfaces__srv__MenuTable_Request__rosidl_typesupport_introspection_c__MenuTable_Request_init_function,  // function to initialize message memory (memory has to be allocated)
  menu_order_interfaces__srv__MenuTable_Request__rosidl_typesupport_introspection_c__MenuTable_Request_fini_function  // function to terminate message instance (will not free memory)
};

// this is not const since it must be initialized on first access
// since C does not allow non-integral compile-time constants
static rosidl_message_type_support_t menu_order_interfaces__srv__MenuTable_Request__rosidl_typesupport_introspection_c__MenuTable_Request_message_type_support_handle = {
  0,
  &menu_order_interfaces__srv__MenuTable_Request__rosidl_typesupport_introspection_c__MenuTable_Request_message_members,
  get_message_typesupport_handle_function,
};

ROSIDL_TYPESUPPORT_INTROSPECTION_C_EXPORT_menu_order_interfaces
const rosidl_message_type_support_t *
ROSIDL_TYPESUPPORT_INTERFACE__MESSAGE_SYMBOL_NAME(rosidl_typesupport_introspection_c, menu_order_interfaces, srv, MenuTable_Request)() {
  if (!menu_order_interfaces__srv__MenuTable_Request__rosidl_typesupport_introspection_c__MenuTable_Request_message_type_support_handle.typesupport_identifier) {
    menu_order_interfaces__srv__MenuTable_Request__rosidl_typesupport_introspection_c__MenuTable_Request_message_type_support_handle.typesupport_identifier =
      rosidl_typesupport_introspection_c__identifier;
  }
  return &menu_order_interfaces__srv__MenuTable_Request__rosidl_typesupport_introspection_c__MenuTable_Request_message_type_support_handle;
}
#ifdef __cplusplus
}
#endif

// already included above
// #include <stddef.h>
// already included above
// #include "menu_order_interfaces/srv/detail/menu_table__rosidl_typesupport_introspection_c.h"
// already included above
// #include "menu_order_interfaces/msg/rosidl_typesupport_introspection_c__visibility_control.h"
// already included above
// #include "rosidl_typesupport_introspection_c/field_types.h"
// already included above
// #include "rosidl_typesupport_introspection_c/identifier.h"
// already included above
// #include "rosidl_typesupport_introspection_c/message_introspection.h"
// already included above
// #include "menu_order_interfaces/srv/detail/menu_table__functions.h"
// already included above
// #include "menu_order_interfaces/srv/detail/menu_table__struct.h"


// Include directives for member types
// Member `table_data`
// already included above
// #include "rosidl_runtime_c/string_functions.h"

#ifdef __cplusplus
extern "C"
{
#endif

void menu_order_interfaces__srv__MenuTable_Response__rosidl_typesupport_introspection_c__MenuTable_Response_init_function(
  void * message_memory, enum rosidl_runtime_c__message_initialization _init)
{
  // TODO(karsten1987): initializers are not yet implemented for typesupport c
  // see https://github.com/ros2/ros2/issues/397
  (void) _init;
  menu_order_interfaces__srv__MenuTable_Response__init(message_memory);
}

void menu_order_interfaces__srv__MenuTable_Response__rosidl_typesupport_introspection_c__MenuTable_Response_fini_function(void * message_memory)
{
  menu_order_interfaces__srv__MenuTable_Response__fini(message_memory);
}

size_t menu_order_interfaces__srv__MenuTable_Response__rosidl_typesupport_introspection_c__size_function__MenuTable_Response__table_data(
  const void * untyped_member)
{
  const rosidl_runtime_c__String__Sequence * member =
    (const rosidl_runtime_c__String__Sequence *)(untyped_member);
  return member->size;
}

const void * menu_order_interfaces__srv__MenuTable_Response__rosidl_typesupport_introspection_c__get_const_function__MenuTable_Response__table_data(
  const void * untyped_member, size_t index)
{
  const rosidl_runtime_c__String__Sequence * member =
    (const rosidl_runtime_c__String__Sequence *)(untyped_member);
  return &member->data[index];
}

void * menu_order_interfaces__srv__MenuTable_Response__rosidl_typesupport_introspection_c__get_function__MenuTable_Response__table_data(
  void * untyped_member, size_t index)
{
  rosidl_runtime_c__String__Sequence * member =
    (rosidl_runtime_c__String__Sequence *)(untyped_member);
  return &member->data[index];
}

void menu_order_interfaces__srv__MenuTable_Response__rosidl_typesupport_introspection_c__fetch_function__MenuTable_Response__table_data(
  const void * untyped_member, size_t index, void * untyped_value)
{
  const rosidl_runtime_c__String * item =
    ((const rosidl_runtime_c__String *)
    menu_order_interfaces__srv__MenuTable_Response__rosidl_typesupport_introspection_c__get_const_function__MenuTable_Response__table_data(untyped_member, index));
  rosidl_runtime_c__String * value =
    (rosidl_runtime_c__String *)(untyped_value);
  *value = *item;
}

void menu_order_interfaces__srv__MenuTable_Response__rosidl_typesupport_introspection_c__assign_function__MenuTable_Response__table_data(
  void * untyped_member, size_t index, const void * untyped_value)
{
  rosidl_runtime_c__String * item =
    ((rosidl_runtime_c__String *)
    menu_order_interfaces__srv__MenuTable_Response__rosidl_typesupport_introspection_c__get_function__MenuTable_Response__table_data(untyped_member, index));
  const rosidl_runtime_c__String * value =
    (const rosidl_runtime_c__String *)(untyped_value);
  *item = *value;
}

bool menu_order_interfaces__srv__MenuTable_Response__rosidl_typesupport_introspection_c__resize_function__MenuTable_Response__table_data(
  void * untyped_member, size_t size)
{
  rosidl_runtime_c__String__Sequence * member =
    (rosidl_runtime_c__String__Sequence *)(untyped_member);
  rosidl_runtime_c__String__Sequence__fini(member);
  return rosidl_runtime_c__String__Sequence__init(member, size);
}

static rosidl_typesupport_introspection_c__MessageMember menu_order_interfaces__srv__MenuTable_Response__rosidl_typesupport_introspection_c__MenuTable_Response_message_member_array[1] = {
  {
    "table_data",  // name
    rosidl_typesupport_introspection_c__ROS_TYPE_STRING,  // type
    0,  // upper bound of string
    NULL,  // members of sub message
    true,  // is array
    0,  // array size
    false,  // is upper bound
    offsetof(menu_order_interfaces__srv__MenuTable_Response, table_data),  // bytes offset in struct
    NULL,  // default value
    menu_order_interfaces__srv__MenuTable_Response__rosidl_typesupport_introspection_c__size_function__MenuTable_Response__table_data,  // size() function pointer
    menu_order_interfaces__srv__MenuTable_Response__rosidl_typesupport_introspection_c__get_const_function__MenuTable_Response__table_data,  // get_const(index) function pointer
    menu_order_interfaces__srv__MenuTable_Response__rosidl_typesupport_introspection_c__get_function__MenuTable_Response__table_data,  // get(index) function pointer
    menu_order_interfaces__srv__MenuTable_Response__rosidl_typesupport_introspection_c__fetch_function__MenuTable_Response__table_data,  // fetch(index, &value) function pointer
    menu_order_interfaces__srv__MenuTable_Response__rosidl_typesupport_introspection_c__assign_function__MenuTable_Response__table_data,  // assign(index, value) function pointer
    menu_order_interfaces__srv__MenuTable_Response__rosidl_typesupport_introspection_c__resize_function__MenuTable_Response__table_data  // resize(index) function pointer
  }
};

static const rosidl_typesupport_introspection_c__MessageMembers menu_order_interfaces__srv__MenuTable_Response__rosidl_typesupport_introspection_c__MenuTable_Response_message_members = {
  "menu_order_interfaces__srv",  // message namespace
  "MenuTable_Response",  // message name
  1,  // number of fields
  sizeof(menu_order_interfaces__srv__MenuTable_Response),
  menu_order_interfaces__srv__MenuTable_Response__rosidl_typesupport_introspection_c__MenuTable_Response_message_member_array,  // message members
  menu_order_interfaces__srv__MenuTable_Response__rosidl_typesupport_introspection_c__MenuTable_Response_init_function,  // function to initialize message memory (memory has to be allocated)
  menu_order_interfaces__srv__MenuTable_Response__rosidl_typesupport_introspection_c__MenuTable_Response_fini_function  // function to terminate message instance (will not free memory)
};

// this is not const since it must be initialized on first access
// since C does not allow non-integral compile-time constants
static rosidl_message_type_support_t menu_order_interfaces__srv__MenuTable_Response__rosidl_typesupport_introspection_c__MenuTable_Response_message_type_support_handle = {
  0,
  &menu_order_interfaces__srv__MenuTable_Response__rosidl_typesupport_introspection_c__MenuTable_Response_message_members,
  get_message_typesupport_handle_function,
};

ROSIDL_TYPESUPPORT_INTROSPECTION_C_EXPORT_menu_order_interfaces
const rosidl_message_type_support_t *
ROSIDL_TYPESUPPORT_INTERFACE__MESSAGE_SYMBOL_NAME(rosidl_typesupport_introspection_c, menu_order_interfaces, srv, MenuTable_Response)() {
  if (!menu_order_interfaces__srv__MenuTable_Response__rosidl_typesupport_introspection_c__MenuTable_Response_message_type_support_handle.typesupport_identifier) {
    menu_order_interfaces__srv__MenuTable_Response__rosidl_typesupport_introspection_c__MenuTable_Response_message_type_support_handle.typesupport_identifier =
      rosidl_typesupport_introspection_c__identifier;
  }
  return &menu_order_interfaces__srv__MenuTable_Response__rosidl_typesupport_introspection_c__MenuTable_Response_message_type_support_handle;
}
#ifdef __cplusplus
}
#endif

#include "rosidl_runtime_c/service_type_support_struct.h"
// already included above
// #include "menu_order_interfaces/msg/rosidl_typesupport_introspection_c__visibility_control.h"
// already included above
// #include "menu_order_interfaces/srv/detail/menu_table__rosidl_typesupport_introspection_c.h"
// already included above
// #include "rosidl_typesupport_introspection_c/identifier.h"
#include "rosidl_typesupport_introspection_c/service_introspection.h"

// this is intentionally not const to allow initialization later to prevent an initialization race
static rosidl_typesupport_introspection_c__ServiceMembers menu_order_interfaces__srv__detail__menu_table__rosidl_typesupport_introspection_c__MenuTable_service_members = {
  "menu_order_interfaces__srv",  // service namespace
  "MenuTable",  // service name
  // these two fields are initialized below on the first access
  NULL,  // request message
  // menu_order_interfaces__srv__detail__menu_table__rosidl_typesupport_introspection_c__MenuTable_Request_message_type_support_handle,
  NULL  // response message
  // menu_order_interfaces__srv__detail__menu_table__rosidl_typesupport_introspection_c__MenuTable_Response_message_type_support_handle
};

static rosidl_service_type_support_t menu_order_interfaces__srv__detail__menu_table__rosidl_typesupport_introspection_c__MenuTable_service_type_support_handle = {
  0,
  &menu_order_interfaces__srv__detail__menu_table__rosidl_typesupport_introspection_c__MenuTable_service_members,
  get_service_typesupport_handle_function,
};

// Forward declaration of request/response type support functions
const rosidl_message_type_support_t *
ROSIDL_TYPESUPPORT_INTERFACE__MESSAGE_SYMBOL_NAME(rosidl_typesupport_introspection_c, menu_order_interfaces, srv, MenuTable_Request)();

const rosidl_message_type_support_t *
ROSIDL_TYPESUPPORT_INTERFACE__MESSAGE_SYMBOL_NAME(rosidl_typesupport_introspection_c, menu_order_interfaces, srv, MenuTable_Response)();

ROSIDL_TYPESUPPORT_INTROSPECTION_C_EXPORT_menu_order_interfaces
const rosidl_service_type_support_t *
ROSIDL_TYPESUPPORT_INTERFACE__SERVICE_SYMBOL_NAME(rosidl_typesupport_introspection_c, menu_order_interfaces, srv, MenuTable)() {
  if (!menu_order_interfaces__srv__detail__menu_table__rosidl_typesupport_introspection_c__MenuTable_service_type_support_handle.typesupport_identifier) {
    menu_order_interfaces__srv__detail__menu_table__rosidl_typesupport_introspection_c__MenuTable_service_type_support_handle.typesupport_identifier =
      rosidl_typesupport_introspection_c__identifier;
  }
  rosidl_typesupport_introspection_c__ServiceMembers * service_members =
    (rosidl_typesupport_introspection_c__ServiceMembers *)menu_order_interfaces__srv__detail__menu_table__rosidl_typesupport_introspection_c__MenuTable_service_type_support_handle.data;

  if (!service_members->request_members_) {
    service_members->request_members_ =
      (const rosidl_typesupport_introspection_c__MessageMembers *)
      ROSIDL_TYPESUPPORT_INTERFACE__MESSAGE_SYMBOL_NAME(rosidl_typesupport_introspection_c, menu_order_interfaces, srv, MenuTable_Request)()->data;
  }
  if (!service_members->response_members_) {
    service_members->response_members_ =
      (const rosidl_typesupport_introspection_c__MessageMembers *)
      ROSIDL_TYPESUPPORT_INTERFACE__MESSAGE_SYMBOL_NAME(rosidl_typesupport_introspection_c, menu_order_interfaces, srv, MenuTable_Response)()->data;
  }

  return &menu_order_interfaces__srv__detail__menu_table__rosidl_typesupport_introspection_c__MenuTable_service_type_support_handle;
}