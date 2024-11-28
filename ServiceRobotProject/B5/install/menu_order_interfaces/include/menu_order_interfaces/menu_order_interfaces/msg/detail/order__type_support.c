// generated from rosidl_typesupport_introspection_c/resource/idl__type_support.c.em
// with input from menu_order_interfaces:msg/Order.idl
// generated code does not contain a copyright notice

#include <stddef.h>
#include "menu_order_interfaces/msg/detail/order__rosidl_typesupport_introspection_c.h"
#include "menu_order_interfaces/msg/rosidl_typesupport_introspection_c__visibility_control.h"
#include "rosidl_typesupport_introspection_c/field_types.h"
#include "rosidl_typesupport_introspection_c/identifier.h"
#include "rosidl_typesupport_introspection_c/message_introspection.h"
#include "menu_order_interfaces/msg/detail/order__functions.h"
#include "menu_order_interfaces/msg/detail/order__struct.h"


// Include directives for member types
// Member `table_id`
// Member `menu`
#include "rosidl_runtime_c/string_functions.h"

#ifdef __cplusplus
extern "C"
{
#endif

void menu_order_interfaces__msg__Order__rosidl_typesupport_introspection_c__Order_init_function(
  void * message_memory, enum rosidl_runtime_c__message_initialization _init)
{
  // TODO(karsten1987): initializers are not yet implemented for typesupport c
  // see https://github.com/ros2/ros2/issues/397
  (void) _init;
  menu_order_interfaces__msg__Order__init(message_memory);
}

void menu_order_interfaces__msg__Order__rosidl_typesupport_introspection_c__Order_fini_function(void * message_memory)
{
  menu_order_interfaces__msg__Order__fini(message_memory);
}

static rosidl_typesupport_introspection_c__MessageMember menu_order_interfaces__msg__Order__rosidl_typesupport_introspection_c__Order_message_member_array[3] = {
  {
    "table_id",  // name
    rosidl_typesupport_introspection_c__ROS_TYPE_STRING,  // type
    0,  // upper bound of string
    NULL,  // members of sub message
    false,  // is array
    0,  // array size
    false,  // is upper bound
    offsetof(menu_order_interfaces__msg__Order, table_id),  // bytes offset in struct
    NULL,  // default value
    NULL,  // size() function pointer
    NULL,  // get_const(index) function pointer
    NULL,  // get(index) function pointer
    NULL,  // fetch(index, &value) function pointer
    NULL,  // assign(index, value) function pointer
    NULL  // resize(index) function pointer
  },
  {
    "menu",  // name
    rosidl_typesupport_introspection_c__ROS_TYPE_STRING,  // type
    0,  // upper bound of string
    NULL,  // members of sub message
    false,  // is array
    0,  // array size
    false,  // is upper bound
    offsetof(menu_order_interfaces__msg__Order, menu),  // bytes offset in struct
    NULL,  // default value
    NULL,  // size() function pointer
    NULL,  // get_const(index) function pointer
    NULL,  // get(index) function pointer
    NULL,  // fetch(index, &value) function pointer
    NULL,  // assign(index, value) function pointer
    NULL  // resize(index) function pointer
  },
  {
    "quantity",  // name
    rosidl_typesupport_introspection_c__ROS_TYPE_INT32,  // type
    0,  // upper bound of string
    NULL,  // members of sub message
    false,  // is array
    0,  // array size
    false,  // is upper bound
    offsetof(menu_order_interfaces__msg__Order, quantity),  // bytes offset in struct
    NULL,  // default value
    NULL,  // size() function pointer
    NULL,  // get_const(index) function pointer
    NULL,  // get(index) function pointer
    NULL,  // fetch(index, &value) function pointer
    NULL,  // assign(index, value) function pointer
    NULL  // resize(index) function pointer
  }
};

static const rosidl_typesupport_introspection_c__MessageMembers menu_order_interfaces__msg__Order__rosidl_typesupport_introspection_c__Order_message_members = {
  "menu_order_interfaces__msg",  // message namespace
  "Order",  // message name
  3,  // number of fields
  sizeof(menu_order_interfaces__msg__Order),
  menu_order_interfaces__msg__Order__rosidl_typesupport_introspection_c__Order_message_member_array,  // message members
  menu_order_interfaces__msg__Order__rosidl_typesupport_introspection_c__Order_init_function,  // function to initialize message memory (memory has to be allocated)
  menu_order_interfaces__msg__Order__rosidl_typesupport_introspection_c__Order_fini_function  // function to terminate message instance (will not free memory)
};

// this is not const since it must be initialized on first access
// since C does not allow non-integral compile-time constants
static rosidl_message_type_support_t menu_order_interfaces__msg__Order__rosidl_typesupport_introspection_c__Order_message_type_support_handle = {
  0,
  &menu_order_interfaces__msg__Order__rosidl_typesupport_introspection_c__Order_message_members,
  get_message_typesupport_handle_function,
};

ROSIDL_TYPESUPPORT_INTROSPECTION_C_EXPORT_menu_order_interfaces
const rosidl_message_type_support_t *
ROSIDL_TYPESUPPORT_INTERFACE__MESSAGE_SYMBOL_NAME(rosidl_typesupport_introspection_c, menu_order_interfaces, msg, Order)() {
  if (!menu_order_interfaces__msg__Order__rosidl_typesupport_introspection_c__Order_message_type_support_handle.typesupport_identifier) {
    menu_order_interfaces__msg__Order__rosidl_typesupport_introspection_c__Order_message_type_support_handle.typesupport_identifier =
      rosidl_typesupport_introspection_c__identifier;
  }
  return &menu_order_interfaces__msg__Order__rosidl_typesupport_introspection_c__Order_message_type_support_handle;
}
#ifdef __cplusplus
}
#endif
