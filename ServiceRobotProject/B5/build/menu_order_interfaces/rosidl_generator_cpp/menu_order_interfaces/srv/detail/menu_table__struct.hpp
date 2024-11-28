// generated from rosidl_generator_cpp/resource/idl__struct.hpp.em
// with input from menu_order_interfaces:srv/MenuTable.idl
// generated code does not contain a copyright notice

#ifndef MENU_ORDER_INTERFACES__SRV__DETAIL__MENU_TABLE__STRUCT_HPP_
#define MENU_ORDER_INTERFACES__SRV__DETAIL__MENU_TABLE__STRUCT_HPP_

#include <algorithm>
#include <array>
#include <memory>
#include <string>
#include <vector>

#include "rosidl_runtime_cpp/bounded_vector.hpp"
#include "rosidl_runtime_cpp/message_initialization.hpp"


#ifndef _WIN32
# define DEPRECATED__menu_order_interfaces__srv__MenuTable_Request __attribute__((deprecated))
#else
# define DEPRECATED__menu_order_interfaces__srv__MenuTable_Request __declspec(deprecated)
#endif

namespace menu_order_interfaces
{

namespace srv
{

// message struct
template<class ContainerAllocator>
struct MenuTable_Request_
{
  using Type = MenuTable_Request_<ContainerAllocator>;

  explicit MenuTable_Request_(rosidl_runtime_cpp::MessageInitialization _init = rosidl_runtime_cpp::MessageInitialization::ALL)
  {
    if (rosidl_runtime_cpp::MessageInitialization::ALL == _init ||
      rosidl_runtime_cpp::MessageInitialization::ZERO == _init)
    {
      this->request_type = "";
    }
  }

  explicit MenuTable_Request_(const ContainerAllocator & _alloc, rosidl_runtime_cpp::MessageInitialization _init = rosidl_runtime_cpp::MessageInitialization::ALL)
  : request_type(_alloc)
  {
    if (rosidl_runtime_cpp::MessageInitialization::ALL == _init ||
      rosidl_runtime_cpp::MessageInitialization::ZERO == _init)
    {
      this->request_type = "";
    }
  }

  // field types and members
  using _request_type_type =
    std::basic_string<char, std::char_traits<char>, typename std::allocator_traits<ContainerAllocator>::template rebind_alloc<char>>;
  _request_type_type request_type;

  // setters for named parameter idiom
  Type & set__request_type(
    const std::basic_string<char, std::char_traits<char>, typename std::allocator_traits<ContainerAllocator>::template rebind_alloc<char>> & _arg)
  {
    this->request_type = _arg;
    return *this;
  }

  // constant declarations

  // pointer types
  using RawPtr =
    menu_order_interfaces::srv::MenuTable_Request_<ContainerAllocator> *;
  using ConstRawPtr =
    const menu_order_interfaces::srv::MenuTable_Request_<ContainerAllocator> *;
  using SharedPtr =
    std::shared_ptr<menu_order_interfaces::srv::MenuTable_Request_<ContainerAllocator>>;
  using ConstSharedPtr =
    std::shared_ptr<menu_order_interfaces::srv::MenuTable_Request_<ContainerAllocator> const>;

  template<typename Deleter = std::default_delete<
      menu_order_interfaces::srv::MenuTable_Request_<ContainerAllocator>>>
  using UniquePtrWithDeleter =
    std::unique_ptr<menu_order_interfaces::srv::MenuTable_Request_<ContainerAllocator>, Deleter>;

  using UniquePtr = UniquePtrWithDeleter<>;

  template<typename Deleter = std::default_delete<
      menu_order_interfaces::srv::MenuTable_Request_<ContainerAllocator>>>
  using ConstUniquePtrWithDeleter =
    std::unique_ptr<menu_order_interfaces::srv::MenuTable_Request_<ContainerAllocator> const, Deleter>;
  using ConstUniquePtr = ConstUniquePtrWithDeleter<>;

  using WeakPtr =
    std::weak_ptr<menu_order_interfaces::srv::MenuTable_Request_<ContainerAllocator>>;
  using ConstWeakPtr =
    std::weak_ptr<menu_order_interfaces::srv::MenuTable_Request_<ContainerAllocator> const>;

  // pointer types similar to ROS 1, use SharedPtr / ConstSharedPtr instead
  // NOTE: Can't use 'using' here because GNU C++ can't parse attributes properly
  typedef DEPRECATED__menu_order_interfaces__srv__MenuTable_Request
    std::shared_ptr<menu_order_interfaces::srv::MenuTable_Request_<ContainerAllocator>>
    Ptr;
  typedef DEPRECATED__menu_order_interfaces__srv__MenuTable_Request
    std::shared_ptr<menu_order_interfaces::srv::MenuTable_Request_<ContainerAllocator> const>
    ConstPtr;

  // comparison operators
  bool operator==(const MenuTable_Request_ & other) const
  {
    if (this->request_type != other.request_type) {
      return false;
    }
    return true;
  }
  bool operator!=(const MenuTable_Request_ & other) const
  {
    return !this->operator==(other);
  }
};  // struct MenuTable_Request_

// alias to use template instance with default allocator
using MenuTable_Request =
  menu_order_interfaces::srv::MenuTable_Request_<std::allocator<void>>;

// constant definitions

}  // namespace srv

}  // namespace menu_order_interfaces


#ifndef _WIN32
# define DEPRECATED__menu_order_interfaces__srv__MenuTable_Response __attribute__((deprecated))
#else
# define DEPRECATED__menu_order_interfaces__srv__MenuTable_Response __declspec(deprecated)
#endif

namespace menu_order_interfaces
{

namespace srv
{

// message struct
template<class ContainerAllocator>
struct MenuTable_Response_
{
  using Type = MenuTable_Response_<ContainerAllocator>;

  explicit MenuTable_Response_(rosidl_runtime_cpp::MessageInitialization _init = rosidl_runtime_cpp::MessageInitialization::ALL)
  {
    (void)_init;
  }

  explicit MenuTable_Response_(const ContainerAllocator & _alloc, rosidl_runtime_cpp::MessageInitialization _init = rosidl_runtime_cpp::MessageInitialization::ALL)
  {
    (void)_init;
    (void)_alloc;
  }

  // field types and members
  using _table_data_type =
    std::vector<std::basic_string<char, std::char_traits<char>, typename std::allocator_traits<ContainerAllocator>::template rebind_alloc<char>>, typename std::allocator_traits<ContainerAllocator>::template rebind_alloc<std::basic_string<char, std::char_traits<char>, typename std::allocator_traits<ContainerAllocator>::template rebind_alloc<char>>>>;
  _table_data_type table_data;

  // setters for named parameter idiom
  Type & set__table_data(
    const std::vector<std::basic_string<char, std::char_traits<char>, typename std::allocator_traits<ContainerAllocator>::template rebind_alloc<char>>, typename std::allocator_traits<ContainerAllocator>::template rebind_alloc<std::basic_string<char, std::char_traits<char>, typename std::allocator_traits<ContainerAllocator>::template rebind_alloc<char>>>> & _arg)
  {
    this->table_data = _arg;
    return *this;
  }

  // constant declarations

  // pointer types
  using RawPtr =
    menu_order_interfaces::srv::MenuTable_Response_<ContainerAllocator> *;
  using ConstRawPtr =
    const menu_order_interfaces::srv::MenuTable_Response_<ContainerAllocator> *;
  using SharedPtr =
    std::shared_ptr<menu_order_interfaces::srv::MenuTable_Response_<ContainerAllocator>>;
  using ConstSharedPtr =
    std::shared_ptr<menu_order_interfaces::srv::MenuTable_Response_<ContainerAllocator> const>;

  template<typename Deleter = std::default_delete<
      menu_order_interfaces::srv::MenuTable_Response_<ContainerAllocator>>>
  using UniquePtrWithDeleter =
    std::unique_ptr<menu_order_interfaces::srv::MenuTable_Response_<ContainerAllocator>, Deleter>;

  using UniquePtr = UniquePtrWithDeleter<>;

  template<typename Deleter = std::default_delete<
      menu_order_interfaces::srv::MenuTable_Response_<ContainerAllocator>>>
  using ConstUniquePtrWithDeleter =
    std::unique_ptr<menu_order_interfaces::srv::MenuTable_Response_<ContainerAllocator> const, Deleter>;
  using ConstUniquePtr = ConstUniquePtrWithDeleter<>;

  using WeakPtr =
    std::weak_ptr<menu_order_interfaces::srv::MenuTable_Response_<ContainerAllocator>>;
  using ConstWeakPtr =
    std::weak_ptr<menu_order_interfaces::srv::MenuTable_Response_<ContainerAllocator> const>;

  // pointer types similar to ROS 1, use SharedPtr / ConstSharedPtr instead
  // NOTE: Can't use 'using' here because GNU C++ can't parse attributes properly
  typedef DEPRECATED__menu_order_interfaces__srv__MenuTable_Response
    std::shared_ptr<menu_order_interfaces::srv::MenuTable_Response_<ContainerAllocator>>
    Ptr;
  typedef DEPRECATED__menu_order_interfaces__srv__MenuTable_Response
    std::shared_ptr<menu_order_interfaces::srv::MenuTable_Response_<ContainerAllocator> const>
    ConstPtr;

  // comparison operators
  bool operator==(const MenuTable_Response_ & other) const
  {
    if (this->table_data != other.table_data) {
      return false;
    }
    return true;
  }
  bool operator!=(const MenuTable_Response_ & other) const
  {
    return !this->operator==(other);
  }
};  // struct MenuTable_Response_

// alias to use template instance with default allocator
using MenuTable_Response =
  menu_order_interfaces::srv::MenuTable_Response_<std::allocator<void>>;

// constant definitions

}  // namespace srv

}  // namespace menu_order_interfaces

namespace menu_order_interfaces
{

namespace srv
{

struct MenuTable
{
  using Request = menu_order_interfaces::srv::MenuTable_Request;
  using Response = menu_order_interfaces::srv::MenuTable_Response;
};

}  // namespace srv

}  // namespace menu_order_interfaces

#endif  // MENU_ORDER_INTERFACES__SRV__DETAIL__MENU_TABLE__STRUCT_HPP_
