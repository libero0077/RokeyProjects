// generated from rosidl_generator_c/resource/idl__struct.h.em
// with input from menu_order_interfaces:srv/MenuUpdate.idl
// generated code does not contain a copyright notice

#ifndef MENU_ORDER_INTERFACES__SRV__DETAIL__MENU_UPDATE__STRUCT_H_
#define MENU_ORDER_INTERFACES__SRV__DETAIL__MENU_UPDATE__STRUCT_H_

#ifdef __cplusplus
extern "C"
{
#endif

#include <stdbool.h>
#include <stddef.h>
#include <stdint.h>


// Constants defined in the message

// Include directives for member types
// Member 'result_message'
#include "rosidl_runtime_c/string.h"

/// Struct defined in srv/MenuUpdate in the package menu_order_interfaces.
typedef struct menu_order_interfaces__srv__MenuUpdate_Request
{
  rosidl_runtime_c__String result_message;
} menu_order_interfaces__srv__MenuUpdate_Request;

// Struct for a sequence of menu_order_interfaces__srv__MenuUpdate_Request.
typedef struct menu_order_interfaces__srv__MenuUpdate_Request__Sequence
{
  menu_order_interfaces__srv__MenuUpdate_Request * data;
  /// The number of valid items in data
  size_t size;
  /// The number of allocated items in data
  size_t capacity;
} menu_order_interfaces__srv__MenuUpdate_Request__Sequence;


// Constants defined in the message

/// Struct defined in srv/MenuUpdate in the package menu_order_interfaces.
typedef struct menu_order_interfaces__srv__MenuUpdate_Response
{
  bool success;
} menu_order_interfaces__srv__MenuUpdate_Response;

// Struct for a sequence of menu_order_interfaces__srv__MenuUpdate_Response.
typedef struct menu_order_interfaces__srv__MenuUpdate_Response__Sequence
{
  menu_order_interfaces__srv__MenuUpdate_Response * data;
  /// The number of valid items in data
  size_t size;
  /// The number of allocated items in data
  size_t capacity;
} menu_order_interfaces__srv__MenuUpdate_Response__Sequence;

#ifdef __cplusplus
}
#endif

#endif  // MENU_ORDER_INTERFACES__SRV__DETAIL__MENU_UPDATE__STRUCT_H_
