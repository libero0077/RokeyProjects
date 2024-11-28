// generated from rosidl_generator_cpp/resource/idl__struct.hpp.em
// with input from menu_order_interfaces:srv/MenuUpdate.idl
// generated code does not contain a copyright notice

#ifndef MENU_ORDER_INTERFACES__SRV__DETAIL__MENU_UPDATE__STRUCT_HPP_
#define MENU_ORDER_INTERFACES__SRV__DETAIL__MENU_UPDATE__STRUCT_HPP_

#include <algorithm>
#include <array>
#include <memory>
#include <string>
#include <vector>

#include "rosidl_runtime_cpp/bounded_vector.hpp"
#include "rosidl_runtime_cpp/message_initialization.hpp"


#ifndef _WIN32
# define DEPRECATED__menu_order_interfaces__srv__MenuUpdate_Request __attribute__((deprecated))
#else
# define DEPRECATED__menu_order_interfaces__srv__MenuUpdate_Request __declspec(deprecated)
#endif

namespace menu_order_interfaces
{

namespace srv
{

// message struct
template<class ContainerAllocator>
struct MenuUpdate_Request_
{
  using Type = MenuUpdate_Request_<ContainerAllocator>;

  explicit MenuUpdate_Request_(rosidl_runtime_cpp::MessageInitialization _init = rosidl_runtime_cpp::MessageInitialization::ALL)
  {
    if (rosidl_runtime_cpp::MessageInitialization::ALL == _init ||
      rosidl_runtime_cpp::MessageInitialization::ZERO == _init)
    {
      this->result_message = "";
    }
  }

  explicit MenuUpdate_Request_(const ContainerAllocator & _alloc, rosidl_runtime_cpp::MessageInitialization _init = rosidl_runtime_cpp::MessageInitialization::ALL)
  : result_message(_alloc)
  {
    if (rosidl_runtime_cpp::MessageInitialization::ALL == _init ||
      rosidl_runtime_cpp::MessageInitialization::ZERO == _init)
    {
      this->result_message = "";
    }
  }

  // field types and members
  using _result_message_type =
    std::basic_string<char, std::char_traits<char>, typename std::allocator_traits<ContainerAllocator>::template rebind_alloc<char>>;
  _result_message_type result_message;

  // setters for named parameter idiom
  Type & set__result_message(
    const std::basic_string<char, std::char_traits<char>, typename std::allocator_traits<ContainerAllocator>::template rebind_alloc<char>> & _arg)
  {
    this->result_message = _arg;
    return *this;
  }

  // constant declarations

  // pointer types
  using RawPtr =
    menu_order_interfaces::srv::MenuUpdate_Request_<ContainerAllocator> *;
  using ConstRawPtr =
    const menu_order_interfaces::srv::MenuUpdate_Request_<ContainerAllocator> *;
  using SharedPtr =
    std::shared_ptr<menu_order_interfaces::srv::MenuUpdate_Request_<ContainerAllocator>>;
  using ConstSharedPtr =
    std::shared_ptr<menu_order_interfaces::srv::MenuUpdate_Request_<ContainerAllocator> const>;

  template<typename Deleter = std::default_delete<
      menu_order_interfaces::srv::MenuUpdate_Request_<ContainerAllocator>>>
  using UniquePtrWithDeleter =
    std::unique_ptr<menu_order_interfaces::srv::MenuUpdate_Request_<ContainerAllocator>, Deleter>;

  using UniquePtr = UniquePtrWithDeleter<>;

  template<typename Deleter = std::default_delete<
      menu_order_interfaces::srv::MenuUpdate_Request_<ContainerAllocator>>>
  using ConstUniquePtrWithDeleter =
    std::unique_ptr<menu_order_interfaces::srv::MenuUpdate_Request_<ContainerAllocator> const, Deleter>;
  using ConstUniquePtr = ConstUniquePtrWithDeleter<>;

  using WeakPtr =
    std::weak_ptr<menu_order_interfaces::srv::MenuUpdate_Request_<ContainerAllocator>>;
  using ConstWeakPtr =
    std::weak_ptr<menu_order_interfaces::srv::MenuUpdate_Request_<ContainerAllocator> const>;

  // pointer types similar to ROS 1, use SharedPtr / ConstSharedPtr instead
  // NOTE: Can't use 'using' here because GNU C++ can't parse attributes properly
  typedef DEPRECATED__menu_order_interfaces__srv__MenuUpdate_Request
    std::shared_ptr<menu_order_interfaces::srv::MenuUpdate_Request_<ContainerAllocator>>
    Ptr;
  typedef DEPRECATED__menu_order_interfaces__srv__MenuUpdate_Request
    std::shared_ptr<menu_order_interfaces::srv::MenuUpdate_Request_<ContainerAllocator> const>
    ConstPtr;

  // comparison operators
  bool operator==(const MenuUpdate_Request_ & other) const
  {
    if (this->result_message != other.result_message) {
      return false;
    }
    return true;
  }
  bool operator!=(const MenuUpdate_Request_ & other) const
  {
    return !this->operator==(other);
  }
};  // struct MenuUpdate_Request_

// alias to use template instance with default allocator
using MenuUpdate_Request =
  menu_order_interfaces::srv::MenuUpdate_Request_<std::allocator<void>>;

// constant definitions

}  // namespace srv

}  // namespace menu_order_interfaces


#ifndef _WIN32
# define DEPRECATED__menu_order_interfaces__srv__MenuUpdate_Response __attribute__((deprecated))
#else
# define DEPRECATED__menu_order_interfaces__srv__MenuUpdate_Response __declspec(deprecated)
#endif

namespace menu_order_interfaces
{

namespace srv
{

// message struct
template<class ContainerAllocator>
struct MenuUpdate_Response_
{
  using Type = MenuUpdate_Response_<ContainerAllocator>;

  explicit MenuUpdate_Response_(rosidl_runtime_cpp::MessageInitialization _init = rosidl_runtime_cpp::MessageInitialization::ALL)
  {
    if (rosidl_runtime_cpp::MessageInitialization::ALL == _init ||
      rosidl_runtime_cpp::MessageInitialization::ZERO == _init)
    {
      this->success = false;
    }
  }

  explicit MenuUpdate_Response_(const ContainerAllocator & _alloc, rosidl_runtime_cpp::MessageInitialization _init = rosidl_runtime_cpp::MessageInitialization::ALL)
  {
    (void)_alloc;
    if (rosidl_runtime_cpp::MessageInitialization::ALL == _init ||
      rosidl_runtime_cpp::MessageInitialization::ZERO == _init)
    {
      this->success = false;
    }
  }

  // field types and members
  using _success_type =
    bool;
  _success_type success;

  // setters for named parameter idiom
  Type & set__success(
    const bool & _arg)
  {
    this->success = _arg;
    return *this;
  }

  // constant declarations

  // pointer types
  using RawPtr =
    menu_order_interfaces::srv::MenuUpdate_Response_<ContainerAllocator> *;
  using ConstRawPtr =
    const menu_order_interfaces::srv::MenuUpdate_Response_<ContainerAllocator> *;
  using SharedPtr =
    std::shared_ptr<menu_order_interfaces::srv::MenuUpdate_Response_<ContainerAllocator>>;
  using ConstSharedPtr =
    std::shared_ptr<menu_order_interfaces::srv::MenuUpdate_Response_<ContainerAllocator> const>;

  template<typename Deleter = std::default_delete<
      menu_order_interfaces::srv::MenuUpdate_Response_<ContainerAllocator>>>
  using UniquePtrWithDeleter =
    std::unique_ptr<menu_order_interfaces::srv::MenuUpdate_Response_<ContainerAllocator>, Deleter>;

  using UniquePtr = UniquePtrWithDeleter<>;

  template<typename Deleter = std::default_delete<
      menu_order_interfaces::srv::MenuUpdate_Response_<ContainerAllocator>>>
  using ConstUniquePtrWithDeleter =
    std::unique_ptr<menu_order_interfaces::srv::MenuUpdate_Response_<ContainerAllocator> const, Deleter>;
  using ConstUniquePtr = ConstUniquePtrWithDeleter<>;

  using WeakPtr =
    std::weak_ptr<menu_order_interfaces::srv::MenuUpdate_Response_<ContainerAllocator>>;
  using ConstWeakPtr =
    std::weak_ptr<menu_order_interfaces::srv::MenuUpdate_Response_<ContainerAllocator> const>;

  // pointer types similar to ROS 1, use SharedPtr / ConstSharedPtr instead
  // NOTE: Can't use 'using' here because GNU C++ can't parse attributes properly
  typedef DEPRECATED__menu_order_interfaces__srv__MenuUpdate_Response
    std::shared_ptr<menu_order_interfaces::srv::MenuUpdate_Response_<ContainerAllocator>>
    Ptr;
  typedef DEPRECATED__menu_order_interfaces__srv__MenuUpdate_Response
    std::shared_ptr<menu_order_interfaces::srv::MenuUpdate_Response_<ContainerAllocator> const>
    ConstPtr;

  // comparison operators
  bool operator==(const MenuUpdate_Response_ & other) const
  {
    if (this->success != other.success) {
      return false;
    }
    return true;
  }
  bool operator!=(const MenuUpdate_Response_ & other) const
  {
    return !this->operator==(other);
  }
};  // struct MenuUpdate_Response_

// alias to use template instance with default allocator
using MenuUpdate_Response =
  menu_order_interfaces::srv::MenuUpdate_Response_<std::allocator<void>>;

// constant definitions

}  // namespace srv

}  // namespace menu_order_interfaces

namespace menu_order_interfaces
{

namespace srv
{

struct MenuUpdate
{
  using Request = menu_order_interfaces::srv::MenuUpdate_Request;
  using Response = menu_order_interfaces::srv::MenuUpdate_Response;
};

}  // namespace srv

}  // namespace menu_order_interfaces

#endif  // MENU_ORDER_INTERFACES__SRV__DETAIL__MENU_UPDATE__STRUCT_HPP_
