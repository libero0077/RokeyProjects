// generated from rosidl_generator_cpp/resource/idl__traits.hpp.em
// with input from boxproject_interfaces:action/TaskAction.idl
// generated code does not contain a copyright notice

#ifndef BOXPROJECT_INTERFACES__ACTION__DETAIL__TASK_ACTION__TRAITS_HPP_
#define BOXPROJECT_INTERFACES__ACTION__DETAIL__TASK_ACTION__TRAITS_HPP_

#include <stdint.h>

#include <sstream>
#include <string>
#include <type_traits>

#include "boxproject_interfaces/action/detail/task_action__struct.hpp"
#include "rosidl_runtime_cpp/traits.hpp"

namespace boxproject_interfaces
{

namespace action
{

inline void to_flow_style_yaml(
  const TaskAction_Goal & msg,
  std::ostream & out)
{
  out << "{";
  // member: task
  {
    out << "task: ";
    rosidl_generator_traits::value_to_yaml(msg.task, out);
  }
  out << "}";
}  // NOLINT(readability/fn_size)

inline void to_block_style_yaml(
  const TaskAction_Goal & msg,
  std::ostream & out, size_t indentation = 0)
{
  // member: task
  {
    if (indentation > 0) {
      out << std::string(indentation, ' ');
    }
    out << "task: ";
    rosidl_generator_traits::value_to_yaml(msg.task, out);
    out << "\n";
  }
}  // NOLINT(readability/fn_size)

inline std::string to_yaml(const TaskAction_Goal & msg, bool use_flow_style = false)
{
  std::ostringstream out;
  if (use_flow_style) {
    to_flow_style_yaml(msg, out);
  } else {
    to_block_style_yaml(msg, out);
  }
  return out.str();
}

}  // namespace action

}  // namespace boxproject_interfaces

namespace rosidl_generator_traits
{

[[deprecated("use boxproject_interfaces::action::to_block_style_yaml() instead")]]
inline void to_yaml(
  const boxproject_interfaces::action::TaskAction_Goal & msg,
  std::ostream & out, size_t indentation = 0)
{
  boxproject_interfaces::action::to_block_style_yaml(msg, out, indentation);
}

[[deprecated("use boxproject_interfaces::action::to_yaml() instead")]]
inline std::string to_yaml(const boxproject_interfaces::action::TaskAction_Goal & msg)
{
  return boxproject_interfaces::action::to_yaml(msg);
}

template<>
inline const char * data_type<boxproject_interfaces::action::TaskAction_Goal>()
{
  return "boxproject_interfaces::action::TaskAction_Goal";
}

template<>
inline const char * name<boxproject_interfaces::action::TaskAction_Goal>()
{
  return "boxproject_interfaces/action/TaskAction_Goal";
}

template<>
struct has_fixed_size<boxproject_interfaces::action::TaskAction_Goal>
  : std::integral_constant<bool, false> {};

template<>
struct has_bounded_size<boxproject_interfaces::action::TaskAction_Goal>
  : std::integral_constant<bool, false> {};

template<>
struct is_message<boxproject_interfaces::action::TaskAction_Goal>
  : std::true_type {};

}  // namespace rosidl_generator_traits

namespace boxproject_interfaces
{

namespace action
{

inline void to_flow_style_yaml(
  const TaskAction_Result & msg,
  std::ostream & out)
{
  out << "{";
  // member: status
  {
    out << "status: ";
    rosidl_generator_traits::value_to_yaml(msg.status, out);
  }
  out << "}";
}  // NOLINT(readability/fn_size)

inline void to_block_style_yaml(
  const TaskAction_Result & msg,
  std::ostream & out, size_t indentation = 0)
{
  // member: status
  {
    if (indentation > 0) {
      out << std::string(indentation, ' ');
    }
    out << "status: ";
    rosidl_generator_traits::value_to_yaml(msg.status, out);
    out << "\n";
  }
}  // NOLINT(readability/fn_size)

inline std::string to_yaml(const TaskAction_Result & msg, bool use_flow_style = false)
{
  std::ostringstream out;
  if (use_flow_style) {
    to_flow_style_yaml(msg, out);
  } else {
    to_block_style_yaml(msg, out);
  }
  return out.str();
}

}  // namespace action

}  // namespace boxproject_interfaces

namespace rosidl_generator_traits
{

[[deprecated("use boxproject_interfaces::action::to_block_style_yaml() instead")]]
inline void to_yaml(
  const boxproject_interfaces::action::TaskAction_Result & msg,
  std::ostream & out, size_t indentation = 0)
{
  boxproject_interfaces::action::to_block_style_yaml(msg, out, indentation);
}

[[deprecated("use boxproject_interfaces::action::to_yaml() instead")]]
inline std::string to_yaml(const boxproject_interfaces::action::TaskAction_Result & msg)
{
  return boxproject_interfaces::action::to_yaml(msg);
}

template<>
inline const char * data_type<boxproject_interfaces::action::TaskAction_Result>()
{
  return "boxproject_interfaces::action::TaskAction_Result";
}

template<>
inline const char * name<boxproject_interfaces::action::TaskAction_Result>()
{
  return "boxproject_interfaces/action/TaskAction_Result";
}

template<>
struct has_fixed_size<boxproject_interfaces::action::TaskAction_Result>
  : std::integral_constant<bool, false> {};

template<>
struct has_bounded_size<boxproject_interfaces::action::TaskAction_Result>
  : std::integral_constant<bool, false> {};

template<>
struct is_message<boxproject_interfaces::action::TaskAction_Result>
  : std::true_type {};

}  // namespace rosidl_generator_traits

namespace boxproject_interfaces
{

namespace action
{

inline void to_flow_style_yaml(
  const TaskAction_Feedback & msg,
  std::ostream & out)
{
  out << "{";
  // member: result
  {
    out << "result: ";
    rosidl_generator_traits::value_to_yaml(msg.result, out);
  }
  out << "}";
}  // NOLINT(readability/fn_size)

inline void to_block_style_yaml(
  const TaskAction_Feedback & msg,
  std::ostream & out, size_t indentation = 0)
{
  // member: result
  {
    if (indentation > 0) {
      out << std::string(indentation, ' ');
    }
    out << "result: ";
    rosidl_generator_traits::value_to_yaml(msg.result, out);
    out << "\n";
  }
}  // NOLINT(readability/fn_size)

inline std::string to_yaml(const TaskAction_Feedback & msg, bool use_flow_style = false)
{
  std::ostringstream out;
  if (use_flow_style) {
    to_flow_style_yaml(msg, out);
  } else {
    to_block_style_yaml(msg, out);
  }
  return out.str();
}

}  // namespace action

}  // namespace boxproject_interfaces

namespace rosidl_generator_traits
{

[[deprecated("use boxproject_interfaces::action::to_block_style_yaml() instead")]]
inline void to_yaml(
  const boxproject_interfaces::action::TaskAction_Feedback & msg,
  std::ostream & out, size_t indentation = 0)
{
  boxproject_interfaces::action::to_block_style_yaml(msg, out, indentation);
}

[[deprecated("use boxproject_interfaces::action::to_yaml() instead")]]
inline std::string to_yaml(const boxproject_interfaces::action::TaskAction_Feedback & msg)
{
  return boxproject_interfaces::action::to_yaml(msg);
}

template<>
inline const char * data_type<boxproject_interfaces::action::TaskAction_Feedback>()
{
  return "boxproject_interfaces::action::TaskAction_Feedback";
}

template<>
inline const char * name<boxproject_interfaces::action::TaskAction_Feedback>()
{
  return "boxproject_interfaces/action/TaskAction_Feedback";
}

template<>
struct has_fixed_size<boxproject_interfaces::action::TaskAction_Feedback>
  : std::integral_constant<bool, false> {};

template<>
struct has_bounded_size<boxproject_interfaces::action::TaskAction_Feedback>
  : std::integral_constant<bool, false> {};

template<>
struct is_message<boxproject_interfaces::action::TaskAction_Feedback>
  : std::true_type {};

}  // namespace rosidl_generator_traits

// Include directives for member types
// Member 'goal_id'
#include "unique_identifier_msgs/msg/detail/uuid__traits.hpp"
// Member 'goal'
#include "boxproject_interfaces/action/detail/task_action__traits.hpp"

namespace boxproject_interfaces
{

namespace action
{

inline void to_flow_style_yaml(
  const TaskAction_SendGoal_Request & msg,
  std::ostream & out)
{
  out << "{";
  // member: goal_id
  {
    out << "goal_id: ";
    to_flow_style_yaml(msg.goal_id, out);
    out << ", ";
  }

  // member: goal
  {
    out << "goal: ";
    to_flow_style_yaml(msg.goal, out);
  }
  out << "}";
}  // NOLINT(readability/fn_size)

inline void to_block_style_yaml(
  const TaskAction_SendGoal_Request & msg,
  std::ostream & out, size_t indentation = 0)
{
  // member: goal_id
  {
    if (indentation > 0) {
      out << std::string(indentation, ' ');
    }
    out << "goal_id:\n";
    to_block_style_yaml(msg.goal_id, out, indentation + 2);
  }

  // member: goal
  {
    if (indentation > 0) {
      out << std::string(indentation, ' ');
    }
    out << "goal:\n";
    to_block_style_yaml(msg.goal, out, indentation + 2);
  }
}  // NOLINT(readability/fn_size)

inline std::string to_yaml(const TaskAction_SendGoal_Request & msg, bool use_flow_style = false)
{
  std::ostringstream out;
  if (use_flow_style) {
    to_flow_style_yaml(msg, out);
  } else {
    to_block_style_yaml(msg, out);
  }
  return out.str();
}

}  // namespace action

}  // namespace boxproject_interfaces

namespace rosidl_generator_traits
{

[[deprecated("use boxproject_interfaces::action::to_block_style_yaml() instead")]]
inline void to_yaml(
  const boxproject_interfaces::action::TaskAction_SendGoal_Request & msg,
  std::ostream & out, size_t indentation = 0)
{
  boxproject_interfaces::action::to_block_style_yaml(msg, out, indentation);
}

[[deprecated("use boxproject_interfaces::action::to_yaml() instead")]]
inline std::string to_yaml(const boxproject_interfaces::action::TaskAction_SendGoal_Request & msg)
{
  return boxproject_interfaces::action::to_yaml(msg);
}

template<>
inline const char * data_type<boxproject_interfaces::action::TaskAction_SendGoal_Request>()
{
  return "boxproject_interfaces::action::TaskAction_SendGoal_Request";
}

template<>
inline const char * name<boxproject_interfaces::action::TaskAction_SendGoal_Request>()
{
  return "boxproject_interfaces/action/TaskAction_SendGoal_Request";
}

template<>
struct has_fixed_size<boxproject_interfaces::action::TaskAction_SendGoal_Request>
  : std::integral_constant<bool, has_fixed_size<boxproject_interfaces::action::TaskAction_Goal>::value && has_fixed_size<unique_identifier_msgs::msg::UUID>::value> {};

template<>
struct has_bounded_size<boxproject_interfaces::action::TaskAction_SendGoal_Request>
  : std::integral_constant<bool, has_bounded_size<boxproject_interfaces::action::TaskAction_Goal>::value && has_bounded_size<unique_identifier_msgs::msg::UUID>::value> {};

template<>
struct is_message<boxproject_interfaces::action::TaskAction_SendGoal_Request>
  : std::true_type {};

}  // namespace rosidl_generator_traits

// Include directives for member types
// Member 'stamp'
#include "builtin_interfaces/msg/detail/time__traits.hpp"

namespace boxproject_interfaces
{

namespace action
{

inline void to_flow_style_yaml(
  const TaskAction_SendGoal_Response & msg,
  std::ostream & out)
{
  out << "{";
  // member: accepted
  {
    out << "accepted: ";
    rosidl_generator_traits::value_to_yaml(msg.accepted, out);
    out << ", ";
  }

  // member: stamp
  {
    out << "stamp: ";
    to_flow_style_yaml(msg.stamp, out);
  }
  out << "}";
}  // NOLINT(readability/fn_size)

inline void to_block_style_yaml(
  const TaskAction_SendGoal_Response & msg,
  std::ostream & out, size_t indentation = 0)
{
  // member: accepted
  {
    if (indentation > 0) {
      out << std::string(indentation, ' ');
    }
    out << "accepted: ";
    rosidl_generator_traits::value_to_yaml(msg.accepted, out);
    out << "\n";
  }

  // member: stamp
  {
    if (indentation > 0) {
      out << std::string(indentation, ' ');
    }
    out << "stamp:\n";
    to_block_style_yaml(msg.stamp, out, indentation + 2);
  }
}  // NOLINT(readability/fn_size)

inline std::string to_yaml(const TaskAction_SendGoal_Response & msg, bool use_flow_style = false)
{
  std::ostringstream out;
  if (use_flow_style) {
    to_flow_style_yaml(msg, out);
  } else {
    to_block_style_yaml(msg, out);
  }
  return out.str();
}

}  // namespace action

}  // namespace boxproject_interfaces

namespace rosidl_generator_traits
{

[[deprecated("use boxproject_interfaces::action::to_block_style_yaml() instead")]]
inline void to_yaml(
  const boxproject_interfaces::action::TaskAction_SendGoal_Response & msg,
  std::ostream & out, size_t indentation = 0)
{
  boxproject_interfaces::action::to_block_style_yaml(msg, out, indentation);
}

[[deprecated("use boxproject_interfaces::action::to_yaml() instead")]]
inline std::string to_yaml(const boxproject_interfaces::action::TaskAction_SendGoal_Response & msg)
{
  return boxproject_interfaces::action::to_yaml(msg);
}

template<>
inline const char * data_type<boxproject_interfaces::action::TaskAction_SendGoal_Response>()
{
  return "boxproject_interfaces::action::TaskAction_SendGoal_Response";
}

template<>
inline const char * name<boxproject_interfaces::action::TaskAction_SendGoal_Response>()
{
  return "boxproject_interfaces/action/TaskAction_SendGoal_Response";
}

template<>
struct has_fixed_size<boxproject_interfaces::action::TaskAction_SendGoal_Response>
  : std::integral_constant<bool, has_fixed_size<builtin_interfaces::msg::Time>::value> {};

template<>
struct has_bounded_size<boxproject_interfaces::action::TaskAction_SendGoal_Response>
  : std::integral_constant<bool, has_bounded_size<builtin_interfaces::msg::Time>::value> {};

template<>
struct is_message<boxproject_interfaces::action::TaskAction_SendGoal_Response>
  : std::true_type {};

}  // namespace rosidl_generator_traits

namespace rosidl_generator_traits
{

template<>
inline const char * data_type<boxproject_interfaces::action::TaskAction_SendGoal>()
{
  return "boxproject_interfaces::action::TaskAction_SendGoal";
}

template<>
inline const char * name<boxproject_interfaces::action::TaskAction_SendGoal>()
{
  return "boxproject_interfaces/action/TaskAction_SendGoal";
}

template<>
struct has_fixed_size<boxproject_interfaces::action::TaskAction_SendGoal>
  : std::integral_constant<
    bool,
    has_fixed_size<boxproject_interfaces::action::TaskAction_SendGoal_Request>::value &&
    has_fixed_size<boxproject_interfaces::action::TaskAction_SendGoal_Response>::value
  >
{
};

template<>
struct has_bounded_size<boxproject_interfaces::action::TaskAction_SendGoal>
  : std::integral_constant<
    bool,
    has_bounded_size<boxproject_interfaces::action::TaskAction_SendGoal_Request>::value &&
    has_bounded_size<boxproject_interfaces::action::TaskAction_SendGoal_Response>::value
  >
{
};

template<>
struct is_service<boxproject_interfaces::action::TaskAction_SendGoal>
  : std::true_type
{
};

template<>
struct is_service_request<boxproject_interfaces::action::TaskAction_SendGoal_Request>
  : std::true_type
{
};

template<>
struct is_service_response<boxproject_interfaces::action::TaskAction_SendGoal_Response>
  : std::true_type
{
};

}  // namespace rosidl_generator_traits

// Include directives for member types
// Member 'goal_id'
// already included above
// #include "unique_identifier_msgs/msg/detail/uuid__traits.hpp"

namespace boxproject_interfaces
{

namespace action
{

inline void to_flow_style_yaml(
  const TaskAction_GetResult_Request & msg,
  std::ostream & out)
{
  out << "{";
  // member: goal_id
  {
    out << "goal_id: ";
    to_flow_style_yaml(msg.goal_id, out);
  }
  out << "}";
}  // NOLINT(readability/fn_size)

inline void to_block_style_yaml(
  const TaskAction_GetResult_Request & msg,
  std::ostream & out, size_t indentation = 0)
{
  // member: goal_id
  {
    if (indentation > 0) {
      out << std::string(indentation, ' ');
    }
    out << "goal_id:\n";
    to_block_style_yaml(msg.goal_id, out, indentation + 2);
  }
}  // NOLINT(readability/fn_size)

inline std::string to_yaml(const TaskAction_GetResult_Request & msg, bool use_flow_style = false)
{
  std::ostringstream out;
  if (use_flow_style) {
    to_flow_style_yaml(msg, out);
  } else {
    to_block_style_yaml(msg, out);
  }
  return out.str();
}

}  // namespace action

}  // namespace boxproject_interfaces

namespace rosidl_generator_traits
{

[[deprecated("use boxproject_interfaces::action::to_block_style_yaml() instead")]]
inline void to_yaml(
  const boxproject_interfaces::action::TaskAction_GetResult_Request & msg,
  std::ostream & out, size_t indentation = 0)
{
  boxproject_interfaces::action::to_block_style_yaml(msg, out, indentation);
}

[[deprecated("use boxproject_interfaces::action::to_yaml() instead")]]
inline std::string to_yaml(const boxproject_interfaces::action::TaskAction_GetResult_Request & msg)
{
  return boxproject_interfaces::action::to_yaml(msg);
}

template<>
inline const char * data_type<boxproject_interfaces::action::TaskAction_GetResult_Request>()
{
  return "boxproject_interfaces::action::TaskAction_GetResult_Request";
}

template<>
inline const char * name<boxproject_interfaces::action::TaskAction_GetResult_Request>()
{
  return "boxproject_interfaces/action/TaskAction_GetResult_Request";
}

template<>
struct has_fixed_size<boxproject_interfaces::action::TaskAction_GetResult_Request>
  : std::integral_constant<bool, has_fixed_size<unique_identifier_msgs::msg::UUID>::value> {};

template<>
struct has_bounded_size<boxproject_interfaces::action::TaskAction_GetResult_Request>
  : std::integral_constant<bool, has_bounded_size<unique_identifier_msgs::msg::UUID>::value> {};

template<>
struct is_message<boxproject_interfaces::action::TaskAction_GetResult_Request>
  : std::true_type {};

}  // namespace rosidl_generator_traits

// Include directives for member types
// Member 'result'
// already included above
// #include "boxproject_interfaces/action/detail/task_action__traits.hpp"

namespace boxproject_interfaces
{

namespace action
{

inline void to_flow_style_yaml(
  const TaskAction_GetResult_Response & msg,
  std::ostream & out)
{
  out << "{";
  // member: status
  {
    out << "status: ";
    rosidl_generator_traits::value_to_yaml(msg.status, out);
    out << ", ";
  }

  // member: result
  {
    out << "result: ";
    to_flow_style_yaml(msg.result, out);
  }
  out << "}";
}  // NOLINT(readability/fn_size)

inline void to_block_style_yaml(
  const TaskAction_GetResult_Response & msg,
  std::ostream & out, size_t indentation = 0)
{
  // member: status
  {
    if (indentation > 0) {
      out << std::string(indentation, ' ');
    }
    out << "status: ";
    rosidl_generator_traits::value_to_yaml(msg.status, out);
    out << "\n";
  }

  // member: result
  {
    if (indentation > 0) {
      out << std::string(indentation, ' ');
    }
    out << "result:\n";
    to_block_style_yaml(msg.result, out, indentation + 2);
  }
}  // NOLINT(readability/fn_size)

inline std::string to_yaml(const TaskAction_GetResult_Response & msg, bool use_flow_style = false)
{
  std::ostringstream out;
  if (use_flow_style) {
    to_flow_style_yaml(msg, out);
  } else {
    to_block_style_yaml(msg, out);
  }
  return out.str();
}

}  // namespace action

}  // namespace boxproject_interfaces

namespace rosidl_generator_traits
{

[[deprecated("use boxproject_interfaces::action::to_block_style_yaml() instead")]]
inline void to_yaml(
  const boxproject_interfaces::action::TaskAction_GetResult_Response & msg,
  std::ostream & out, size_t indentation = 0)
{
  boxproject_interfaces::action::to_block_style_yaml(msg, out, indentation);
}

[[deprecated("use boxproject_interfaces::action::to_yaml() instead")]]
inline std::string to_yaml(const boxproject_interfaces::action::TaskAction_GetResult_Response & msg)
{
  return boxproject_interfaces::action::to_yaml(msg);
}

template<>
inline const char * data_type<boxproject_interfaces::action::TaskAction_GetResult_Response>()
{
  return "boxproject_interfaces::action::TaskAction_GetResult_Response";
}

template<>
inline const char * name<boxproject_interfaces::action::TaskAction_GetResult_Response>()
{
  return "boxproject_interfaces/action/TaskAction_GetResult_Response";
}

template<>
struct has_fixed_size<boxproject_interfaces::action::TaskAction_GetResult_Response>
  : std::integral_constant<bool, has_fixed_size<boxproject_interfaces::action::TaskAction_Result>::value> {};

template<>
struct has_bounded_size<boxproject_interfaces::action::TaskAction_GetResult_Response>
  : std::integral_constant<bool, has_bounded_size<boxproject_interfaces::action::TaskAction_Result>::value> {};

template<>
struct is_message<boxproject_interfaces::action::TaskAction_GetResult_Response>
  : std::true_type {};

}  // namespace rosidl_generator_traits

namespace rosidl_generator_traits
{

template<>
inline const char * data_type<boxproject_interfaces::action::TaskAction_GetResult>()
{
  return "boxproject_interfaces::action::TaskAction_GetResult";
}

template<>
inline const char * name<boxproject_interfaces::action::TaskAction_GetResult>()
{
  return "boxproject_interfaces/action/TaskAction_GetResult";
}

template<>
struct has_fixed_size<boxproject_interfaces::action::TaskAction_GetResult>
  : std::integral_constant<
    bool,
    has_fixed_size<boxproject_interfaces::action::TaskAction_GetResult_Request>::value &&
    has_fixed_size<boxproject_interfaces::action::TaskAction_GetResult_Response>::value
  >
{
};

template<>
struct has_bounded_size<boxproject_interfaces::action::TaskAction_GetResult>
  : std::integral_constant<
    bool,
    has_bounded_size<boxproject_interfaces::action::TaskAction_GetResult_Request>::value &&
    has_bounded_size<boxproject_interfaces::action::TaskAction_GetResult_Response>::value
  >
{
};

template<>
struct is_service<boxproject_interfaces::action::TaskAction_GetResult>
  : std::true_type
{
};

template<>
struct is_service_request<boxproject_interfaces::action::TaskAction_GetResult_Request>
  : std::true_type
{
};

template<>
struct is_service_response<boxproject_interfaces::action::TaskAction_GetResult_Response>
  : std::true_type
{
};

}  // namespace rosidl_generator_traits

// Include directives for member types
// Member 'goal_id'
// already included above
// #include "unique_identifier_msgs/msg/detail/uuid__traits.hpp"
// Member 'feedback'
// already included above
// #include "boxproject_interfaces/action/detail/task_action__traits.hpp"

namespace boxproject_interfaces
{

namespace action
{

inline void to_flow_style_yaml(
  const TaskAction_FeedbackMessage & msg,
  std::ostream & out)
{
  out << "{";
  // member: goal_id
  {
    out << "goal_id: ";
    to_flow_style_yaml(msg.goal_id, out);
    out << ", ";
  }

  // member: feedback
  {
    out << "feedback: ";
    to_flow_style_yaml(msg.feedback, out);
  }
  out << "}";
}  // NOLINT(readability/fn_size)

inline void to_block_style_yaml(
  const TaskAction_FeedbackMessage & msg,
  std::ostream & out, size_t indentation = 0)
{
  // member: goal_id
  {
    if (indentation > 0) {
      out << std::string(indentation, ' ');
    }
    out << "goal_id:\n";
    to_block_style_yaml(msg.goal_id, out, indentation + 2);
  }

  // member: feedback
  {
    if (indentation > 0) {
      out << std::string(indentation, ' ');
    }
    out << "feedback:\n";
    to_block_style_yaml(msg.feedback, out, indentation + 2);
  }
}  // NOLINT(readability/fn_size)

inline std::string to_yaml(const TaskAction_FeedbackMessage & msg, bool use_flow_style = false)
{
  std::ostringstream out;
  if (use_flow_style) {
    to_flow_style_yaml(msg, out);
  } else {
    to_block_style_yaml(msg, out);
  }
  return out.str();
}

}  // namespace action

}  // namespace boxproject_interfaces

namespace rosidl_generator_traits
{

[[deprecated("use boxproject_interfaces::action::to_block_style_yaml() instead")]]
inline void to_yaml(
  const boxproject_interfaces::action::TaskAction_FeedbackMessage & msg,
  std::ostream & out, size_t indentation = 0)
{
  boxproject_interfaces::action::to_block_style_yaml(msg, out, indentation);
}

[[deprecated("use boxproject_interfaces::action::to_yaml() instead")]]
inline std::string to_yaml(const boxproject_interfaces::action::TaskAction_FeedbackMessage & msg)
{
  return boxproject_interfaces::action::to_yaml(msg);
}

template<>
inline const char * data_type<boxproject_interfaces::action::TaskAction_FeedbackMessage>()
{
  return "boxproject_interfaces::action::TaskAction_FeedbackMessage";
}

template<>
inline const char * name<boxproject_interfaces::action::TaskAction_FeedbackMessage>()
{
  return "boxproject_interfaces/action/TaskAction_FeedbackMessage";
}

template<>
struct has_fixed_size<boxproject_interfaces::action::TaskAction_FeedbackMessage>
  : std::integral_constant<bool, has_fixed_size<boxproject_interfaces::action::TaskAction_Feedback>::value && has_fixed_size<unique_identifier_msgs::msg::UUID>::value> {};

template<>
struct has_bounded_size<boxproject_interfaces::action::TaskAction_FeedbackMessage>
  : std::integral_constant<bool, has_bounded_size<boxproject_interfaces::action::TaskAction_Feedback>::value && has_bounded_size<unique_identifier_msgs::msg::UUID>::value> {};

template<>
struct is_message<boxproject_interfaces::action::TaskAction_FeedbackMessage>
  : std::true_type {};

}  // namespace rosidl_generator_traits


namespace rosidl_generator_traits
{

template<>
struct is_action<boxproject_interfaces::action::TaskAction>
  : std::true_type
{
};

template<>
struct is_action_goal<boxproject_interfaces::action::TaskAction_Goal>
  : std::true_type
{
};

template<>
struct is_action_result<boxproject_interfaces::action::TaskAction_Result>
  : std::true_type
{
};

template<>
struct is_action_feedback<boxproject_interfaces::action::TaskAction_Feedback>
  : std::true_type
{
};

}  // namespace rosidl_generator_traits


#endif  // BOXPROJECT_INTERFACES__ACTION__DETAIL__TASK_ACTION__TRAITS_HPP_
