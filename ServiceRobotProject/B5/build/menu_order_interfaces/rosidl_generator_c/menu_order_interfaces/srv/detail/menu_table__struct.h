// NOLINT: This file starts with a BOM since it contain non-ASCII characters
// generated from rosidl_generator_c/resource/idl__struct.h.em
// with input from menu_order_interfaces:srv/MenuTable.idl
// generated code does not contain a copyright notice

#ifndef MENU_ORDER_INTERFACES__SRV__DETAIL__MENU_TABLE__STRUCT_H_
#define MENU_ORDER_INTERFACES__SRV__DETAIL__MENU_TABLE__STRUCT_H_

#ifdef __cplusplus
extern "C"
{
#endif

#include <stdbool.h>
#include <stddef.h>
#include <stdint.h>


// Constants defined in the message

// Include directives for member types
// Member 'request_type'
#include "rosidl_runtime_c/string.h"

/// Struct defined in srv/MenuTable in the package menu_order_interfaces.
typedef struct menu_order_interfaces__srv__MenuTable_Request
{
  /// 요청 유형 (e.g., 'get_menu_table')
  rosidl_runtime_c__String request_type;
} menu_order_interfaces__srv__MenuTable_Request;

// Struct for a sequence of menu_order_interfaces__srv__MenuTable_Request.
typedef struct menu_order_interfaces__srv__MenuTable_Request__Sequence
{
  menu_order_interfaces__srv__MenuTable_Request * data;
  /// The number of valid items in data
  size_t size;
  /// The number of allocated items in data
  size_t capacity;
} menu_order_interfaces__srv__MenuTable_Request__Sequence;


// Constants defined in the message

// Include directives for member types
// Member 'table_data'
// already included above
// #include "rosidl_runtime_c/string.h"

/// Struct defined in srv/MenuTable in the package menu_order_interfaces.
typedef struct menu_order_interfaces__srv__MenuTable_Response
{
  /// 테이블 데이터 (모든 행을 문자열로 직렬화)
  rosidl_runtime_c__String__Sequence table_data;
} menu_order_interfaces__srv__MenuTable_Response;

// Struct for a sequence of menu_order_interfaces__srv__MenuTable_Response.
typedef struct menu_order_interfaces__srv__MenuTable_Response__Sequence
{
  menu_order_interfaces__srv__MenuTable_Response * data;
  /// The number of valid items in data
  size_t size;
  /// The number of allocated items in data
  size_t capacity;
} menu_order_interfaces__srv__MenuTable_Response__Sequence;

#ifdef __cplusplus
}
#endif

#endif  // MENU_ORDER_INTERFACES__SRV__DETAIL__MENU_TABLE__STRUCT_H_
