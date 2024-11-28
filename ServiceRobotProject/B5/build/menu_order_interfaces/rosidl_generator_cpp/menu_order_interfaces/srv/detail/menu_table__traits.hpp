// generated from rosidl_generator_cpp/resource/idl__traits.hpp.em
// with input from menu_order_interfaces:srv/MenuTable.idl
// generated code does not contain a copyright notice

#ifndef MENU_ORDER_INTERFACES__SRV__DETAIL__MENU_TABLE__TRAITS_HPP_
#define MENU_ORDER_INTERFACES__SRV__DETAIL__MENU_TABLE__TRAITS_HPP_

#include <stdint.h>

#include <sstream>
#include <string>
#include <type_traits>

#include "menu_order_interfaces/srv/detail/menu_table__struct.hpp"
#include "rosidl_runtime_cpp/traits.hpp"

namespace menu_order_interfaces
{

namespace srv
{

inline void to_flow_style_yaml(
  const MenuTable_Request & msg,
  std::ostream & out)
{
  out << "{";
  // member: request_type
  {
    out << "request_type: ";
    rosidl_generator_traits::value_to_yaml(msg.request_type, out);
  }
  out << "}";
}  // NOLINT(readability/fn_size)

inline void to_block_style_yaml(
  const MenuTable_Request & msg,
  std::ostream & out, size_t indentation = 0)
{
  // member: request_type
  {
    if (indentation > 0) {
      out << std::string(indentation, ' ');
    }
    out << "request_type: ";
    rosidl_generator_traits::value_to_yaml(msg.request_type, out);
    out << "\n";
  }
}  // NOLINT(readability/fn_size)

inline std::string to_yaml(const MenuTable_Request & msg, bool use_flow_style = false)
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
  const menu_order_interfaces::srv::MenuTable_Request & msg,
  std::ostream & out, size_t indentation = 0)
{
  menu_order_interfaces::srv::to_block_style_yaml(msg, out, indentation);
}

[[deprecated("use menu_order_interfaces::srv::to_yaml() instead")]]
inline std::string to_yaml(const menu_order_interfaces::srv::MenuTable_Request & msg)
{
  return menu_order_interfaces::srv::to_yaml(msg);
}

template<>
inline const char * data_type<menu_order_interfaces::srv::MenuTable_Request>()
{
  return "menu_order_interfaces::srv::MenuTable_Request";
}

template<>
inline const char * name<menu_order_interfaces::srv::MenuTable_Request>()
{
  return "menu_order_interfaces/srv/MenuTable_Request";
}

template<>
struct has_fixed_size<menu_order_interfaces::srv::MenuTable_Request>
  : std::integral_constant<bool, false> {};

template<>
struct has_bounded_size<menu_order_interfaces::srv::MenuTable_Request>
  : std::integral_constant<bool, false> {};

template<>
struct is_message<menu_order_interfaces::srv::MenuTable_Request>
  : std::true_type {};

}  // namespace rosidl_generator_traits

namespace menu_order_interfaces
{

namespace srv
{

inline void to_flow_style_yaml(
  const MenuTable_Response & msg,
  std::ostream & out)
{
  out << "{";
  // member: table_data
  {
    if (msg.table_data.size() == 0) {
      out << "table_data: []";
    } else {
      out << "table_data: [";
      size_t pending_items = msg.table_data.size();
      for (auto item : msg.table_data) {
        rosidl_generator_traits::value_to_yaml(item, out);
        if (--pending_items > 0) {
          out << ", ";
        }
      }
      out << "]";
    }
  }
  out << "}";
}  // NOLINT(readability/fn_size)

inline void to_block_style_yaml(
  const MenuTable_Response & msg,
  std::ostream & out, size_t indentation = 0)
{
  // member: table_data
  {
    if (indentation > 0) {
      out << std::string(indentation, ' ');
    }
    if (msg.table_data.size() == 0) {
      out << "table_data: []\n";
    } else {
      out << "table_data:\n";
      for (auto item : msg.table_data) {
        if (indentation > 0) {
          out << std::string(indentation, ' ');
        }
        out << "- ";
        rosidl_generator_traits::value_to_yaml(item, out);
        out << "\n";
      }
    }
  }
}  // NOLINT(readability/fn_size)

inline std::string to_yaml(const MenuTable_Response & msg, bool use_flow_style = false)
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
  const menu_order_interfaces::srv::MenuTable_Response & msg,
  std::ostream & out, size_t indentation = 0)
{
  menu_order_interfaces::srv::to_block_style_yaml(msg, out, indentation);
}

[[deprecated("use menu_order_interfaces::srv::to_yaml() instead")]]
inline std::string to_yaml(const menu_order_interfaces::srv::MenuTable_Response & msg)
{
  return menu_order_interfaces::srv::to_yaml(msg);
}

template<>
inline const char * data_type<menu_order_interfaces::srv::MenuTable_Response>()
{
  return "menu_order_interfaces::srv::MenuTable_Response";
}

template<>
inline const char * name<menu_order_interfaces::srv::MenuTable_Response>()
{
  return "menu_order_interfaces/srv/MenuTable_Response";
}

template<>
struct has_fixed_size<menu_order_interfaces::srv::MenuTable_Response>
  : std::integral_constant<bool, false> {};

template<>
struct has_bounded_size<menu_order_interfaces::srv::MenuTable_Response>
  : std::integral_constant<bool, false> {};

template<>
struct is_message<menu_order_interfaces::srv::MenuTable_Response>
  : std::true_type {};

}  // namespace rosidl_generator_traits

namespace rosidl_generator_traits
{

template<>
inline const char * data_type<menu_order_interfaces::srv::MenuTable>()
{
  return "menu_order_interfaces::srv::MenuTable";
}

template<>
inline const char * name<menu_order_interfaces::srv::MenuTable>()
{
  return "menu_order_interfaces/srv/MenuTable";
}

template<>
struct has_fixed_size<menu_order_interfaces::srv::MenuTable>
  : std::integral_constant<
    bool,
    has_fixed_size<menu_order_interfaces::srv::MenuTable_Request>::value &&
    has_fixed_size<menu_order_interfaces::srv::MenuTable_Response>::value
  >
{
};

template<>
struct has_bounded_size<menu_order_interfaces::srv::MenuTable>
  : std::integral_constant<
    bool,
    has_bounded_size<menu_order_interfaces::srv::MenuTable_Request>::value &&
    has_bounded_size<menu_order_interfaces::srv::MenuTable_Response>::value
  >
{
};

template<>
struct is_service<menu_order_interfaces::srv::MenuTable>
  : std::true_type
{
};

template<>
struct is_service_request<menu_order_interfaces::srv::MenuTable_Request>
  : std::true_type
{
};

template<>
struct is_service_response<menu_order_interfaces::srv::MenuTable_Response>
  : std::true_type
{
};

}  // namespace rosidl_generator_traits

#endif  // MENU_ORDER_INTERFACES__SRV__DETAIL__MENU_TABLE__TRAITS_HPP_
