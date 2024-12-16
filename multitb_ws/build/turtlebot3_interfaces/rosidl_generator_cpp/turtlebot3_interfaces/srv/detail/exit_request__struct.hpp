// generated from rosidl_generator_cpp/resource/idl__struct.hpp.em
// with input from turtlebot3_interfaces:srv/ExitRequest.idl
// generated code does not contain a copyright notice

#ifndef TURTLEBOT3_INTERFACES__SRV__DETAIL__EXIT_REQUEST__STRUCT_HPP_
#define TURTLEBOT3_INTERFACES__SRV__DETAIL__EXIT_REQUEST__STRUCT_HPP_

#include <algorithm>
#include <array>
#include <memory>
#include <string>
#include <vector>

#include "rosidl_runtime_cpp/bounded_vector.hpp"
#include "rosidl_runtime_cpp/message_initialization.hpp"


#ifndef _WIN32
# define DEPRECATED__turtlebot3_interfaces__srv__ExitRequest_Request __attribute__((deprecated))
#else
# define DEPRECATED__turtlebot3_interfaces__srv__ExitRequest_Request __declspec(deprecated)
#endif

namespace turtlebot3_interfaces
{

namespace srv
{

// message struct
template<class ContainerAllocator>
struct ExitRequest_Request_
{
  using Type = ExitRequest_Request_<ContainerAllocator>;

  explicit ExitRequest_Request_(rosidl_runtime_cpp::MessageInitialization _init = rosidl_runtime_cpp::MessageInitialization::ALL)
  {
    if (rosidl_runtime_cpp::MessageInitialization::ALL == _init ||
      rosidl_runtime_cpp::MessageInitialization::ZERO == _init)
    {
      this->car_number = "";
    }
  }

  explicit ExitRequest_Request_(const ContainerAllocator & _alloc, rosidl_runtime_cpp::MessageInitialization _init = rosidl_runtime_cpp::MessageInitialization::ALL)
  : car_number(_alloc)
  {
    if (rosidl_runtime_cpp::MessageInitialization::ALL == _init ||
      rosidl_runtime_cpp::MessageInitialization::ZERO == _init)
    {
      this->car_number = "";
    }
  }

  // field types and members
  using _car_number_type =
    std::basic_string<char, std::char_traits<char>, typename std::allocator_traits<ContainerAllocator>::template rebind_alloc<char>>;
  _car_number_type car_number;

  // setters for named parameter idiom
  Type & set__car_number(
    const std::basic_string<char, std::char_traits<char>, typename std::allocator_traits<ContainerAllocator>::template rebind_alloc<char>> & _arg)
  {
    this->car_number = _arg;
    return *this;
  }

  // constant declarations

  // pointer types
  using RawPtr =
    turtlebot3_interfaces::srv::ExitRequest_Request_<ContainerAllocator> *;
  using ConstRawPtr =
    const turtlebot3_interfaces::srv::ExitRequest_Request_<ContainerAllocator> *;
  using SharedPtr =
    std::shared_ptr<turtlebot3_interfaces::srv::ExitRequest_Request_<ContainerAllocator>>;
  using ConstSharedPtr =
    std::shared_ptr<turtlebot3_interfaces::srv::ExitRequest_Request_<ContainerAllocator> const>;

  template<typename Deleter = std::default_delete<
      turtlebot3_interfaces::srv::ExitRequest_Request_<ContainerAllocator>>>
  using UniquePtrWithDeleter =
    std::unique_ptr<turtlebot3_interfaces::srv::ExitRequest_Request_<ContainerAllocator>, Deleter>;

  using UniquePtr = UniquePtrWithDeleter<>;

  template<typename Deleter = std::default_delete<
      turtlebot3_interfaces::srv::ExitRequest_Request_<ContainerAllocator>>>
  using ConstUniquePtrWithDeleter =
    std::unique_ptr<turtlebot3_interfaces::srv::ExitRequest_Request_<ContainerAllocator> const, Deleter>;
  using ConstUniquePtr = ConstUniquePtrWithDeleter<>;

  using WeakPtr =
    std::weak_ptr<turtlebot3_interfaces::srv::ExitRequest_Request_<ContainerAllocator>>;
  using ConstWeakPtr =
    std::weak_ptr<turtlebot3_interfaces::srv::ExitRequest_Request_<ContainerAllocator> const>;

  // pointer types similar to ROS 1, use SharedPtr / ConstSharedPtr instead
  // NOTE: Can't use 'using' here because GNU C++ can't parse attributes properly
  typedef DEPRECATED__turtlebot3_interfaces__srv__ExitRequest_Request
    std::shared_ptr<turtlebot3_interfaces::srv::ExitRequest_Request_<ContainerAllocator>>
    Ptr;
  typedef DEPRECATED__turtlebot3_interfaces__srv__ExitRequest_Request
    std::shared_ptr<turtlebot3_interfaces::srv::ExitRequest_Request_<ContainerAllocator> const>
    ConstPtr;

  // comparison operators
  bool operator==(const ExitRequest_Request_ & other) const
  {
    if (this->car_number != other.car_number) {
      return false;
    }
    return true;
  }
  bool operator!=(const ExitRequest_Request_ & other) const
  {
    return !this->operator==(other);
  }
};  // struct ExitRequest_Request_

// alias to use template instance with default allocator
using ExitRequest_Request =
  turtlebot3_interfaces::srv::ExitRequest_Request_<std::allocator<void>>;

// constant definitions

}  // namespace srv

}  // namespace turtlebot3_interfaces


#ifndef _WIN32
# define DEPRECATED__turtlebot3_interfaces__srv__ExitRequest_Response __attribute__((deprecated))
#else
# define DEPRECATED__turtlebot3_interfaces__srv__ExitRequest_Response __declspec(deprecated)
#endif

namespace turtlebot3_interfaces
{

namespace srv
{

// message struct
template<class ContainerAllocator>
struct ExitRequest_Response_
{
  using Type = ExitRequest_Response_<ContainerAllocator>;

  explicit ExitRequest_Response_(rosidl_runtime_cpp::MessageInitialization _init = rosidl_runtime_cpp::MessageInitialization::ALL)
  {
    if (rosidl_runtime_cpp::MessageInitialization::ALL == _init ||
      rosidl_runtime_cpp::MessageInitialization::ZERO == _init)
    {
      this->status = false;
      this->entry_time = "";
      this->fee = 0l;
      this->log = "";
    }
  }

  explicit ExitRequest_Response_(const ContainerAllocator & _alloc, rosidl_runtime_cpp::MessageInitialization _init = rosidl_runtime_cpp::MessageInitialization::ALL)
  : entry_time(_alloc),
    log(_alloc)
  {
    if (rosidl_runtime_cpp::MessageInitialization::ALL == _init ||
      rosidl_runtime_cpp::MessageInitialization::ZERO == _init)
    {
      this->status = false;
      this->entry_time = "";
      this->fee = 0l;
      this->log = "";
    }
  }

  // field types and members
  using _status_type =
    bool;
  _status_type status;
  using _entry_time_type =
    std::basic_string<char, std::char_traits<char>, typename std::allocator_traits<ContainerAllocator>::template rebind_alloc<char>>;
  _entry_time_type entry_time;
  using _fee_type =
    int32_t;
  _fee_type fee;
  using _log_type =
    std::basic_string<char, std::char_traits<char>, typename std::allocator_traits<ContainerAllocator>::template rebind_alloc<char>>;
  _log_type log;

  // setters for named parameter idiom
  Type & set__status(
    const bool & _arg)
  {
    this->status = _arg;
    return *this;
  }
  Type & set__entry_time(
    const std::basic_string<char, std::char_traits<char>, typename std::allocator_traits<ContainerAllocator>::template rebind_alloc<char>> & _arg)
  {
    this->entry_time = _arg;
    return *this;
  }
  Type & set__fee(
    const int32_t & _arg)
  {
    this->fee = _arg;
    return *this;
  }
  Type & set__log(
    const std::basic_string<char, std::char_traits<char>, typename std::allocator_traits<ContainerAllocator>::template rebind_alloc<char>> & _arg)
  {
    this->log = _arg;
    return *this;
  }

  // constant declarations

  // pointer types
  using RawPtr =
    turtlebot3_interfaces::srv::ExitRequest_Response_<ContainerAllocator> *;
  using ConstRawPtr =
    const turtlebot3_interfaces::srv::ExitRequest_Response_<ContainerAllocator> *;
  using SharedPtr =
    std::shared_ptr<turtlebot3_interfaces::srv::ExitRequest_Response_<ContainerAllocator>>;
  using ConstSharedPtr =
    std::shared_ptr<turtlebot3_interfaces::srv::ExitRequest_Response_<ContainerAllocator> const>;

  template<typename Deleter = std::default_delete<
      turtlebot3_interfaces::srv::ExitRequest_Response_<ContainerAllocator>>>
  using UniquePtrWithDeleter =
    std::unique_ptr<turtlebot3_interfaces::srv::ExitRequest_Response_<ContainerAllocator>, Deleter>;

  using UniquePtr = UniquePtrWithDeleter<>;

  template<typename Deleter = std::default_delete<
      turtlebot3_interfaces::srv::ExitRequest_Response_<ContainerAllocator>>>
  using ConstUniquePtrWithDeleter =
    std::unique_ptr<turtlebot3_interfaces::srv::ExitRequest_Response_<ContainerAllocator> const, Deleter>;
  using ConstUniquePtr = ConstUniquePtrWithDeleter<>;

  using WeakPtr =
    std::weak_ptr<turtlebot3_interfaces::srv::ExitRequest_Response_<ContainerAllocator>>;
  using ConstWeakPtr =
    std::weak_ptr<turtlebot3_interfaces::srv::ExitRequest_Response_<ContainerAllocator> const>;

  // pointer types similar to ROS 1, use SharedPtr / ConstSharedPtr instead
  // NOTE: Can't use 'using' here because GNU C++ can't parse attributes properly
  typedef DEPRECATED__turtlebot3_interfaces__srv__ExitRequest_Response
    std::shared_ptr<turtlebot3_interfaces::srv::ExitRequest_Response_<ContainerAllocator>>
    Ptr;
  typedef DEPRECATED__turtlebot3_interfaces__srv__ExitRequest_Response
    std::shared_ptr<turtlebot3_interfaces::srv::ExitRequest_Response_<ContainerAllocator> const>
    ConstPtr;

  // comparison operators
  bool operator==(const ExitRequest_Response_ & other) const
  {
    if (this->status != other.status) {
      return false;
    }
    if (this->entry_time != other.entry_time) {
      return false;
    }
    if (this->fee != other.fee) {
      return false;
    }
    if (this->log != other.log) {
      return false;
    }
    return true;
  }
  bool operator!=(const ExitRequest_Response_ & other) const
  {
    return !this->operator==(other);
  }
};  // struct ExitRequest_Response_

// alias to use template instance with default allocator
using ExitRequest_Response =
  turtlebot3_interfaces::srv::ExitRequest_Response_<std::allocator<void>>;

// constant definitions

}  // namespace srv

}  // namespace turtlebot3_interfaces

namespace turtlebot3_interfaces
{

namespace srv
{

struct ExitRequest
{
  using Request = turtlebot3_interfaces::srv::ExitRequest_Request;
  using Response = turtlebot3_interfaces::srv::ExitRequest_Response;
};

}  // namespace srv

}  // namespace turtlebot3_interfaces

#endif  // TURTLEBOT3_INTERFACES__SRV__DETAIL__EXIT_REQUEST__STRUCT_HPP_
