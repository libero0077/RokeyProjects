// generated from rosidl_generator_cpp/resource/idl__builder.hpp.em
// with input from menu_order_interfaces:action/Serve.idl
// generated code does not contain a copyright notice

#ifndef MENU_ORDER_INTERFACES__ACTION__DETAIL__SERVE__BUILDER_HPP_
#define MENU_ORDER_INTERFACES__ACTION__DETAIL__SERVE__BUILDER_HPP_

#include <algorithm>
#include <utility>

#include "menu_order_interfaces/action/detail/serve__struct.hpp"
#include "rosidl_runtime_cpp/message_initialization.hpp"


namespace menu_order_interfaces
{

namespace action
{

namespace builder
{

class Init_Serve_Goal_y
{
public:
  explicit Init_Serve_Goal_y(::menu_order_interfaces::action::Serve_Goal & msg)
  : msg_(msg)
  {}
  ::menu_order_interfaces::action::Serve_Goal y(::menu_order_interfaces::action::Serve_Goal::_y_type arg)
  {
    msg_.y = std::move(arg);
    return std::move(msg_);
  }

private:
  ::menu_order_interfaces::action::Serve_Goal msg_;
};

class Init_Serve_Goal_x
{
public:
  explicit Init_Serve_Goal_x(::menu_order_interfaces::action::Serve_Goal & msg)
  : msg_(msg)
  {}
  Init_Serve_Goal_y x(::menu_order_interfaces::action::Serve_Goal::_x_type arg)
  {
    msg_.x = std::move(arg);
    return Init_Serve_Goal_y(msg_);
  }

private:
  ::menu_order_interfaces::action::Serve_Goal msg_;
};

class Init_Serve_Goal_table_id
{
public:
  Init_Serve_Goal_table_id()
  : msg_(::rosidl_runtime_cpp::MessageInitialization::SKIP)
  {}
  Init_Serve_Goal_x table_id(::menu_order_interfaces::action::Serve_Goal::_table_id_type arg)
  {
    msg_.table_id = std::move(arg);
    return Init_Serve_Goal_x(msg_);
  }

private:
  ::menu_order_interfaces::action::Serve_Goal msg_;
};

}  // namespace builder

}  // namespace action

template<typename MessageType>
auto build();

template<>
inline
auto build<::menu_order_interfaces::action::Serve_Goal>()
{
  return menu_order_interfaces::action::builder::Init_Serve_Goal_table_id();
}

}  // namespace menu_order_interfaces


namespace menu_order_interfaces
{

namespace action
{

namespace builder
{

class Init_Serve_Result_message
{
public:
  explicit Init_Serve_Result_message(::menu_order_interfaces::action::Serve_Result & msg)
  : msg_(msg)
  {}
  ::menu_order_interfaces::action::Serve_Result message(::menu_order_interfaces::action::Serve_Result::_message_type arg)
  {
    msg_.message = std::move(arg);
    return std::move(msg_);
  }

private:
  ::menu_order_interfaces::action::Serve_Result msg_;
};

class Init_Serve_Result_reached
{
public:
  Init_Serve_Result_reached()
  : msg_(::rosidl_runtime_cpp::MessageInitialization::SKIP)
  {}
  Init_Serve_Result_message reached(::menu_order_interfaces::action::Serve_Result::_reached_type arg)
  {
    msg_.reached = std::move(arg);
    return Init_Serve_Result_message(msg_);
  }

private:
  ::menu_order_interfaces::action::Serve_Result msg_;
};

}  // namespace builder

}  // namespace action

template<typename MessageType>
auto build();

template<>
inline
auto build<::menu_order_interfaces::action::Serve_Result>()
{
  return menu_order_interfaces::action::builder::Init_Serve_Result_reached();
}

}  // namespace menu_order_interfaces


namespace menu_order_interfaces
{

namespace action
{

namespace builder
{

class Init_Serve_Feedback_status
{
public:
  explicit Init_Serve_Feedback_status(::menu_order_interfaces::action::Serve_Feedback & msg)
  : msg_(msg)
  {}
  ::menu_order_interfaces::action::Serve_Feedback status(::menu_order_interfaces::action::Serve_Feedback::_status_type arg)
  {
    msg_.status = std::move(arg);
    return std::move(msg_);
  }

private:
  ::menu_order_interfaces::action::Serve_Feedback msg_;
};

class Init_Serve_Feedback_progress
{
public:
  Init_Serve_Feedback_progress()
  : msg_(::rosidl_runtime_cpp::MessageInitialization::SKIP)
  {}
  Init_Serve_Feedback_status progress(::menu_order_interfaces::action::Serve_Feedback::_progress_type arg)
  {
    msg_.progress = std::move(arg);
    return Init_Serve_Feedback_status(msg_);
  }

private:
  ::menu_order_interfaces::action::Serve_Feedback msg_;
};

}  // namespace builder

}  // namespace action

template<typename MessageType>
auto build();

template<>
inline
auto build<::menu_order_interfaces::action::Serve_Feedback>()
{
  return menu_order_interfaces::action::builder::Init_Serve_Feedback_progress();
}

}  // namespace menu_order_interfaces


namespace menu_order_interfaces
{

namespace action
{

namespace builder
{

class Init_Serve_SendGoal_Request_goal
{
public:
  explicit Init_Serve_SendGoal_Request_goal(::menu_order_interfaces::action::Serve_SendGoal_Request & msg)
  : msg_(msg)
  {}
  ::menu_order_interfaces::action::Serve_SendGoal_Request goal(::menu_order_interfaces::action::Serve_SendGoal_Request::_goal_type arg)
  {
    msg_.goal = std::move(arg);
    return std::move(msg_);
  }

private:
  ::menu_order_interfaces::action::Serve_SendGoal_Request msg_;
};

class Init_Serve_SendGoal_Request_goal_id
{
public:
  Init_Serve_SendGoal_Request_goal_id()
  : msg_(::rosidl_runtime_cpp::MessageInitialization::SKIP)
  {}
  Init_Serve_SendGoal_Request_goal goal_id(::menu_order_interfaces::action::Serve_SendGoal_Request::_goal_id_type arg)
  {
    msg_.goal_id = std::move(arg);
    return Init_Serve_SendGoal_Request_goal(msg_);
  }

private:
  ::menu_order_interfaces::action::Serve_SendGoal_Request msg_;
};

}  // namespace builder

}  // namespace action

template<typename MessageType>
auto build();

template<>
inline
auto build<::menu_order_interfaces::action::Serve_SendGoal_Request>()
{
  return menu_order_interfaces::action::builder::Init_Serve_SendGoal_Request_goal_id();
}

}  // namespace menu_order_interfaces


namespace menu_order_interfaces
{

namespace action
{

namespace builder
{

class Init_Serve_SendGoal_Response_stamp
{
public:
  explicit Init_Serve_SendGoal_Response_stamp(::menu_order_interfaces::action::Serve_SendGoal_Response & msg)
  : msg_(msg)
  {}
  ::menu_order_interfaces::action::Serve_SendGoal_Response stamp(::menu_order_interfaces::action::Serve_SendGoal_Response::_stamp_type arg)
  {
    msg_.stamp = std::move(arg);
    return std::move(msg_);
  }

private:
  ::menu_order_interfaces::action::Serve_SendGoal_Response msg_;
};

class Init_Serve_SendGoal_Response_accepted
{
public:
  Init_Serve_SendGoal_Response_accepted()
  : msg_(::rosidl_runtime_cpp::MessageInitialization::SKIP)
  {}
  Init_Serve_SendGoal_Response_stamp accepted(::menu_order_interfaces::action::Serve_SendGoal_Response::_accepted_type arg)
  {
    msg_.accepted = std::move(arg);
    return Init_Serve_SendGoal_Response_stamp(msg_);
  }

private:
  ::menu_order_interfaces::action::Serve_SendGoal_Response msg_;
};

}  // namespace builder

}  // namespace action

template<typename MessageType>
auto build();

template<>
inline
auto build<::menu_order_interfaces::action::Serve_SendGoal_Response>()
{
  return menu_order_interfaces::action::builder::Init_Serve_SendGoal_Response_accepted();
}

}  // namespace menu_order_interfaces


namespace menu_order_interfaces
{

namespace action
{

namespace builder
{

class Init_Serve_GetResult_Request_goal_id
{
public:
  Init_Serve_GetResult_Request_goal_id()
  : msg_(::rosidl_runtime_cpp::MessageInitialization::SKIP)
  {}
  ::menu_order_interfaces::action::Serve_GetResult_Request goal_id(::menu_order_interfaces::action::Serve_GetResult_Request::_goal_id_type arg)
  {
    msg_.goal_id = std::move(arg);
    return std::move(msg_);
  }

private:
  ::menu_order_interfaces::action::Serve_GetResult_Request msg_;
};

}  // namespace builder

}  // namespace action

template<typename MessageType>
auto build();

template<>
inline
auto build<::menu_order_interfaces::action::Serve_GetResult_Request>()
{
  return menu_order_interfaces::action::builder::Init_Serve_GetResult_Request_goal_id();
}

}  // namespace menu_order_interfaces


namespace menu_order_interfaces
{

namespace action
{

namespace builder
{

class Init_Serve_GetResult_Response_result
{
public:
  explicit Init_Serve_GetResult_Response_result(::menu_order_interfaces::action::Serve_GetResult_Response & msg)
  : msg_(msg)
  {}
  ::menu_order_interfaces::action::Serve_GetResult_Response result(::menu_order_interfaces::action::Serve_GetResult_Response::_result_type arg)
  {
    msg_.result = std::move(arg);
    return std::move(msg_);
  }

private:
  ::menu_order_interfaces::action::Serve_GetResult_Response msg_;
};

class Init_Serve_GetResult_Response_status
{
public:
  Init_Serve_GetResult_Response_status()
  : msg_(::rosidl_runtime_cpp::MessageInitialization::SKIP)
  {}
  Init_Serve_GetResult_Response_result status(::menu_order_interfaces::action::Serve_GetResult_Response::_status_type arg)
  {
    msg_.status = std::move(arg);
    return Init_Serve_GetResult_Response_result(msg_);
  }

private:
  ::menu_order_interfaces::action::Serve_GetResult_Response msg_;
};

}  // namespace builder

}  // namespace action

template<typename MessageType>
auto build();

template<>
inline
auto build<::menu_order_interfaces::action::Serve_GetResult_Response>()
{
  return menu_order_interfaces::action::builder::Init_Serve_GetResult_Response_status();
}

}  // namespace menu_order_interfaces


namespace menu_order_interfaces
{

namespace action
{

namespace builder
{

class Init_Serve_FeedbackMessage_feedback
{
public:
  explicit Init_Serve_FeedbackMessage_feedback(::menu_order_interfaces::action::Serve_FeedbackMessage & msg)
  : msg_(msg)
  {}
  ::menu_order_interfaces::action::Serve_FeedbackMessage feedback(::menu_order_interfaces::action::Serve_FeedbackMessage::_feedback_type arg)
  {
    msg_.feedback = std::move(arg);
    return std::move(msg_);
  }

private:
  ::menu_order_interfaces::action::Serve_FeedbackMessage msg_;
};

class Init_Serve_FeedbackMessage_goal_id
{
public:
  Init_Serve_FeedbackMessage_goal_id()
  : msg_(::rosidl_runtime_cpp::MessageInitialization::SKIP)
  {}
  Init_Serve_FeedbackMessage_feedback goal_id(::menu_order_interfaces::action::Serve_FeedbackMessage::_goal_id_type arg)
  {
    msg_.goal_id = std::move(arg);
    return Init_Serve_FeedbackMessage_feedback(msg_);
  }

private:
  ::menu_order_interfaces::action::Serve_FeedbackMessage msg_;
};

}  // namespace builder

}  // namespace action

template<typename MessageType>
auto build();

template<>
inline
auto build<::menu_order_interfaces::action::Serve_FeedbackMessage>()
{
  return menu_order_interfaces::action::builder::Init_Serve_FeedbackMessage_goal_id();
}

}  // namespace menu_order_interfaces

#endif  // MENU_ORDER_INTERFACES__ACTION__DETAIL__SERVE__BUILDER_HPP_
