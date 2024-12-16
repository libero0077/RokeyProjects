// generated from rosidl_generator_cpp/resource/idl__struct.hpp.em
// with input from turtlebot3_interfaces:srv/GetSystemState.idl
// generated code does not contain a copyright notice

#ifndef TURTLEBOT3_INTERFACES__SRV__DETAIL__GET_SYSTEM_STATE__STRUCT_HPP_
#define TURTLEBOT3_INTERFACES__SRV__DETAIL__GET_SYSTEM_STATE__STRUCT_HPP_

#include <algorithm>
#include <array>
#include <memory>
#include <string>
#include <vector>

#include "rosidl_runtime_cpp/bounded_vector.hpp"
#include "rosidl_runtime_cpp/message_initialization.hpp"


#ifndef _WIN32
# define DEPRECATED__turtlebot3_interfaces__srv__GetSystemState_Request __attribute__((deprecated))
#else
# define DEPRECATED__turtlebot3_interfaces__srv__GetSystemState_Request __declspec(deprecated)
#endif

namespace turtlebot3_interfaces
{

namespace srv
{

// message struct
template<class ContainerAllocator>
struct GetSystemState_Request_
{
  using Type = GetSystemState_Request_<ContainerAllocator>;

  explicit GetSystemState_Request_(rosidl_runtime_cpp::MessageInitialization _init = rosidl_runtime_cpp::MessageInitialization::ALL)
  {
    if (rosidl_runtime_cpp::MessageInitialization::ALL == _init ||
      rosidl_runtime_cpp::MessageInitialization::ZERO == _init)
    {
      this->structure_needs_at_least_one_member = 0;
    }
  }

  explicit GetSystemState_Request_(const ContainerAllocator & _alloc, rosidl_runtime_cpp::MessageInitialization _init = rosidl_runtime_cpp::MessageInitialization::ALL)
  {
    (void)_alloc;
    if (rosidl_runtime_cpp::MessageInitialization::ALL == _init ||
      rosidl_runtime_cpp::MessageInitialization::ZERO == _init)
    {
      this->structure_needs_at_least_one_member = 0;
    }
  }

  // field types and members
  using _structure_needs_at_least_one_member_type =
    uint8_t;
  _structure_needs_at_least_one_member_type structure_needs_at_least_one_member;


  // constant declarations

  // pointer types
  using RawPtr =
    turtlebot3_interfaces::srv::GetSystemState_Request_<ContainerAllocator> *;
  using ConstRawPtr =
    const turtlebot3_interfaces::srv::GetSystemState_Request_<ContainerAllocator> *;
  using SharedPtr =
    std::shared_ptr<turtlebot3_interfaces::srv::GetSystemState_Request_<ContainerAllocator>>;
  using ConstSharedPtr =
    std::shared_ptr<turtlebot3_interfaces::srv::GetSystemState_Request_<ContainerAllocator> const>;

  template<typename Deleter = std::default_delete<
      turtlebot3_interfaces::srv::GetSystemState_Request_<ContainerAllocator>>>
  using UniquePtrWithDeleter =
    std::unique_ptr<turtlebot3_interfaces::srv::GetSystemState_Request_<ContainerAllocator>, Deleter>;

  using UniquePtr = UniquePtrWithDeleter<>;

  template<typename Deleter = std::default_delete<
      turtlebot3_interfaces::srv::GetSystemState_Request_<ContainerAllocator>>>
  using ConstUniquePtrWithDeleter =
    std::unique_ptr<turtlebot3_interfaces::srv::GetSystemState_Request_<ContainerAllocator> const, Deleter>;
  using ConstUniquePtr = ConstUniquePtrWithDeleter<>;

  using WeakPtr =
    std::weak_ptr<turtlebot3_interfaces::srv::GetSystemState_Request_<ContainerAllocator>>;
  using ConstWeakPtr =
    std::weak_ptr<turtlebot3_interfaces::srv::GetSystemState_Request_<ContainerAllocator> const>;

  // pointer types similar to ROS 1, use SharedPtr / ConstSharedPtr instead
  // NOTE: Can't use 'using' here because GNU C++ can't parse attributes properly
  typedef DEPRECATED__turtlebot3_interfaces__srv__GetSystemState_Request
    std::shared_ptr<turtlebot3_interfaces::srv::GetSystemState_Request_<ContainerAllocator>>
    Ptr;
  typedef DEPRECATED__turtlebot3_interfaces__srv__GetSystemState_Request
    std::shared_ptr<turtlebot3_interfaces::srv::GetSystemState_Request_<ContainerAllocator> const>
    ConstPtr;

  // comparison operators
  bool operator==(const GetSystemState_Request_ & other) const
  {
    if (this->structure_needs_at_least_one_member != other.structure_needs_at_least_one_member) {
      return false;
    }
    return true;
  }
  bool operator!=(const GetSystemState_Request_ & other) const
  {
    return !this->operator==(other);
  }
};  // struct GetSystemState_Request_

// alias to use template instance with default allocator
using GetSystemState_Request =
  turtlebot3_interfaces::srv::GetSystemState_Request_<std::allocator<void>>;

// constant definitions

}  // namespace srv

}  // namespace turtlebot3_interfaces


#ifndef _WIN32
# define DEPRECATED__turtlebot3_interfaces__srv__GetSystemState_Response __attribute__((deprecated))
#else
# define DEPRECATED__turtlebot3_interfaces__srv__GetSystemState_Response __declspec(deprecated)
#endif

namespace turtlebot3_interfaces
{

namespace srv
{

// message struct
template<class ContainerAllocator>
struct GetSystemState_Response_
{
  using Type = GetSystemState_Response_<ContainerAllocator>;

  explicit GetSystemState_Response_(rosidl_runtime_cpp::MessageInitialization _init = rosidl_runtime_cpp::MessageInitialization::ALL)
  {
    if (rosidl_runtime_cpp::MessageInitialization::ALL == _init ||
      rosidl_runtime_cpp::MessageInitialization::ZERO == _init)
    {
      this->robot_status_json = "";
      this->slot_status_json = "";
    }
  }

  explicit GetSystemState_Response_(const ContainerAllocator & _alloc, rosidl_runtime_cpp::MessageInitialization _init = rosidl_runtime_cpp::MessageInitialization::ALL)
  : robot_status_json(_alloc),
    slot_status_json(_alloc)
  {
    if (rosidl_runtime_cpp::MessageInitialization::ALL == _init ||
      rosidl_runtime_cpp::MessageInitialization::ZERO == _init)
    {
      this->robot_status_json = "";
      this->slot_status_json = "";
    }
  }

  // field types and members
  using _robot_status_json_type =
    std::basic_string<char, std::char_traits<char>, typename std::allocator_traits<ContainerAllocator>::template rebind_alloc<char>>;
  _robot_status_json_type robot_status_json;
  using _slot_status_json_type =
    std::basic_string<char, std::char_traits<char>, typename std::allocator_traits<ContainerAllocator>::template rebind_alloc<char>>;
  _slot_status_json_type slot_status_json;

  // setters for named parameter idiom
  Type & set__robot_status_json(
    const std::basic_string<char, std::char_traits<char>, typename std::allocator_traits<ContainerAllocator>::template rebind_alloc<char>> & _arg)
  {
    this->robot_status_json = _arg;
    return *this;
  }
  Type & set__slot_status_json(
    const std::basic_string<char, std::char_traits<char>, typename std::allocator_traits<ContainerAllocator>::template rebind_alloc<char>> & _arg)
  {
    this->slot_status_json = _arg;
    return *this;
  }

  // constant declarations

  // pointer types
  using RawPtr =
    turtlebot3_interfaces::srv::GetSystemState_Response_<ContainerAllocator> *;
  using ConstRawPtr =
    const turtlebot3_interfaces::srv::GetSystemState_Response_<ContainerAllocator> *;
  using SharedPtr =
    std::shared_ptr<turtlebot3_interfaces::srv::GetSystemState_Response_<ContainerAllocator>>;
  using ConstSharedPtr =
    std::shared_ptr<turtlebot3_interfaces::srv::GetSystemState_Response_<ContainerAllocator> const>;

  template<typename Deleter = std::default_delete<
      turtlebot3_interfaces::srv::GetSystemState_Response_<ContainerAllocator>>>
  using UniquePtrWithDeleter =
    std::unique_ptr<turtlebot3_interfaces::srv::GetSystemState_Response_<ContainerAllocator>, Deleter>;

  using UniquePtr = UniquePtrWithDeleter<>;

  template<typename Deleter = std::default_delete<
      turtlebot3_interfaces::srv::GetSystemState_Response_<ContainerAllocator>>>
  using ConstUniquePtrWithDeleter =
    std::unique_ptr<turtlebot3_interfaces::srv::GetSystemState_Response_<ContainerAllocator> const, Deleter>;
  using ConstUniquePtr = ConstUniquePtrWithDeleter<>;

  using WeakPtr =
    std::weak_ptr<turtlebot3_interfaces::srv::GetSystemState_Response_<ContainerAllocator>>;
  using ConstWeakPtr =
    std::weak_ptr<turtlebot3_interfaces::srv::GetSystemState_Response_<ContainerAllocator> const>;

  // pointer types similar to ROS 1, use SharedPtr / ConstSharedPtr instead
  // NOTE: Can't use 'using' here because GNU C++ can't parse attributes properly
  typedef DEPRECATED__turtlebot3_interfaces__srv__GetSystemState_Response
    std::shared_ptr<turtlebot3_interfaces::srv::GetSystemState_Response_<ContainerAllocator>>
    Ptr;
  typedef DEPRECATED__turtlebot3_interfaces__srv__GetSystemState_Response
    std::shared_ptr<turtlebot3_interfaces::srv::GetSystemState_Response_<ContainerAllocator> const>
    ConstPtr;

  // comparison operators
  bool operator==(const GetSystemState_Response_ & other) const
  {
    if (this->robot_status_json != other.robot_status_json) {
      return false;
    }
    if (this->slot_status_json != other.slot_status_json) {
      return false;
    }
    return true;
  }
  bool operator!=(const GetSystemState_Response_ & other) const
  {
    return !this->operator==(other);
  }
};  // struct GetSystemState_Response_

// alias to use template instance with default allocator
using GetSystemState_Response =
  turtlebot3_interfaces::srv::GetSystemState_Response_<std::allocator<void>>;

// constant definitions

}  // namespace srv

}  // namespace turtlebot3_interfaces

namespace turtlebot3_interfaces
{

namespace srv
{

struct GetSystemState
{
  using Request = turtlebot3_interfaces::srv::GetSystemState_Request;
  using Response = turtlebot3_interfaces::srv::GetSystemState_Response;
};

}  // namespace srv

}  // namespace turtlebot3_interfaces

#endif  // TURTLEBOT3_INTERFACES__SRV__DETAIL__GET_SYSTEM_STATE__STRUCT_HPP_
