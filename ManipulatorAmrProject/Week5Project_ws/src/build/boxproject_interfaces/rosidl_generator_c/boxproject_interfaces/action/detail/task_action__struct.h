// generated from rosidl_generator_c/resource/idl__struct.h.em
// with input from boxproject_interfaces:action/TaskAction.idl
// generated code does not contain a copyright notice

#ifndef BOXPROJECT_INTERFACES__ACTION__DETAIL__TASK_ACTION__STRUCT_H_
#define BOXPROJECT_INTERFACES__ACTION__DETAIL__TASK_ACTION__STRUCT_H_

#ifdef __cplusplus
extern "C"
{
#endif

#include <stdbool.h>
#include <stddef.h>
#include <stdint.h>


// Constants defined in the message

// Include directives for member types
// Member 'task'
#include "rosidl_runtime_c/string.h"

/// Struct defined in action/TaskAction in the package boxproject_interfaces.
typedef struct boxproject_interfaces__action__TaskAction_Goal
{
  rosidl_runtime_c__String task;
} boxproject_interfaces__action__TaskAction_Goal;

// Struct for a sequence of boxproject_interfaces__action__TaskAction_Goal.
typedef struct boxproject_interfaces__action__TaskAction_Goal__Sequence
{
  boxproject_interfaces__action__TaskAction_Goal * data;
  /// The number of valid items in data
  size_t size;
  /// The number of allocated items in data
  size_t capacity;
} boxproject_interfaces__action__TaskAction_Goal__Sequence;


// Constants defined in the message

// Include directives for member types
// Member 'status'
// already included above
// #include "rosidl_runtime_c/string.h"

/// Struct defined in action/TaskAction in the package boxproject_interfaces.
typedef struct boxproject_interfaces__action__TaskAction_Result
{
  rosidl_runtime_c__String status;
} boxproject_interfaces__action__TaskAction_Result;

// Struct for a sequence of boxproject_interfaces__action__TaskAction_Result.
typedef struct boxproject_interfaces__action__TaskAction_Result__Sequence
{
  boxproject_interfaces__action__TaskAction_Result * data;
  /// The number of valid items in data
  size_t size;
  /// The number of allocated items in data
  size_t capacity;
} boxproject_interfaces__action__TaskAction_Result__Sequence;


// Constants defined in the message

// Include directives for member types
// Member 'result'
// already included above
// #include "rosidl_runtime_c/string.h"

/// Struct defined in action/TaskAction in the package boxproject_interfaces.
typedef struct boxproject_interfaces__action__TaskAction_Feedback
{
  rosidl_runtime_c__String result;
} boxproject_interfaces__action__TaskAction_Feedback;

// Struct for a sequence of boxproject_interfaces__action__TaskAction_Feedback.
typedef struct boxproject_interfaces__action__TaskAction_Feedback__Sequence
{
  boxproject_interfaces__action__TaskAction_Feedback * data;
  /// The number of valid items in data
  size_t size;
  /// The number of allocated items in data
  size_t capacity;
} boxproject_interfaces__action__TaskAction_Feedback__Sequence;


// Constants defined in the message

// Include directives for member types
// Member 'goal_id'
#include "unique_identifier_msgs/msg/detail/uuid__struct.h"
// Member 'goal'
#include "boxproject_interfaces/action/detail/task_action__struct.h"

/// Struct defined in action/TaskAction in the package boxproject_interfaces.
typedef struct boxproject_interfaces__action__TaskAction_SendGoal_Request
{
  unique_identifier_msgs__msg__UUID goal_id;
  boxproject_interfaces__action__TaskAction_Goal goal;
} boxproject_interfaces__action__TaskAction_SendGoal_Request;

// Struct for a sequence of boxproject_interfaces__action__TaskAction_SendGoal_Request.
typedef struct boxproject_interfaces__action__TaskAction_SendGoal_Request__Sequence
{
  boxproject_interfaces__action__TaskAction_SendGoal_Request * data;
  /// The number of valid items in data
  size_t size;
  /// The number of allocated items in data
  size_t capacity;
} boxproject_interfaces__action__TaskAction_SendGoal_Request__Sequence;


// Constants defined in the message

// Include directives for member types
// Member 'stamp'
#include "builtin_interfaces/msg/detail/time__struct.h"

/// Struct defined in action/TaskAction in the package boxproject_interfaces.
typedef struct boxproject_interfaces__action__TaskAction_SendGoal_Response
{
  bool accepted;
  builtin_interfaces__msg__Time stamp;
} boxproject_interfaces__action__TaskAction_SendGoal_Response;

// Struct for a sequence of boxproject_interfaces__action__TaskAction_SendGoal_Response.
typedef struct boxproject_interfaces__action__TaskAction_SendGoal_Response__Sequence
{
  boxproject_interfaces__action__TaskAction_SendGoal_Response * data;
  /// The number of valid items in data
  size_t size;
  /// The number of allocated items in data
  size_t capacity;
} boxproject_interfaces__action__TaskAction_SendGoal_Response__Sequence;


// Constants defined in the message

// Include directives for member types
// Member 'goal_id'
// already included above
// #include "unique_identifier_msgs/msg/detail/uuid__struct.h"

/// Struct defined in action/TaskAction in the package boxproject_interfaces.
typedef struct boxproject_interfaces__action__TaskAction_GetResult_Request
{
  unique_identifier_msgs__msg__UUID goal_id;
} boxproject_interfaces__action__TaskAction_GetResult_Request;

// Struct for a sequence of boxproject_interfaces__action__TaskAction_GetResult_Request.
typedef struct boxproject_interfaces__action__TaskAction_GetResult_Request__Sequence
{
  boxproject_interfaces__action__TaskAction_GetResult_Request * data;
  /// The number of valid items in data
  size_t size;
  /// The number of allocated items in data
  size_t capacity;
} boxproject_interfaces__action__TaskAction_GetResult_Request__Sequence;


// Constants defined in the message

// Include directives for member types
// Member 'result'
// already included above
// #include "boxproject_interfaces/action/detail/task_action__struct.h"

/// Struct defined in action/TaskAction in the package boxproject_interfaces.
typedef struct boxproject_interfaces__action__TaskAction_GetResult_Response
{
  int8_t status;
  boxproject_interfaces__action__TaskAction_Result result;
} boxproject_interfaces__action__TaskAction_GetResult_Response;

// Struct for a sequence of boxproject_interfaces__action__TaskAction_GetResult_Response.
typedef struct boxproject_interfaces__action__TaskAction_GetResult_Response__Sequence
{
  boxproject_interfaces__action__TaskAction_GetResult_Response * data;
  /// The number of valid items in data
  size_t size;
  /// The number of allocated items in data
  size_t capacity;
} boxproject_interfaces__action__TaskAction_GetResult_Response__Sequence;


// Constants defined in the message

// Include directives for member types
// Member 'goal_id'
// already included above
// #include "unique_identifier_msgs/msg/detail/uuid__struct.h"
// Member 'feedback'
// already included above
// #include "boxproject_interfaces/action/detail/task_action__struct.h"

/// Struct defined in action/TaskAction in the package boxproject_interfaces.
typedef struct boxproject_interfaces__action__TaskAction_FeedbackMessage
{
  unique_identifier_msgs__msg__UUID goal_id;
  boxproject_interfaces__action__TaskAction_Feedback feedback;
} boxproject_interfaces__action__TaskAction_FeedbackMessage;

// Struct for a sequence of boxproject_interfaces__action__TaskAction_FeedbackMessage.
typedef struct boxproject_interfaces__action__TaskAction_FeedbackMessage__Sequence
{
  boxproject_interfaces__action__TaskAction_FeedbackMessage * data;
  /// The number of valid items in data
  size_t size;
  /// The number of allocated items in data
  size_t capacity;
} boxproject_interfaces__action__TaskAction_FeedbackMessage__Sequence;

#ifdef __cplusplus
}
#endif

#endif  // BOXPROJECT_INTERFACES__ACTION__DETAIL__TASK_ACTION__STRUCT_H_
