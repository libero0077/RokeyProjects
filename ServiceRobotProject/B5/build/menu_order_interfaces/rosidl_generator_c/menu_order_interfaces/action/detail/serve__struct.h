// NOLINT: This file starts with a BOM since it contain non-ASCII characters
// generated from rosidl_generator_c/resource/idl__struct.h.em
// with input from menu_order_interfaces:action/Serve.idl
// generated code does not contain a copyright notice

#ifndef MENU_ORDER_INTERFACES__ACTION__DETAIL__SERVE__STRUCT_H_
#define MENU_ORDER_INTERFACES__ACTION__DETAIL__SERVE__STRUCT_H_

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
#include "rosidl_runtime_c/string.h"

/// Struct defined in action/Serve in the package menu_order_interfaces.
typedef struct menu_order_interfaces__action__Serve_Goal
{
  /// 이동할 테이블 ID
  rosidl_runtime_c__String table_id;
  /// 테이블의 X 좌표
  double x;
  /// 테이블의 Y 좌표
  double y;
} menu_order_interfaces__action__Serve_Goal;

// Struct for a sequence of menu_order_interfaces__action__Serve_Goal.
typedef struct menu_order_interfaces__action__Serve_Goal__Sequence
{
  menu_order_interfaces__action__Serve_Goal * data;
  /// The number of valid items in data
  size_t size;
  /// The number of allocated items in data
  size_t capacity;
} menu_order_interfaces__action__Serve_Goal__Sequence;


// Constants defined in the message

// Include directives for member types
// Member 'message'
// already included above
// #include "rosidl_runtime_c/string.h"

/// Struct defined in action/Serve in the package menu_order_interfaces.
typedef struct menu_order_interfaces__action__Serve_Result
{
  /// 도착 여부
  bool reached;
  /// 도착 메시지
  rosidl_runtime_c__String message;
} menu_order_interfaces__action__Serve_Result;

// Struct for a sequence of menu_order_interfaces__action__Serve_Result.
typedef struct menu_order_interfaces__action__Serve_Result__Sequence
{
  menu_order_interfaces__action__Serve_Result * data;
  /// The number of valid items in data
  size_t size;
  /// The number of allocated items in data
  size_t capacity;
} menu_order_interfaces__action__Serve_Result__Sequence;


// Constants defined in the message

// Include directives for member types
// Member 'status'
// already included above
// #include "rosidl_runtime_c/string.h"

/// Struct defined in action/Serve in the package menu_order_interfaces.
typedef struct menu_order_interfaces__action__Serve_Feedback
{
  /// 진행 상황 (0.0 ~ 1.0)
  float progress;
  /// 현재 상태 ("Moving", "Waiting", etc.)
  rosidl_runtime_c__String status;
} menu_order_interfaces__action__Serve_Feedback;

// Struct for a sequence of menu_order_interfaces__action__Serve_Feedback.
typedef struct menu_order_interfaces__action__Serve_Feedback__Sequence
{
  menu_order_interfaces__action__Serve_Feedback * data;
  /// The number of valid items in data
  size_t size;
  /// The number of allocated items in data
  size_t capacity;
} menu_order_interfaces__action__Serve_Feedback__Sequence;


// Constants defined in the message

// Include directives for member types
// Member 'goal_id'
#include "unique_identifier_msgs/msg/detail/uuid__struct.h"
// Member 'goal'
#include "menu_order_interfaces/action/detail/serve__struct.h"

/// Struct defined in action/Serve in the package menu_order_interfaces.
typedef struct menu_order_interfaces__action__Serve_SendGoal_Request
{
  unique_identifier_msgs__msg__UUID goal_id;
  menu_order_interfaces__action__Serve_Goal goal;
} menu_order_interfaces__action__Serve_SendGoal_Request;

// Struct for a sequence of menu_order_interfaces__action__Serve_SendGoal_Request.
typedef struct menu_order_interfaces__action__Serve_SendGoal_Request__Sequence
{
  menu_order_interfaces__action__Serve_SendGoal_Request * data;
  /// The number of valid items in data
  size_t size;
  /// The number of allocated items in data
  size_t capacity;
} menu_order_interfaces__action__Serve_SendGoal_Request__Sequence;


// Constants defined in the message

// Include directives for member types
// Member 'stamp'
#include "builtin_interfaces/msg/detail/time__struct.h"

/// Struct defined in action/Serve in the package menu_order_interfaces.
typedef struct menu_order_interfaces__action__Serve_SendGoal_Response
{
  bool accepted;
  builtin_interfaces__msg__Time stamp;
} menu_order_interfaces__action__Serve_SendGoal_Response;

// Struct for a sequence of menu_order_interfaces__action__Serve_SendGoal_Response.
typedef struct menu_order_interfaces__action__Serve_SendGoal_Response__Sequence
{
  menu_order_interfaces__action__Serve_SendGoal_Response * data;
  /// The number of valid items in data
  size_t size;
  /// The number of allocated items in data
  size_t capacity;
} menu_order_interfaces__action__Serve_SendGoal_Response__Sequence;


// Constants defined in the message

// Include directives for member types
// Member 'goal_id'
// already included above
// #include "unique_identifier_msgs/msg/detail/uuid__struct.h"

/// Struct defined in action/Serve in the package menu_order_interfaces.
typedef struct menu_order_interfaces__action__Serve_GetResult_Request
{
  unique_identifier_msgs__msg__UUID goal_id;
} menu_order_interfaces__action__Serve_GetResult_Request;

// Struct for a sequence of menu_order_interfaces__action__Serve_GetResult_Request.
typedef struct menu_order_interfaces__action__Serve_GetResult_Request__Sequence
{
  menu_order_interfaces__action__Serve_GetResult_Request * data;
  /// The number of valid items in data
  size_t size;
  /// The number of allocated items in data
  size_t capacity;
} menu_order_interfaces__action__Serve_GetResult_Request__Sequence;


// Constants defined in the message

// Include directives for member types
// Member 'result'
// already included above
// #include "menu_order_interfaces/action/detail/serve__struct.h"

/// Struct defined in action/Serve in the package menu_order_interfaces.
typedef struct menu_order_interfaces__action__Serve_GetResult_Response
{
  int8_t status;
  menu_order_interfaces__action__Serve_Result result;
} menu_order_interfaces__action__Serve_GetResult_Response;

// Struct for a sequence of menu_order_interfaces__action__Serve_GetResult_Response.
typedef struct menu_order_interfaces__action__Serve_GetResult_Response__Sequence
{
  menu_order_interfaces__action__Serve_GetResult_Response * data;
  /// The number of valid items in data
  size_t size;
  /// The number of allocated items in data
  size_t capacity;
} menu_order_interfaces__action__Serve_GetResult_Response__Sequence;


// Constants defined in the message

// Include directives for member types
// Member 'goal_id'
// already included above
// #include "unique_identifier_msgs/msg/detail/uuid__struct.h"
// Member 'feedback'
// already included above
// #include "menu_order_interfaces/action/detail/serve__struct.h"

/// Struct defined in action/Serve in the package menu_order_interfaces.
typedef struct menu_order_interfaces__action__Serve_FeedbackMessage
{
  unique_identifier_msgs__msg__UUID goal_id;
  menu_order_interfaces__action__Serve_Feedback feedback;
} menu_order_interfaces__action__Serve_FeedbackMessage;

// Struct for a sequence of menu_order_interfaces__action__Serve_FeedbackMessage.
typedef struct menu_order_interfaces__action__Serve_FeedbackMessage__Sequence
{
  menu_order_interfaces__action__Serve_FeedbackMessage * data;
  /// The number of valid items in data
  size_t size;
  /// The number of allocated items in data
  size_t capacity;
} menu_order_interfaces__action__Serve_FeedbackMessage__Sequence;

#ifdef __cplusplus
}
#endif

#endif  // MENU_ORDER_INTERFACES__ACTION__DETAIL__SERVE__STRUCT_H_
