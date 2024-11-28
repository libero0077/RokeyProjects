// NOLINT: This file starts with a BOM since it contain non-ASCII characters
// generated from rosidl_generator_c/resource/idl__struct.h.em
// with input from menu_order_interfaces:msg/Order.idl
// generated code does not contain a copyright notice

#ifndef MENU_ORDER_INTERFACES__MSG__DETAIL__ORDER__STRUCT_H_
#define MENU_ORDER_INTERFACES__MSG__DETAIL__ORDER__STRUCT_H_

#ifdef __cplusplus
extern "C"
{
#endif

#include <stdbool.h>
#include <stddef.h>
#include <stdint.h>


// Constants defined in the message

// Include directives for member types
// Member 'table_id'
// Member 'menu'
#include "rosidl_runtime_c/string.h"

/// Struct defined in msg/Order in the package menu_order_interfaces.
typedef struct menu_order_interfaces__msg__Order
{
  /// 테이블 ID
  rosidl_runtime_c__String table_id;
  /// 메뉴 이름
  rosidl_runtime_c__String menu;
  /// 주문 수량
  int32_t quantity;
} menu_order_interfaces__msg__Order;

// Struct for a sequence of menu_order_interfaces__msg__Order.
typedef struct menu_order_interfaces__msg__Order__Sequence
{
  menu_order_interfaces__msg__Order * data;
  /// The number of valid items in data
  size_t size;
  /// The number of allocated items in data
  size_t capacity;
} menu_order_interfaces__msg__Order__Sequence;

#ifdef __cplusplus
}
#endif

#endif  // MENU_ORDER_INTERFACES__MSG__DETAIL__ORDER__STRUCT_H_
