// generated from rosidl_generator_cpp/resource/idl__traits.hpp.em
// with input from menu_order_interfaces:srv/MenuUpdate.idl
// generated code does not contain a copyright notice

#ifndef MENU_ORDER_INTERFACES__SRV__DETAIL__MENU_UPDATE__TRAITS_HPP_
#define MENU_ORDER_INTERFACES__SRV__DETAIL__MENU_UPDATE__TRAITS_HPP_

#include <stdint.h>

#include <sstream>
#include <string>
#include <type_traits>

#include "menu_order_interfaces/srv/detail/menu_update__struct.hpp"
#include "rosidl_runtime_cpp/traits.hpp"

namespace menu_order_interfaces
{

namespace srv
{

inline void to_flow_style_yaml(
  const MenuUpdate_Request & msg,
  std::ostream & out)
{
  out << "{";
  // member: result_message
  {
    out << "result_message: ";
    rosidl_generator_traits::value_to_yaml(msg.result_message, out);
  }
  out << "}";
}  // NOLINT(readability/fn_size)

inline void to_block_style_yaml(
  const MenuUpdate_Request & msg,
  std::ostream & out, size_t indentation = 0)
{
  // member: result_message
  {
    if (indentation > 0) {
      out << std::string(indentation, ' ');
    }
    out << "result_message: ";
    rosidl_generator_traits::value_to_yaml(msg.result_message, out);
    out << "\n";
  }
}  // NOLINT(readability/fn_size)

inline std::string to_yaml(const MenuUpdate_Request & msg, bool use_flow_style = false)
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

}  // namespace menu_order_interfaces

namespace rosidl_generator_traits
{

[[deprecated("use menu_order_interfaces::srv::to_block_style_yaml() instead")]]
inline void to_yaml(
  const menu_order_interfaces::srv::MenuUpdate_Request & msg,
  std::ostream & out, size_t indentation = 0)
{
  menu_order_interfaces::srv::to_block_style_yaml(msg, out, indentation);
}

[[deprecated("use menu_order_interfaces::srv::to_yaml() instead")]]
inline std::string to_yaml(const menu_order_interfaces::srv::MenuUpdate_Request & msg)
{
  return menu_order_interfaces::srv::to_yaml(msg);
}

template<>
inline const char * data_type<menu_order_interfaces::srv::MenuUpdate_Request>()
{
  return "menu_order_interfaces::srv::MenuUpdate_Request";
}

template<>
inline const char * name<menu_order_interfaces::srv::MenuUpdate_Request>()
{
  return "menu_order_interfaces/srv/MenuUpdate_Request";
}

template<>
struct has_fixed_size<menu_order_interfaces::srv::MenuUpdate_Request>
  : std::integral_constant<bool, false> {};

template<>
struct has_bounded_size<menu_order_interfaces::srv::MenuUpdate_Request>
  : std::integral_constant<bool, false> {};

template<>
struct is_message<menu_order_interfaces::srv::MenuUpdate_Request>
  : std::true_type {};

}  // namespace rosidl_generator_traits

namespace menu_order_interfaces
{

namespace srv
{

inline void to_flow_style_yaml(
  const MenuUpdate_Response & msg,
  std::ostream & out)
{
  out << "{";
  // member: success
  {
    out << "success: ";
    rosidl_generator_traits::value_to_yaml(msg.success, out);
  }
  out << "}";
}  // NOLINT(readability/fn_size)

inline void to_block_style_yaml(
  const MenuUpdate_Response & msg,
  std::ostream & out, size_t indentation = 0)
{
  // member: success
  {
    if (indentation > 0) {
      out << std::string(indentation, ' ');
    }
    out << "success: ";
    rosidl_generator_traits::value_to_yaml(msg.success, out);
    out << "\n";
  }
}  // NOLINT(readability/fn_size)

inline std::string to_yaml(const MenuUpdate_Response & msg, bool use_flow_style = false)
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

}  // namespace menu_order_interfaces

namespace rosidl_generator_traits
{

[[deprecated("use menu_order_interfaces::srv::to_block_style_yaml() instead")]]
inline void to_yaml(
  const menu_order_interfaces::srv::MenuUpdate_Response & msg,
  std::ostream & out, size_t indentation = 0)
{
  menu_order_interfaces::srv::to_block_style_yaml(msg, out, indentation);
}

[[deprecated("use menu_order_interfaces::srv::to_yaml() instead")]]
inline std::string to_yaml(const menu_order_interfaces::srv::MenuUpdate_Response & msg)
{
  return menu_order_interfaces::srv::to_yaml(msg);
}

template<>
inline const char * data_type<menu_order_interfaces::srv::MenuUpdate_Response>()
{
  return "menu_order_interfaces::srv::MenuUpdate_Response";
}

template<>
inline const char * name<menu_order_interfaces::srv::MenuUpdate_Response>()
{
  return "menu_order_interfaces/srv/MenuUpdate_Response";
}

template<>
struct has_fixed_size<menu_order_interfaces::srv::MenuUpdate_Response>
  : std::integral_constant<bool, true> {};

template<>
struct has_bounded_size<menu_order_interfaces::srv::MenuUpdate_Response>
  : std::integral_constant<bool, true> {};

template<>
struct is_message<menu_order_interfaces::srv::MenuUpdate_Response>
  : std::true_type {};

}  // namespace rosidl_generator_traits

namespace rosidl_generator_traits
{

template<>
inline const char * data_type<menu_order_interfaces::srv::MenuUpdate>()
{
  return "menu_order_interfaces::srv::MenuUpdate";
}

template<>
inline const char * name<menu_order_interfaces::srv::MenuUpdate>()
{
  return "menu_order_interfaces/srv/MenuUpdate";
}

template<>
struct has_fixed_size<menu_order_interfaces::srv::MenuUpdate>
  : std::integral_constant<
    bool,
    has_fixed_size<menu_order_interfaces::srv::MenuUpdate_Request>::value &&
    has_fixed_size<menu_order_interfaces::srv::MenuUpdate_Response>::value
  >
{
};

template<>
struct has_bounded_size<menu_order_interfaces::srv::MenuUpdate>
  : std::integral_constant<
    bool,
    has_bounded_size<menu_order_interfaces::srv::MenuUpdate_Request>::value &&
    has_bounded_size<menu_order_interfaces::srv::MenuUpdate_Response>::value
  >
{
};

template<>
struct is_service<menu_order_interfaces::srv::MenuUpdate>
  : std::true_type
{
};

template<>
struct is_service_request<menu_order_interfaces::srv::MenuUpdate_Request>
  : std::true_type
{
};

template<>
struct is_service_response<menu_order_interfaces::srv::MenuUpdate_Response>
  : std::true_type
{
};

}  // namespace rosidl_generator_traits

#endif  // MENU_ORDER_INTERFACES__SRV__DETAIL__MENU_UPDATE__TRAITS_HPP_
