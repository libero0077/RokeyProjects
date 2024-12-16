// generated from rosidl_generator_cpp/resource/idl__builder.hpp.em
// with input from turtlebot3_interfaces:srv/GetSystemState.idl
// generated code does not contain a copyright notice

#ifndef TURTLEBOT3_INTERFACES__SRV__DETAIL__GET_SYSTEM_STATE__BUILDER_HPP_
#define TURTLEBOT3_INTERFACES__SRV__DETAIL__GET_SYSTEM_STATE__BUILDER_HPP_

#include <algorithm>
#include <utility>

#include "turtlebot3_interfaces/srv/detail/get_system_state__struct.hpp"
#include "rosidl_runtime_cpp/message_initialization.hpp"


namespace turtlebot3_interfaces
{

namespace srv
{


}  // namespace srv

template<typename MessageType>
auto build();

template<>
inline
auto build<::turtlebot3_interfaces::srv::GetSystemState_Request>()
{
  return ::turtlebot3_interfaces::srv::GetSystemState_Request(rosidl_runtime_cpp::MessageInitialization::ZERO);
}

}  // namespace turtlebot3_interfaces


namespace turtlebot3_interfaces
{

namespace srv
{

namespace builder
{

class Init_GetSystemState_Response_slot_status_json
{
public:
  explicit Init_GetSystemState_Response_slot_status_json(::turtlebot3_interfaces::srv::GetSystemState_Response & msg)
  : msg_(msg)
  {}
  ::turtlebot3_interfaces::srv::GetSystemState_Response slot_status_json(::turtlebot3_interfaces::srv::GetSystemState_Response::_slot_status_json_type arg)
  {
    msg_.slot_status_json = std::move(arg);
    return std::move(msg_);
  }

private:
  ::turtlebot3_interfaces::srv::GetSystemState_Response msg_;
};

class Init_GetSystemState_Response_robot_status_json
{
public:
  Init_GetSystemState_Response_robot_status_json()
  : msg_(::rosidl_runtime_cpp::MessageInitialization::SKIP)
  {}
  Init_GetSystemState_Response_slot_status_json robot_status_json(::turtlebot3_interfaces::srv::GetSystemState_Response::_robot_status_json_type arg)
  {
    msg_.robot_status_json = std::move(arg);
    return Init_GetSystemState_Response_slot_status_json(msg_);
  }

private:
  ::turtlebot3_interfaces::srv::GetSystemState_Response msg_;
};

}  // namespace builder

}  // namespace srv

template<typename MessageType>
auto build();

template<>
inline
auto build<::turtlebot3_interfaces::srv::GetSystemState_Response>()
{
  return turtlebot3_interfaces::srv::builder::Init_GetSystemState_Response_robot_status_json();
}

}  // namespace turtlebot3_interfaces

#endif  // TURTLEBOT3_INTERFACES__SRV__DETAIL__GET_SYSTEM_STATE__BUILDER_HPP_
