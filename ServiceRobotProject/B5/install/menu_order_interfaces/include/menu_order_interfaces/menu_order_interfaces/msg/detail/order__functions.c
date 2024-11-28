// generated from rosidl_generator_c/resource/idl__functions.c.em
// with input from menu_order_interfaces:msg/Order.idl
// generated code does not contain a copyright notice
#include "menu_order_interfaces/msg/detail/order__functions.h"

#include <assert.h>
#include <stdbool.h>
#include <stdlib.h>
#include <string.h>

#include "rcutils/allocator.h"


// Include directives for member types
// Member `table_id`
// Member `menu`
#include "rosidl_runtime_c/string_functions.h"

bool
menu_order_interfaces__msg__Order__init(menu_order_interfaces__msg__Order * msg)
{
  if (!msg) {
    return false;
  }
  // table_id
  if (!rosidl_runtime_c__String__init(&msg->table_id)) {
    menu_order_interfaces__msg__Order__fini(msg);
    return false;
  }
  // menu
  if (!rosidl_runtime_c__String__init(&msg->menu)) {
    menu_order_interfaces__msg__Order__fini(msg);
    return false;
  }
  // quantity
  return true;
}

void
menu_order_interfaces__msg__Order__fini(menu_order_interfaces__msg__Order * msg)
{
  if (!msg) {
    return;
  }
  // table_id
  rosidl_runtime_c__String__fini(&msg->table_id);
  // menu
  rosidl_runtime_c__String__fini(&msg->menu);
  // quantity
}

bool
menu_order_interfaces__msg__Order__are_equal(const menu_order_interfaces__msg__Order * lhs, const menu_order_interfaces__msg__Order * rhs)
{
  if (!lhs || !rhs) {
    return false;
  }
  // table_id
  if (!rosidl_runtime_c__String__are_equal(
      &(lhs->table_id), &(rhs->table_id)))
  {
    return false;
  }
  // menu
  if (!rosidl_runtime_c__String__are_equal(
      &(lhs->menu), &(rhs->menu)))
  {
    return false;
  }
  // quantity
  if (lhs->quantity != rhs->quantity) {
    return false;
  }
  return true;
}

bool
menu_order_interfaces__msg__Order__copy(
  const menu_order_interfaces__msg__Order * input,
  menu_order_interfaces__msg__Order * output)
{
  if (!input || !output) {
    return false;
  }
  // table_id
  if (!rosidl_runtime_c__String__copy(
      &(input->table_id), &(output->table_id)))
  {
    return false;
  }
  // menu
  if (!rosidl_runtime_c__String__copy(
      &(input->menu), &(output->menu)))
  {
    return false;
  }
  // quantity
  output->quantity = input->quantity;
  return true;
}

menu_order_interfaces__msg__Order *
menu_order_interfaces__msg__Order__create()
{
  rcutils_allocator_t allocator = rcutils_get_default_allocator();
  menu_order_interfaces__msg__Order * msg = (menu_order_interfaces__msg__Order *)allocator.allocate(sizeof(menu_order_interfaces__msg__Order), allocator.state);
  if (!msg) {
    return NULL;
  }
  memset(msg, 0, sizeof(menu_order_interfaces__msg__Order));
  bool success = menu_order_interfaces__msg__Order__init(msg);
  if (!success) {
    allocator.deallocate(msg, allocator.state);
    return NULL;
  }
  return msg;
}

void
menu_order_interfaces__msg__Order__destroy(menu_order_interfaces__msg__Order * msg)
{
  rcutils_allocator_t allocator = rcutils_get_default_allocator();
  if (msg) {
    menu_order_interfaces__msg__Order__fini(msg);
  }
  allocator.deallocate(msg, allocator.state);
}


bool
menu_order_interfaces__msg__Order__Sequence__init(menu_order_interfaces__msg__Order__Sequence * array, size_t size)
{
  if (!array) {
    return false;
  }
  rcutils_allocator_t allocator = rcutils_get_default_allocator();
  menu_order_interfaces__msg__Order * data = NULL;

  if (size) {
    data = (menu_order_interfaces__msg__Order *)allocator.zero_allocate(size, sizeof(menu_order_interfaces__msg__Order), allocator.state);
    if (!data) {
      return false;
    }
    // initialize all array elements
    size_t i;
    for (i = 0; i < size; ++i) {
      bool success = menu_order_interfaces__msg__Order__init(&data[i]);
      if (!success) {
        break;
      }
    }
    if (i < size) {
      // if initialization failed finalize the already initialized array elements
      for (; i > 0; --i) {
        menu_order_interfaces__msg__Order__fini(&data[i - 1]);
      }
      allocator.deallocate(data, allocator.state);
      return false;
    }
  }
  array->data = data;
  array->size = size;
  array->capacity = size;
  return true;
}

void
menu_order_interfaces__msg__Order__Sequence__fini(menu_order_interfaces__msg__Order__Sequence * array)
{
  if (!array) {
    return;
  }
  rcutils_allocator_t allocator = rcutils_get_default_allocator();

  if (array->data) {
    // ensure that data and capacity values are consistent
    assert(array->capacity > 0);
    // finalize all array elements
    for (size_t i = 0; i < array->capacity; ++i) {
      menu_order_interfaces__msg__Order__fini(&array->data[i]);
    }
    allocator.deallocate(array->data, allocator.state);
    array->data = NULL;
    array->size = 0;
    array->capacity = 0;
  } else {
    // ensure that data, size, and capacity values are consistent
    assert(0 == array->size);
    assert(0 == array->capacity);
  }
}

menu_order_interfaces__msg__Order__Sequence *
menu_order_interfaces__msg__Order__Sequence__create(size_t size)
{
  rcutils_allocator_t allocator = rcutils_get_default_allocator();
  menu_order_interfaces__msg__Order__Sequence * array = (menu_order_interfaces__msg__Order__Sequence *)allocator.allocate(sizeof(menu_order_interfaces__msg__Order__Sequence), allocator.state);
  if (!array) {
    return NULL;
  }
  bool success = menu_order_interfaces__msg__Order__Sequence__init(array, size);
  if (!success) {
    allocator.deallocate(array, allocator.state);
    return NULL;
  }
  return array;
}

void
menu_order_interfaces__msg__Order__Sequence__destroy(menu_order_interfaces__msg__Order__Sequence * array)
{
  rcutils_allocator_t allocator = rcutils_get_default_allocator();
  if (array) {
    menu_order_interfaces__msg__Order__Sequence__fini(array);
  }
  allocator.deallocate(array, allocator.state);
}

bool
menu_order_interfaces__msg__Order__Sequence__are_equal(const menu_order_interfaces__msg__Order__Sequence * lhs, const menu_order_interfaces__msg__Order__Sequence * rhs)
{
  if (!lhs || !rhs) {
    return false;
  }
  if (lhs->size != rhs->size) {
    return false;
  }
  for (size_t i = 0; i < lhs->size; ++i) {
    if (!menu_order_interfaces__msg__Order__are_equal(&(lhs->data[i]), &(rhs->data[i]))) {
      return false;
    }
  }
  return true;
}

bool
menu_order_interfaces__msg__Order__Sequence__copy(
  const menu_order_interfaces__msg__Order__Sequence * input,
  menu_order_interfaces__msg__Order__Sequence * output)
{
  if (!input || !output) {
    return false;
  }
  if (output->capacity < input->size) {
    const size_t allocation_size =
      input->size * sizeof(menu_order_interfaces__msg__Order);
    rcutils_allocator_t allocator = rcutils_get_default_allocator();
    menu_order_interfaces__msg__Order * data =
      (menu_order_interfaces__msg__Order *)allocator.reallocate(
      output->data, allocation_size, allocator.state);
    if (!data) {
      return false;
    }
    // If reallocation succeeded, memory may or may not have been moved
    // to fulfill the allocation request, invalidating output->data.
    output->data = data;
    for (size_t i = output->capacity; i < input->size; ++i) {
      if (!menu_order_interfaces__msg__Order__init(&output->data[i])) {
        // If initialization of any new item fails, roll back
        // all previously initialized items. Existing items
        // in output are to be left unmodified.
        for (; i-- > output->capacity; ) {
          menu_order_interfaces__msg__Order__fini(&output->data[i]);
        }
        return false;
      }
    }
    output->capacity = input->size;
  }
  output->size = input->size;
  for (size_t i = 0; i < input->size; ++i) {
    if (!menu_order_interfaces__msg__Order__copy(
        &(input->data[i]), &(output->data[i])))
    {
      return false;
    }
  }
  return true;
}
