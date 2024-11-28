// generated from rosidl_generator_cpp/resource/idl__traits.hpp.em
// with input from menu_order_interfaces:msg/Order.idl
// generated code does not contain a copyright notice

#ifndef MENU_ORDER_INTERFACES__MSG__DETAIL__ORDER__TRAITS_HPP_
#define MENU_ORDER_INTERFACES__MSG__DETAIL__ORDER__TRAITS_HPP_

#include <stdint.h>

#include <sstream>
#include <string>
#include <type_traits>

#include "menu_order_interfaces/msg/detail/order__struct.hpp"
#include "rosidl_runtime_cpp/traits.hpp"

namespace menu_order_interfaces
{

namespace msg
{

inline void to_flow_style_yaml(
  const Order & msg,
  std::ostream & out)
{
  out << "{";
  // member: table_id
  {
    out << "table_id: ";
    rosidl_generator_traits::value_to_yaml(msg.table_id, out);
    out << ", ";
  }

  // member: menu
  {
    out << "menu: ";
    rosidl_generator_traits::value_to_yaml(msg.menu, out);
    out << ", ";
  }

  // member: quantity
  {
    out << "quantity: ";
    rosidl_generator_traits::value_to_yaml(msg.quantity, out);
  }
  out << "}";
}  // NOLINT(readability/fn_size)

inline void to_block_style_yaml(
  const Order & msg,
  std::ostream & out, size_t indentation = 0)
{
  // member: table_id
  {
    if (indentation > 0) {
      out << std::string(indentation, ' ');
    }
    out << "table_id: ";
    rosidl_generator_traits::value_to_yaml(msg.table_id, out);
    out << "\n";
  }

  // member: menu
  {
    if (indentation > 0) {
      out << std::string(indentation, ' ');
    }
    out << "menu: ";
    rosidl_generator_traits::value_to_yaml(msg.menu, out);
    out << "\n";
  }

  // member: quantity
  {
    if (indentation > 0) {
      out << std::string(indentation, ' ');
    }
    out << "quantity: ";
    rosidl_generator_traits::value_to_yaml(msg.quantity, out);
    out << "\n";
  }
}  // NOLINT(readability/fn_size)

inline std::string to_yaml(const Order & msg, bool use_flow_style = false)
{
  std::ostringstream out;
  if (use_flow_style) {
    to_flow_style_yaml(msg, out);
  } else {
    to_block_style_yaml(msg, out);
  }
  return out.str();
}

}  // namespace msg

}  // namespace menu_order_interfaces

namespace rosidl_generator_traits
{

[[deprecated("use menu_order_interfaces::msg::to_block_style_yaml() instead")]]
inline void to_yaml(
  const menu_order_interfaces::msg::Order & msg,
  std::ostream & out, size_t indentation = 0)
{
  menu_order_interfaces::msg::to_block_style_yaml(msg, out, indentation);
}

[[deprecated("use menu_order_interfaces::msg::to_yaml() instead")]]
inline std::string to_yaml(const menu_order_interfaces::msg::Order & msg)
{
  return menu_order_interfaces::msg::to_yaml(msg);
}

template<>
inline const char * data_type<menu_order_interfaces::msg::Order>()
{
  return "menu_order_interfaces::msg::Order";
}

template<>
inline const char * name<menu_order_interfaces::msg::Order>()
{
  return "menu_order_interfaces/msg/Order";
}

template<>
struct has_fixed_size<menu_order_interfaces::msg::Order>
  : std::integral_constant<bool, false> {};

template<>
struct has_bounded_size<menu_order_interfaces::msg::Order>
  : std::integral_constant<bool, false> {};

template<>
struct is_message<menu_order_interfaces::msg::Order>
  : std::true_type {};

}  // namespace rosidl_generator_traits

#endif  // MENU_ORDER_INTERFACES__MSG__DETAIL__ORDER__TRAITS_HPP_
