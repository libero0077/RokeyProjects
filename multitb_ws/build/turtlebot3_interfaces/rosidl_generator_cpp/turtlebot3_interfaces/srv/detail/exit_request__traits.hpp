// generated from rosidl_generator_cpp/resource/idl__traits.hpp.em
// with input from turtlebot3_interfaces:srv/ExitRequest.idl
// generated code does not contain a copyright notice

#ifndef TURTLEBOT3_INTERFACES__SRV__DETAIL__EXIT_REQUEST__TRAITS_HPP_
#define TURTLEBOT3_INTERFACES__SRV__DETAIL__EXIT_REQUEST__TRAITS_HPP_

#include <stdint.h>

#include <sstream>
#include <string>
#include <type_traits>

#include "turtlebot3_interfaces/srv/detail/exit_request__struct.hpp"
#include "rosidl_runtime_cpp/traits.hpp"

namespace turtlebot3_interfaces
{

namespace srv
{

inline void to_flow_style_yaml(
  const ExitRequest_Request & msg,
  std::ostream & out)
{
  out << "{";
  // member: car_number
  {
    out << "car_number: ";
    rosidl_generator_traits::value_to_yaml(msg.car_number, out);
  }
  out << "}";
}  // NOLINT(readability/fn_size)

inline void to_block_style_yaml(
  const ExitRequest_Request & msg,
  std::ostream & out, size_t indentation = 0)
{
  // member: car_number
  {
    if (indentation > 0) {
      out << std::string(indentation, ' ');
    }
    out << "car_number: ";
    rosidl_generator_traits::value_to_yaml(msg.car_number, out);
    out << "\n";
  }
}  // NOLINT(readability/fn_size)

inline std::string to_yaml(const ExitRequest_Request & msg, bool use_flow_style = false)
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
  const turtlebot3_interfaces::srv::ExitRequest_Request & msg,
  std::ostream & out, size_t indentation = 0)
{
  turtlebot3_interfaces::srv::to_block_style_yaml(msg, out, indentation);
}

[[deprecated("use turtlebot3_interfaces::srv::to_yaml() instead")]]
inline std::string to_yaml(const turtlebot3_interfaces::srv::ExitRequest_Request & msg)
{
  return turtlebot3_interfaces::srv::to_yaml(msg);
}

template<>
inline const char * data_type<turtlebot3_interfaces::srv::ExitRequest_Request>()
{
  return "turtlebot3_interfaces::srv::ExitRequest_Request";
}

template<>
inline const char * name<turtlebot3_interfaces::srv::ExitRequest_Request>()
{
  return "turtlebot3_interfaces/srv/ExitRequest_Request";
}

template<>
struct has_fixed_size<turtlebot3_interfaces::srv::ExitRequest_Request>
  : std::integral_constant<bool, false> {};

template<>
struct has_bounded_size<turtlebot3_interfaces::srv::ExitRequest_Request>
  : std::integral_constant<bool, false> {};

template<>
struct is_message<turtlebot3_interfaces::srv::ExitRequest_Request>
  : std::true_type {};

}  // namespace rosidl_generator_traits

namespace turtlebot3_interfaces
{

namespace srv
{

inline void to_flow_style_yaml(
  const ExitRequest_Response & msg,
  std::ostream & out)
{
  out << "{";
  // member: status
  {
    out << "status: ";
    rosidl_generator_traits::value_to_yaml(msg.status, out);
    out << ", ";
  }

  // member: entry_time
  {
    out << "entry_time: ";
    rosidl_generator_traits::value_to_yaml(msg.entry_time, out);
    out << ", ";
  }

  // member: fee
  {
    out << "fee: ";
    rosidl_generator_traits::value_to_yaml(msg.fee, out);
    out << ", ";
  }

  // member: log
  {
    out << "log: ";
    rosidl_generator_traits::value_to_yaml(msg.log, out);
  }
  out << "}";
}  // NOLINT(readability/fn_size)

inline void to_block_style_yaml(
  const ExitRequest_Response & msg,
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

  // member: entry_time
  {
    if (indentation > 0) {
      out << std::string(indentation, ' ');
    }
    out << "entry_time: ";
    rosidl_generator_traits::value_to_yaml(msg.entry_time, out);
    out << "\n";
  }

  // member: fee
  {
    if (indentation > 0) {
      out << std::string(indentation, ' ');
    }
    out << "fee: ";
    rosidl_generator_traits::value_to_yaml(msg.fee, out);
    out << "\n";
  }

  // member: log
  {
    if (indentation > 0) {
      out << std::string(indentation, ' ');
    }
    out << "log: ";
    rosidl_generator_traits::value_to_yaml(msg.log, out);
    out << "\n";
  }
}  // NOLINT(readability/fn_size)

inline std::string to_yaml(const ExitRequest_Response & msg, bool use_flow_style = false)
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
  const turtlebot3_interfaces::srv::ExitRequest_Response & msg,
  std::ostream & out, size_t indentation = 0)
{
  turtlebot3_interfaces::srv::to_block_style_yaml(msg, out, indentation);
}

[[deprecated("use turtlebot3_interfaces::srv::to_yaml() instead")]]
inline std::string to_yaml(const turtlebot3_interfaces::srv::ExitRequest_Response & msg)
{
  return turtlebot3_interfaces::srv::to_yaml(msg);
}

template<>
inline const char * data_type<turtlebot3_interfaces::srv::ExitRequest_Response>()
{
  return "turtlebot3_interfaces::srv::ExitRequest_Response";
}

template<>
inline const char * name<turtlebot3_interfaces::srv::ExitRequest_Response>()
{
  return "turtlebot3_interfaces/srv/ExitRequest_Response";
}

template<>
struct has_fixed_size<turtlebot3_interfaces::srv::ExitRequest_Response>
  : std::integral_constant<bool, false> {};

template<>
struct has_bounded_size<turtlebot3_interfaces::srv::ExitRequest_Response>
  : std::integral_constant<bool, false> {};

template<>
struct is_message<turtlebot3_interfaces::srv::ExitRequest_Response>
  : std::true_type {};

}  // namespace rosidl_generator_traits

namespace rosidl_generator_traits
{

template<>
inline const char * data_type<turtlebot3_interfaces::srv::ExitRequest>()
{
  return "turtlebot3_interfaces::srv::ExitRequest";
}

template<>
inline const char * name<turtlebot3_interfaces::srv::ExitRequest>()
{
  return "turtlebot3_interfaces/srv/ExitRequest";
}

template<>
struct has_fixed_size<turtlebot3_interfaces::srv::ExitRequest>
  : std::integral_constant<
    bool,
    has_fixed_size<turtlebot3_interfaces::srv::ExitRequest_Request>::value &&
    has_fixed_size<turtlebot3_interfaces::srv::ExitRequest_Response>::value
  >
{
};

template<>
struct has_bounded_size<turtlebot3_interfaces::srv::ExitRequest>
  : std::integral_constant<
    bool,
    has_bounded_size<turtlebot3_interfaces::srv::ExitRequest_Request>::value &&
    has_bounded_size<turtlebot3_interfaces::srv::ExitRequest_Response>::value
  >
{
};

template<>
struct is_service<turtlebot3_interfaces::srv::ExitRequest>
  : std::true_type
{
};

template<>
struct is_service_request<turtlebot3_interfaces::srv::ExitRequest_Request>
  : std::true_type
{
};

template<>
struct is_service_response<turtlebot3_interfaces::srv::ExitRequest_Response>
  : std::true_type
{
};

}  // namespace rosidl_generator_traits

#endif  // TURTLEBOT3_INTERFACES__SRV__DETAIL__EXIT_REQUEST__TRAITS_HPP_
