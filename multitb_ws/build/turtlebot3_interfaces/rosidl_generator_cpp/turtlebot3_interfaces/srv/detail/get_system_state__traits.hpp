// generated from rosidl_generator_cpp/resource/idl__traits.hpp.em
// with input from turtlebot3_interfaces:srv/GetSystemState.idl
// generated code does not contain a copyright notice

#ifndef TURTLEBOT3_INTERFACES__SRV__DETAIL__GET_SYSTEM_STATE__TRAITS_HPP_
#define TURTLEBOT3_INTERFACES__SRV__DETAIL__GET_SYSTEM_STATE__TRAITS_HPP_

#include <stdint.h>

#include <sstream>
#include <string>
#include <type_traits>

#include "turtlebot3_interfaces/srv/detail/get_system_state__struct.hpp"
#include "rosidl_runtime_cpp/traits.hpp"

namespace turtlebot3_interfaces
{

namespace srv
{

inline void to_flow_style_yaml(
  const GetSystemState_Request & msg,
  std::ostream & out)
{
  (void)msg;
  out << "null";
}  // NOLINT(readability/fn_size)

inline void to_block_style_yaml(
  const GetSystemState_Request & msg,
  std::ostream & out, size_t indentation = 0)
{
  (void)msg;
  (void)indentation;
  out << "null\n";
}  // NOLINT(readability/fn_size)

inline std::string to_yaml(const GetSystemState_Request & msg, bool use_flow_style = false)
{
  std::ostringstream out;
  if (use_flow_style) {
    to_flow_style_yaml(msg, out);
  } else {
    to_block_style_yaml(msg, out);
  }
  return out.str();
}

}  // namespace srv

}  // namespace turtlebot3_interfaces

namespace rosidl_generator_traits
{

[[deprecated("use turtlebot3_interfaces::srv::to_block_style_yaml() instead")]]
inline void to_yaml(
  const turtlebot3_interfaces::srv::GetSystemState_Request & msg,
  std::ostream & out, size_t indentation = 0)
{
  turtlebot3_interfaces::srv::to_block_style_yaml(msg, out, indentation);
}

[[deprecated("use turtlebot3_interfaces::srv::to_yaml() instead")]]
inline std::string to_yaml(const turtlebot3_interfaces::srv::GetSystemState_Request & msg)
{
  return turtlebot3_interfaces::srv::to_yaml(msg);
}

template<>
inline const char * data_type<turtlebot3_interfaces::srv::GetSystemState_Request>()
{
  return "turtlebot3_interfaces::srv::GetSystemState_Request";
}

template<>
inline const char * name<turtlebot3_interfaces::srv::GetSystemState_Request>()
{
  return "turtlebot3_interfaces/srv/GetSystemState_Request";
}

template<>
struct has_fixed_size<turtlebot3_interfaces::srv::GetSystemState_Request>
  : std::integral_constant<bool, true> {};

template<>
struct has_bounded_size<turtlebot3_interfaces::srv::GetSystemState_Request>
  : std::integral_constant<bool, true> {};

template<>
struct is_message<turtlebot3_interfaces::srv::GetSystemState_Request>
  : std::true_type {};

}  // namespace rosidl_generator_traits

namespace turtlebot3_interfaces
{

namespace srv
{

inline void to_flow_style_yaml(
  const GetSystemState_Response & msg,
  std::ostream & out)
{
  out << "{";
  // member: robot_status_json
  {
    out << "robot_status_json: ";
    rosidl_generator_traits::value_to_yaml(msg.robot_status_json, out);
    out << ", ";
  }

  // member: slot_status_json
  {
    out << "slot_status_json: ";
    rosidl_generator_traits::value_to_yaml(msg.slot_status_json, out);
  }
  out << "}";
}  // NOLINT(readability/fn_size)

inline void to_block_style_yaml(
  const GetSystemState_Response & msg,
  std::ostream & out, size_t indentation = 0)
{
  // member: robot_status_json
  {
    if (indentation > 0) {
      out << std::string(indentation, ' ');
    }
    out << "robot_status_json: ";
    rosidl_generator_traits::value_to_yaml(msg.robot_status_json, out);
    out << "\n";
  }

  // member: slot_status_json
  {
    if (indentation > 0) {
      out << std::string(indentation, ' ');
    }
    out << "slot_status_json: ";
    rosidl_generator_traits::value_to_yaml(msg.slot_status_json, out);
    out << "\n";
  }
}  // NOLINT(readability/fn_size)

inline std::string to_yaml(const GetSystemState_Response & msg, bool use_flow_style = false)
{
  std::ostringstream out;
  if (use_flow_style) {
    to_flow_style_yaml(msg, out);
  } else {
    to_block_style_yaml(msg, out);
  }
  return out.str();
}

}  // namespace srv

}  // namespace turtlebot3_interfaces

namespace rosidl_generator_traits
{

[[deprecated("use turtlebot3_interfaces::srv::to_block_style_yaml() instead")]]
inline void to_yaml(
  const turtlebot3_interfaces::srv::GetSystemState_Response & msg,
  std::ostream & out, size_t indentation = 0)
{
  turtlebot3_interfaces::srv::to_block_style_yaml(msg, out, indentation);
}

[[deprecated("use turtlebot3_interfaces::srv::to_yaml() instead")]]
inline std::string to_yaml(const turtlebot3_interfaces::srv::GetSystemState_Response & msg)
{
  return turtlebot3_interfaces::srv::to_yaml(msg);
}

template<>
inline const char * data_type<turtlebot3_interfaces::srv::GetSystemState_Response>()
{
  return "turtlebot3_interfaces::srv::GetSystemState_Response";
}

template<>
inline const char * name<turtlebot3_interfaces::srv::GetSystemState_Response>()
{
  return "turtlebot3_interfaces/srv/GetSystemState_Response";
}

template<>
struct has_fixed_size<turtlebot3_interfaces::srv::GetSystemState_Response>
  : std::integral_constant<bool, false> {};

template<>
struct has_bounded_size<turtlebot3_interfaces::srv::GetSystemState_Response>
  : std::integral_constant<bool, false> {};

template<>
struct is_message<turtlebot3_interfaces::srv::GetSystemState_Response>
  : std::true_type {};

}  // namespace rosidl_generator_traits

namespace rosidl_generator_traits
{

template<>
inline const char * data_type<turtlebot3_interfaces::srv::GetSystemState>()
{
  return "turtlebot3_interfaces::srv::GetSystemState";
}

template<>
inline const char * name<turtlebot3_interfaces::srv::GetSystemState>()
{
  return "turtlebot3_interfaces/srv/GetSystemState";
}

template<>
struct has_fixed_size<turtlebot3_interfaces::srv::GetSystemState>
  : std::integral_constant<
    bool,
    has_fixed_size<turtlebot3_interfaces::srv::GetSystemState_Request>::value &&
    has_fixed_size<turtlebot3_interfaces::srv::GetSystemState_Response>::value
  >
{
};

template<>
struct has_bounded_size<turtlebot3_interfaces::srv::GetSystemState>
  : std::integral_constant<
    bool,
    has_bounded_size<turtlebot3_interfaces::srv::GetSystemState_Request>::value &&
    has_bounded_size<turtlebot3_interfaces::srv::GetSystemState_Response>::value
  >
{
};

template<>
struct is_service<turtlebot3_interfaces::srv::GetSystemState>
  : std::true_type
{
};

template<>
struct is_service_request<turtlebot3_interfaces::srv::GetSystemState_Request>
  : std::true_type
{
};

template<>
struct is_service_response<turtlebot3_interfaces::srv::GetSystemState_Response>
  : std::true_type
{
};

}  // namespace rosidl_generator_traits

#endif  // TURTLEBOT3_INTERFACES__SRV__DETAIL__GET_SYSTEM_STATE__TRAITS_HPP_
