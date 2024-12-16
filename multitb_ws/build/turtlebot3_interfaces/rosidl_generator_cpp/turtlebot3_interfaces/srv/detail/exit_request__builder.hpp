// generated from rosidl_generator_cpp/resource/idl__builder.hpp.em
// with input from turtlebot3_interfaces:srv/ExitRequest.idl
// generated code does not contain a copyright notice

#ifndef TURTLEBOT3_INTERFACES__SRV__DETAIL__EXIT_REQUEST__BUILDER_HPP_
#define TURTLEBOT3_INTERFACES__SRV__DETAIL__EXIT_REQUEST__BUILDER_HPP_

#include <algorithm>
#include <utility>

#include "turtlebot3_interfaces/srv/detail/exit_request__struct.hpp"
#include "rosidl_runtime_cpp/message_initialization.hpp"


namespace turtlebot3_interfaces
{

namespace srv
{

namespace builder
{

class Init_ExitRequest_Request_car_number
{
public:
  Init_ExitRequest_Request_car_number()
  : msg_(::rosidl_runtime_cpp::MessageInitialization::SKIP)
  {}
  ::turtlebot3_interfaces::srv::ExitRequest_Request car_number(::turtlebot3_interfaces::srv::ExitRequest_Request::_car_number_type arg)
  {
    msg_.car_number = std::move(arg);
    return std::move(msg_);
  }

private:
  ::turtlebot3_interfaces::srv::ExitRequest_Request msg_;
};

}  // namespace builder

}  // namespace srv

template<typename MessageType>
auto build();

template<>
inline
auto build<::turtlebot3_interfaces::srv::ExitRequest_Request>()
{
  return turtlebot3_interfaces::srv::builder::Init_ExitRequest_Request_car_number();
}

}  // namespace turtlebot3_interfaces


namespace turtlebot3_interfaces
{

namespace srv
{

namespace builder
{

class Init_ExitRequest_Response_log
{
public:
  explicit Init_ExitRequest_Response_log(::turtlebot3_interfaces::srv::ExitRequest_Response & msg)
  : msg_(msg)
  {}
  ::turtlebot3_interfaces::srv::ExitRequest_Response log(::turtlebot3_interfaces::srv::ExitRequest_Response::_log_type arg)
  {
    msg_.log = std::move(arg);
    return std::move(msg_);
  }

private:
  ::turtlebot3_interfaces::srv::ExitRequest_Response msg_;
};

class Init_ExitRequest_Response_fee
{
public:
  explicit Init_ExitRequest_Response_fee(::turtlebot3_interfaces::srv::ExitRequest_Response & msg)
  : msg_(msg)
  {}
  Init_ExitRequest_Response_log fee(::turtlebot3_interfaces::srv::ExitRequest_Response::_fee_type arg)
  {
    msg_.fee = std::move(arg);
    return Init_ExitRequest_Response_log(msg_);
  }

private:
  ::turtlebot3_interfaces::srv::ExitRequest_Response msg_;
};

class Init_ExitRequest_Response_entry_time
{
public:
  explicit Init_ExitRequest_Response_entry_time(::turtlebot3_interfaces::srv::ExitRequest_Response & msg)
  : msg_(msg)
  {}
  Init_ExitRequest_Response_fee entry_time(::turtlebot3_interfaces::srv::ExitRequest_Response::_entry_time_type arg)
  {
    msg_.entry_time = std::move(arg);
    return Init_ExitRequest_Response_fee(msg_);
  }

private:
  ::turtlebot3_interfaces::srv::ExitRequest_Response msg_;
};

class Init_ExitRequest_Response_status
{
public:
  Init_ExitRequest_Response_status()
  : msg_(::rosidl_runtime_cpp::MessageInitialization::SKIP)
  {}
  Init_ExitRequest_Response_entry_time status(::turtlebot3_interfaces::srv::ExitRequest_Response::_status_type arg)
  {
    msg_.status = std::move(arg);
    return Init_ExitRequest_Response_entry_time(msg_);
  }

private:
  ::turtlebot3_interfaces::srv::ExitRequest_Response msg_;
};

}  // namespace builder

}  // namespace srv

template<typename MessageType>
auto build();

template<>
inline
auto build<::turtlebot3_interfaces::srv::ExitRequest_Response>()
{
  return turtlebot3_interfaces::srv::builder::Init_ExitRequest_Response_status();
}

}  // namespace turtlebot3_interfaces

#endif  // TURTLEBOT3_INTERFACES__SRV__DETAIL__EXIT_REQUEST__BUILDER_HPP_
