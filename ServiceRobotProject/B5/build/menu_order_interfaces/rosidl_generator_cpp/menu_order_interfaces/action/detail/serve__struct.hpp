// generated from rosidl_generator_cpp/resource/idl__struct.hpp.em
// with input from menu_order_interfaces:action/Serve.idl
// generated code does not contain a copyright notice

#ifndef MENU_ORDER_INTERFACES__ACTION__DETAIL__SERVE__STRUCT_HPP_
#define MENU_ORDER_INTERFACES__ACTION__DETAIL__SERVE__STRUCT_HPP_

#include <algorithm>
#include <array>
#include <memory>
#include <string>
#include <vector>

#include "rosidl_runtime_cpp/bounded_vector.hpp"
#include "rosidl_runtime_cpp/message_initialization.hpp"


#ifndef _WIN32
# define DEPRECATED__menu_order_interfaces__action__Serve_Goal __attribute__((deprecated))
#else
# define DEPRECATED__menu_order_interfaces__action__Serve_Goal __declspec(deprecated)
#endif

namespace menu_order_interfaces
{

namespace action
{

// message struct
template<class ContainerAllocator>
struct Serve_Goal_
{
  using Type = Serve_Goal_<ContainerAllocator>;

  explicit Serve_Goal_(rosidl_runtime_cpp::MessageInitialization _init = rosidl_runtime_cpp::MessageInitialization::ALL)
  {
    if (rosidl_runtime_cpp::MessageInitialization::ALL == _init ||
      rosidl_runtime_cpp::MessageInitialization::ZERO == _init)
    {
      this->table_id = "";
      this->x = 0.0;
      this->y = 0.0;
    }
  }

  explicit Serve_Goal_(const ContainerAllocator & _alloc, rosidl_runtime_cpp::MessageInitialization _init = rosidl_runtime_cpp::MessageInitialization::ALL)
  : table_id(_alloc)
  {
    if (rosidl_runtime_cpp::MessageInitialization::ALL == _init ||
      rosidl_runtime_cpp::MessageInitialization::ZERO == _init)
    {
      this->table_id = "";
      this->x = 0.0;
      this->y = 0.0;
    }
  }

  // field types and members
  using _table_id_type =
    std::basic_string<char, std::char_traits<char>, typename std::allocator_traits<ContainerAllocator>::template rebind_alloc<char>>;
  _table_id_type table_id;
  using _x_type =
    double;
  _x_type x;
  using _y_type =
    double;
  _y_type y;

  // setters for named parameter idiom
  Type & set__table_id(
    const std::basic_string<char, std::char_traits<char>, typename std::allocator_traits<ContainerAllocator>::template rebind_alloc<char>> & _arg)
  {
    this->table_id = _arg;
    return *this;
  }
  Type & set__x(
    const double & _arg)
  {
    this->x = _arg;
    return *this;
  }
  Type & set__y(
    const double & _arg)
  {
    this->y = _arg;
    return *this;
  }

  // constant declarations

  // pointer types
  using RawPtr =
    menu_order_interfaces::action::Serve_Goal_<ContainerAllocator> *;
  using ConstRawPtr =
    const menu_order_interfaces::action::Serve_Goal_<ContainerAllocator> *;
  using SharedPtr =
    std::shared_ptr<menu_order_interfaces::action::Serve_Goal_<ContainerAllocator>>;
  using ConstSharedPtr =
    std::shared_ptr<menu_order_interfaces::action::Serve_Goal_<ContainerAllocator> const>;

  template<typename Deleter = std::default_delete<
      menu_order_interfaces::action::Serve_Goal_<ContainerAllocator>>>
  using UniquePtrWithDeleter =
    std::unique_ptr<menu_order_interfaces::action::Serve_Goal_<ContainerAllocator>, Deleter>;

  using UniquePtr = UniquePtrWithDeleter<>;

  template<typename Deleter = std::default_delete<
      menu_order_interfaces::action::Serve_Goal_<ContainerAllocator>>>
  using ConstUniquePtrWithDeleter =
    std::unique_ptr<menu_order_interfaces::action::Serve_Goal_<ContainerAllocator> const, Deleter>;
  using ConstUniquePtr = ConstUniquePtrWithDeleter<>;

  using WeakPtr =
    std::weak_ptr<menu_order_interfaces::action::Serve_Goal_<ContainerAllocator>>;
  using ConstWeakPtr =
    std::weak_ptr<menu_order_interfaces::action::Serve_Goal_<ContainerAllocator> const>;

  // pointer types similar to ROS 1, use SharedPtr / ConstSharedPtr instead
  // NOTE: Can't use 'using' here because GNU C++ can't parse attributes properly
  typedef DEPRECATED__menu_order_interfaces__action__Serve_Goal
    std::shared_ptr<menu_order_interfaces::action::Serve_Goal_<ContainerAllocator>>
    Ptr;
  typedef DEPRECATED__menu_order_interfaces__action__Serve_Goal
    std::shared_ptr<menu_order_interfaces::action::Serve_Goal_<ContainerAllocator> const>
    ConstPtr;

  // comparison operators
  bool operator==(const Serve_Goal_ & other) const
  {
    if (this->table_id != other.table_id) {
      return false;
    }
    if (this->x != other.x) {
      return false;
    }
    if (this->y != other.y) {
      return false;
    }
    return true;
  }
  bool operator!=(const Serve_Goal_ & other) const
  {
    return !this->operator==(other);
  }
};  // struct Serve_Goal_

// alias to use template instance with default allocator
using Serve_Goal =
  menu_order_interfaces::action::Serve_Goal_<std::allocator<void>>;

// constant definitions

}  // namespace action

}  // namespace menu_order_interfaces


#ifndef _WIN32
# define DEPRECATED__menu_order_interfaces__action__Serve_Result __attribute__((deprecated))
#else
# define DEPRECATED__menu_order_interfaces__action__Serve_Result __declspec(deprecated)
#endif

namespace menu_order_interfaces
{

namespace action
{

// message struct
template<class ContainerAllocator>
struct Serve_Result_
{
  using Type = Serve_Result_<ContainerAllocator>;

  explicit Serve_Result_(rosidl_runtime_cpp::MessageInitialization _init = rosidl_runtime_cpp::MessageInitialization::ALL)
  {
    if (rosidl_runtime_cpp::MessageInitialization::ALL == _init ||
      rosidl_runtime_cpp::MessageInitialization::ZERO == _init)
    {
      this->reached = false;
      this->message = "";
    }
  }

  explicit Serve_Result_(const ContainerAllocator & _alloc, rosidl_runtime_cpp::MessageInitialization _init = rosidl_runtime_cpp::MessageInitialization::ALL)
  : message(_alloc)
  {
    if (rosidl_runtime_cpp::MessageInitialization::ALL == _init ||
      rosidl_runtime_cpp::MessageInitialization::ZERO == _init)
    {
      this->reached = false;
      this->message = "";
    }
  }

  // field types and members
  using _reached_type =
    bool;
  _reached_type reached;
  using _message_type =
    std::basic_string<char, std::char_traits<char>, typename std::allocator_traits<ContainerAllocator>::template rebind_alloc<char>>;
  _message_type message;

  // setters for named parameter idiom
  Type & set__reached(
    const bool & _arg)
  {
    this->reached = _arg;
    return *this;
  }
  Type & set__message(
    const std::basic_string<char, std::char_traits<char>, typename std::allocator_traits<ContainerAllocator>::template rebind_alloc<char>> & _arg)
  {
    this->message = _arg;
    return *this;
  }

  // constant declarations

  // pointer types
  using RawPtr =
    menu_order_interfaces::action::Serve_Result_<ContainerAllocator> *;
  using ConstRawPtr =
    const menu_order_interfaces::action::Serve_Result_<ContainerAllocator> *;
  using SharedPtr =
    std::shared_ptr<menu_order_interfaces::action::Serve_Result_<ContainerAllocator>>;
  using ConstSharedPtr =
    std::shared_ptr<menu_order_interfaces::action::Serve_Result_<ContainerAllocator> const>;

  template<typename Deleter = std::default_delete<
      menu_order_interfaces::action::Serve_Result_<ContainerAllocator>>>
  using UniquePtrWithDeleter =
    std::unique_ptr<menu_order_interfaces::action::Serve_Result_<ContainerAllocator>, Deleter>;

  using UniquePtr = UniquePtrWithDeleter<>;

  template<typename Deleter = std::default_delete<
      menu_order_interfaces::action::Serve_Result_<ContainerAllocator>>>
  using ConstUniquePtrWithDeleter =
    std::unique_ptr<menu_order_interfaces::action::Serve_Result_<ContainerAllocator> const, Deleter>;
  using ConstUniquePtr = ConstUniquePtrWithDeleter<>;

  using WeakPtr =
    std::weak_ptr<menu_order_interfaces::action::Serve_Result_<ContainerAllocator>>;
  using ConstWeakPtr =
    std::weak_ptr<menu_order_interfaces::action::Serve_Result_<ContainerAllocator> const>;

  // pointer types similar to ROS 1, use SharedPtr / ConstSharedPtr instead
  // NOTE: Can't use 'using' here because GNU C++ can't parse attributes properly
  typedef DEPRECATED__menu_order_interfaces__action__Serve_Result
    std::shared_ptr<menu_order_interfaces::action::Serve_Result_<ContainerAllocator>>
    Ptr;
  typedef DEPRECATED__menu_order_interfaces__action__Serve_Result
    std::shared_ptr<menu_order_interfaces::action::Serve_Result_<ContainerAllocator> const>
    ConstPtr;

  // comparison operators
  bool operator==(const Serve_Result_ & other) const
  {
    if (this->reached != other.reached) {
      return false;
    }
    if (this->message != other.message) {
      return false;
    }
    return true;
  }
  bool operator!=(const Serve_Result_ & other) const
  {
    return !this->operator==(other);
  }
};  // struct Serve_Result_

// alias to use template instance with default allocator
using Serve_Result =
  menu_order_interfaces::action::Serve_Result_<std::allocator<void>>;

// constant definitions

}  // namespace action

}  // namespace menu_order_interfaces


#ifndef _WIN32
# define DEPRECATED__menu_order_interfaces__action__Serve_Feedback __attribute__((deprecated))
#else
# define DEPRECATED__menu_order_interfaces__action__Serve_Feedback __declspec(deprecated)
#endif

namespace menu_order_interfaces
{

namespace action
{

// message struct
template<class ContainerAllocator>
struct Serve_Feedback_
{
  using Type = Serve_Feedback_<ContainerAllocator>;

  explicit Serve_Feedback_(rosidl_runtime_cpp::MessageInitialization _init = rosidl_runtime_cpp::MessageInitialization::ALL)
  {
    if (rosidl_runtime_cpp::MessageInitialization::ALL == _init ||
      rosidl_runtime_cpp::MessageInitialization::ZERO == _init)
    {
      this->progress = 0.0f;
      this->status = "";
    }
  }

  explicit Serve_Feedback_(const ContainerAllocator & _alloc, rosidl_runtime_cpp::MessageInitialization _init = rosidl_runtime_cpp::MessageInitialization::ALL)
  : status(_alloc)
  {
    if (rosidl_runtime_cpp::MessageInitialization::ALL == _init ||
      rosidl_runtime_cpp::MessageInitialization::ZERO == _init)
    {
      this->progress = 0.0f;
      this->status = "";
    }
  }

  // field types and members
  using _progress_type =
    float;
  _progress_type progress;
  using _status_type =
    std::basic_string<char, std::char_traits<char>, typename std::allocator_traits<ContainerAllocator>::template rebind_alloc<char>>;
  _status_type status;

  // setters for named parameter idiom
  Type & set__progress(
    const float & _arg)
  {
    this->progress = _arg;
    return *this;
  }
  Type & set__status(
    const std::basic_string<char, std::char_traits<char>, typename std::allocator_traits<ContainerAllocator>::template rebind_alloc<char>> & _arg)
  {
    this->status = _arg;
    return *this;
  }

  // constant declarations

  // pointer types
  using RawPtr =
    menu_order_interfaces::action::Serve_Feedback_<ContainerAllocator> *;
  using ConstRawPtr =
    const menu_order_interfaces::action::Serve_Feedback_<ContainerAllocator> *;
  using SharedPtr =
    std::shared_ptr<menu_order_interfaces::action::Serve_Feedback_<ContainerAllocator>>;
  using ConstSharedPtr =
    std::shared_ptr<menu_order_interfaces::action::Serve_Feedback_<ContainerAllocator> const>;

  template<typename Deleter = std::default_delete<
      menu_order_interfaces::action::Serve_Feedback_<ContainerAllocator>>>
  using UniquePtrWithDeleter =
    std::unique_ptr<menu_order_interfaces::action::Serve_Feedback_<ContainerAllocator>, Deleter>;

  using UniquePtr = UniquePtrWithDeleter<>;

  template<typename Deleter = std::default_delete<
      menu_order_interfaces::action::Serve_Feedback_<ContainerAllocator>>>
  using ConstUniquePtrWithDeleter =
    std::unique_ptr<menu_order_interfaces::action::Serve_Feedback_<ContainerAllocator> const, Deleter>;
  using ConstUniquePtr = ConstUniquePtrWithDeleter<>;

  using WeakPtr =
    std::weak_ptr<menu_order_interfaces::action::Serve_Feedback_<ContainerAllocator>>;
  using ConstWeakPtr =
    std::weak_ptr<menu_order_interfaces::action::Serve_Feedback_<ContainerAllocator> const>;

  // pointer types similar to ROS 1, use SharedPtr / ConstSharedPtr instead
  // NOTE: Can't use 'using' here because GNU C++ can't parse attributes properly
  typedef DEPRECATED__menu_order_interfaces__action__Serve_Feedback
    std::shared_ptr<menu_order_interfaces::action::Serve_Feedback_<ContainerAllocator>>
    Ptr;
  typedef DEPRECATED__menu_order_interfaces__action__Serve_Feedback
    std::shared_ptr<menu_order_interfaces::action::Serve_Feedback_<ContainerAllocator> const>
    ConstPtr;

  // comparison operators
  bool operator==(const Serve_Feedback_ & other) const
  {
    if (this->progress != other.progress) {
      return false;
    }
    if (this->status != other.status) {
      return false;
    }
    return true;
  }
  bool operator!=(const Serve_Feedback_ & other) const
  {
    return !this->operator==(other);
  }
};  // struct Serve_Feedback_

// alias to use template instance with default allocator
using Serve_Feedback =
  menu_order_interfaces::action::Serve_Feedback_<std::allocator<void>>;

// constant definitions

}  // namespace action

}  // namespace menu_order_interfaces


// Include directives for member types
// Member 'goal_id'
#include "unique_identifier_msgs/msg/detail/uuid__struct.hpp"
// Member 'goal'
#include "menu_order_interfaces/action/detail/serve__struct.hpp"

#ifndef _WIN32
# define DEPRECATED__menu_order_interfaces__action__Serve_SendGoal_Request __attribute__((deprecated))
#else
# define DEPRECATED__menu_order_interfaces__action__Serve_SendGoal_Request __declspec(deprecated)
#endif

namespace menu_order_interfaces
{

namespace action
{

// message struct
template<class ContainerAllocator>
struct Serve_SendGoal_Request_
{
  using Type = Serve_SendGoal_Request_<ContainerAllocator>;

  explicit Serve_SendGoal_Request_(rosidl_runtime_cpp::MessageInitialization _init = rosidl_runtime_cpp::MessageInitialization::ALL)
  : goal_id(_init),
    goal(_init)
  {
    (void)_init;
  }

  explicit Serve_SendGoal_Request_(const ContainerAllocator & _alloc, rosidl_runtime_cpp::MessageInitialization _init = rosidl_runtime_cpp::MessageInitialization::ALL)
  : goal_id(_alloc, _init),
    goal(_alloc, _init)
  {
    (void)_init;
  }

  // field types and members
  using _goal_id_type =
    unique_identifier_msgs::msg::UUID_<ContainerAllocator>;
  _goal_id_type goal_id;
  using _goal_type =
    menu_order_interfaces::action::Serve_Goal_<ContainerAllocator>;
  _goal_type goal;

  // setters for named parameter idiom
  Type & set__goal_id(
    const unique_identifier_msgs::msg::UUID_<ContainerAllocator> & _arg)
  {
    this->goal_id = _arg;
    return *this;
  }
  Type & set__goal(
    const menu_order_interfaces::action::Serve_Goal_<ContainerAllocator> & _arg)
  {
    this->goal = _arg;
    return *this;
  }

  // constant declarations

  // pointer types
  using RawPtr =
    menu_order_interfaces::action::Serve_SendGoal_Request_<ContainerAllocator> *;
  using ConstRawPtr =
    const menu_order_interfaces::action::Serve_SendGoal_Request_<ContainerAllocator> *;
  using SharedPtr =
    std::shared_ptr<menu_order_interfaces::action::Serve_SendGoal_Request_<ContainerAllocator>>;
  using ConstSharedPtr =
    std::shared_ptr<menu_order_interfaces::action::Serve_SendGoal_Request_<ContainerAllocator> const>;

  template<typename Deleter = std::default_delete<
      menu_order_interfaces::action::Serve_SendGoal_Request_<ContainerAllocator>>>
  using UniquePtrWithDeleter =
    std::unique_ptr<menu_order_interfaces::action::Serve_SendGoal_Request_<ContainerAllocator>, Deleter>;

  using UniquePtr = UniquePtrWithDeleter<>;

  template<typename Deleter = std::default_delete<
      menu_order_interfaces::action::Serve_SendGoal_Request_<ContainerAllocator>>>
  using ConstUniquePtrWithDeleter =
    std::unique_ptr<menu_order_interfaces::action::Serve_SendGoal_Request_<ContainerAllocator> const, Deleter>;
  using ConstUniquePtr = ConstUniquePtrWithDeleter<>;

  using WeakPtr =
    std::weak_ptr<menu_order_interfaces::action::Serve_SendGoal_Request_<ContainerAllocator>>;
  using ConstWeakPtr =
    std::weak_ptr<menu_order_interfaces::action::Serve_SendGoal_Request_<ContainerAllocator> const>;

  // pointer types similar to ROS 1, use SharedPtr / ConstSharedPtr instead
  // NOTE: Can't use 'using' here because GNU C++ can't parse attributes properly
  typedef DEPRECATED__menu_order_interfaces__action__Serve_SendGoal_Request
    std::shared_ptr<menu_order_interfaces::action::Serve_SendGoal_Request_<ContainerAllocator>>
    Ptr;
  typedef DEPRECATED__menu_order_interfaces__action__Serve_SendGoal_Request
    std::shared_ptr<menu_order_interfaces::action::Serve_SendGoal_Request_<ContainerAllocator> const>
    ConstPtr;

  // comparison operators
  bool operator==(const Serve_SendGoal_Request_ & other) const
  {
    if (this->goal_id != other.goal_id) {
      return false;
    }
    if (this->goal != other.goal) {
      return false;
    }
    return true;
  }
  bool operator!=(const Serve_SendGoal_Request_ & other) const
  {
    return !this->operator==(other);
  }
};  // struct Serve_SendGoal_Request_

// alias to use template instance with default allocator
using Serve_SendGoal_Request =
  menu_order_interfaces::action::Serve_SendGoal_Request_<std::allocator<void>>;

// constant definitions

}  // namespace action

}  // namespace menu_order_interfaces


// Include directives for member types
// Member 'stamp'
#include "builtin_interfaces/msg/detail/time__struct.hpp"

#ifndef _WIN32
# define DEPRECATED__menu_order_interfaces__action__Serve_SendGoal_Response __attribute__((deprecated))
#else
# define DEPRECATED__menu_order_interfaces__action__Serve_SendGoal_Response __declspec(deprecated)
#endif

namespace menu_order_interfaces
{

namespace action
{

// message struct
template<class ContainerAllocator>
struct Serve_SendGoal_Response_
{
  using Type = Serve_SendGoal_Response_<ContainerAllocator>;

  explicit Serve_SendGoal_Response_(rosidl_runtime_cpp::MessageInitialization _init = rosidl_runtime_cpp::MessageInitialization::ALL)
  : stamp(_init)
  {
    if (rosidl_runtime_cpp::MessageInitialization::ALL == _init ||
      rosidl_runtime_cpp::MessageInitialization::ZERO == _init)
    {
      this->accepted = false;
    }
  }

  explicit Serve_SendGoal_Response_(const ContainerAllocator & _alloc, rosidl_runtime_cpp::MessageInitialization _init = rosidl_runtime_cpp::MessageInitialization::ALL)
  : stamp(_alloc, _init)
  {
    if (rosidl_runtime_cpp::MessageInitialization::ALL == _init ||
      rosidl_runtime_cpp::MessageInitialization::ZERO == _init)
    {
      this->accepted = false;
    }
  }

  // field types and members
  using _accepted_type =
    bool;
  _accepted_type accepted;
  using _stamp_type =
    builtin_interfaces::msg::Time_<ContainerAllocator>;
  _stamp_type stamp;

  // setters for named parameter idiom
  Type & set__accepted(
    const bool & _arg)
  {
    this->accepted = _arg;
    return *this;
  }
  Type & set__stamp(
    const builtin_interfaces::msg::Time_<ContainerAllocator> & _arg)
  {
    this->stamp = _arg;
    return *this;
  }

  // constant declarations

  // pointer types
  using RawPtr =
    menu_order_interfaces::action::Serve_SendGoal_Response_<ContainerAllocator> *;
  using ConstRawPtr =
    const menu_order_interfaces::action::Serve_SendGoal_Response_<ContainerAllocator> *;
  using SharedPtr =
    std::shared_ptr<menu_order_interfaces::action::Serve_SendGoal_Response_<ContainerAllocator>>;
  using ConstSharedPtr =
    std::shared_ptr<menu_order_interfaces::action::Serve_SendGoal_Response_<ContainerAllocator> const>;

  template<typename Deleter = std::default_delete<
      menu_order_interfaces::action::Serve_SendGoal_Response_<ContainerAllocator>>>
  using UniquePtrWithDeleter =
    std::unique_ptr<menu_order_interfaces::action::Serve_SendGoal_Response_<ContainerAllocator>, Deleter>;

  using UniquePtr = UniquePtrWithDeleter<>;

  template<typename Deleter = std::default_delete<
      menu_order_interfaces::action::Serve_SendGoal_Response_<ContainerAllocator>>>
  using ConstUniquePtrWithDeleter =
    std::unique_ptr<menu_order_interfaces::action::Serve_SendGoal_Response_<ContainerAllocator> const, Deleter>;
  using ConstUniquePtr = ConstUniquePtrWithDeleter<>;

  using WeakPtr =
    std::weak_ptr<menu_order_interfaces::action::Serve_SendGoal_Response_<ContainerAllocator>>;
  using ConstWeakPtr =
    std::weak_ptr<menu_order_interfaces::action::Serve_SendGoal_Response_<ContainerAllocator> const>;

  // pointer types similar to ROS 1, use SharedPtr / ConstSharedPtr instead
  // NOTE: Can't use 'using' here because GNU C++ can't parse attributes properly
  typedef DEPRECATED__menu_order_interfaces__action__Serve_SendGoal_Response
    std::shared_ptr<menu_order_interfaces::action::Serve_SendGoal_Response_<ContainerAllocator>>
    Ptr;
  typedef DEPRECATED__menu_order_interfaces__action__Serve_SendGoal_Response
    std::shared_ptr<menu_order_interfaces::action::Serve_SendGoal_Response_<ContainerAllocator> const>
    ConstPtr;

  // comparison operators
  bool operator==(const Serve_SendGoal_Response_ & other) const
  {
    if (this->accepted != other.accepted) {
      return false;
    }
    if (this->stamp != other.stamp) {
      return false;
    }
    return true;
  }
  bool operator!=(const Serve_SendGoal_Response_ & other) const
  {
    return !this->operator==(other);
  }
};  // struct Serve_SendGoal_Response_

// alias to use template instance with default allocator
using Serve_SendGoal_Response =
  menu_order_interfaces::action::Serve_SendGoal_Response_<std::allocator<void>>;

// constant definitions

}  // namespace action

}  // namespace menu_order_interfaces

namespace menu_order_interfaces
{

namespace action
{

struct Serve_SendGoal
{
  using Request = menu_order_interfaces::action::Serve_SendGoal_Request;
  using Response = menu_order_interfaces::action::Serve_SendGoal_Response;
};

}  // namespace action

}  // namespace menu_order_interfaces


// Include directives for member types
// Member 'goal_id'
// already included above
// #include "unique_identifier_msgs/msg/detail/uuid__struct.hpp"

#ifndef _WIN32
# define DEPRECATED__menu_order_interfaces__action__Serve_GetResult_Request __attribute__((deprecated))
#else
# define DEPRECATED__menu_order_interfaces__action__Serve_GetResult_Request __declspec(deprecated)
#endif

namespace menu_order_interfaces
{

namespace action
{

// message struct
template<class ContainerAllocator>
struct Serve_GetResult_Request_
{
  using Type = Serve_GetResult_Request_<ContainerAllocator>;

  explicit Serve_GetResult_Request_(rosidl_runtime_cpp::MessageInitialization _init = rosidl_runtime_cpp::MessageInitialization::ALL)
  : goal_id(_init)
  {
    (void)_init;
  }

  explicit Serve_GetResult_Request_(const ContainerAllocator & _alloc, rosidl_runtime_cpp::MessageInitialization _init = rosidl_runtime_cpp::MessageInitialization::ALL)
  : goal_id(_alloc, _init)
  {
    (void)_init;
  }

  // field types and members
  using _goal_id_type =
    unique_identifier_msgs::msg::UUID_<ContainerAllocator>;
  _goal_id_type goal_id;

  // setters for named parameter idiom
  Type & set__goal_id(
    const unique_identifier_msgs::msg::UUID_<ContainerAllocator> & _arg)
  {
    this->goal_id = _arg;
    return *this;
  }

  // constant declarations

  // pointer types
  using RawPtr =
    menu_order_interfaces::action::Serve_GetResult_Request_<ContainerAllocator> *;
  using ConstRawPtr =
    const menu_order_interfaces::action::Serve_GetResult_Request_<ContainerAllocator> *;
  using SharedPtr =
    std::shared_ptr<menu_order_interfaces::action::Serve_GetResult_Request_<ContainerAllocator>>;
  using ConstSharedPtr =
    std::shared_ptr<menu_order_interfaces::action::Serve_GetResult_Request_<ContainerAllocator> const>;

  template<typename Deleter = std::default_delete<
      menu_order_interfaces::action::Serve_GetResult_Request_<ContainerAllocator>>>
  using UniquePtrWithDeleter =
    std::unique_ptr<menu_order_interfaces::action::Serve_GetResult_Request_<ContainerAllocator>, Deleter>;

  using UniquePtr = UniquePtrWithDeleter<>;

  template<typename Deleter = std::default_delete<
      menu_order_interfaces::action::Serve_GetResult_Request_<ContainerAllocator>>>
  using ConstUniquePtrWithDeleter =
    std::unique_ptr<menu_order_interfaces::action::Serve_GetResult_Request_<ContainerAllocator> const, Deleter>;
  using ConstUniquePtr = ConstUniquePtrWithDeleter<>;

  using WeakPtr =
    std::weak_ptr<menu_order_interfaces::action::Serve_GetResult_Request_<ContainerAllocator>>;
  using ConstWeakPtr =
    std::weak_ptr<menu_order_interfaces::action::Serve_GetResult_Request_<ContainerAllocator> const>;

  // pointer types similar to ROS 1, use SharedPtr / ConstSharedPtr instead
  // NOTE: Can't use 'using' here because GNU C++ can't parse attributes properly
  typedef DEPRECATED__menu_order_interfaces__action__Serve_GetResult_Request
    std::shared_ptr<menu_order_interfaces::action::Serve_GetResult_Request_<ContainerAllocator>>
    Ptr;
  typedef DEPRECATED__menu_order_interfaces__action__Serve_GetResult_Request
    std::shared_ptr<menu_order_interfaces::action::Serve_GetResult_Request_<ContainerAllocator> const>
    ConstPtr;

  // comparison operators
  bool operator==(const Serve_GetResult_Request_ & other) const
  {
    if (this->goal_id != other.goal_id) {
      return false;
    }
    return true;
  }
  bool operator!=(const Serve_GetResult_Request_ & other) const
  {
    return !this->operator==(other);
  }
};  // struct Serve_GetResult_Request_

// alias to use template instance with default allocator
using Serve_GetResult_Request =
  menu_order_interfaces::action::Serve_GetResult_Request_<std::allocator<void>>;

// constant definitions

}  // namespace action

}  // namespace menu_order_interfaces


// Include directives for member types
// Member 'result'
// already included above
// #include "menu_order_interfaces/action/detail/serve__struct.hpp"

#ifndef _WIN32
# define DEPRECATED__menu_order_interfaces__action__Serve_GetResult_Response __attribute__((deprecated))
#else
# define DEPRECATED__menu_order_interfaces__action__Serve_GetResult_Response __declspec(deprecated)
#endif

namespace menu_order_interfaces
{

namespace action
{

// message struct
template<class ContainerAllocator>
struct Serve_GetResult_Response_
{
  using Type = Serve_GetResult_Response_<ContainerAllocator>;

  explicit Serve_GetResult_Response_(rosidl_runtime_cpp::MessageInitialization _init = rosidl_runtime_cpp::MessageInitialization::ALL)
  : result(_init)
  {
    if (rosidl_runtime_cpp::MessageInitialization::ALL == _init ||
      rosidl_runtime_cpp::MessageInitialization::ZERO == _init)
    {
      this->status = 0;
    }
  }

  explicit Serve_GetResult_Response_(const ContainerAllocator & _alloc, rosidl_runtime_cpp::MessageInitialization _init = rosidl_runtime_cpp::MessageInitialization::ALL)
  : result(_alloc, _init)
  {
    if (rosidl_runtime_cpp::MessageInitialization::ALL == _init ||
      rosidl_runtime_cpp::MessageInitialization::ZERO == _init)
    {
      this->status = 0;
    }
  }

  // field types and members
  using _status_type =
    int8_t;
  _status_type status;
  using _result_type =
    menu_order_interfaces::action::Serve_Result_<ContainerAllocator>;
  _result_type result;

  // setters for named parameter idiom
  Type & set__status(
    const int8_t & _arg)
  {
    this->status = _arg;
    return *this;
  }
  Type & set__result(
    const menu_order_interfaces::action::Serve_Result_<ContainerAllocator> & _arg)
  {
    this->result = _arg;
    return *this;
  }

  // constant declarations

  // pointer types
  using RawPtr =
    menu_order_interfaces::action::Serve_GetResult_Response_<ContainerAllocator> *;
  using ConstRawPtr =
    const menu_order_interfaces::action::Serve_GetResult_Response_<ContainerAllocator> *;
  using SharedPtr =
    std::shared_ptr<menu_order_interfaces::action::Serve_GetResult_Response_<ContainerAllocator>>;
  using ConstSharedPtr =
    std::shared_ptr<menu_order_interfaces::action::Serve_GetResult_Response_<ContainerAllocator> const>;

  template<typename Deleter = std::default_delete<
      menu_order_interfaces::action::Serve_GetResult_Response_<ContainerAllocator>>>
  using UniquePtrWithDeleter =
    std::unique_ptr<menu_order_interfaces::action::Serve_GetResult_Response_<ContainerAllocator>, Deleter>;

  using UniquePtr = UniquePtrWithDeleter<>;

  template<typename Deleter = std::default_delete<
      menu_order_interfaces::action::Serve_GetResult_Response_<ContainerAllocator>>>
  using ConstUniquePtrWithDeleter =
    std::unique_ptr<menu_order_interfaces::action::Serve_GetResult_Response_<ContainerAllocator> const, Deleter>;
  using ConstUniquePtr = ConstUniquePtrWithDeleter<>;

  using WeakPtr =
    std::weak_ptr<menu_order_interfaces::action::Serve_GetResult_Response_<ContainerAllocator>>;
  using ConstWeakPtr =
    std::weak_ptr<menu_order_interfaces::action::Serve_GetResult_Response_<ContainerAllocator> const>;

  // pointer types similar to ROS 1, use SharedPtr / ConstSharedPtr instead
  // NOTE: Can't use 'using' here because GNU C++ can't parse attributes properly
  typedef DEPRECATED__menu_order_interfaces__action__Serve_GetResult_Response
    std::shared_ptr<menu_order_interfaces::action::Serve_GetResult_Response_<ContainerAllocator>>
    Ptr;
  typedef DEPRECATED__menu_order_interfaces__action__Serve_GetResult_Response
    std::shared_ptr<menu_order_interfaces::action::Serve_GetResult_Response_<ContainerAllocator> const>
    ConstPtr;

  // comparison operators
  bool operator==(const Serve_GetResult_Response_ & other) const
  {
    if (this->status != other.status) {
      return false;
    }
    if (this->result != other.result) {
      return false;
    }
    return true;
  }
  bool operator!=(const Serve_GetResult_Response_ & other) const
  {
    return !this->operator==(other);
  }
};  // struct Serve_GetResult_Response_

// alias to use template instance with default allocator
using Serve_GetResult_Response =
  menu_order_interfaces::action::Serve_GetResult_Response_<std::allocator<void>>;

// constant definitions

}  // namespace action

}  // namespace menu_order_interfaces

namespace menu_order_interfaces
{

namespace action
{

struct Serve_GetResult
{
  using Request = menu_order_interfaces::action::Serve_GetResult_Request;
  using Response = menu_order_interfaces::action::Serve_GetResult_Response;
};

}  // namespace action

}  // namespace menu_order_interfaces


// Include directives for member types
// Member 'goal_id'
// already included above
// #include "unique_identifier_msgs/msg/detail/uuid__struct.hpp"
// Member 'feedback'
// already included above
// #include "menu_order_interfaces/action/detail/serve__struct.hpp"

#ifndef _WIN32
# define DEPRECATED__menu_order_interfaces__action__Serve_FeedbackMessage __attribute__((deprecated))
#else
# define DEPRECATED__menu_order_interfaces__action__Serve_FeedbackMessage __declspec(deprecated)
#endif

namespace menu_order_interfaces
{

namespace action
{

// message struct
template<class ContainerAllocator>
struct Serve_FeedbackMessage_
{
  using Type = Serve_FeedbackMessage_<ContainerAllocator>;

  explicit Serve_FeedbackMessage_(rosidl_runtime_cpp::MessageInitialization _init = rosidl_runtime_cpp::MessageInitialization::ALL)
  : goal_id(_init),
    feedback(_init)
  {
    (void)_init;
  }

  explicit Serve_FeedbackMessage_(const ContainerAllocator & _alloc, rosidl_runtime_cpp::MessageInitialization _init = rosidl_runtime_cpp::MessageInitialization::ALL)
  : goal_id(_alloc, _init),
    feedback(_alloc, _init)
  {
    (void)_init;
  }

  // field types and members
  using _goal_id_type =
    unique_identifier_msgs::msg::UUID_<ContainerAllocator>;
  _goal_id_type goal_id;
  using _feedback_type =
    menu_order_interfaces::action::Serve_Feedback_<ContainerAllocator>;
  _feedback_type feedback;

  // setters for named parameter idiom
  Type & set__goal_id(
    const unique_identifier_msgs::msg::UUID_<ContainerAllocator> & _arg)
  {
    this->goal_id = _arg;
    return *this;
  }
  Type & set__feedback(
    const menu_order_interfaces::action::Serve_Feedback_<ContainerAllocator> & _arg)
  {
    this->feedback = _arg;
    return *this;
  }

  // constant declarations

  // pointer types
  using RawPtr =
    menu_order_interfaces::action::Serve_FeedbackMessage_<ContainerAllocator> *;
  using ConstRawPtr =
    const menu_order_interfaces::action::Serve_FeedbackMessage_<ContainerAllocator> *;
  using SharedPtr =
    std::shared_ptr<menu_order_interfaces::action::Serve_FeedbackMessage_<ContainerAllocator>>;
  using ConstSharedPtr =
    std::shared_ptr<menu_order_interfaces::action::Serve_FeedbackMessage_<ContainerAllocator> const>;

  template<typename Deleter = std::default_delete<
      menu_order_interfaces::action::Serve_FeedbackMessage_<ContainerAllocator>>>
  using UniquePtrWithDeleter =
    std::unique_ptr<menu_order_interfaces::action::Serve_FeedbackMessage_<ContainerAllocator>, Deleter>;

  using UniquePtr = UniquePtrWithDeleter<>;

  template<typename Deleter = std::default_delete<
      menu_order_interfaces::action::Serve_FeedbackMessage_<ContainerAllocator>>>
  using ConstUniquePtrWithDeleter =
    std::unique_ptr<menu_order_interfaces::action::Serve_FeedbackMessage_<ContainerAllocator> const, Deleter>;
  using ConstUniquePtr = ConstUniquePtrWithDeleter<>;

  using WeakPtr =
    std::weak_ptr<menu_order_interfaces::action::Serve_FeedbackMessage_<ContainerAllocator>>;
  using ConstWeakPtr =
    std::weak_ptr<menu_order_interfaces::action::Serve_FeedbackMessage_<ContainerAllocator> const>;

  // pointer types similar to ROS 1, use SharedPtr / ConstSharedPtr instead
  // NOTE: Can't use 'using' here because GNU C++ can't parse attributes properly
  typedef DEPRECATED__menu_order_interfaces__action__Serve_FeedbackMessage
    std::shared_ptr<menu_order_interfaces::action::Serve_FeedbackMessage_<ContainerAllocator>>
    Ptr;
  typedef DEPRECATED__menu_order_interfaces__action__Serve_FeedbackMessage
    std::shared_ptr<menu_order_interfaces::action::Serve_FeedbackMessage_<ContainerAllocator> const>
    ConstPtr;

  // comparison operators
  bool operator==(const Serve_FeedbackMessage_ & other) const
  {
    if (this->goal_id != other.goal_id) {
      return false;
    }
    if (this->feedback != other.feedback) {
      return false;
    }
    return true;
  }
  bool operator!=(const Serve_FeedbackMessage_ & other) const
  {
    return !this->operator==(other);
  }
};  // struct Serve_FeedbackMessage_

// alias to use template instance with default allocator
using Serve_FeedbackMessage =
  menu_order_interfaces::action::Serve_FeedbackMessage_<std::allocator<void>>;

// constant definitions

}  // namespace action

}  // namespace menu_order_interfaces

#include "action_msgs/srv/cancel_goal.hpp"
#include "action_msgs/msg/goal_info.hpp"
#include "action_msgs/msg/goal_status_array.hpp"

namespace menu_order_interfaces
{

namespace action
{

struct Serve
{
  /// The goal message defined in the action definition.
  using Goal = menu_order_interfaces::action::Serve_Goal;
  /// The result message defined in the action definition.
  using Result = menu_order_interfaces::action::Serve_Result;
  /// The feedback message defined in the action definition.
  using Feedback = menu_order_interfaces::action::Serve_Feedback;

  struct Impl
  {
    /// The send_goal service using a wrapped version of the goal message as a request.
    using SendGoalService = menu_order_interfaces::action::Serve_SendGoal;
    /// The get_result service using a wrapped version of the result message as a response.
    using GetResultService = menu_order_interfaces::action::Serve_GetResult;
    /// The feedback message with generic fields which wraps the feedback message.
    using FeedbackMessage = menu_order_interfaces::action::Serve_FeedbackMessage;

    /// The generic service to cancel a goal.
    using CancelGoalService = action_msgs::srv::CancelGoal;
    /// The generic message for the status of a goal.
    using GoalStatusMessage = action_msgs::msg::GoalStatusArray;
  };
};

typedef struct Serve Serve;

}  // namespace action

}  // namespace menu_order_interfaces

#endif  // MENU_ORDER_INTERFACES__ACTION__DETAIL__SERVE__STRUCT_HPP_
