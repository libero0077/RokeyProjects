// generated from rosidl_generator_cpp/resource/idl__builder.hpp.em
// with input from menu_order_interfaces:msg/Order.idl
// generated code does not contain a copyright notice

#ifndef MENU_ORDER_INTERFACES__MSG__DETAIL__ORDER__BUILDER_HPP_
#define MENU_ORDER_INTERFACES__MSG__DETAIL__ORDER__BUILDER_HPP_

#include <algorithm>
#include <utility>

#include "menu_order_interfaces/msg/detail/order__struct.hpp"
#include "rosidl_runtime_cpp/message_initialization.hpp"


namespace menu_order_interfaces
{

namespace msg
{

namespace builder
{

class Init_Order_quantity
{
public:
  explicit Init_Order_quantity(::menu_order_interfaces::msg::Order & msg)
  : msg_(msg)
  {}
  ::menu_order_interfaces::msg::Order quantity(::menu_order_interfaces::msg::Order::_quantity_type arg)
  {
    msg_.quantity = std::move(arg);
    return std::move(msg_);
  }

private:
  ::menu_order_interfaces::msg::Order msg_;
};

class Init_Order_menu
{
public:
  explicit Init_Order_menu(::menu_order_interfaces::msg::Order & msg)
  : msg_(msg)
  {}
  Init_Order_quantity menu(::menu_order_interfaces::msg::Order::_menu_type arg)
  {
    msg_.menu = std::move(arg);
    return Init_Order_quantity(msg_);
  }

private:
  ::menu_order_interfaces::msg::Order msg_;
};

class Init_Order_table_id
{
public:
  Init_Order_table_id()
  : msg_(::rosidl_runtime_cpp::MessageInitialization::SKIP)
  {}
  Init_Order_menu table_id(::menu_order_interfaces::msg::Order::_table_id_type arg)
  {
    msg_.table_id = std::move(arg);
    return Init_Order_menu(msg_);
  }

private:
  ::menu_order_interfaces::msg::Order msg_;
};

}  // namespace builder

}  // namespace msg

template<typename MessageType>
auto build();

template<>
inline
auto build<::menu_order_interfaces::msg::Order>()
{
  return menu_order_interfaces::msg::builder::Init_Order_table_id();
}

}  // namespace menu_order_interfaces

#endif  // MENU_ORDER_INTERFACES__MSG__DETAIL__ORDER__BUILDER_HPP_
