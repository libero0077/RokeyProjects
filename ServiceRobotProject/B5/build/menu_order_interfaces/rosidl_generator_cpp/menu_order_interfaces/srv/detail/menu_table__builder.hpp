// generated from rosidl_generator_cpp/resource/idl__builder.hpp.em
// with input from menu_order_interfaces:srv/MenuTable.idl
// generated code does not contain a copyright notice

#ifndef MENU_ORDER_INTERFACES__SRV__DETAIL__MENU_TABLE__BUILDER_HPP_
#define MENU_ORDER_INTERFACES__SRV__DETAIL__MENU_TABLE__BUILDER_HPP_

#include <algorithm>
#include <utility>

#include "menu_order_interfaces/srv/detail/menu_table__struct.hpp"
#include "rosidl_runtime_cpp/message_initialization.hpp"


namespace menu_order_interfaces
{

namespace srv
{

namespace builder
{

class Init_MenuTable_Request_request_type
{
public:
  Init_MenuTable_Request_request_type()
  : msg_(::rosidl_runtime_cpp::MessageInitialization::SKIP)
  {}
  ::menu_order_interfaces::srv::MenuTable_Request request_type(::menu_order_interfaces::srv::MenuTable_Request::_request_type_type arg)
  {
    msg_.request_type = std::move(arg);
    return std::move(msg_);
  }

private:
  ::menu_order_interfaces::srv::MenuTable_Request msg_;
};

}  // namespace builder

}  // namespace srv

template<typename MessageType>
auto build();

template<>
inline
auto build<::menu_order_interfaces::srv::MenuTable_Request>()
{
  return menu_order_interfaces::srv::builder::Init_MenuTable_Request_request_type();
}

}  // namespace menu_order_interfaces


namespace menu_order_interfaces
{

namespace srv
{

namespace builder
{

class Init_MenuTable_Response_table_data
{
public:
  Init_MenuTable_Response_table_data()
  : msg_(::rosidl_runtime_cpp::MessageInitialization::SKIP)
  {}
  ::menu_order_interfaces::srv::MenuTable_Response table_data(::menu_order_interfaces::srv::MenuTable_Response::_table_data_type arg)
  {
    msg_.table_data = std::move(arg);
    return std::move(msg_);
  }

private:
  ::menu_order_interfaces::srv::MenuTable_Response msg_;
};

}  // namespace builder

}  // namespace srv

template<typename MessageType>
auto build();

template<>
inline
auto build<::menu_order_interfaces::srv::MenuTable_Response>()
{
  return menu_order_interfaces::srv::builder::Init_MenuTable_Response_table_data();
}

}  // namespace menu_order_interfaces

#endif  // MENU_ORDER_INTERFACES__SRV__DETAIL__MENU_TABLE__BUILDER_HPP_
