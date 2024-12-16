// generated from rosidl_generator_c/resource/idl__struct.h.em
// with input from turtlebot3_interfaces:srv/ExitRequest.idl
// generated code does not contain a copyright notice

#ifndef TURTLEBOT3_INTERFACES__SRV__DETAIL__EXIT_REQUEST__STRUCT_H_
#define TURTLEBOT3_INTERFACES__SRV__DETAIL__EXIT_REQUEST__STRUCT_H_

#ifdef __cplusplus
extern "C"
{
#endif

#include <stdbool.h>
#include <stddef.h>
#include <stdint.h>


// Constants defined in the message

// Include directives for member types
// Member 'car_number'
#include "rosidl_runtime_c/string.h"

/// Struct defined in srv/ExitRequest in the package turtlebot3_interfaces.
typedef struct turtlebot3_interfaces__srv__ExitRequest_Request
{
  rosidl_runtime_c__String car_number;
} turtlebot3_interfaces__srv__ExitRequest_Request;

// Struct for a sequence of turtlebot3_interfaces__srv__ExitRequest_Request.
typedef struct turtlebot3_interfaces__srv__ExitRequest_Request__Sequence
{
  turtlebot3_interfaces__srv__ExitRequest_Request * data;
  /// The number of valid items in data
  size_t size;
  /// The number of allocated items in data
  size_t capacity;
} turtlebot3_interfaces__srv__ExitRequest_Request__Sequence;


// Constants defined in the message

// Include directives for member types
// Member 'entry_time'
// Member 'log'
// already included above
// #include "rosidl_runtime_c/string.h"

/// Struct defined in srv/ExitRequest in the package turtlebot3_interfaces.
typedef struct turtlebot3_interfaces__srv__ExitRequest_Response
{
  bool status;
  rosidl_runtime_c__String entry_time;
  int32_t fee;
  rosidl_runtime_c__String log;
} turtlebot3_interfaces__srv__ExitRequest_Response;

// Struct for a sequence of turtlebot3_interfaces__srv__ExitRequest_Response.
typedef struct turtlebot3_interfaces__srv__ExitRequest_Response__Sequence
{
  turtlebot3_interfaces__srv__ExitRequest_Response * data;
  /// The number of valid items in data
  size_t size;
  /// The number of allocated items in data
  size_t capacity;
} turtlebot3_interfaces__srv__ExitRequest_Response__Sequence;

#ifdef __cplusplus
}
#endif

#endif  // TURTLEBOT3_INTERFACES__SRV__DETAIL__EXIT_REQUEST__STRUCT_H_
