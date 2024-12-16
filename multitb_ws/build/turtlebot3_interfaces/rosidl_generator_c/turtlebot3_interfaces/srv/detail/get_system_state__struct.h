// generated from rosidl_generator_c/resource/idl__struct.h.em
// with input from turtlebot3_interfaces:srv/GetSystemState.idl
// generated code does not contain a copyright notice

#ifndef TURTLEBOT3_INTERFACES__SRV__DETAIL__GET_SYSTEM_STATE__STRUCT_H_
#define TURTLEBOT3_INTERFACES__SRV__DETAIL__GET_SYSTEM_STATE__STRUCT_H_

#ifdef __cplusplus
extern "C"
{
#endif

#include <stdbool.h>
#include <stddef.h>
#include <stdint.h>


// Constants defined in the message

/// Struct defined in srv/GetSystemState in the package turtlebot3_interfaces.
typedef struct turtlebot3_interfaces__srv__GetSystemState_Request
{
  uint8_t structure_needs_at_least_one_member;
} turtlebot3_interfaces__srv__GetSystemState_Request;

// Struct for a sequence of turtlebot3_interfaces__srv__GetSystemState_Request.
typedef struct turtlebot3_interfaces__srv__GetSystemState_Request__Sequence
{
  turtlebot3_interfaces__srv__GetSystemState_Request * data;
  /// The number of valid items in data
  size_t size;
  /// The number of allocated items in data
  size_t capacity;
} turtlebot3_interfaces__srv__GetSystemState_Request__Sequence;


// Constants defined in the message

// Include directives for member types
// Member 'robot_status_json'
// Member 'slot_status_json'
#include "rosidl_runtime_c/string.h"

/// Struct defined in srv/GetSystemState in the package turtlebot3_interfaces.
typedef struct turtlebot3_interfaces__srv__GetSystemState_Response
{
  rosidl_runtime_c__String robot_status_json;
  rosidl_runtime_c__String slot_status_json;
} turtlebot3_interfaces__srv__GetSystemState_Response;

// Struct for a sequence of turtlebot3_interfaces__srv__GetSystemState_Response.
typedef struct turtlebot3_interfaces__srv__GetSystemState_Response__Sequence
{
  turtlebot3_interfaces__srv__GetSystemState_Response * data;
  /// The number of valid items in data
  size_t size;
  /// The number of allocated items in data
  size_t capacity;
} turtlebot3_interfaces__srv__GetSystemState_Response__Sequence;

#ifdef __cplusplus
}
#endif

#endif  // TURTLEBOT3_INTERFACES__SRV__DETAIL__GET_SYSTEM_STATE__STRUCT_H_
