// generated from rosidl_generator_cpp/resource/idl__struct.hpp.em
// with input from menu_order_interfaces:msg/Order.idl
// generated code does not contain a copyright notice

#ifndef MENU_ORDER_INTERFACES__MSG__DETAIL__ORDER__STRUCT_HPP_
#define MENU_ORDER_INTERFACES__MSG__DETAIL__ORDER__STRUCT_HPP_

#include <algorithm>
#include <array>
#include <memory>
#include <string>
#include <vector>

#include "rosidl_runtime_cpp/bounded_vector.hpp"
#include "rosidl_runtime_cpp/message_initialization.hpp"


#ifndef _WIN32
# define DEPRECATED__menu_order_interfaces__msg__Order __attribute__((deprecated))
#else
# define DEPRECATED__menu_order_interfaces__msg__Order __declspec(deprecated)
#endif

namespace menu_order_interfaces
{

namespace msg
{

// message struct
template<class ContainerAllocator>
struct Order_
{
  using Type = Order_<ContainerAllocator>;

  explicit Order_(rosidl_runtime_cpp::MessageInitialization _init = rosidl_runtime_cpp::MessageInitialization::ALL)
  {
    if (rosidl_runtime_cpp::MessageInitialization::ALL == _init ||
      rosidl_runtime_cpp::MessageInitialization::ZERO == _init)
    {
      this->table_id = "";
      this->menu = "";
      this->quantity = 0l;
    }
  }

  explicit Order_(const ContainerAllocator & _alloc, rosidl_runtime_cpp::MessageInitialization _init = rosidl_runtime_cpp::MessageInitialization::ALL)
  : table_id(_alloc),
    menu(_alloc)
  {
    if (rosidl_runtime_cpp::MessageInitialization::ALL == _init ||
      rosidl_runtime_cpp::MessageInitialization::ZERO == _init)
    {
      this->table_id = "";
      this->menu = "";
      this->quantity = 0l;
    }
  }

  // field types and members
  using _table_id_type =
    std::basic_string<char, std::char_traits<char>, typename std::allocator_traits<ContainerAllocator>::template rebind_alloc<char>>;
  _table_id_type table_id;
  using _menu_type =
    std::basic_string<char, std::char_traits<char>, typename std::allocator_traits<ContainerAllocator>::template rebind_alloc<char>>;
  _menu_type menu;
  using _quantity_type =
    int32_t;
  _quantity_type quantity;

  // setters for named parameter idiom
  Type & set__table_id(
    const std::basic_string<char, std::char_traits<char>, typename std::allocator_traits<ContainerAllocator>::template rebind_alloc<char>> & _arg)
  {
    this->table_id = _arg;
    return *this;
  }
  Type & set__menu(
    const std::basic_string<char, std::char_traits<char>, typename std::allocator_traits<ContainerAllocator>::template rebind_alloc<char>> & _arg)
  {
    this->menu = _arg;
    return *this;
  }
  Type & set__quantity(
    const int32_t & _arg)
  {
    this->quantity = _arg;
    return *this;
  }

  // constant declarations

  // pointer types
  using RawPtr =
    menu_order_interfaces::msg::Order_<ContainerAllocator> *;
  using ConstRawPtr =
    const menu_order_interfaces::msg::Order_<ContainerAllocator> *;
  using SharedPtr =
    std::shared_ptr<menu_order_interfaces::msg::Order_<ContainerAllocator>>;
  using ConstSharedPtr =
    std::shared_ptr<menu_order_interfaces::msg::Order_<ContainerAllocator> const>;

  template<typename Deleter = std::default_delete<
      menu_order_interfaces::msg::Order_<ContainerAllocator>>>
  using UniquePtrWithDeleter =
    std::unique_ptr<menu_order_interfaces::msg::Order_<ContainerAllocator>, Deleter>;

  using UniquePtr = UniquePtrWithDeleter<>;

  template<typename Deleter = std::default_delete<
      menu_order_interfaces::msg::Order_<ContainerAllocator>>>
  using ConstUniquePtrWithDeleter =
    std::unique_ptr<menu_order_interfaces::msg::Order_<ContainerAllocator> const, Deleter>;
  using ConstUniquePtr = ConstUniquePtrWithDeleter<>;

  using WeakPtr =
    std::weak_ptr<menu_order_interfaces::msg::Order_<ContainerAllocator>>;
  using ConstWeakPtr =
    std::weak_ptr<menu_order_interfaces::msg::Order_<ContainerAllocator> const>;

  // pointer types similar to ROS 1, use SharedPtr / ConstSharedPtr instead
  // NOTE: Can't use 'using' here because GNU C++ can't parse attributes properly
  typedef DEPRECATED__menu_order_interfaces__msg__Order
    std::shared_ptr<menu_order_interfaces::msg::Order_<ContainerAllocator>>
    Ptr;
  typedef DEPRECATED__menu_order_interfaces__msg__Order
    std::shared_ptr<menu_order_interfaces::msg::Order_<ContainerAllocator> const>
    ConstPtr;

  // comparison operators
  bool operator==(const Order_ & other) const
  {
    if (this->table_id != other.table_id) {
      return false;
    }
    if (this->menu != other.menu) {
      return false;
    }
    if (this->quantity != other.quantity) {
      return false;
    }
    return true;
  }
  bool operator!=(const Order_ & other) const
  {
    return !this->operator==(other);
  }
};  // struct Order_

// alias to use template instance with default allocator
using Order =
  menu_order_interfaces::msg::Order_<std::allocator<void>>;

// constant definitions

}  // namespace msg

}  // namespace menu_order_interfaces

#endif  // MENU_ORDER_INTERFACES__MSG__DETAIL__ORDER__STRUCT_HPP_
