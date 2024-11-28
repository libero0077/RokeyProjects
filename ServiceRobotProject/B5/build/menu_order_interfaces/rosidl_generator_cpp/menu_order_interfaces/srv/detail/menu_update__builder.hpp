// generated from rosidl_generator_cpp/resource/idl__builder.hpp.em
// with input from menu_order_interfaces:srv/MenuUpdate.idl
// generated code does not contain a copyright notice

#ifndef MENU_ORDER_INTERFACES__SRV__DETAIL__MENU_UPDATE__BUILDER_HPP_
#define MENU_ORDER_INTERFACES__SRV__DETAIL__MENU_UPDATE__BUILDER_HPP_

#include <algorithm>
#include <utility>

#include "menu_order_interfaces/srv/detail/menu_update__struct.hpp"
#include "rosidl_runtime_cpp/message_initialization.hpp"


namespace menu_order_interfaces
{

namespace srv
{

namespace builder
{

class Init_MenuUpdate_Request_result_message
{
public:
  Init_MenuUpdate_Request_result_message()
  : msg_(::rosidl_runtime_cpp::MessageInitialization::SKIP)
  {}
  ::menu_order_interfaces::srv::MenuUpdate_Request result_message(::menu_order_interfaces::srv::MenuUpdate_Request::_result_message_type arg)
  {
    msg_.result_message = std::move(arg);
    return std::move(msg_);
  }

private:
  ::menu_order_interfaces::srv::MenuUpdate_Request msg_;
};

}  // namespace builder

}  // namespace srv

template<typename MessageType>
auto build();

template<>
inline
auto build<::menu_order_interfaces::srv::MenuUpdate_Request>()
{
  return menu_order_interfaces::srv::builder::Init_MenuUpdate_Request_result_message();
}

}  // namespace menu_order_interfaces


namespace menu_order_interfaces
{

namespace srv
{

namespace builder
{

class Init_MenuUpdate_Response_success
{
public:
  Init_MenuUpdate_Response_success()
  : msg_(::rosidl_runtime_cpp::MessageInitialization::SKIP)
  {}
  ::menu_order_interfaces::srv::MenuUpdate_Response success(::menu_order_interfaces::srv::MenuUpdate_Response::_success_type arg)
  {
    msg_.success = std::move(arg);
    return std::move(msg_);
  }

private:
  ::menu_order_interfaces::srv::MenuUpdate_Response msg_;
};

}  // namespace builder

}  // namespace srv

template<typename MessageType>
auto build();

template<>
inline
auto build<::menu_order_interfaces::srv::MenuUpdate_Response>()
{
  return menu_order_interfaces::srv::builder::Init_MenuUpdate_Response_success();
}

}  // namespace menu_order_interfaces

#endif  // MENU_ORDER_INTERFACES__SRV__DETAIL__MENU_UPDATE__BUILDER_HPP_
