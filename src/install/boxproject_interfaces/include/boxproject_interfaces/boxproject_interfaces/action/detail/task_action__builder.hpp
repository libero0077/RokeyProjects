// generated from rosidl_generator_cpp/resource/idl__builder.hpp.em
// with input from boxproject_interfaces:action/TaskAction.idl
// generated code does not contain a copyright notice

#ifndef BOXPROJECT_INTERFACES__ACTION__DETAIL__TASK_ACTION__BUILDER_HPP_
#define BOXPROJECT_INTERFACES__ACTION__DETAIL__TASK_ACTION__BUILDER_HPP_

#include <algorithm>
#include <utility>

#include "boxproject_interfaces/action/detail/task_action__struct.hpp"
#include "rosidl_runtime_cpp/message_initialization.hpp"


namespace boxproject_interfaces
{

namespace action
{

namespace builder
{

class Init_TaskAction_Goal_task
{
public:
  Init_TaskAction_Goal_task()
  : msg_(::rosidl_runtime_cpp::MessageInitialization::SKIP)
  {}
  ::boxproject_interfaces::action::TaskAction_Goal task(::boxproject_interfaces::action::TaskAction_Goal::_task_type arg)
  {
    msg_.task = std::move(arg);
    return std::move(msg_);
  }

private:
  ::boxproject_interfaces::action::TaskAction_Goal msg_;
};

}  // namespace builder

}  // namespace action

template<typename MessageType>
auto build();

template<>
inline
auto build<::boxproject_interfaces::action::TaskAction_Goal>()
{
  return boxproject_interfaces::action::builder::Init_TaskAction_Goal_task();
}

}  // namespace boxproject_interfaces


namespace boxproject_interfaces
{

namespace action
{

namespace builder
{

class Init_TaskAction_Result_status
{
public:
  Init_TaskAction_Result_status()
  : msg_(::rosidl_runtime_cpp::MessageInitialization::SKIP)
  {}
  ::boxproject_interfaces::action::TaskAction_Result status(::boxproject_interfaces::action::TaskAction_Result::_status_type arg)
  {
    msg_.status = std::move(arg);
    return std::move(msg_);
  }

private:
  ::boxproject_interfaces::action::TaskAction_Result msg_;
};

}  // namespace builder

}  // namespace action

template<typename MessageType>
auto build();

template<>
inline
auto build<::boxproject_interfaces::action::TaskAction_Result>()
{
  return boxproject_interfaces::action::builder::Init_TaskAction_Result_status();
}

}  // namespace boxproject_interfaces


namespace boxproject_interfaces
{

namespace action
{

namespace builder
{

class Init_TaskAction_Feedback_result
{
public:
  Init_TaskAction_Feedback_result()
  : msg_(::rosidl_runtime_cpp::MessageInitialization::SKIP)
  {}
  ::boxproject_interfaces::action::TaskAction_Feedback result(::boxproject_interfaces::action::TaskAction_Feedback::_result_type arg)
  {
    msg_.result = std::move(arg);
    return std::move(msg_);
  }

private:
  ::boxproject_interfaces::action::TaskAction_Feedback msg_;
};

}  // namespace builder

}  // namespace action

template<typename MessageType>
auto build();

template<>
inline
auto build<::boxproject_interfaces::action::TaskAction_Feedback>()
{
  return boxproject_interfaces::action::builder::Init_TaskAction_Feedback_result();
}

}  // namespace boxproject_interfaces


namespace boxproject_interfaces
{

namespace action
{

namespace builder
{

class Init_TaskAction_SendGoal_Request_goal
{
public:
  explicit Init_TaskAction_SendGoal_Request_goal(::boxproject_interfaces::action::TaskAction_SendGoal_Request & msg)
  : msg_(msg)
  {}
  ::boxproject_interfaces::action::TaskAction_SendGoal_Request goal(::boxproject_interfaces::action::TaskAction_SendGoal_Request::_goal_type arg)
  {
    msg_.goal = std::move(arg);
    return std::move(msg_);
  }

private:
  ::boxproject_interfaces::action::TaskAction_SendGoal_Request msg_;
};

class Init_TaskAction_SendGoal_Request_goal_id
{
public:
  Init_TaskAction_SendGoal_Request_goal_id()
  : msg_(::rosidl_runtime_cpp::MessageInitialization::SKIP)
  {}
  Init_TaskAction_SendGoal_Request_goal goal_id(::boxproject_interfaces::action::TaskAction_SendGoal_Request::_goal_id_type arg)
  {
    msg_.goal_id = std::move(arg);
    return Init_TaskAction_SendGoal_Request_goal(msg_);
  }

private:
  ::boxproject_interfaces::action::TaskAction_SendGoal_Request msg_;
};

}  // namespace builder

}  // namespace action

template<typename MessageType>
auto build();

template<>
inline
auto build<::boxproject_interfaces::action::TaskAction_SendGoal_Request>()
{
  return boxproject_interfaces::action::builder::Init_TaskAction_SendGoal_Request_goal_id();
}

}  // namespace boxproject_interfaces


namespace boxproject_interfaces
{

namespace action
{

namespace builder
{

class Init_TaskAction_SendGoal_Response_stamp
{
public:
  explicit Init_TaskAction_SendGoal_Response_stamp(::boxproject_interfaces::action::TaskAction_SendGoal_Response & msg)
  : msg_(msg)
  {}
  ::boxproject_interfaces::action::TaskAction_SendGoal_Response stamp(::boxproject_interfaces::action::TaskAction_SendGoal_Response::_stamp_type arg)
  {
    msg_.stamp = std::move(arg);
    return std::move(msg_);
  }

private:
  ::boxproject_interfaces::action::TaskAction_SendGoal_Response msg_;
};

class Init_TaskAction_SendGoal_Response_accepted
{
public:
  Init_TaskAction_SendGoal_Response_accepted()
  : msg_(::rosidl_runtime_cpp::MessageInitialization::SKIP)
  {}
  Init_TaskAction_SendGoal_Response_stamp accepted(::boxproject_interfaces::action::TaskAction_SendGoal_Response::_accepted_type arg)
  {
    msg_.accepted = std::move(arg);
    return Init_TaskAction_SendGoal_Response_stamp(msg_);
  }

private:
  ::boxproject_interfaces::action::TaskAction_SendGoal_Response msg_;
};

}  // namespace builder

}  // namespace action

template<typename MessageType>
auto build();

template<>
inline
auto build<::boxproject_interfaces::action::TaskAction_SendGoal_Response>()
{
  return boxproject_interfaces::action::builder::Init_TaskAction_SendGoal_Response_accepted();
}

}  // namespace boxproject_interfaces


namespace boxproject_interfaces
{

namespace action
{

namespace builder
{

class Init_TaskAction_GetResult_Request_goal_id
{
public:
  Init_TaskAction_GetResult_Request_goal_id()
  : msg_(::rosidl_runtime_cpp::MessageInitialization::SKIP)
  {}
  ::boxproject_interfaces::action::TaskAction_GetResult_Request goal_id(::boxproject_interfaces::action::TaskAction_GetResult_Request::_goal_id_type arg)
  {
    msg_.goal_id = std::move(arg);
    return std::move(msg_);
  }

private:
  ::boxproject_interfaces::action::TaskAction_GetResult_Request msg_;
};

}  // namespace builder

}  // namespace action

template<typename MessageType>
auto build();

template<>
inline
auto build<::boxproject_interfaces::action::TaskAction_GetResult_Request>()
{
  return boxproject_interfaces::action::builder::Init_TaskAction_GetResult_Request_goal_id();
}

}  // namespace boxproject_interfaces


namespace boxproject_interfaces
{

namespace action
{

namespace builder
{

class Init_TaskAction_GetResult_Response_result
{
public:
  explicit Init_TaskAction_GetResult_Response_result(::boxproject_interfaces::action::TaskAction_GetResult_Response & msg)
  : msg_(msg)
  {}
  ::boxproject_interfaces::action::TaskAction_GetResult_Response result(::boxproject_interfaces::action::TaskAction_GetResult_Response::_result_type arg)
  {
    msg_.result = std::move(arg);
    return std::move(msg_);
  }

private:
  ::boxproject_interfaces::action::TaskAction_GetResult_Response msg_;
};

class Init_TaskAction_GetResult_Response_status
{
public:
  Init_TaskAction_GetResult_Response_status()
  : msg_(::rosidl_runtime_cpp::MessageInitialization::SKIP)
  {}
  Init_TaskAction_GetResult_Response_result status(::boxproject_interfaces::action::TaskAction_GetResult_Response::_status_type arg)
  {
    msg_.status = std::move(arg);
    return Init_TaskAction_GetResult_Response_result(msg_);
  }

private:
  ::boxproject_interfaces::action::TaskAction_GetResult_Response msg_;
};

}  // namespace builder

}  // namespace action

template<typename MessageType>
auto build();

template<>
inline
auto build<::boxproject_interfaces::action::TaskAction_GetResult_Response>()
{
  return boxproject_interfaces::action::builder::Init_TaskAction_GetResult_Response_status();
}

}  // namespace boxproject_interfaces


namespace boxproject_interfaces
{

namespace action
{

namespace builder
{

class Init_TaskAction_FeedbackMessage_feedback
{
public:
  explicit Init_TaskAction_FeedbackMessage_feedback(::boxproject_interfaces::action::TaskAction_FeedbackMessage & msg)
  : msg_(msg)
  {}
  ::boxproject_interfaces::action::TaskAction_FeedbackMessage feedback(::boxproject_interfaces::action::TaskAction_FeedbackMessage::_feedback_type arg)
  {
    msg_.feedback = std::move(arg);
    return std::move(msg_);
  }

private:
  ::boxproject_interfaces::action::TaskAction_FeedbackMessage msg_;
};

class Init_TaskAction_FeedbackMessage_goal_id
{
public:
  Init_TaskAction_FeedbackMessage_goal_id()
  : msg_(::rosidl_runtime_cpp::MessageInitialization::SKIP)
  {}
  Init_TaskAction_FeedbackMessage_feedback goal_id(::boxproject_interfaces::action::TaskAction_FeedbackMessage::_goal_id_type arg)
  {
    msg_.goal_id = std::move(arg);
    return Init_TaskAction_FeedbackMessage_feedback(msg_);
  }

private:
  ::boxproject_interfaces::action::TaskAction_FeedbackMessage msg_;
};

}  // namespace builder

}  // namespace action

template<typename MessageType>
auto build();

template<>
inline
auto build<::boxproject_interfaces::action::TaskAction_FeedbackMessage>()
{
  return boxproject_interfaces::action::builder::Init_TaskAction_FeedbackMessage_goal_id();
}

}  // namespace boxproject_interfaces

#endif  // BOXPROJECT_INTERFACES__ACTION__DETAIL__TASK_ACTION__BUILDER_HPP_
