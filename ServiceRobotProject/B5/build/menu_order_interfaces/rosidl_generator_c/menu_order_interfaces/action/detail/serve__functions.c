// generated from rosidl_generator_c/resource/idl__functions.c.em
// with input from menu_order_interfaces:action/Serve.idl
// generated code does not contain a copyright notice
#include "menu_order_interfaces/action/detail/serve__functions.h"

#include <assert.h>
#include <stdbool.h>
#include <stdlib.h>
#include <string.h>

#include "rcutils/allocator.h"


// Include directives for member types
// Member `table_id`
#include "rosidl_runtime_c/string_functions.h"

bool
menu_order_interfaces__action__Serve_Goal__init(menu_order_interfaces__action__Serve_Goal * msg)
{
  if (!msg) {
    return false;
  }
  // table_id
  if (!rosidl_runtime_c__String__init(&msg->table_id)) {
    menu_order_interfaces__action__Serve_Goal__fini(msg);
    return false;
  }
  // x
  // y
  return true;
}

void
menu_order_interfaces__action__Serve_Goal__fini(menu_order_interfaces__action__Serve_Goal * msg)
{
  if (!msg) {
    return;
  }
  // table_id
  rosidl_runtime_c__String__fini(&msg->table_id);
  // x
  // y
}

bool
menu_order_interfaces__action__Serve_Goal__are_equal(const menu_order_interfaces__action__Serve_Goal * lhs, const menu_order_interfaces__action__Serve_Goal * rhs)
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
  // x
  if (lhs->x != rhs->x) {
    return false;
  }
  // y
  if (lhs->y != rhs->y) {
    return false;
  }
  return true;
}

bool
menu_order_interfaces__action__Serve_Goal__copy(
  const menu_order_interfaces__action__Serve_Goal * input,
  menu_order_interfaces__action__Serve_Goal * output)
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
  // x
  output->x = input->x;
  // y
  output->y = input->y;
  return true;
}

menu_order_interfaces__action__Serve_Goal *
menu_order_interfaces__action__Serve_Goal__create()
{
  rcutils_allocator_t allocator = rcutils_get_default_allocator();
  menu_order_interfaces__action__Serve_Goal * msg = (menu_order_interfaces__action__Serve_Goal *)allocator.allocate(sizeof(menu_order_interfaces__action__Serve_Goal), allocator.state);
  if (!msg) {
    return NULL;
  }
  memset(msg, 0, sizeof(menu_order_interfaces__action__Serve_Goal));
  bool success = menu_order_interfaces__action__Serve_Goal__init(msg);
  if (!success) {
    allocator.deallocate(msg, allocator.state);
    return NULL;
  }
  return msg;
}

void
menu_order_interfaces__action__Serve_Goal__destroy(menu_order_interfaces__action__Serve_Goal * msg)
{
  rcutils_allocator_t allocator = rcutils_get_default_allocator();
  if (msg) {
    menu_order_interfaces__action__Serve_Goal__fini(msg);
  }
  allocator.deallocate(msg, allocator.state);
}


bool
menu_order_interfaces__action__Serve_Goal__Sequence__init(menu_order_interfaces__action__Serve_Goal__Sequence * array, size_t size)
{
  if (!array) {
    return false;
  }
  rcutils_allocator_t allocator = rcutils_get_default_allocator();
  menu_order_interfaces__action__Serve_Goal * data = NULL;

  if (size) {
    data = (menu_order_interfaces__action__Serve_Goal *)allocator.zero_allocate(size, sizeof(menu_order_interfaces__action__Serve_Goal), allocator.state);
    if (!data) {
      return false;
    }
    // initialize all array elements
    size_t i;
    for (i = 0; i < size; ++i) {
      bool success = menu_order_interfaces__action__Serve_Goal__init(&data[i]);
      if (!success) {
        break;
      }
    }
    if (i < size) {
      // if initialization failed finalize the already initialized array elements
      for (; i > 0; --i) {
        menu_order_interfaces__action__Serve_Goal__fini(&data[i - 1]);
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
menu_order_interfaces__action__Serve_Goal__Sequence__fini(menu_order_interfaces__action__Serve_Goal__Sequence * array)
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
      menu_order_interfaces__action__Serve_Goal__fini(&array->data[i]);
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

menu_order_interfaces__action__Serve_Goal__Sequence *
menu_order_interfaces__action__Serve_Goal__Sequence__create(size_t size)
{
  rcutils_allocator_t allocator = rcutils_get_default_allocator();
  menu_order_interfaces__action__Serve_Goal__Sequence * array = (menu_order_interfaces__action__Serve_Goal__Sequence *)allocator.allocate(sizeof(menu_order_interfaces__action__Serve_Goal__Sequence), allocator.state);
  if (!array) {
    return NULL;
  }
  bool success = menu_order_interfaces__action__Serve_Goal__Sequence__init(array, size);
  if (!success) {
    allocator.deallocate(array, allocator.state);
    return NULL;
  }
  return array;
}

void
menu_order_interfaces__action__Serve_Goal__Sequence__destroy(menu_order_interfaces__action__Serve_Goal__Sequence * array)
{
  rcutils_allocator_t allocator = rcutils_get_default_allocator();
  if (array) {
    menu_order_interfaces__action__Serve_Goal__Sequence__fini(array);
  }
  allocator.deallocate(array, allocator.state);
}

bool
menu_order_interfaces__action__Serve_Goal__Sequence__are_equal(const menu_order_interfaces__action__Serve_Goal__Sequence * lhs, const menu_order_interfaces__action__Serve_Goal__Sequence * rhs)
{
  if (!lhs || !rhs) {
    return false;
  }
  if (lhs->size != rhs->size) {
    return false;
  }
  for (size_t i = 0; i < lhs->size; ++i) {
    if (!menu_order_interfaces__action__Serve_Goal__are_equal(&(lhs->data[i]), &(rhs->data[i]))) {
      return false;
    }
  }
  return true;
}

bool
menu_order_interfaces__action__Serve_Goal__Sequence__copy(
  const menu_order_interfaces__action__Serve_Goal__Sequence * input,
  menu_order_interfaces__action__Serve_Goal__Sequence * output)
{
  if (!input || !output) {
    return false;
  }
  if (output->capacity < input->size) {
    const size_t allocation_size =
      input->size * sizeof(menu_order_interfaces__action__Serve_Goal);
    rcutils_allocator_t allocator = rcutils_get_default_allocator();
    menu_order_interfaces__action__Serve_Goal * data =
      (menu_order_interfaces__action__Serve_Goal *)allocator.reallocate(
      output->data, allocation_size, allocator.state);
    if (!data) {
      return false;
    }
    // If reallocation succeeded, memory may or may not have been moved
    // to fulfill the allocation request, invalidating output->data.
    output->data = data;
    for (size_t i = output->capacity; i < input->size; ++i) {
      if (!menu_order_interfaces__action__Serve_Goal__init(&output->data[i])) {
        // If initialization of any new item fails, roll back
        // all previously initialized items. Existing items
        // in output are to be left unmodified.
        for (; i-- > output->capacity; ) {
          menu_order_interfaces__action__Serve_Goal__fini(&output->data[i]);
        }
        return false;
      }
    }
    output->capacity = input->size;
  }
  output->size = input->size;
  for (size_t i = 0; i < input->size; ++i) {
    if (!menu_order_interfaces__action__Serve_Goal__copy(
        &(input->data[i]), &(output->data[i])))
    {
      return false;
    }
  }
  return true;
}


// Include directives for member types
// Member `message`
// already included above
// #include "rosidl_runtime_c/string_functions.h"

bool
menu_order_interfaces__action__Serve_Result__init(menu_order_interfaces__action__Serve_Result * msg)
{
  if (!msg) {
    return false;
  }
  // reached
  // message
  if (!rosidl_runtime_c__String__init(&msg->message)) {
    menu_order_interfaces__action__Serve_Result__fini(msg);
    return false;
  }
  return true;
}

void
menu_order_interfaces__action__Serve_Result__fini(menu_order_interfaces__action__Serve_Result * msg)
{
  if (!msg) {
    return;
  }
  // reached
  // message
  rosidl_runtime_c__String__fini(&msg->message);
}

bool
menu_order_interfaces__action__Serve_Result__are_equal(const menu_order_interfaces__action__Serve_Result * lhs, const menu_order_interfaces__action__Serve_Result * rhs)
{
  if (!lhs || !rhs) {
    return false;
  }
  // reached
  if (lhs->reached != rhs->reached) {
    return false;
  }
  // message
  if (!rosidl_runtime_c__String__are_equal(
      &(lhs->message), &(rhs->message)))
  {
    return false;
  }
  return true;
}

bool
menu_order_interfaces__action__Serve_Result__copy(
  const menu_order_interfaces__action__Serve_Result * input,
  menu_order_interfaces__action__Serve_Result * output)
{
  if (!input || !output) {
    return false;
  }
  // reached
  output->reached = input->reached;
  // message
  if (!rosidl_runtime_c__String__copy(
      &(input->message), &(output->message)))
  {
    return false;
  }
  return true;
}

menu_order_interfaces__action__Serve_Result *
menu_order_interfaces__action__Serve_Result__create()
{
  rcutils_allocator_t allocator = rcutils_get_default_allocator();
  menu_order_interfaces__action__Serve_Result * msg = (menu_order_interfaces__action__Serve_Result *)allocator.allocate(sizeof(menu_order_interfaces__action__Serve_Result), allocator.state);
  if (!msg) {
    return NULL;
  }
  memset(msg, 0, sizeof(menu_order_interfaces__action__Serve_Result));
  bool success = menu_order_interfaces__action__Serve_Result__init(msg);
  if (!success) {
    allocator.deallocate(msg, allocator.state);
    return NULL;
  }
  return msg;
}

void
menu_order_interfaces__action__Serve_Result__destroy(menu_order_interfaces__action__Serve_Result * msg)
{
  rcutils_allocator_t allocator = rcutils_get_default_allocator();
  if (msg) {
    menu_order_interfaces__action__Serve_Result__fini(msg);
  }
  allocator.deallocate(msg, allocator.state);
}


bool
menu_order_interfaces__action__Serve_Result__Sequence__init(menu_order_interfaces__action__Serve_Result__Sequence * array, size_t size)
{
  if (!array) {
    return false;
  }
  rcutils_allocator_t allocator = rcutils_get_default_allocator();
  menu_order_interfaces__action__Serve_Result * data = NULL;

  if (size) {
    data = (menu_order_interfaces__action__Serve_Result *)allocator.zero_allocate(size, sizeof(menu_order_interfaces__action__Serve_Result), allocator.state);
    if (!data) {
      return false;
    }
    // initialize all array elements
    size_t i;
    for (i = 0; i < size; ++i) {
      bool success = menu_order_interfaces__action__Serve_Result__init(&data[i]);
      if (!success) {
        break;
      }
    }
    if (i < size) {
      // if initialization failed finalize the already initialized array elements
      for (; i > 0; --i) {
        menu_order_interfaces__action__Serve_Result__fini(&data[i - 1]);
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
menu_order_interfaces__action__Serve_Result__Sequence__fini(menu_order_interfaces__action__Serve_Result__Sequence * array)
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
      menu_order_interfaces__action__Serve_Result__fini(&array->data[i]);
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

menu_order_interfaces__action__Serve_Result__Sequence *
menu_order_interfaces__action__Serve_Result__Sequence__create(size_t size)
{
  rcutils_allocator_t allocator = rcutils_get_default_allocator();
  menu_order_interfaces__action__Serve_Result__Sequence * array = (menu_order_interfaces__action__Serve_Result__Sequence *)allocator.allocate(sizeof(menu_order_interfaces__action__Serve_Result__Sequence), allocator.state);
  if (!array) {
    return NULL;
  }
  bool success = menu_order_interfaces__action__Serve_Result__Sequence__init(array, size);
  if (!success) {
    allocator.deallocate(array, allocator.state);
    return NULL;
  }
  return array;
}

void
menu_order_interfaces__action__Serve_Result__Sequence__destroy(menu_order_interfaces__action__Serve_Result__Sequence * array)
{
  rcutils_allocator_t allocator = rcutils_get_default_allocator();
  if (array) {
    menu_order_interfaces__action__Serve_Result__Sequence__fini(array);
  }
  allocator.deallocate(array, allocator.state);
}

bool
menu_order_interfaces__action__Serve_Result__Sequence__are_equal(const menu_order_interfaces__action__Serve_Result__Sequence * lhs, const menu_order_interfaces__action__Serve_Result__Sequence * rhs)
{
  if (!lhs || !rhs) {
    return false;
  }
  if (lhs->size != rhs->size) {
    return false;
  }
  for (size_t i = 0; i < lhs->size; ++i) {
    if (!menu_order_interfaces__action__Serve_Result__are_equal(&(lhs->data[i]), &(rhs->data[i]))) {
      return false;
    }
  }
  return true;
}

bool
menu_order_interfaces__action__Serve_Result__Sequence__copy(
  const menu_order_interfaces__action__Serve_Result__Sequence * input,
  menu_order_interfaces__action__Serve_Result__Sequence * output)
{
  if (!input || !output) {
    return false;
  }
  if (output->capacity < input->size) {
    const size_t allocation_size =
      input->size * sizeof(menu_order_interfaces__action__Serve_Result);
    rcutils_allocator_t allocator = rcutils_get_default_allocator();
    menu_order_interfaces__action__Serve_Result * data =
      (menu_order_interfaces__action__Serve_Result *)allocator.reallocate(
      output->data, allocation_size, allocator.state);
    if (!data) {
      return false;
    }
    // If reallocation succeeded, memory may or may not have been moved
    // to fulfill the allocation request, invalidating output->data.
    output->data = data;
    for (size_t i = output->capacity; i < input->size; ++i) {
      if (!menu_order_interfaces__action__Serve_Result__init(&output->data[i])) {
        // If initialization of any new item fails, roll back
        // all previously initialized items. Existing items
        // in output are to be left unmodified.
        for (; i-- > output->capacity; ) {
          menu_order_interfaces__action__Serve_Result__fini(&output->data[i]);
        }
        return false;
      }
    }
    output->capacity = input->size;
  }
  output->size = input->size;
  for (size_t i = 0; i < input->size; ++i) {
    if (!menu_order_interfaces__action__Serve_Result__copy(
        &(input->data[i]), &(output->data[i])))
    {
      return false;
    }
  }
  return true;
}


// Include directives for member types
// Member `status`
// already included above
// #include "rosidl_runtime_c/string_functions.h"

bool
menu_order_interfaces__action__Serve_Feedback__init(menu_order_interfaces__action__Serve_Feedback * msg)
{
  if (!msg) {
    return false;
  }
  // progress
  // status
  if (!rosidl_runtime_c__String__init(&msg->status)) {
    menu_order_interfaces__action__Serve_Feedback__fini(msg);
    return false;
  }
  return true;
}

void
menu_order_interfaces__action__Serve_Feedback__fini(menu_order_interfaces__action__Serve_Feedback * msg)
{
  if (!msg) {
    return;
  }
  // progress
  // status
  rosidl_runtime_c__String__fini(&msg->status);
}

bool
menu_order_interfaces__action__Serve_Feedback__are_equal(const menu_order_interfaces__action__Serve_Feedback * lhs, const menu_order_interfaces__action__Serve_Feedback * rhs)
{
  if (!lhs || !rhs) {
    return false;
  }
  // progress
  if (lhs->progress != rhs->progress) {
    return false;
  }
  // status
  if (!rosidl_runtime_c__String__are_equal(
      &(lhs->status), &(rhs->status)))
  {
    return false;
  }
  return true;
}

bool
menu_order_interfaces__action__Serve_Feedback__copy(
  const menu_order_interfaces__action__Serve_Feedback * input,
  menu_order_interfaces__action__Serve_Feedback * output)
{
  if (!input || !output) {
    return false;
  }
  // progress
  output->progress = input->progress;
  // status
  if (!rosidl_runtime_c__String__copy(
      &(input->status), &(output->status)))
  {
    return false;
  }
  return true;
}

menu_order_interfaces__action__Serve_Feedback *
menu_order_interfaces__action__Serve_Feedback__create()
{
  rcutils_allocator_t allocator = rcutils_get_default_allocator();
  menu_order_interfaces__action__Serve_Feedback * msg = (menu_order_interfaces__action__Serve_Feedback *)allocator.allocate(sizeof(menu_order_interfaces__action__Serve_Feedback), allocator.state);
  if (!msg) {
    return NULL;
  }
  memset(msg, 0, sizeof(menu_order_interfaces__action__Serve_Feedback));
  bool success = menu_order_interfaces__action__Serve_Feedback__init(msg);
  if (!success) {
    allocator.deallocate(msg, allocator.state);
    return NULL;
  }
  return msg;
}

void
menu_order_interfaces__action__Serve_Feedback__destroy(menu_order_interfaces__action__Serve_Feedback * msg)
{
  rcutils_allocator_t allocator = rcutils_get_default_allocator();
  if (msg) {
    menu_order_interfaces__action__Serve_Feedback__fini(msg);
  }
  allocator.deallocate(msg, allocator.state);
}


bool
menu_order_interfaces__action__Serve_Feedback__Sequence__init(menu_order_interfaces__action__Serve_Feedback__Sequence * array, size_t size)
{
  if (!array) {
    return false;
  }
  rcutils_allocator_t allocator = rcutils_get_default_allocator();
  menu_order_interfaces__action__Serve_Feedback * data = NULL;

  if (size) {
    data = (menu_order_interfaces__action__Serve_Feedback *)allocator.zero_allocate(size, sizeof(menu_order_interfaces__action__Serve_Feedback), allocator.state);
    if (!data) {
      return false;
    }
    // initialize all array elements
    size_t i;
    for (i = 0; i < size; ++i) {
      bool success = menu_order_interfaces__action__Serve_Feedback__init(&data[i]);
      if (!success) {
        break;
      }
    }
    if (i < size) {
      // if initialization failed finalize the already initialized array elements
      for (; i > 0; --i) {
        menu_order_interfaces__action__Serve_Feedback__fini(&data[i - 1]);
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
menu_order_interfaces__action__Serve_Feedback__Sequence__fini(menu_order_interfaces__action__Serve_Feedback__Sequence * array)
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
      menu_order_interfaces__action__Serve_Feedback__fini(&array->data[i]);
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

menu_order_interfaces__action__Serve_Feedback__Sequence *
menu_order_interfaces__action__Serve_Feedback__Sequence__create(size_t size)
{
  rcutils_allocator_t allocator = rcutils_get_default_allocator();
  menu_order_interfaces__action__Serve_Feedback__Sequence * array = (menu_order_interfaces__action__Serve_Feedback__Sequence *)allocator.allocate(sizeof(menu_order_interfaces__action__Serve_Feedback__Sequence), allocator.state);
  if (!array) {
    return NULL;
  }
  bool success = menu_order_interfaces__action__Serve_Feedback__Sequence__init(array, size);
  if (!success) {
    allocator.deallocate(array, allocator.state);
    return NULL;
  }
  return array;
}

void
menu_order_interfaces__action__Serve_Feedback__Sequence__destroy(menu_order_interfaces__action__Serve_Feedback__Sequence * array)
{
  rcutils_allocator_t allocator = rcutils_get_default_allocator();
  if (array) {
    menu_order_interfaces__action__Serve_Feedback__Sequence__fini(array);
  }
  allocator.deallocate(array, allocator.state);
}

bool
menu_order_interfaces__action__Serve_Feedback__Sequence__are_equal(const menu_order_interfaces__action__Serve_Feedback__Sequence * lhs, const menu_order_interfaces__action__Serve_Feedback__Sequence * rhs)
{
  if (!lhs || !rhs) {
    return false;
  }
  if (lhs->size != rhs->size) {
    return false;
  }
  for (size_t i = 0; i < lhs->size; ++i) {
    if (!menu_order_interfaces__action__Serve_Feedback__are_equal(&(lhs->data[i]), &(rhs->data[i]))) {
      return false;
    }
  }
  return true;
}

bool
menu_order_interfaces__action__Serve_Feedback__Sequence__copy(
  const menu_order_interfaces__action__Serve_Feedback__Sequence * input,
  menu_order_interfaces__action__Serve_Feedback__Sequence * output)
{
  if (!input || !output) {
    return false;
  }
  if (output->capacity < input->size) {
    const size_t allocation_size =
      input->size * sizeof(menu_order_interfaces__action__Serve_Feedback);
    rcutils_allocator_t allocator = rcutils_get_default_allocator();
    menu_order_interfaces__action__Serve_Feedback * data =
      (menu_order_interfaces__action__Serve_Feedback *)allocator.reallocate(
      output->data, allocation_size, allocator.state);
    if (!data) {
      return false;
    }
    // If reallocation succeeded, memory may or may not have been moved
    // to fulfill the allocation request, invalidating output->data.
    output->data = data;
    for (size_t i = output->capacity; i < input->size; ++i) {
      if (!menu_order_interfaces__action__Serve_Feedback__init(&output->data[i])) {
        // If initialization of any new item fails, roll back
        // all previously initialized items. Existing items
        // in output are to be left unmodified.
        for (; i-- > output->capacity; ) {
          menu_order_interfaces__action__Serve_Feedback__fini(&output->data[i]);
        }
        return false;
      }
    }
    output->capacity = input->size;
  }
  output->size = input->size;
  for (size_t i = 0; i < input->size; ++i) {
    if (!menu_order_interfaces__action__Serve_Feedback__copy(
        &(input->data[i]), &(output->data[i])))
    {
      return false;
    }
  }
  return true;
}


// Include directives for member types
// Member `goal_id`
#include "unique_identifier_msgs/msg/detail/uuid__functions.h"
// Member `goal`
// already included above
// #include "menu_order_interfaces/action/detail/serve__functions.h"

bool
menu_order_interfaces__action__Serve_SendGoal_Request__init(menu_order_interfaces__action__Serve_SendGoal_Request * msg)
{
  if (!msg) {
    return false;
  }
  // goal_id
  if (!unique_identifier_msgs__msg__UUID__init(&msg->goal_id)) {
    menu_order_interfaces__action__Serve_SendGoal_Request__fini(msg);
    return false;
  }
  // goal
  if (!menu_order_interfaces__action__Serve_Goal__init(&msg->goal)) {
    menu_order_interfaces__action__Serve_SendGoal_Request__fini(msg);
    return false;
  }
  return true;
}

void
menu_order_interfaces__action__Serve_SendGoal_Request__fini(menu_order_interfaces__action__Serve_SendGoal_Request * msg)
{
  if (!msg) {
    return;
  }
  // goal_id
  unique_identifier_msgs__msg__UUID__fini(&msg->goal_id);
  // goal
  menu_order_interfaces__action__Serve_Goal__fini(&msg->goal);
}

bool
menu_order_interfaces__action__Serve_SendGoal_Request__are_equal(const menu_order_interfaces__action__Serve_SendGoal_Request * lhs, const menu_order_interfaces__action__Serve_SendGoal_Request * rhs)
{
  if (!lhs || !rhs) {
    return false;
  }
  // goal_id
  if (!unique_identifier_msgs__msg__UUID__are_equal(
      &(lhs->goal_id), &(rhs->goal_id)))
  {
    return false;
  }
  // goal
  if (!menu_order_interfaces__action__Serve_Goal__are_equal(
      &(lhs->goal), &(rhs->goal)))
  {
    return false;
  }
  return true;
}

bool
menu_order_interfaces__action__Serve_SendGoal_Request__copy(
  const menu_order_interfaces__action__Serve_SendGoal_Request * input,
  menu_order_interfaces__action__Serve_SendGoal_Request * output)
{
  if (!input || !output) {
    return false;
  }
  // goal_id
  if (!unique_identifier_msgs__msg__UUID__copy(
      &(input->goal_id), &(output->goal_id)))
  {
    return false;
  }
  // goal
  if (!menu_order_interfaces__action__Serve_Goal__copy(
      &(input->goal), &(output->goal)))
  {
    return false;
  }
  return true;
}

menu_order_interfaces__action__Serve_SendGoal_Request *
menu_order_interfaces__action__Serve_SendGoal_Request__create()
{
  rcutils_allocator_t allocator = rcutils_get_default_allocator();
  menu_order_interfaces__action__Serve_SendGoal_Request * msg = (menu_order_interfaces__action__Serve_SendGoal_Request *)allocator.allocate(sizeof(menu_order_interfaces__action__Serve_SendGoal_Request), allocator.state);
  if (!msg) {
    return NULL;
  }
  memset(msg, 0, sizeof(menu_order_interfaces__action__Serve_SendGoal_Request));
  bool success = menu_order_interfaces__action__Serve_SendGoal_Request__init(msg);
  if (!success) {
    allocator.deallocate(msg, allocator.state);
    return NULL;
  }
  return msg;
}

void
menu_order_interfaces__action__Serve_SendGoal_Request__destroy(menu_order_interfaces__action__Serve_SendGoal_Request * msg)
{
  rcutils_allocator_t allocator = rcutils_get_default_allocator();
  if (msg) {
    menu_order_interfaces__action__Serve_SendGoal_Request__fini(msg);
  }
  allocator.deallocate(msg, allocator.state);
}


bool
menu_order_interfaces__action__Serve_SendGoal_Request__Sequence__init(menu_order_interfaces__action__Serve_SendGoal_Request__Sequence * array, size_t size)
{
  if (!array) {
    return false;
  }
  rcutils_allocator_t allocator = rcutils_get_default_allocator();
  menu_order_interfaces__action__Serve_SendGoal_Request * data = NULL;

  if (size) {
    data = (menu_order_interfaces__action__Serve_SendGoal_Request *)allocator.zero_allocate(size, sizeof(menu_order_interfaces__action__Serve_SendGoal_Request), allocator.state);
    if (!data) {
      return false;
    }
    // initialize all array elements
    size_t i;
    for (i = 0; i < size; ++i) {
      bool success = menu_order_interfaces__action__Serve_SendGoal_Request__init(&data[i]);
      if (!success) {
        break;
      }
    }
    if (i < size) {
      // if initialization failed finalize the already initialized array elements
      for (; i > 0; --i) {
        menu_order_interfaces__action__Serve_SendGoal_Request__fini(&data[i - 1]);
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
menu_order_interfaces__action__Serve_SendGoal_Request__Sequence__fini(menu_order_interfaces__action__Serve_SendGoal_Request__Sequence * array)
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
      menu_order_interfaces__action__Serve_SendGoal_Request__fini(&array->data[i]);
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

menu_order_interfaces__action__Serve_SendGoal_Request__Sequence *
menu_order_interfaces__action__Serve_SendGoal_Request__Sequence__create(size_t size)
{
  rcutils_allocator_t allocator = rcutils_get_default_allocator();
  menu_order_interfaces__action__Serve_SendGoal_Request__Sequence * array = (menu_order_interfaces__action__Serve_SendGoal_Request__Sequence *)allocator.allocate(sizeof(menu_order_interfaces__action__Serve_SendGoal_Request__Sequence), allocator.state);
  if (!array) {
    return NULL;
  }
  bool success = menu_order_interfaces__action__Serve_SendGoal_Request__Sequence__init(array, size);
  if (!success) {
    allocator.deallocate(array, allocator.state);
    return NULL;
  }
  return array;
}

void
menu_order_interfaces__action__Serve_SendGoal_Request__Sequence__destroy(menu_order_interfaces__action__Serve_SendGoal_Request__Sequence * array)
{
  rcutils_allocator_t allocator = rcutils_get_default_allocator();
  if (array) {
    menu_order_interfaces__action__Serve_SendGoal_Request__Sequence__fini(array);
  }
  allocator.deallocate(array, allocator.state);
}

bool
menu_order_interfaces__action__Serve_SendGoal_Request__Sequence__are_equal(const menu_order_interfaces__action__Serve_SendGoal_Request__Sequence * lhs, const menu_order_interfaces__action__Serve_SendGoal_Request__Sequence * rhs)
{
  if (!lhs || !rhs) {
    return false;
  }
  if (lhs->size != rhs->size) {
    return false;
  }
  for (size_t i = 0; i < lhs->size; ++i) {
    if (!menu_order_interfaces__action__Serve_SendGoal_Request__are_equal(&(lhs->data[i]), &(rhs->data[i]))) {
      return false;
    }
  }
  return true;
}

bool
menu_order_interfaces__action__Serve_SendGoal_Request__Sequence__copy(
  const menu_order_interfaces__action__Serve_SendGoal_Request__Sequence * input,
  menu_order_interfaces__action__Serve_SendGoal_Request__Sequence * output)
{
  if (!input || !output) {
    return false;
  }
  if (output->capacity < input->size) {
    const size_t allocation_size =
      input->size * sizeof(menu_order_interfaces__action__Serve_SendGoal_Request);
    rcutils_allocator_t allocator = rcutils_get_default_allocator();
    menu_order_interfaces__action__Serve_SendGoal_Request * data =
      (menu_order_interfaces__action__Serve_SendGoal_Request *)allocator.reallocate(
      output->data, allocation_size, allocator.state);
    if (!data) {
      return false;
    }
    // If reallocation succeeded, memory may or may not have been moved
    // to fulfill the allocation request, invalidating output->data.
    output->data = data;
    for (size_t i = output->capacity; i < input->size; ++i) {
      if (!menu_order_interfaces__action__Serve_SendGoal_Request__init(&output->data[i])) {
        // If initialization of any new item fails, roll back
        // all previously initialized items. Existing items
        // in output are to be left unmodified.
        for (; i-- > output->capacity; ) {
          menu_order_interfaces__action__Serve_SendGoal_Request__fini(&output->data[i]);
        }
        return false;
      }
    }
    output->capacity = input->size;
  }
  output->size = input->size;
  for (size_t i = 0; i < input->size; ++i) {
    if (!menu_order_interfaces__action__Serve_SendGoal_Request__copy(
        &(input->data[i]), &(output->data[i])))
    {
      return false;
    }
  }
  return true;
}


// Include directives for member types
// Member `stamp`
#include "builtin_interfaces/msg/detail/time__functions.h"

bool
menu_order_interfaces__action__Serve_SendGoal_Response__init(menu_order_interfaces__action__Serve_SendGoal_Response * msg)
{
  if (!msg) {
    return false;
  }
  // accepted
  // stamp
  if (!builtin_interfaces__msg__Time__init(&msg->stamp)) {
    menu_order_interfaces__action__Serve_SendGoal_Response__fini(msg);
    return false;
  }
  return true;
}

void
menu_order_interfaces__action__Serve_SendGoal_Response__fini(menu_order_interfaces__action__Serve_SendGoal_Response * msg)
{
  if (!msg) {
    return;
  }
  // accepted
  // stamp
  builtin_interfaces__msg__Time__fini(&msg->stamp);
}

bool
menu_order_interfaces__action__Serve_SendGoal_Response__are_equal(const menu_order_interfaces__action__Serve_SendGoal_Response * lhs, const menu_order_interfaces__action__Serve_SendGoal_Response * rhs)
{
  if (!lhs || !rhs) {
    return false;
  }
  // accepted
  if (lhs->accepted != rhs->accepted) {
    return false;
  }
  // stamp
  if (!builtin_interfaces__msg__Time__are_equal(
      &(lhs->stamp), &(rhs->stamp)))
  {
    return false;
  }
  return true;
}

bool
menu_order_interfaces__action__Serve_SendGoal_Response__copy(
  const menu_order_interfaces__action__Serve_SendGoal_Response * input,
  menu_order_interfaces__action__Serve_SendGoal_Response * output)
{
  if (!input || !output) {
    return false;
  }
  // accepted
  output->accepted = input->accepted;
  // stamp
  if (!builtin_interfaces__msg__Time__copy(
      &(input->stamp), &(output->stamp)))
  {
    return false;
  }
  return true;
}

menu_order_interfaces__action__Serve_SendGoal_Response *
menu_order_interfaces__action__Serve_SendGoal_Response__create()
{
  rcutils_allocator_t allocator = rcutils_get_default_allocator();
  menu_order_interfaces__action__Serve_SendGoal_Response * msg = (menu_order_interfaces__action__Serve_SendGoal_Response *)allocator.allocate(sizeof(menu_order_interfaces__action__Serve_SendGoal_Response), allocator.state);
  if (!msg) {
    return NULL;
  }
  memset(msg, 0, sizeof(menu_order_interfaces__action__Serve_SendGoal_Response));
  bool success = menu_order_interfaces__action__Serve_SendGoal_Response__init(msg);
  if (!success) {
    allocator.deallocate(msg, allocator.state);
    return NULL;
  }
  return msg;
}

void
menu_order_interfaces__action__Serve_SendGoal_Response__destroy(menu_order_interfaces__action__Serve_SendGoal_Response * msg)
{
  rcutils_allocator_t allocator = rcutils_get_default_allocator();
  if (msg) {
    menu_order_interfaces__action__Serve_SendGoal_Response__fini(msg);
  }
  allocator.deallocate(msg, allocator.state);
}


bool
menu_order_interfaces__action__Serve_SendGoal_Response__Sequence__init(menu_order_interfaces__action__Serve_SendGoal_Response__Sequence * array, size_t size)
{
  if (!array) {
    return false;
  }
  rcutils_allocator_t allocator = rcutils_get_default_allocator();
  menu_order_interfaces__action__Serve_SendGoal_Response * data = NULL;

  if (size) {
    data = (menu_order_interfaces__action__Serve_SendGoal_Response *)allocator.zero_allocate(size, sizeof(menu_order_interfaces__action__Serve_SendGoal_Response), allocator.state);
    if (!data) {
      return false;
    }
    // initialize all array elements
    size_t i;
    for (i = 0; i < size; ++i) {
      bool success = menu_order_interfaces__action__Serve_SendGoal_Response__init(&data[i]);
      if (!success) {
        break;
      }
    }
    if (i < size) {
      // if initialization failed finalize the already initialized array elements
      for (; i > 0; --i) {
        menu_order_interfaces__action__Serve_SendGoal_Response__fini(&data[i - 1]);
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
menu_order_interfaces__action__Serve_SendGoal_Response__Sequence__fini(menu_order_interfaces__action__Serve_SendGoal_Response__Sequence * array)
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
      menu_order_interfaces__action__Serve_SendGoal_Response__fini(&array->data[i]);
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

menu_order_interfaces__action__Serve_SendGoal_Response__Sequence *
menu_order_interfaces__action__Serve_SendGoal_Response__Sequence__create(size_t size)
{
  rcutils_allocator_t allocator = rcutils_get_default_allocator();
  menu_order_interfaces__action__Serve_SendGoal_Response__Sequence * array = (menu_order_interfaces__action__Serve_SendGoal_Response__Sequence *)allocator.allocate(sizeof(menu_order_interfaces__action__Serve_SendGoal_Response__Sequence), allocator.state);
  if (!array) {
    return NULL;
  }
  bool success = menu_order_interfaces__action__Serve_SendGoal_Response__Sequence__init(array, size);
  if (!success) {
    allocator.deallocate(array, allocator.state);
    return NULL;
  }
  return array;
}

void
menu_order_interfaces__action__Serve_SendGoal_Response__Sequence__destroy(menu_order_interfaces__action__Serve_SendGoal_Response__Sequence * array)
{
  rcutils_allocator_t allocator = rcutils_get_default_allocator();
  if (array) {
    menu_order_interfaces__action__Serve_SendGoal_Response__Sequence__fini(array);
  }
  allocator.deallocate(array, allocator.state);
}

bool
menu_order_interfaces__action__Serve_SendGoal_Response__Sequence__are_equal(const menu_order_interfaces__action__Serve_SendGoal_Response__Sequence * lhs, const menu_order_interfaces__action__Serve_SendGoal_Response__Sequence * rhs)
{
  if (!lhs || !rhs) {
    return false;
  }
  if (lhs->size != rhs->size) {
    return false;
  }
  for (size_t i = 0; i < lhs->size; ++i) {
    if (!menu_order_interfaces__action__Serve_SendGoal_Response__are_equal(&(lhs->data[i]), &(rhs->data[i]))) {
      return false;
    }
  }
  return true;
}

bool
menu_order_interfaces__action__Serve_SendGoal_Response__Sequence__copy(
  const menu_order_interfaces__action__Serve_SendGoal_Response__Sequence * input,
  menu_order_interfaces__action__Serve_SendGoal_Response__Sequence * output)
{
  if (!input || !output) {
    return false;
  }
  if (output->capacity < input->size) {
    const size_t allocation_size =
      input->size * sizeof(menu_order_interfaces__action__Serve_SendGoal_Response);
    rcutils_allocator_t allocator = rcutils_get_default_allocator();
    menu_order_interfaces__action__Serve_SendGoal_Response * data =
      (menu_order_interfaces__action__Serve_SendGoal_Response *)allocator.reallocate(
      output->data, allocation_size, allocator.state);
    if (!data) {
      return false;
    }
    // If reallocation succeeded, memory may or may not have been moved
    // to fulfill the allocation request, invalidating output->data.
    output->data = data;
    for (size_t i = output->capacity; i < input->size; ++i) {
      if (!menu_order_interfaces__action__Serve_SendGoal_Response__init(&output->data[i])) {
        // If initialization of any new item fails, roll back
        // all previously initialized items. Existing items
        // in output are to be left unmodified.
        for (; i-- > output->capacity; ) {
          menu_order_interfaces__action__Serve_SendGoal_Response__fini(&output->data[i]);
        }
        return false;
      }
    }
    output->capacity = input->size;
  }
  output->size = input->size;
  for (size_t i = 0; i < input->size; ++i) {
    if (!menu_order_interfaces__action__Serve_SendGoal_Response__copy(
        &(input->data[i]), &(output->data[i])))
    {
      return false;
    }
  }
  return true;
}


// Include directives for member types
// Member `goal_id`
// already included above
// #include "unique_identifier_msgs/msg/detail/uuid__functions.h"

bool
menu_order_interfaces__action__Serve_GetResult_Request__init(menu_order_interfaces__action__Serve_GetResult_Request * msg)
{
  if (!msg) {
    return false;
  }
  // goal_id
  if (!unique_identifier_msgs__msg__UUID__init(&msg->goal_id)) {
    menu_order_interfaces__action__Serve_GetResult_Request__fini(msg);
    return false;
  }
  return true;
}

void
menu_order_interfaces__action__Serve_GetResult_Request__fini(menu_order_interfaces__action__Serve_GetResult_Request * msg)
{
  if (!msg) {
    return;
  }
  // goal_id
  unique_identifier_msgs__msg__UUID__fini(&msg->goal_id);
}

bool
menu_order_interfaces__action__Serve_GetResult_Request__are_equal(const menu_order_interfaces__action__Serve_GetResult_Request * lhs, const menu_order_interfaces__action__Serve_GetResult_Request * rhs)
{
  if (!lhs || !rhs) {
    return false;
  }
  // goal_id
  if (!unique_identifier_msgs__msg__UUID__are_equal(
      &(lhs->goal_id), &(rhs->goal_id)))
  {
    return false;
  }
  return true;
}

bool
menu_order_interfaces__action__Serve_GetResult_Request__copy(
  const menu_order_interfaces__action__Serve_GetResult_Request * input,
  menu_order_interfaces__action__Serve_GetResult_Request * output)
{
  if (!input || !output) {
    return false;
  }
  // goal_id
  if (!unique_identifier_msgs__msg__UUID__copy(
      &(input->goal_id), &(output->goal_id)))
  {
    return false;
  }
  return true;
}

menu_order_interfaces__action__Serve_GetResult_Request *
menu_order_interfaces__action__Serve_GetResult_Request__create()
{
  rcutils_allocator_t allocator = rcutils_get_default_allocator();
  menu_order_interfaces__action__Serve_GetResult_Request * msg = (menu_order_interfaces__action__Serve_GetResult_Request *)allocator.allocate(sizeof(menu_order_interfaces__action__Serve_GetResult_Request), allocator.state);
  if (!msg) {
    return NULL;
  }
  memset(msg, 0, sizeof(menu_order_interfaces__action__Serve_GetResult_Request));
  bool success = menu_order_interfaces__action__Serve_GetResult_Request__init(msg);
  if (!success) {
    allocator.deallocate(msg, allocator.state);
    return NULL;
  }
  return msg;
}

void
menu_order_interfaces__action__Serve_GetResult_Request__destroy(menu_order_interfaces__action__Serve_GetResult_Request * msg)
{
  rcutils_allocator_t allocator = rcutils_get_default_allocator();
  if (msg) {
    menu_order_interfaces__action__Serve_GetResult_Request__fini(msg);
  }
  allocator.deallocate(msg, allocator.state);
}


bool
menu_order_interfaces__action__Serve_GetResult_Request__Sequence__init(menu_order_interfaces__action__Serve_GetResult_Request__Sequence * array, size_t size)
{
  if (!array) {
    return false;
  }
  rcutils_allocator_t allocator = rcutils_get_default_allocator();
  menu_order_interfaces__action__Serve_GetResult_Request * data = NULL;

  if (size) {
    data = (menu_order_interfaces__action__Serve_GetResult_Request *)allocator.zero_allocate(size, sizeof(menu_order_interfaces__action__Serve_GetResult_Request), allocator.state);
    if (!data) {
      return false;
    }
    // initialize all array elements
    size_t i;
    for (i = 0; i < size; ++i) {
      bool success = menu_order_interfaces__action__Serve_GetResult_Request__init(&data[i]);
      if (!success) {
        break;
      }
    }
    if (i < size) {
      // if initialization failed finalize the already initialized array elements
      for (; i > 0; --i) {
        menu_order_interfaces__action__Serve_GetResult_Request__fini(&data[i - 1]);
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
menu_order_interfaces__action__Serve_GetResult_Request__Sequence__fini(menu_order_interfaces__action__Serve_GetResult_Request__Sequence * array)
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
      menu_order_interfaces__action__Serve_GetResult_Request__fini(&array->data[i]);
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

menu_order_interfaces__action__Serve_GetResult_Request__Sequence *
menu_order_interfaces__action__Serve_GetResult_Request__Sequence__create(size_t size)
{
  rcutils_allocator_t allocator = rcutils_get_default_allocator();
  menu_order_interfaces__action__Serve_GetResult_Request__Sequence * array = (menu_order_interfaces__action__Serve_GetResult_Request__Sequence *)allocator.allocate(sizeof(menu_order_interfaces__action__Serve_GetResult_Request__Sequence), allocator.state);
  if (!array) {
    return NULL;
  }
  bool success = menu_order_interfaces__action__Serve_GetResult_Request__Sequence__init(array, size);
  if (!success) {
    allocator.deallocate(array, allocator.state);
    return NULL;
  }
  return array;
}

void
menu_order_interfaces__action__Serve_GetResult_Request__Sequence__destroy(menu_order_interfaces__action__Serve_GetResult_Request__Sequence * array)
{
  rcutils_allocator_t allocator = rcutils_get_default_allocator();
  if (array) {
    menu_order_interfaces__action__Serve_GetResult_Request__Sequence__fini(array);
  }
  allocator.deallocate(array, allocator.state);
}

bool
menu_order_interfaces__action__Serve_GetResult_Request__Sequence__are_equal(const menu_order_interfaces__action__Serve_GetResult_Request__Sequence * lhs, const menu_order_interfaces__action__Serve_GetResult_Request__Sequence * rhs)
{
  if (!lhs || !rhs) {
    return false;
  }
  if (lhs->size != rhs->size) {
    return false;
  }
  for (size_t i = 0; i < lhs->size; ++i) {
    if (!menu_order_interfaces__action__Serve_GetResult_Request__are_equal(&(lhs->data[i]), &(rhs->data[i]))) {
      return false;
    }
  }
  return true;
}

bool
menu_order_interfaces__action__Serve_GetResult_Request__Sequence__copy(
  const menu_order_interfaces__action__Serve_GetResult_Request__Sequence * input,
  menu_order_interfaces__action__Serve_GetResult_Request__Sequence * output)
{
  if (!input || !output) {
    return false;
  }
  if (output->capacity < input->size) {
    const size_t allocation_size =
      input->size * sizeof(menu_order_interfaces__action__Serve_GetResult_Request);
    rcutils_allocator_t allocator = rcutils_get_default_allocator();
    menu_order_interfaces__action__Serve_GetResult_Request * data =
      (menu_order_interfaces__action__Serve_GetResult_Request *)allocator.reallocate(
      output->data, allocation_size, allocator.state);
    if (!data) {
      return false;
    }
    // If reallocation succeeded, memory may or may not have been moved
    // to fulfill the allocation request, invalidating output->data.
    output->data = data;
    for (size_t i = output->capacity; i < input->size; ++i) {
      if (!menu_order_interfaces__action__Serve_GetResult_Request__init(&output->data[i])) {
        // If initialization of any new item fails, roll back
        // all previously initialized items. Existing items
        // in output are to be left unmodified.
        for (; i-- > output->capacity; ) {
          menu_order_interfaces__action__Serve_GetResult_Request__fini(&output->data[i]);
        }
        return false;
      }
    }
    output->capacity = input->size;
  }
  output->size = input->size;
  for (size_t i = 0; i < input->size; ++i) {
    if (!menu_order_interfaces__action__Serve_GetResult_Request__copy(
        &(input->data[i]), &(output->data[i])))
    {
      return false;
    }
  }
  return true;
}


// Include directives for member types
// Member `result`
// already included above
// #include "menu_order_interfaces/action/detail/serve__functions.h"

bool
menu_order_interfaces__action__Serve_GetResult_Response__init(menu_order_interfaces__action__Serve_GetResult_Response * msg)
{
  if (!msg) {
    return false;
  }
  // status
  // result
  if (!menu_order_interfaces__action__Serve_Result__init(&msg->result)) {
    menu_order_interfaces__action__Serve_GetResult_Response__fini(msg);
    return false;
  }
  return true;
}

void
menu_order_interfaces__action__Serve_GetResult_Response__fini(menu_order_interfaces__action__Serve_GetResult_Response * msg)
{
  if (!msg) {
    return;
  }
  // status
  // result
  menu_order_interfaces__action__Serve_Result__fini(&msg->result);
}

bool
menu_order_interfaces__action__Serve_GetResult_Response__are_equal(const menu_order_interfaces__action__Serve_GetResult_Response * lhs, const menu_order_interfaces__action__Serve_GetResult_Response * rhs)
{
  if (!lhs || !rhs) {
    return false;
  }
  // status
  if (lhs->status != rhs->status) {
    return false;
  }
  // result
  if (!menu_order_interfaces__action__Serve_Result__are_equal(
      &(lhs->result), &(rhs->result)))
  {
    return false;
  }
  return true;
}

bool
menu_order_interfaces__action__Serve_GetResult_Response__copy(
  const menu_order_interfaces__action__Serve_GetResult_Response * input,
  menu_order_interfaces__action__Serve_GetResult_Response * output)
{
  if (!input || !output) {
    return false;
  }
  // status
  output->status = input->status;
  // result
  if (!menu_order_interfaces__action__Serve_Result__copy(
      &(input->result), &(output->result)))
  {
    return false;
  }
  return true;
}

menu_order_interfaces__action__Serve_GetResult_Response *
menu_order_interfaces__action__Serve_GetResult_Response__create()
{
  rcutils_allocator_t allocator = rcutils_get_default_allocator();
  menu_order_interfaces__action__Serve_GetResult_Response * msg = (menu_order_interfaces__action__Serve_GetResult_Response *)allocator.allocate(sizeof(menu_order_interfaces__action__Serve_GetResult_Response), allocator.state);
  if (!msg) {
    return NULL;
  }
  memset(msg, 0, sizeof(menu_order_interfaces__action__Serve_GetResult_Response));
  bool success = menu_order_interfaces__action__Serve_GetResult_Response__init(msg);
  if (!success) {
    allocator.deallocate(msg, allocator.state);
    return NULL;
  }
  return msg;
}

void
menu_order_interfaces__action__Serve_GetResult_Response__destroy(menu_order_interfaces__action__Serve_GetResult_Response * msg)
{
  rcutils_allocator_t allocator = rcutils_get_default_allocator();
  if (msg) {
    menu_order_interfaces__action__Serve_GetResult_Response__fini(msg);
  }
  allocator.deallocate(msg, allocator.state);
}


bool
menu_order_interfaces__action__Serve_GetResult_Response__Sequence__init(menu_order_interfaces__action__Serve_GetResult_Response__Sequence * array, size_t size)
{
  if (!array) {
    return false;
  }
  rcutils_allocator_t allocator = rcutils_get_default_allocator();
  menu_order_interfaces__action__Serve_GetResult_Response * data = NULL;

  if (size) {
    data = (menu_order_interfaces__action__Serve_GetResult_Response *)allocator.zero_allocate(size, sizeof(menu_order_interfaces__action__Serve_GetResult_Response), allocator.state);
    if (!data) {
      return false;
    }
    // initialize all array elements
    size_t i;
    for (i = 0; i < size; ++i) {
      bool success = menu_order_interfaces__action__Serve_GetResult_Response__init(&data[i]);
      if (!success) {
        break;
      }
    }
    if (i < size) {
      // if initialization failed finalize the already initialized array elements
      for (; i > 0; --i) {
        menu_order_interfaces__action__Serve_GetResult_Response__fini(&data[i - 1]);
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
menu_order_interfaces__action__Serve_GetResult_Response__Sequence__fini(menu_order_interfaces__action__Serve_GetResult_Response__Sequence * array)
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
      menu_order_interfaces__action__Serve_GetResult_Response__fini(&array->data[i]);
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

menu_order_interfaces__action__Serve_GetResult_Response__Sequence *
menu_order_interfaces__action__Serve_GetResult_Response__Sequence__create(size_t size)
{
  rcutils_allocator_t allocator = rcutils_get_default_allocator();
  menu_order_interfaces__action__Serve_GetResult_Response__Sequence * array = (menu_order_interfaces__action__Serve_GetResult_Response__Sequence *)allocator.allocate(sizeof(menu_order_interfaces__action__Serve_GetResult_Response__Sequence), allocator.state);
  if (!array) {
    return NULL;
  }
  bool success = menu_order_interfaces__action__Serve_GetResult_Response__Sequence__init(array, size);
  if (!success) {
    allocator.deallocate(array, allocator.state);
    return NULL;
  }
  return array;
}

void
menu_order_interfaces__action__Serve_GetResult_Response__Sequence__destroy(menu_order_interfaces__action__Serve_GetResult_Response__Sequence * array)
{
  rcutils_allocator_t allocator = rcutils_get_default_allocator();
  if (array) {
    menu_order_interfaces__action__Serve_GetResult_Response__Sequence__fini(array);
  }
  allocator.deallocate(array, allocator.state);
}

bool
menu_order_interfaces__action__Serve_GetResult_Response__Sequence__are_equal(const menu_order_interfaces__action__Serve_GetResult_Response__Sequence * lhs, const menu_order_interfaces__action__Serve_GetResult_Response__Sequence * rhs)
{
  if (!lhs || !rhs) {
    return false;
  }
  if (lhs->size != rhs->size) {
    return false;
  }
  for (size_t i = 0; i < lhs->size; ++i) {
    if (!menu_order_interfaces__action__Serve_GetResult_Response__are_equal(&(lhs->data[i]), &(rhs->data[i]))) {
      return false;
    }
  }
  return true;
}

bool
menu_order_interfaces__action__Serve_GetResult_Response__Sequence__copy(
  const menu_order_interfaces__action__Serve_GetResult_Response__Sequence * input,
  menu_order_interfaces__action__Serve_GetResult_Response__Sequence * output)
{
  if (!input || !output) {
    return false;
  }
  if (output->capacity < input->size) {
    const size_t allocation_size =
      input->size * sizeof(menu_order_interfaces__action__Serve_GetResult_Response);
    rcutils_allocator_t allocator = rcutils_get_default_allocator();
    menu_order_interfaces__action__Serve_GetResult_Response * data =
      (menu_order_interfaces__action__Serve_GetResult_Response *)allocator.reallocate(
      output->data, allocation_size, allocator.state);
    if (!data) {
      return false;
    }
    // If reallocation succeeded, memory may or may not have been moved
    // to fulfill the allocation request, invalidating output->data.
    output->data = data;
    for (size_t i = output->capacity; i < input->size; ++i) {
      if (!menu_order_interfaces__action__Serve_GetResult_Response__init(&output->data[i])) {
        // If initialization of any new item fails, roll back
        // all previously initialized items. Existing items
        // in output are to be left unmodified.
        for (; i-- > output->capacity; ) {
          menu_order_interfaces__action__Serve_GetResult_Response__fini(&output->data[i]);
        }
        return false;
      }
    }
    output->capacity = input->size;
  }
  output->size = input->size;
  for (size_t i = 0; i < input->size; ++i) {
    if (!menu_order_interfaces__action__Serve_GetResult_Response__copy(
        &(input->data[i]), &(output->data[i])))
    {
      return false;
    }
  }
  return true;
}


// Include directives for member types
// Member `goal_id`
// already included above
// #include "unique_identifier_msgs/msg/detail/uuid__functions.h"
// Member `feedback`
// already included above
// #include "menu_order_interfaces/action/detail/serve__functions.h"

bool
menu_order_interfaces__action__Serve_FeedbackMessage__init(menu_order_interfaces__action__Serve_FeedbackMessage * msg)
{
  if (!msg) {
    return false;
  }
  // goal_id
  if (!unique_identifier_msgs__msg__UUID__init(&msg->goal_id)) {
    menu_order_interfaces__action__Serve_FeedbackMessage__fini(msg);
    return false;
  }
  // feedback
  if (!menu_order_interfaces__action__Serve_Feedback__init(&msg->feedback)) {
    menu_order_interfaces__action__Serve_FeedbackMessage__fini(msg);
    return false;
  }
  return true;
}

void
menu_order_interfaces__action__Serve_FeedbackMessage__fini(menu_order_interfaces__action__Serve_FeedbackMessage * msg)
{
  if (!msg) {
    return;
  }
  // goal_id
  unique_identifier_msgs__msg__UUID__fini(&msg->goal_id);
  // feedback
  menu_order_interfaces__action__Serve_Feedback__fini(&msg->feedback);
}

bool
menu_order_interfaces__action__Serve_FeedbackMessage__are_equal(const menu_order_interfaces__action__Serve_FeedbackMessage * lhs, const menu_order_interfaces__action__Serve_FeedbackMessage * rhs)
{
  if (!lhs || !rhs) {
    return false;
  }
  // goal_id
  if (!unique_identifier_msgs__msg__UUID__are_equal(
      &(lhs->goal_id), &(rhs->goal_id)))
  {
    return false;
  }
  // feedback
  if (!menu_order_interfaces__action__Serve_Feedback__are_equal(
      &(lhs->feedback), &(rhs->feedback)))
  {
    return false;
  }
  return true;
}

bool
menu_order_interfaces__action__Serve_FeedbackMessage__copy(
  const menu_order_interfaces__action__Serve_FeedbackMessage * input,
  menu_order_interfaces__action__Serve_FeedbackMessage * output)
{
  if (!input || !output) {
    return false;
  }
  // goal_id
  if (!unique_identifier_msgs__msg__UUID__copy(
      &(input->goal_id), &(output->goal_id)))
  {
    return false;
  }
  // feedback
  if (!menu_order_interfaces__action__Serve_Feedback__copy(
      &(input->feedback), &(output->feedback)))
  {
    return false;
  }
  return true;
}

menu_order_interfaces__action__Serve_FeedbackMessage *
menu_order_interfaces__action__Serve_FeedbackMessage__create()
{
  rcutils_allocator_t allocator = rcutils_get_default_allocator();
  menu_order_interfaces__action__Serve_FeedbackMessage * msg = (menu_order_interfaces__action__Serve_FeedbackMessage *)allocator.allocate(sizeof(menu_order_interfaces__action__Serve_FeedbackMessage), allocator.state);
  if (!msg) {
    return NULL;
  }
  memset(msg, 0, sizeof(menu_order_interfaces__action__Serve_FeedbackMessage));
  bool success = menu_order_interfaces__action__Serve_FeedbackMessage__init(msg);
  if (!success) {
    allocator.deallocate(msg, allocator.state);
    return NULL;
  }
  return msg;
}

void
menu_order_interfaces__action__Serve_FeedbackMessage__destroy(menu_order_interfaces__action__Serve_FeedbackMessage * msg)
{
  rcutils_allocator_t allocator = rcutils_get_default_allocator();
  if (msg) {
    menu_order_interfaces__action__Serve_FeedbackMessage__fini(msg);
  }
  allocator.deallocate(msg, allocator.state);
}


bool
menu_order_interfaces__action__Serve_FeedbackMessage__Sequence__init(menu_order_interfaces__action__Serve_FeedbackMessage__Sequence * array, size_t size)
{
  if (!array) {
    return false;
  }
  rcutils_allocator_t allocator = rcutils_get_default_allocator();
  menu_order_interfaces__action__Serve_FeedbackMessage * data = NULL;

  if (size) {
    data = (menu_order_interfaces__action__Serve_FeedbackMessage *)allocator.zero_allocate(size, sizeof(menu_order_interfaces__action__Serve_FeedbackMessage), allocator.state);
    if (!data) {
      return false;
    }
    // initialize all array elements
    size_t i;
    for (i = 0; i < size; ++i) {
      bool success = menu_order_interfaces__action__Serve_FeedbackMessage__init(&data[i]);
      if (!success) {
        break;
      }
    }
    if (i < size) {
      // if initialization failed finalize the already initialized array elements
      for (; i > 0; --i) {
        menu_order_interfaces__action__Serve_FeedbackMessage__fini(&data[i - 1]);
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
menu_order_interfaces__action__Serve_FeedbackMessage__Sequence__fini(menu_order_interfaces__action__Serve_FeedbackMessage__Sequence * array)
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
      menu_order_interfaces__action__Serve_FeedbackMessage__fini(&array->data[i]);
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

menu_order_interfaces__action__Serve_FeedbackMessage__Sequence *
menu_order_interfaces__action__Serve_FeedbackMessage__Sequence__create(size_t size)
{
  rcutils_allocator_t allocator = rcutils_get_default_allocator();
  menu_order_interfaces__action__Serve_FeedbackMessage__Sequence * array = (menu_order_interfaces__action__Serve_FeedbackMessage__Sequence *)allocator.allocate(sizeof(menu_order_interfaces__action__Serve_FeedbackMessage__Sequence), allocator.state);
  if (!array) {
    return NULL;
  }
  bool success = menu_order_interfaces__action__Serve_FeedbackMessage__Sequence__init(array, size);
  if (!success) {
    allocator.deallocate(array, allocator.state);
    return NULL;
  }
  return array;
}

void
menu_order_interfaces__action__Serve_FeedbackMessage__Sequence__destroy(menu_order_interfaces__action__Serve_FeedbackMessage__Sequence * array)
{
  rcutils_allocator_t allocator = rcutils_get_default_allocator();
  if (array) {
    menu_order_interfaces__action__Serve_FeedbackMessage__Sequence__fini(array);
  }
  allocator.deallocate(array, allocator.state);
}

bool
menu_order_interfaces__action__Serve_FeedbackMessage__Sequence__are_equal(const menu_order_interfaces__action__Serve_FeedbackMessage__Sequence * lhs, const menu_order_interfaces__action__Serve_FeedbackMessage__Sequence * rhs)
{
  if (!lhs || !rhs) {
    return false;
  }
  if (lhs->size != rhs->size) {
    return false;
  }
  for (size_t i = 0; i < lhs->size; ++i) {
    if (!menu_order_interfaces__action__Serve_FeedbackMessage__are_equal(&(lhs->data[i]), &(rhs->data[i]))) {
      return false;
    }
  }
  return true;
}

bool
menu_order_interfaces__action__Serve_FeedbackMessage__Sequence__copy(
  const menu_order_interfaces__action__Serve_FeedbackMessage__Sequence * input,
  menu_order_interfaces__action__Serve_FeedbackMessage__Sequence * output)
{
  if (!input || !output) {
    return false;
  }
  if (output->capacity < input->size) {
    const size_t allocation_size =
      input->size * sizeof(menu_order_interfaces__action__Serve_FeedbackMessage);
    rcutils_allocator_t allocator = rcutils_get_default_allocator();
    menu_order_interfaces__action__Serve_FeedbackMessage * data =
      (menu_order_interfaces__action__Serve_FeedbackMessage *)allocator.reallocate(
      output->data, allocation_size, allocator.state);
    if (!data) {
      return false;
    }
    // If reallocation succeeded, memory may or may not have been moved
    // to fulfill the allocation request, invalidating output->data.
    output->data = data;
    for (size_t i = output->capacity; i < input->size; ++i) {
      if (!menu_order_interfaces__action__Serve_FeedbackMessage__init(&output->data[i])) {
        // If initialization of any new item fails, roll back
        // all previously initialized items. Existing items
        // in output are to be left unmodified.
        for (; i-- > output->capacity; ) {
          menu_order_interfaces__action__Serve_FeedbackMessage__fini(&output->data[i]);
        }
        return false;
      }
    }
    output->capacity = input->size;
  }
  output->size = input->size;
  for (size_t i = 0; i < input->size; ++i) {
    if (!menu_order_interfaces__action__Serve_FeedbackMessage__copy(
        &(input->data[i]), &(output->data[i])))
    {
      return false;
    }
  }
  return true;
}
