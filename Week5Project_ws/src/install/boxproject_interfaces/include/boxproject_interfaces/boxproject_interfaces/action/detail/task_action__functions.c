// generated from rosidl_generator_c/resource/idl__functions.c.em
// with input from boxproject_interfaces:action/TaskAction.idl
// generated code does not contain a copyright notice
#include "boxproject_interfaces/action/detail/task_action__functions.h"

#include <assert.h>
#include <stdbool.h>
#include <stdlib.h>
#include <string.h>

#include "rcutils/allocator.h"


// Include directives for member types
// Member `task`
#include "rosidl_runtime_c/string_functions.h"

bool
boxproject_interfaces__action__TaskAction_Goal__init(boxproject_interfaces__action__TaskAction_Goal * msg)
{
  if (!msg) {
    return false;
  }
  // task
  if (!rosidl_runtime_c__String__init(&msg->task)) {
    boxproject_interfaces__action__TaskAction_Goal__fini(msg);
    return false;
  }
  return true;
}

void
boxproject_interfaces__action__TaskAction_Goal__fini(boxproject_interfaces__action__TaskAction_Goal * msg)
{
  if (!msg) {
    return;
  }
  // task
  rosidl_runtime_c__String__fini(&msg->task);
}

bool
boxproject_interfaces__action__TaskAction_Goal__are_equal(const boxproject_interfaces__action__TaskAction_Goal * lhs, const boxproject_interfaces__action__TaskAction_Goal * rhs)
{
  if (!lhs || !rhs) {
    return false;
  }
  // task
  if (!rosidl_runtime_c__String__are_equal(
      &(lhs->task), &(rhs->task)))
  {
    return false;
  }
  return true;
}

bool
boxproject_interfaces__action__TaskAction_Goal__copy(
  const boxproject_interfaces__action__TaskAction_Goal * input,
  boxproject_interfaces__action__TaskAction_Goal * output)
{
  if (!input || !output) {
    return false;
  }
  // task
  if (!rosidl_runtime_c__String__copy(
      &(input->task), &(output->task)))
  {
    return false;
  }
  return true;
}

boxproject_interfaces__action__TaskAction_Goal *
boxproject_interfaces__action__TaskAction_Goal__create()
{
  rcutils_allocator_t allocator = rcutils_get_default_allocator();
  boxproject_interfaces__action__TaskAction_Goal * msg = (boxproject_interfaces__action__TaskAction_Goal *)allocator.allocate(sizeof(boxproject_interfaces__action__TaskAction_Goal), allocator.state);
  if (!msg) {
    return NULL;
  }
  memset(msg, 0, sizeof(boxproject_interfaces__action__TaskAction_Goal));
  bool success = boxproject_interfaces__action__TaskAction_Goal__init(msg);
  if (!success) {
    allocator.deallocate(msg, allocator.state);
    return NULL;
  }
  return msg;
}

void
boxproject_interfaces__action__TaskAction_Goal__destroy(boxproject_interfaces__action__TaskAction_Goal * msg)
{
  rcutils_allocator_t allocator = rcutils_get_default_allocator();
  if (msg) {
    boxproject_interfaces__action__TaskAction_Goal__fini(msg);
  }
  allocator.deallocate(msg, allocator.state);
}


bool
boxproject_interfaces__action__TaskAction_Goal__Sequence__init(boxproject_interfaces__action__TaskAction_Goal__Sequence * array, size_t size)
{
  if (!array) {
    return false;
  }
  rcutils_allocator_t allocator = rcutils_get_default_allocator();
  boxproject_interfaces__action__TaskAction_Goal * data = NULL;

  if (size) {
    data = (boxproject_interfaces__action__TaskAction_Goal *)allocator.zero_allocate(size, sizeof(boxproject_interfaces__action__TaskAction_Goal), allocator.state);
    if (!data) {
      return false;
    }
    // initialize all array elements
    size_t i;
    for (i = 0; i < size; ++i) {
      bool success = boxproject_interfaces__action__TaskAction_Goal__init(&data[i]);
      if (!success) {
        break;
      }
    }
    if (i < size) {
      // if initialization failed finalize the already initialized array elements
      for (; i > 0; --i) {
        boxproject_interfaces__action__TaskAction_Goal__fini(&data[i - 1]);
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
boxproject_interfaces__action__TaskAction_Goal__Sequence__fini(boxproject_interfaces__action__TaskAction_Goal__Sequence * array)
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
      boxproject_interfaces__action__TaskAction_Goal__fini(&array->data[i]);
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

boxproject_interfaces__action__TaskAction_Goal__Sequence *
boxproject_interfaces__action__TaskAction_Goal__Sequence__create(size_t size)
{
  rcutils_allocator_t allocator = rcutils_get_default_allocator();
  boxproject_interfaces__action__TaskAction_Goal__Sequence * array = (boxproject_interfaces__action__TaskAction_Goal__Sequence *)allocator.allocate(sizeof(boxproject_interfaces__action__TaskAction_Goal__Sequence), allocator.state);
  if (!array) {
    return NULL;
  }
  bool success = boxproject_interfaces__action__TaskAction_Goal__Sequence__init(array, size);
  if (!success) {
    allocator.deallocate(array, allocator.state);
    return NULL;
  }
  return array;
}

void
boxproject_interfaces__action__TaskAction_Goal__Sequence__destroy(boxproject_interfaces__action__TaskAction_Goal__Sequence * array)
{
  rcutils_allocator_t allocator = rcutils_get_default_allocator();
  if (array) {
    boxproject_interfaces__action__TaskAction_Goal__Sequence__fini(array);
  }
  allocator.deallocate(array, allocator.state);
}

bool
boxproject_interfaces__action__TaskAction_Goal__Sequence__are_equal(const boxproject_interfaces__action__TaskAction_Goal__Sequence * lhs, const boxproject_interfaces__action__TaskAction_Goal__Sequence * rhs)
{
  if (!lhs || !rhs) {
    return false;
  }
  if (lhs->size != rhs->size) {
    return false;
  }
  for (size_t i = 0; i < lhs->size; ++i) {
    if (!boxproject_interfaces__action__TaskAction_Goal__are_equal(&(lhs->data[i]), &(rhs->data[i]))) {
      return false;
    }
  }
  return true;
}

bool
boxproject_interfaces__action__TaskAction_Goal__Sequence__copy(
  const boxproject_interfaces__action__TaskAction_Goal__Sequence * input,
  boxproject_interfaces__action__TaskAction_Goal__Sequence * output)
{
  if (!input || !output) {
    return false;
  }
  if (output->capacity < input->size) {
    const size_t allocation_size =
      input->size * sizeof(boxproject_interfaces__action__TaskAction_Goal);
    rcutils_allocator_t allocator = rcutils_get_default_allocator();
    boxproject_interfaces__action__TaskAction_Goal * data =
      (boxproject_interfaces__action__TaskAction_Goal *)allocator.reallocate(
      output->data, allocation_size, allocator.state);
    if (!data) {
      return false;
    }
    // If reallocation succeeded, memory may or may not have been moved
    // to fulfill the allocation request, invalidating output->data.
    output->data = data;
    for (size_t i = output->capacity; i < input->size; ++i) {
      if (!boxproject_interfaces__action__TaskAction_Goal__init(&output->data[i])) {
        // If initialization of any new item fails, roll back
        // all previously initialized items. Existing items
        // in output are to be left unmodified.
        for (; i-- > output->capacity; ) {
          boxproject_interfaces__action__TaskAction_Goal__fini(&output->data[i]);
        }
        return false;
      }
    }
    output->capacity = input->size;
  }
  output->size = input->size;
  for (size_t i = 0; i < input->size; ++i) {
    if (!boxproject_interfaces__action__TaskAction_Goal__copy(
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
boxproject_interfaces__action__TaskAction_Result__init(boxproject_interfaces__action__TaskAction_Result * msg)
{
  if (!msg) {
    return false;
  }
  // status
  if (!rosidl_runtime_c__String__init(&msg->status)) {
    boxproject_interfaces__action__TaskAction_Result__fini(msg);
    return false;
  }
  return true;
}

void
boxproject_interfaces__action__TaskAction_Result__fini(boxproject_interfaces__action__TaskAction_Result * msg)
{
  if (!msg) {
    return;
  }
  // status
  rosidl_runtime_c__String__fini(&msg->status);
}

bool
boxproject_interfaces__action__TaskAction_Result__are_equal(const boxproject_interfaces__action__TaskAction_Result * lhs, const boxproject_interfaces__action__TaskAction_Result * rhs)
{
  if (!lhs || !rhs) {
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
boxproject_interfaces__action__TaskAction_Result__copy(
  const boxproject_interfaces__action__TaskAction_Result * input,
  boxproject_interfaces__action__TaskAction_Result * output)
{
  if (!input || !output) {
    return false;
  }
  // status
  if (!rosidl_runtime_c__String__copy(
      &(input->status), &(output->status)))
  {
    return false;
  }
  return true;
}

boxproject_interfaces__action__TaskAction_Result *
boxproject_interfaces__action__TaskAction_Result__create()
{
  rcutils_allocator_t allocator = rcutils_get_default_allocator();
  boxproject_interfaces__action__TaskAction_Result * msg = (boxproject_interfaces__action__TaskAction_Result *)allocator.allocate(sizeof(boxproject_interfaces__action__TaskAction_Result), allocator.state);
  if (!msg) {
    return NULL;
  }
  memset(msg, 0, sizeof(boxproject_interfaces__action__TaskAction_Result));
  bool success = boxproject_interfaces__action__TaskAction_Result__init(msg);
  if (!success) {
    allocator.deallocate(msg, allocator.state);
    return NULL;
  }
  return msg;
}

void
boxproject_interfaces__action__TaskAction_Result__destroy(boxproject_interfaces__action__TaskAction_Result * msg)
{
  rcutils_allocator_t allocator = rcutils_get_default_allocator();
  if (msg) {
    boxproject_interfaces__action__TaskAction_Result__fini(msg);
  }
  allocator.deallocate(msg, allocator.state);
}


bool
boxproject_interfaces__action__TaskAction_Result__Sequence__init(boxproject_interfaces__action__TaskAction_Result__Sequence * array, size_t size)
{
  if (!array) {
    return false;
  }
  rcutils_allocator_t allocator = rcutils_get_default_allocator();
  boxproject_interfaces__action__TaskAction_Result * data = NULL;

  if (size) {
    data = (boxproject_interfaces__action__TaskAction_Result *)allocator.zero_allocate(size, sizeof(boxproject_interfaces__action__TaskAction_Result), allocator.state);
    if (!data) {
      return false;
    }
    // initialize all array elements
    size_t i;
    for (i = 0; i < size; ++i) {
      bool success = boxproject_interfaces__action__TaskAction_Result__init(&data[i]);
      if (!success) {
        break;
      }
    }
    if (i < size) {
      // if initialization failed finalize the already initialized array elements
      for (; i > 0; --i) {
        boxproject_interfaces__action__TaskAction_Result__fini(&data[i - 1]);
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
boxproject_interfaces__action__TaskAction_Result__Sequence__fini(boxproject_interfaces__action__TaskAction_Result__Sequence * array)
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
      boxproject_interfaces__action__TaskAction_Result__fini(&array->data[i]);
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

boxproject_interfaces__action__TaskAction_Result__Sequence *
boxproject_interfaces__action__TaskAction_Result__Sequence__create(size_t size)
{
  rcutils_allocator_t allocator = rcutils_get_default_allocator();
  boxproject_interfaces__action__TaskAction_Result__Sequence * array = (boxproject_interfaces__action__TaskAction_Result__Sequence *)allocator.allocate(sizeof(boxproject_interfaces__action__TaskAction_Result__Sequence), allocator.state);
  if (!array) {
    return NULL;
  }
  bool success = boxproject_interfaces__action__TaskAction_Result__Sequence__init(array, size);
  if (!success) {
    allocator.deallocate(array, allocator.state);
    return NULL;
  }
  return array;
}

void
boxproject_interfaces__action__TaskAction_Result__Sequence__destroy(boxproject_interfaces__action__TaskAction_Result__Sequence * array)
{
  rcutils_allocator_t allocator = rcutils_get_default_allocator();
  if (array) {
    boxproject_interfaces__action__TaskAction_Result__Sequence__fini(array);
  }
  allocator.deallocate(array, allocator.state);
}

bool
boxproject_interfaces__action__TaskAction_Result__Sequence__are_equal(const boxproject_interfaces__action__TaskAction_Result__Sequence * lhs, const boxproject_interfaces__action__TaskAction_Result__Sequence * rhs)
{
  if (!lhs || !rhs) {
    return false;
  }
  if (lhs->size != rhs->size) {
    return false;
  }
  for (size_t i = 0; i < lhs->size; ++i) {
    if (!boxproject_interfaces__action__TaskAction_Result__are_equal(&(lhs->data[i]), &(rhs->data[i]))) {
      return false;
    }
  }
  return true;
}

bool
boxproject_interfaces__action__TaskAction_Result__Sequence__copy(
  const boxproject_interfaces__action__TaskAction_Result__Sequence * input,
  boxproject_interfaces__action__TaskAction_Result__Sequence * output)
{
  if (!input || !output) {
    return false;
  }
  if (output->capacity < input->size) {
    const size_t allocation_size =
      input->size * sizeof(boxproject_interfaces__action__TaskAction_Result);
    rcutils_allocator_t allocator = rcutils_get_default_allocator();
    boxproject_interfaces__action__TaskAction_Result * data =
      (boxproject_interfaces__action__TaskAction_Result *)allocator.reallocate(
      output->data, allocation_size, allocator.state);
    if (!data) {
      return false;
    }
    // If reallocation succeeded, memory may or may not have been moved
    // to fulfill the allocation request, invalidating output->data.
    output->data = data;
    for (size_t i = output->capacity; i < input->size; ++i) {
      if (!boxproject_interfaces__action__TaskAction_Result__init(&output->data[i])) {
        // If initialization of any new item fails, roll back
        // all previously initialized items. Existing items
        // in output are to be left unmodified.
        for (; i-- > output->capacity; ) {
          boxproject_interfaces__action__TaskAction_Result__fini(&output->data[i]);
        }
        return false;
      }
    }
    output->capacity = input->size;
  }
  output->size = input->size;
  for (size_t i = 0; i < input->size; ++i) {
    if (!boxproject_interfaces__action__TaskAction_Result__copy(
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
// #include "rosidl_runtime_c/string_functions.h"

bool
boxproject_interfaces__action__TaskAction_Feedback__init(boxproject_interfaces__action__TaskAction_Feedback * msg)
{
  if (!msg) {
    return false;
  }
  // result
  if (!rosidl_runtime_c__String__init(&msg->result)) {
    boxproject_interfaces__action__TaskAction_Feedback__fini(msg);
    return false;
  }
  return true;
}

void
boxproject_interfaces__action__TaskAction_Feedback__fini(boxproject_interfaces__action__TaskAction_Feedback * msg)
{
  if (!msg) {
    return;
  }
  // result
  rosidl_runtime_c__String__fini(&msg->result);
}

bool
boxproject_interfaces__action__TaskAction_Feedback__are_equal(const boxproject_interfaces__action__TaskAction_Feedback * lhs, const boxproject_interfaces__action__TaskAction_Feedback * rhs)
{
  if (!lhs || !rhs) {
    return false;
  }
  // result
  if (!rosidl_runtime_c__String__are_equal(
      &(lhs->result), &(rhs->result)))
  {
    return false;
  }
  return true;
}

bool
boxproject_interfaces__action__TaskAction_Feedback__copy(
  const boxproject_interfaces__action__TaskAction_Feedback * input,
  boxproject_interfaces__action__TaskAction_Feedback * output)
{
  if (!input || !output) {
    return false;
  }
  // result
  if (!rosidl_runtime_c__String__copy(
      &(input->result), &(output->result)))
  {
    return false;
  }
  return true;
}

boxproject_interfaces__action__TaskAction_Feedback *
boxproject_interfaces__action__TaskAction_Feedback__create()
{
  rcutils_allocator_t allocator = rcutils_get_default_allocator();
  boxproject_interfaces__action__TaskAction_Feedback * msg = (boxproject_interfaces__action__TaskAction_Feedback *)allocator.allocate(sizeof(boxproject_interfaces__action__TaskAction_Feedback), allocator.state);
  if (!msg) {
    return NULL;
  }
  memset(msg, 0, sizeof(boxproject_interfaces__action__TaskAction_Feedback));
  bool success = boxproject_interfaces__action__TaskAction_Feedback__init(msg);
  if (!success) {
    allocator.deallocate(msg, allocator.state);
    return NULL;
  }
  return msg;
}

void
boxproject_interfaces__action__TaskAction_Feedback__destroy(boxproject_interfaces__action__TaskAction_Feedback * msg)
{
  rcutils_allocator_t allocator = rcutils_get_default_allocator();
  if (msg) {
    boxproject_interfaces__action__TaskAction_Feedback__fini(msg);
  }
  allocator.deallocate(msg, allocator.state);
}


bool
boxproject_interfaces__action__TaskAction_Feedback__Sequence__init(boxproject_interfaces__action__TaskAction_Feedback__Sequence * array, size_t size)
{
  if (!array) {
    return false;
  }
  rcutils_allocator_t allocator = rcutils_get_default_allocator();
  boxproject_interfaces__action__TaskAction_Feedback * data = NULL;

  if (size) {
    data = (boxproject_interfaces__action__TaskAction_Feedback *)allocator.zero_allocate(size, sizeof(boxproject_interfaces__action__TaskAction_Feedback), allocator.state);
    if (!data) {
      return false;
    }
    // initialize all array elements
    size_t i;
    for (i = 0; i < size; ++i) {
      bool success = boxproject_interfaces__action__TaskAction_Feedback__init(&data[i]);
      if (!success) {
        break;
      }
    }
    if (i < size) {
      // if initialization failed finalize the already initialized array elements
      for (; i > 0; --i) {
        boxproject_interfaces__action__TaskAction_Feedback__fini(&data[i - 1]);
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
boxproject_interfaces__action__TaskAction_Feedback__Sequence__fini(boxproject_interfaces__action__TaskAction_Feedback__Sequence * array)
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
      boxproject_interfaces__action__TaskAction_Feedback__fini(&array->data[i]);
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

boxproject_interfaces__action__TaskAction_Feedback__Sequence *
boxproject_interfaces__action__TaskAction_Feedback__Sequence__create(size_t size)
{
  rcutils_allocator_t allocator = rcutils_get_default_allocator();
  boxproject_interfaces__action__TaskAction_Feedback__Sequence * array = (boxproject_interfaces__action__TaskAction_Feedback__Sequence *)allocator.allocate(sizeof(boxproject_interfaces__action__TaskAction_Feedback__Sequence), allocator.state);
  if (!array) {
    return NULL;
  }
  bool success = boxproject_interfaces__action__TaskAction_Feedback__Sequence__init(array, size);
  if (!success) {
    allocator.deallocate(array, allocator.state);
    return NULL;
  }
  return array;
}

void
boxproject_interfaces__action__TaskAction_Feedback__Sequence__destroy(boxproject_interfaces__action__TaskAction_Feedback__Sequence * array)
{
  rcutils_allocator_t allocator = rcutils_get_default_allocator();
  if (array) {
    boxproject_interfaces__action__TaskAction_Feedback__Sequence__fini(array);
  }
  allocator.deallocate(array, allocator.state);
}

bool
boxproject_interfaces__action__TaskAction_Feedback__Sequence__are_equal(const boxproject_interfaces__action__TaskAction_Feedback__Sequence * lhs, const boxproject_interfaces__action__TaskAction_Feedback__Sequence * rhs)
{
  if (!lhs || !rhs) {
    return false;
  }
  if (lhs->size != rhs->size) {
    return false;
  }
  for (size_t i = 0; i < lhs->size; ++i) {
    if (!boxproject_interfaces__action__TaskAction_Feedback__are_equal(&(lhs->data[i]), &(rhs->data[i]))) {
      return false;
    }
  }
  return true;
}

bool
boxproject_interfaces__action__TaskAction_Feedback__Sequence__copy(
  const boxproject_interfaces__action__TaskAction_Feedback__Sequence * input,
  boxproject_interfaces__action__TaskAction_Feedback__Sequence * output)
{
  if (!input || !output) {
    return false;
  }
  if (output->capacity < input->size) {
    const size_t allocation_size =
      input->size * sizeof(boxproject_interfaces__action__TaskAction_Feedback);
    rcutils_allocator_t allocator = rcutils_get_default_allocator();
    boxproject_interfaces__action__TaskAction_Feedback * data =
      (boxproject_interfaces__action__TaskAction_Feedback *)allocator.reallocate(
      output->data, allocation_size, allocator.state);
    if (!data) {
      return false;
    }
    // If reallocation succeeded, memory may or may not have been moved
    // to fulfill the allocation request, invalidating output->data.
    output->data = data;
    for (size_t i = output->capacity; i < input->size; ++i) {
      if (!boxproject_interfaces__action__TaskAction_Feedback__init(&output->data[i])) {
        // If initialization of any new item fails, roll back
        // all previously initialized items. Existing items
        // in output are to be left unmodified.
        for (; i-- > output->capacity; ) {
          boxproject_interfaces__action__TaskAction_Feedback__fini(&output->data[i]);
        }
        return false;
      }
    }
    output->capacity = input->size;
  }
  output->size = input->size;
  for (size_t i = 0; i < input->size; ++i) {
    if (!boxproject_interfaces__action__TaskAction_Feedback__copy(
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
// #include "boxproject_interfaces/action/detail/task_action__functions.h"

bool
boxproject_interfaces__action__TaskAction_SendGoal_Request__init(boxproject_interfaces__action__TaskAction_SendGoal_Request * msg)
{
  if (!msg) {
    return false;
  }
  // goal_id
  if (!unique_identifier_msgs__msg__UUID__init(&msg->goal_id)) {
    boxproject_interfaces__action__TaskAction_SendGoal_Request__fini(msg);
    return false;
  }
  // goal
  if (!boxproject_interfaces__action__TaskAction_Goal__init(&msg->goal)) {
    boxproject_interfaces__action__TaskAction_SendGoal_Request__fini(msg);
    return false;
  }
  return true;
}

void
boxproject_interfaces__action__TaskAction_SendGoal_Request__fini(boxproject_interfaces__action__TaskAction_SendGoal_Request * msg)
{
  if (!msg) {
    return;
  }
  // goal_id
  unique_identifier_msgs__msg__UUID__fini(&msg->goal_id);
  // goal
  boxproject_interfaces__action__TaskAction_Goal__fini(&msg->goal);
}

bool
boxproject_interfaces__action__TaskAction_SendGoal_Request__are_equal(const boxproject_interfaces__action__TaskAction_SendGoal_Request * lhs, const boxproject_interfaces__action__TaskAction_SendGoal_Request * rhs)
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
  if (!boxproject_interfaces__action__TaskAction_Goal__are_equal(
      &(lhs->goal), &(rhs->goal)))
  {
    return false;
  }
  return true;
}

bool
boxproject_interfaces__action__TaskAction_SendGoal_Request__copy(
  const boxproject_interfaces__action__TaskAction_SendGoal_Request * input,
  boxproject_interfaces__action__TaskAction_SendGoal_Request * output)
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
  if (!boxproject_interfaces__action__TaskAction_Goal__copy(
      &(input->goal), &(output->goal)))
  {
    return false;
  }
  return true;
}

boxproject_interfaces__action__TaskAction_SendGoal_Request *
boxproject_interfaces__action__TaskAction_SendGoal_Request__create()
{
  rcutils_allocator_t allocator = rcutils_get_default_allocator();
  boxproject_interfaces__action__TaskAction_SendGoal_Request * msg = (boxproject_interfaces__action__TaskAction_SendGoal_Request *)allocator.allocate(sizeof(boxproject_interfaces__action__TaskAction_SendGoal_Request), allocator.state);
  if (!msg) {
    return NULL;
  }
  memset(msg, 0, sizeof(boxproject_interfaces__action__TaskAction_SendGoal_Request));
  bool success = boxproject_interfaces__action__TaskAction_SendGoal_Request__init(msg);
  if (!success) {
    allocator.deallocate(msg, allocator.state);
    return NULL;
  }
  return msg;
}

void
boxproject_interfaces__action__TaskAction_SendGoal_Request__destroy(boxproject_interfaces__action__TaskAction_SendGoal_Request * msg)
{
  rcutils_allocator_t allocator = rcutils_get_default_allocator();
  if (msg) {
    boxproject_interfaces__action__TaskAction_SendGoal_Request__fini(msg);
  }
  allocator.deallocate(msg, allocator.state);
}


bool
boxproject_interfaces__action__TaskAction_SendGoal_Request__Sequence__init(boxproject_interfaces__action__TaskAction_SendGoal_Request__Sequence * array, size_t size)
{
  if (!array) {
    return false;
  }
  rcutils_allocator_t allocator = rcutils_get_default_allocator();
  boxproject_interfaces__action__TaskAction_SendGoal_Request * data = NULL;

  if (size) {
    data = (boxproject_interfaces__action__TaskAction_SendGoal_Request *)allocator.zero_allocate(size, sizeof(boxproject_interfaces__action__TaskAction_SendGoal_Request), allocator.state);
    if (!data) {
      return false;
    }
    // initialize all array elements
    size_t i;
    for (i = 0; i < size; ++i) {
      bool success = boxproject_interfaces__action__TaskAction_SendGoal_Request__init(&data[i]);
      if (!success) {
        break;
      }
    }
    if (i < size) {
      // if initialization failed finalize the already initialized array elements
      for (; i > 0; --i) {
        boxproject_interfaces__action__TaskAction_SendGoal_Request__fini(&data[i - 1]);
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
boxproject_interfaces__action__TaskAction_SendGoal_Request__Sequence__fini(boxproject_interfaces__action__TaskAction_SendGoal_Request__Sequence * array)
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
      boxproject_interfaces__action__TaskAction_SendGoal_Request__fini(&array->data[i]);
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

boxproject_interfaces__action__TaskAction_SendGoal_Request__Sequence *
boxproject_interfaces__action__TaskAction_SendGoal_Request__Sequence__create(size_t size)
{
  rcutils_allocator_t allocator = rcutils_get_default_allocator();
  boxproject_interfaces__action__TaskAction_SendGoal_Request__Sequence * array = (boxproject_interfaces__action__TaskAction_SendGoal_Request__Sequence *)allocator.allocate(sizeof(boxproject_interfaces__action__TaskAction_SendGoal_Request__Sequence), allocator.state);
  if (!array) {
    return NULL;
  }
  bool success = boxproject_interfaces__action__TaskAction_SendGoal_Request__Sequence__init(array, size);
  if (!success) {
    allocator.deallocate(array, allocator.state);
    return NULL;
  }
  return array;
}

void
boxproject_interfaces__action__TaskAction_SendGoal_Request__Sequence__destroy(boxproject_interfaces__action__TaskAction_SendGoal_Request__Sequence * array)
{
  rcutils_allocator_t allocator = rcutils_get_default_allocator();
  if (array) {
    boxproject_interfaces__action__TaskAction_SendGoal_Request__Sequence__fini(array);
  }
  allocator.deallocate(array, allocator.state);
}

bool
boxproject_interfaces__action__TaskAction_SendGoal_Request__Sequence__are_equal(const boxproject_interfaces__action__TaskAction_SendGoal_Request__Sequence * lhs, const boxproject_interfaces__action__TaskAction_SendGoal_Request__Sequence * rhs)
{
  if (!lhs || !rhs) {
    return false;
  }
  if (lhs->size != rhs->size) {
    return false;
  }
  for (size_t i = 0; i < lhs->size; ++i) {
    if (!boxproject_interfaces__action__TaskAction_SendGoal_Request__are_equal(&(lhs->data[i]), &(rhs->data[i]))) {
      return false;
    }
  }
  return true;
}

bool
boxproject_interfaces__action__TaskAction_SendGoal_Request__Sequence__copy(
  const boxproject_interfaces__action__TaskAction_SendGoal_Request__Sequence * input,
  boxproject_interfaces__action__TaskAction_SendGoal_Request__Sequence * output)
{
  if (!input || !output) {
    return false;
  }
  if (output->capacity < input->size) {
    const size_t allocation_size =
      input->size * sizeof(boxproject_interfaces__action__TaskAction_SendGoal_Request);
    rcutils_allocator_t allocator = rcutils_get_default_allocator();
    boxproject_interfaces__action__TaskAction_SendGoal_Request * data =
      (boxproject_interfaces__action__TaskAction_SendGoal_Request *)allocator.reallocate(
      output->data, allocation_size, allocator.state);
    if (!data) {
      return false;
    }
    // If reallocation succeeded, memory may or may not have been moved
    // to fulfill the allocation request, invalidating output->data.
    output->data = data;
    for (size_t i = output->capacity; i < input->size; ++i) {
      if (!boxproject_interfaces__action__TaskAction_SendGoal_Request__init(&output->data[i])) {
        // If initialization of any new item fails, roll back
        // all previously initialized items. Existing items
        // in output are to be left unmodified.
        for (; i-- > output->capacity; ) {
          boxproject_interfaces__action__TaskAction_SendGoal_Request__fini(&output->data[i]);
        }
        return false;
      }
    }
    output->capacity = input->size;
  }
  output->size = input->size;
  for (size_t i = 0; i < input->size; ++i) {
    if (!boxproject_interfaces__action__TaskAction_SendGoal_Request__copy(
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
boxproject_interfaces__action__TaskAction_SendGoal_Response__init(boxproject_interfaces__action__TaskAction_SendGoal_Response * msg)
{
  if (!msg) {
    return false;
  }
  // accepted
  // stamp
  if (!builtin_interfaces__msg__Time__init(&msg->stamp)) {
    boxproject_interfaces__action__TaskAction_SendGoal_Response__fini(msg);
    return false;
  }
  return true;
}

void
boxproject_interfaces__action__TaskAction_SendGoal_Response__fini(boxproject_interfaces__action__TaskAction_SendGoal_Response * msg)
{
  if (!msg) {
    return;
  }
  // accepted
  // stamp
  builtin_interfaces__msg__Time__fini(&msg->stamp);
}

bool
boxproject_interfaces__action__TaskAction_SendGoal_Response__are_equal(const boxproject_interfaces__action__TaskAction_SendGoal_Response * lhs, const boxproject_interfaces__action__TaskAction_SendGoal_Response * rhs)
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
boxproject_interfaces__action__TaskAction_SendGoal_Response__copy(
  const boxproject_interfaces__action__TaskAction_SendGoal_Response * input,
  boxproject_interfaces__action__TaskAction_SendGoal_Response * output)
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

boxproject_interfaces__action__TaskAction_SendGoal_Response *
boxproject_interfaces__action__TaskAction_SendGoal_Response__create()
{
  rcutils_allocator_t allocator = rcutils_get_default_allocator();
  boxproject_interfaces__action__TaskAction_SendGoal_Response * msg = (boxproject_interfaces__action__TaskAction_SendGoal_Response *)allocator.allocate(sizeof(boxproject_interfaces__action__TaskAction_SendGoal_Response), allocator.state);
  if (!msg) {
    return NULL;
  }
  memset(msg, 0, sizeof(boxproject_interfaces__action__TaskAction_SendGoal_Response));
  bool success = boxproject_interfaces__action__TaskAction_SendGoal_Response__init(msg);
  if (!success) {
    allocator.deallocate(msg, allocator.state);
    return NULL;
  }
  return msg;
}

void
boxproject_interfaces__action__TaskAction_SendGoal_Response__destroy(boxproject_interfaces__action__TaskAction_SendGoal_Response * msg)
{
  rcutils_allocator_t allocator = rcutils_get_default_allocator();
  if (msg) {
    boxproject_interfaces__action__TaskAction_SendGoal_Response__fini(msg);
  }
  allocator.deallocate(msg, allocator.state);
}


bool
boxproject_interfaces__action__TaskAction_SendGoal_Response__Sequence__init(boxproject_interfaces__action__TaskAction_SendGoal_Response__Sequence * array, size_t size)
{
  if (!array) {
    return false;
  }
  rcutils_allocator_t allocator = rcutils_get_default_allocator();
  boxproject_interfaces__action__TaskAction_SendGoal_Response * data = NULL;

  if (size) {
    data = (boxproject_interfaces__action__TaskAction_SendGoal_Response *)allocator.zero_allocate(size, sizeof(boxproject_interfaces__action__TaskAction_SendGoal_Response), allocator.state);
    if (!data) {
      return false;
    }
    // initialize all array elements
    size_t i;
    for (i = 0; i < size; ++i) {
      bool success = boxproject_interfaces__action__TaskAction_SendGoal_Response__init(&data[i]);
      if (!success) {
        break;
      }
    }
    if (i < size) {
      // if initialization failed finalize the already initialized array elements
      for (; i > 0; --i) {
        boxproject_interfaces__action__TaskAction_SendGoal_Response__fini(&data[i - 1]);
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
boxproject_interfaces__action__TaskAction_SendGoal_Response__Sequence__fini(boxproject_interfaces__action__TaskAction_SendGoal_Response__Sequence * array)
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
      boxproject_interfaces__action__TaskAction_SendGoal_Response__fini(&array->data[i]);
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

boxproject_interfaces__action__TaskAction_SendGoal_Response__Sequence *
boxproject_interfaces__action__TaskAction_SendGoal_Response__Sequence__create(size_t size)
{
  rcutils_allocator_t allocator = rcutils_get_default_allocator();
  boxproject_interfaces__action__TaskAction_SendGoal_Response__Sequence * array = (boxproject_interfaces__action__TaskAction_SendGoal_Response__Sequence *)allocator.allocate(sizeof(boxproject_interfaces__action__TaskAction_SendGoal_Response__Sequence), allocator.state);
  if (!array) {
    return NULL;
  }
  bool success = boxproject_interfaces__action__TaskAction_SendGoal_Response__Sequence__init(array, size);
  if (!success) {
    allocator.deallocate(array, allocator.state);
    return NULL;
  }
  return array;
}

void
boxproject_interfaces__action__TaskAction_SendGoal_Response__Sequence__destroy(boxproject_interfaces__action__TaskAction_SendGoal_Response__Sequence * array)
{
  rcutils_allocator_t allocator = rcutils_get_default_allocator();
  if (array) {
    boxproject_interfaces__action__TaskAction_SendGoal_Response__Sequence__fini(array);
  }
  allocator.deallocate(array, allocator.state);
}

bool
boxproject_interfaces__action__TaskAction_SendGoal_Response__Sequence__are_equal(const boxproject_interfaces__action__TaskAction_SendGoal_Response__Sequence * lhs, const boxproject_interfaces__action__TaskAction_SendGoal_Response__Sequence * rhs)
{
  if (!lhs || !rhs) {
    return false;
  }
  if (lhs->size != rhs->size) {
    return false;
  }
  for (size_t i = 0; i < lhs->size; ++i) {
    if (!boxproject_interfaces__action__TaskAction_SendGoal_Response__are_equal(&(lhs->data[i]), &(rhs->data[i]))) {
      return false;
    }
  }
  return true;
}

bool
boxproject_interfaces__action__TaskAction_SendGoal_Response__Sequence__copy(
  const boxproject_interfaces__action__TaskAction_SendGoal_Response__Sequence * input,
  boxproject_interfaces__action__TaskAction_SendGoal_Response__Sequence * output)
{
  if (!input || !output) {
    return false;
  }
  if (output->capacity < input->size) {
    const size_t allocation_size =
      input->size * sizeof(boxproject_interfaces__action__TaskAction_SendGoal_Response);
    rcutils_allocator_t allocator = rcutils_get_default_allocator();
    boxproject_interfaces__action__TaskAction_SendGoal_Response * data =
      (boxproject_interfaces__action__TaskAction_SendGoal_Response *)allocator.reallocate(
      output->data, allocation_size, allocator.state);
    if (!data) {
      return false;
    }
    // If reallocation succeeded, memory may or may not have been moved
    // to fulfill the allocation request, invalidating output->data.
    output->data = data;
    for (size_t i = output->capacity; i < input->size; ++i) {
      if (!boxproject_interfaces__action__TaskAction_SendGoal_Response__init(&output->data[i])) {
        // If initialization of any new item fails, roll back
        // all previously initialized items. Existing items
        // in output are to be left unmodified.
        for (; i-- > output->capacity; ) {
          boxproject_interfaces__action__TaskAction_SendGoal_Response__fini(&output->data[i]);
        }
        return false;
      }
    }
    output->capacity = input->size;
  }
  output->size = input->size;
  for (size_t i = 0; i < input->size; ++i) {
    if (!boxproject_interfaces__action__TaskAction_SendGoal_Response__copy(
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
boxproject_interfaces__action__TaskAction_GetResult_Request__init(boxproject_interfaces__action__TaskAction_GetResult_Request * msg)
{
  if (!msg) {
    return false;
  }
  // goal_id
  if (!unique_identifier_msgs__msg__UUID__init(&msg->goal_id)) {
    boxproject_interfaces__action__TaskAction_GetResult_Request__fini(msg);
    return false;
  }
  return true;
}

void
boxproject_interfaces__action__TaskAction_GetResult_Request__fini(boxproject_interfaces__action__TaskAction_GetResult_Request * msg)
{
  if (!msg) {
    return;
  }
  // goal_id
  unique_identifier_msgs__msg__UUID__fini(&msg->goal_id);
}

bool
boxproject_interfaces__action__TaskAction_GetResult_Request__are_equal(const boxproject_interfaces__action__TaskAction_GetResult_Request * lhs, const boxproject_interfaces__action__TaskAction_GetResult_Request * rhs)
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
boxproject_interfaces__action__TaskAction_GetResult_Request__copy(
  const boxproject_interfaces__action__TaskAction_GetResult_Request * input,
  boxproject_interfaces__action__TaskAction_GetResult_Request * output)
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

boxproject_interfaces__action__TaskAction_GetResult_Request *
boxproject_interfaces__action__TaskAction_GetResult_Request__create()
{
  rcutils_allocator_t allocator = rcutils_get_default_allocator();
  boxproject_interfaces__action__TaskAction_GetResult_Request * msg = (boxproject_interfaces__action__TaskAction_GetResult_Request *)allocator.allocate(sizeof(boxproject_interfaces__action__TaskAction_GetResult_Request), allocator.state);
  if (!msg) {
    return NULL;
  }
  memset(msg, 0, sizeof(boxproject_interfaces__action__TaskAction_GetResult_Request));
  bool success = boxproject_interfaces__action__TaskAction_GetResult_Request__init(msg);
  if (!success) {
    allocator.deallocate(msg, allocator.state);
    return NULL;
  }
  return msg;
}

void
boxproject_interfaces__action__TaskAction_GetResult_Request__destroy(boxproject_interfaces__action__TaskAction_GetResult_Request * msg)
{
  rcutils_allocator_t allocator = rcutils_get_default_allocator();
  if (msg) {
    boxproject_interfaces__action__TaskAction_GetResult_Request__fini(msg);
  }
  allocator.deallocate(msg, allocator.state);
}


bool
boxproject_interfaces__action__TaskAction_GetResult_Request__Sequence__init(boxproject_interfaces__action__TaskAction_GetResult_Request__Sequence * array, size_t size)
{
  if (!array) {
    return false;
  }
  rcutils_allocator_t allocator = rcutils_get_default_allocator();
  boxproject_interfaces__action__TaskAction_GetResult_Request * data = NULL;

  if (size) {
    data = (boxproject_interfaces__action__TaskAction_GetResult_Request *)allocator.zero_allocate(size, sizeof(boxproject_interfaces__action__TaskAction_GetResult_Request), allocator.state);
    if (!data) {
      return false;
    }
    // initialize all array elements
    size_t i;
    for (i = 0; i < size; ++i) {
      bool success = boxproject_interfaces__action__TaskAction_GetResult_Request__init(&data[i]);
      if (!success) {
        break;
      }
    }
    if (i < size) {
      // if initialization failed finalize the already initialized array elements
      for (; i > 0; --i) {
        boxproject_interfaces__action__TaskAction_GetResult_Request__fini(&data[i - 1]);
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
boxproject_interfaces__action__TaskAction_GetResult_Request__Sequence__fini(boxproject_interfaces__action__TaskAction_GetResult_Request__Sequence * array)
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
      boxproject_interfaces__action__TaskAction_GetResult_Request__fini(&array->data[i]);
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

boxproject_interfaces__action__TaskAction_GetResult_Request__Sequence *
boxproject_interfaces__action__TaskAction_GetResult_Request__Sequence__create(size_t size)
{
  rcutils_allocator_t allocator = rcutils_get_default_allocator();
  boxproject_interfaces__action__TaskAction_GetResult_Request__Sequence * array = (boxproject_interfaces__action__TaskAction_GetResult_Request__Sequence *)allocator.allocate(sizeof(boxproject_interfaces__action__TaskAction_GetResult_Request__Sequence), allocator.state);
  if (!array) {
    return NULL;
  }
  bool success = boxproject_interfaces__action__TaskAction_GetResult_Request__Sequence__init(array, size);
  if (!success) {
    allocator.deallocate(array, allocator.state);
    return NULL;
  }
  return array;
}

void
boxproject_interfaces__action__TaskAction_GetResult_Request__Sequence__destroy(boxproject_interfaces__action__TaskAction_GetResult_Request__Sequence * array)
{
  rcutils_allocator_t allocator = rcutils_get_default_allocator();
  if (array) {
    boxproject_interfaces__action__TaskAction_GetResult_Request__Sequence__fini(array);
  }
  allocator.deallocate(array, allocator.state);
}

bool
boxproject_interfaces__action__TaskAction_GetResult_Request__Sequence__are_equal(const boxproject_interfaces__action__TaskAction_GetResult_Request__Sequence * lhs, const boxproject_interfaces__action__TaskAction_GetResult_Request__Sequence * rhs)
{
  if (!lhs || !rhs) {
    return false;
  }
  if (lhs->size != rhs->size) {
    return false;
  }
  for (size_t i = 0; i < lhs->size; ++i) {
    if (!boxproject_interfaces__action__TaskAction_GetResult_Request__are_equal(&(lhs->data[i]), &(rhs->data[i]))) {
      return false;
    }
  }
  return true;
}

bool
boxproject_interfaces__action__TaskAction_GetResult_Request__Sequence__copy(
  const boxproject_interfaces__action__TaskAction_GetResult_Request__Sequence * input,
  boxproject_interfaces__action__TaskAction_GetResult_Request__Sequence * output)
{
  if (!input || !output) {
    return false;
  }
  if (output->capacity < input->size) {
    const size_t allocation_size =
      input->size * sizeof(boxproject_interfaces__action__TaskAction_GetResult_Request);
    rcutils_allocator_t allocator = rcutils_get_default_allocator();
    boxproject_interfaces__action__TaskAction_GetResult_Request * data =
      (boxproject_interfaces__action__TaskAction_GetResult_Request *)allocator.reallocate(
      output->data, allocation_size, allocator.state);
    if (!data) {
      return false;
    }
    // If reallocation succeeded, memory may or may not have been moved
    // to fulfill the allocation request, invalidating output->data.
    output->data = data;
    for (size_t i = output->capacity; i < input->size; ++i) {
      if (!boxproject_interfaces__action__TaskAction_GetResult_Request__init(&output->data[i])) {
        // If initialization of any new item fails, roll back
        // all previously initialized items. Existing items
        // in output are to be left unmodified.
        for (; i-- > output->capacity; ) {
          boxproject_interfaces__action__TaskAction_GetResult_Request__fini(&output->data[i]);
        }
        return false;
      }
    }
    output->capacity = input->size;
  }
  output->size = input->size;
  for (size_t i = 0; i < input->size; ++i) {
    if (!boxproject_interfaces__action__TaskAction_GetResult_Request__copy(
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
// #include "boxproject_interfaces/action/detail/task_action__functions.h"

bool
boxproject_interfaces__action__TaskAction_GetResult_Response__init(boxproject_interfaces__action__TaskAction_GetResult_Response * msg)
{
  if (!msg) {
    return false;
  }
  // status
  // result
  if (!boxproject_interfaces__action__TaskAction_Result__init(&msg->result)) {
    boxproject_interfaces__action__TaskAction_GetResult_Response__fini(msg);
    return false;
  }
  return true;
}

void
boxproject_interfaces__action__TaskAction_GetResult_Response__fini(boxproject_interfaces__action__TaskAction_GetResult_Response * msg)
{
  if (!msg) {
    return;
  }
  // status
  // result
  boxproject_interfaces__action__TaskAction_Result__fini(&msg->result);
}

bool
boxproject_interfaces__action__TaskAction_GetResult_Response__are_equal(const boxproject_interfaces__action__TaskAction_GetResult_Response * lhs, const boxproject_interfaces__action__TaskAction_GetResult_Response * rhs)
{
  if (!lhs || !rhs) {
    return false;
  }
  // status
  if (lhs->status != rhs->status) {
    return false;
  }
  // result
  if (!boxproject_interfaces__action__TaskAction_Result__are_equal(
      &(lhs->result), &(rhs->result)))
  {
    return false;
  }
  return true;
}

bool
boxproject_interfaces__action__TaskAction_GetResult_Response__copy(
  const boxproject_interfaces__action__TaskAction_GetResult_Response * input,
  boxproject_interfaces__action__TaskAction_GetResult_Response * output)
{
  if (!input || !output) {
    return false;
  }
  // status
  output->status = input->status;
  // result
  if (!boxproject_interfaces__action__TaskAction_Result__copy(
      &(input->result), &(output->result)))
  {
    return false;
  }
  return true;
}

boxproject_interfaces__action__TaskAction_GetResult_Response *
boxproject_interfaces__action__TaskAction_GetResult_Response__create()
{
  rcutils_allocator_t allocator = rcutils_get_default_allocator();
  boxproject_interfaces__action__TaskAction_GetResult_Response * msg = (boxproject_interfaces__action__TaskAction_GetResult_Response *)allocator.allocate(sizeof(boxproject_interfaces__action__TaskAction_GetResult_Response), allocator.state);
  if (!msg) {
    return NULL;
  }
  memset(msg, 0, sizeof(boxproject_interfaces__action__TaskAction_GetResult_Response));
  bool success = boxproject_interfaces__action__TaskAction_GetResult_Response__init(msg);
  if (!success) {
    allocator.deallocate(msg, allocator.state);
    return NULL;
  }
  return msg;
}

void
boxproject_interfaces__action__TaskAction_GetResult_Response__destroy(boxproject_interfaces__action__TaskAction_GetResult_Response * msg)
{
  rcutils_allocator_t allocator = rcutils_get_default_allocator();
  if (msg) {
    boxproject_interfaces__action__TaskAction_GetResult_Response__fini(msg);
  }
  allocator.deallocate(msg, allocator.state);
}


bool
boxproject_interfaces__action__TaskAction_GetResult_Response__Sequence__init(boxproject_interfaces__action__TaskAction_GetResult_Response__Sequence * array, size_t size)
{
  if (!array) {
    return false;
  }
  rcutils_allocator_t allocator = rcutils_get_default_allocator();
  boxproject_interfaces__action__TaskAction_GetResult_Response * data = NULL;

  if (size) {
    data = (boxproject_interfaces__action__TaskAction_GetResult_Response *)allocator.zero_allocate(size, sizeof(boxproject_interfaces__action__TaskAction_GetResult_Response), allocator.state);
    if (!data) {
      return false;
    }
    // initialize all array elements
    size_t i;
    for (i = 0; i < size; ++i) {
      bool success = boxproject_interfaces__action__TaskAction_GetResult_Response__init(&data[i]);
      if (!success) {
        break;
      }
    }
    if (i < size) {
      // if initialization failed finalize the already initialized array elements
      for (; i > 0; --i) {
        boxproject_interfaces__action__TaskAction_GetResult_Response__fini(&data[i - 1]);
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
boxproject_interfaces__action__TaskAction_GetResult_Response__Sequence__fini(boxproject_interfaces__action__TaskAction_GetResult_Response__Sequence * array)
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
      boxproject_interfaces__action__TaskAction_GetResult_Response__fini(&array->data[i]);
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

boxproject_interfaces__action__TaskAction_GetResult_Response__Sequence *
boxproject_interfaces__action__TaskAction_GetResult_Response__Sequence__create(size_t size)
{
  rcutils_allocator_t allocator = rcutils_get_default_allocator();
  boxproject_interfaces__action__TaskAction_GetResult_Response__Sequence * array = (boxproject_interfaces__action__TaskAction_GetResult_Response__Sequence *)allocator.allocate(sizeof(boxproject_interfaces__action__TaskAction_GetResult_Response__Sequence), allocator.state);
  if (!array) {
    return NULL;
  }
  bool success = boxproject_interfaces__action__TaskAction_GetResult_Response__Sequence__init(array, size);
  if (!success) {
    allocator.deallocate(array, allocator.state);
    return NULL;
  }
  return array;
}

void
boxproject_interfaces__action__TaskAction_GetResult_Response__Sequence__destroy(boxproject_interfaces__action__TaskAction_GetResult_Response__Sequence * array)
{
  rcutils_allocator_t allocator = rcutils_get_default_allocator();
  if (array) {
    boxproject_interfaces__action__TaskAction_GetResult_Response__Sequence__fini(array);
  }
  allocator.deallocate(array, allocator.state);
}

bool
boxproject_interfaces__action__TaskAction_GetResult_Response__Sequence__are_equal(const boxproject_interfaces__action__TaskAction_GetResult_Response__Sequence * lhs, const boxproject_interfaces__action__TaskAction_GetResult_Response__Sequence * rhs)
{
  if (!lhs || !rhs) {
    return false;
  }
  if (lhs->size != rhs->size) {
    return false;
  }
  for (size_t i = 0; i < lhs->size; ++i) {
    if (!boxproject_interfaces__action__TaskAction_GetResult_Response__are_equal(&(lhs->data[i]), &(rhs->data[i]))) {
      return false;
    }
  }
  return true;
}

bool
boxproject_interfaces__action__TaskAction_GetResult_Response__Sequence__copy(
  const boxproject_interfaces__action__TaskAction_GetResult_Response__Sequence * input,
  boxproject_interfaces__action__TaskAction_GetResult_Response__Sequence * output)
{
  if (!input || !output) {
    return false;
  }
  if (output->capacity < input->size) {
    const size_t allocation_size =
      input->size * sizeof(boxproject_interfaces__action__TaskAction_GetResult_Response);
    rcutils_allocator_t allocator = rcutils_get_default_allocator();
    boxproject_interfaces__action__TaskAction_GetResult_Response * data =
      (boxproject_interfaces__action__TaskAction_GetResult_Response *)allocator.reallocate(
      output->data, allocation_size, allocator.state);
    if (!data) {
      return false;
    }
    // If reallocation succeeded, memory may or may not have been moved
    // to fulfill the allocation request, invalidating output->data.
    output->data = data;
    for (size_t i = output->capacity; i < input->size; ++i) {
      if (!boxproject_interfaces__action__TaskAction_GetResult_Response__init(&output->data[i])) {
        // If initialization of any new item fails, roll back
        // all previously initialized items. Existing items
        // in output are to be left unmodified.
        for (; i-- > output->capacity; ) {
          boxproject_interfaces__action__TaskAction_GetResult_Response__fini(&output->data[i]);
        }
        return false;
      }
    }
    output->capacity = input->size;
  }
  output->size = input->size;
  for (size_t i = 0; i < input->size; ++i) {
    if (!boxproject_interfaces__action__TaskAction_GetResult_Response__copy(
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
// #include "boxproject_interfaces/action/detail/task_action__functions.h"

bool
boxproject_interfaces__action__TaskAction_FeedbackMessage__init(boxproject_interfaces__action__TaskAction_FeedbackMessage * msg)
{
  if (!msg) {
    return false;
  }
  // goal_id
  if (!unique_identifier_msgs__msg__UUID__init(&msg->goal_id)) {
    boxproject_interfaces__action__TaskAction_FeedbackMessage__fini(msg);
    return false;
  }
  // feedback
  if (!boxproject_interfaces__action__TaskAction_Feedback__init(&msg->feedback)) {
    boxproject_interfaces__action__TaskAction_FeedbackMessage__fini(msg);
    return false;
  }
  return true;
}

void
boxproject_interfaces__action__TaskAction_FeedbackMessage__fini(boxproject_interfaces__action__TaskAction_FeedbackMessage * msg)
{
  if (!msg) {
    return;
  }
  // goal_id
  unique_identifier_msgs__msg__UUID__fini(&msg->goal_id);
  // feedback
  boxproject_interfaces__action__TaskAction_Feedback__fini(&msg->feedback);
}

bool
boxproject_interfaces__action__TaskAction_FeedbackMessage__are_equal(const boxproject_interfaces__action__TaskAction_FeedbackMessage * lhs, const boxproject_interfaces__action__TaskAction_FeedbackMessage * rhs)
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
  if (!boxproject_interfaces__action__TaskAction_Feedback__are_equal(
      &(lhs->feedback), &(rhs->feedback)))
  {
    return false;
  }
  return true;
}

bool
boxproject_interfaces__action__TaskAction_FeedbackMessage__copy(
  const boxproject_interfaces__action__TaskAction_FeedbackMessage * input,
  boxproject_interfaces__action__TaskAction_FeedbackMessage * output)
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
  if (!boxproject_interfaces__action__TaskAction_Feedback__copy(
      &(input->feedback), &(output->feedback)))
  {
    return false;
  }
  return true;
}

boxproject_interfaces__action__TaskAction_FeedbackMessage *
boxproject_interfaces__action__TaskAction_FeedbackMessage__create()
{
  rcutils_allocator_t allocator = rcutils_get_default_allocator();
  boxproject_interfaces__action__TaskAction_FeedbackMessage * msg = (boxproject_interfaces__action__TaskAction_FeedbackMessage *)allocator.allocate(sizeof(boxproject_interfaces__action__TaskAction_FeedbackMessage), allocator.state);
  if (!msg) {
    return NULL;
  }
  memset(msg, 0, sizeof(boxproject_interfaces__action__TaskAction_FeedbackMessage));
  bool success = boxproject_interfaces__action__TaskAction_FeedbackMessage__init(msg);
  if (!success) {
    allocator.deallocate(msg, allocator.state);
    return NULL;
  }
  return msg;
}

void
boxproject_interfaces__action__TaskAction_FeedbackMessage__destroy(boxproject_interfaces__action__TaskAction_FeedbackMessage * msg)
{
  rcutils_allocator_t allocator = rcutils_get_default_allocator();
  if (msg) {
    boxproject_interfaces__action__TaskAction_FeedbackMessage__fini(msg);
  }
  allocator.deallocate(msg, allocator.state);
}


bool
boxproject_interfaces__action__TaskAction_FeedbackMessage__Sequence__init(boxproject_interfaces__action__TaskAction_FeedbackMessage__Sequence * array, size_t size)
{
  if (!array) {
    return false;
  }
  rcutils_allocator_t allocator = rcutils_get_default_allocator();
  boxproject_interfaces__action__TaskAction_FeedbackMessage * data = NULL;

  if (size) {
    data = (boxproject_interfaces__action__TaskAction_FeedbackMessage *)allocator.zero_allocate(size, sizeof(boxproject_interfaces__action__TaskAction_FeedbackMessage), allocator.state);
    if (!data) {
      return false;
    }
    // initialize all array elements
    size_t i;
    for (i = 0; i < size; ++i) {
      bool success = boxproject_interfaces__action__TaskAction_FeedbackMessage__init(&data[i]);
      if (!success) {
        break;
      }
    }
    if (i < size) {
      // if initialization failed finalize the already initialized array elements
      for (; i > 0; --i) {
        boxproject_interfaces__action__TaskAction_FeedbackMessage__fini(&data[i - 1]);
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
boxproject_interfaces__action__TaskAction_FeedbackMessage__Sequence__fini(boxproject_interfaces__action__TaskAction_FeedbackMessage__Sequence * array)
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
      boxproject_interfaces__action__TaskAction_FeedbackMessage__fini(&array->data[i]);
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

boxproject_interfaces__action__TaskAction_FeedbackMessage__Sequence *
boxproject_interfaces__action__TaskAction_FeedbackMessage__Sequence__create(size_t size)
{
  rcutils_allocator_t allocator = rcutils_get_default_allocator();
  boxproject_interfaces__action__TaskAction_FeedbackMessage__Sequence * array = (boxproject_interfaces__action__TaskAction_FeedbackMessage__Sequence *)allocator.allocate(sizeof(boxproject_interfaces__action__TaskAction_FeedbackMessage__Sequence), allocator.state);
  if (!array) {
    return NULL;
  }
  bool success = boxproject_interfaces__action__TaskAction_FeedbackMessage__Sequence__init(array, size);
  if (!success) {
    allocator.deallocate(array, allocator.state);
    return NULL;
  }
  return array;
}

void
boxproject_interfaces__action__TaskAction_FeedbackMessage__Sequence__destroy(boxproject_interfaces__action__TaskAction_FeedbackMessage__Sequence * array)
{
  rcutils_allocator_t allocator = rcutils_get_default_allocator();
  if (array) {
    boxproject_interfaces__action__TaskAction_FeedbackMessage__Sequence__fini(array);
  }
  allocator.deallocate(array, allocator.state);
}

bool
boxproject_interfaces__action__TaskAction_FeedbackMessage__Sequence__are_equal(const boxproject_interfaces__action__TaskAction_FeedbackMessage__Sequence * lhs, const boxproject_interfaces__action__TaskAction_FeedbackMessage__Sequence * rhs)
{
  if (!lhs || !rhs) {
    return false;
  }
  if (lhs->size != rhs->size) {
    return false;
  }
  for (size_t i = 0; i < lhs->size; ++i) {
    if (!boxproject_interfaces__action__TaskAction_FeedbackMessage__are_equal(&(lhs->data[i]), &(rhs->data[i]))) {
      return false;
    }
  }
  return true;
}

bool
boxproject_interfaces__action__TaskAction_FeedbackMessage__Sequence__copy(
  const boxproject_interfaces__action__TaskAction_FeedbackMessage__Sequence * input,
  boxproject_interfaces__action__TaskAction_FeedbackMessage__Sequence * output)
{
  if (!input || !output) {
    return false;
  }
  if (output->capacity < input->size) {
    const size_t allocation_size =
      input->size * sizeof(boxproject_interfaces__action__TaskAction_FeedbackMessage);
    rcutils_allocator_t allocator = rcutils_get_default_allocator();
    boxproject_interfaces__action__TaskAction_FeedbackMessage * data =
      (boxproject_interfaces__action__TaskAction_FeedbackMessage *)allocator.reallocate(
      output->data, allocation_size, allocator.state);
    if (!data) {
      return false;
    }
    // If reallocation succeeded, memory may or may not have been moved
    // to fulfill the allocation request, invalidating output->data.
    output->data = data;
    for (size_t i = output->capacity; i < input->size; ++i) {
      if (!boxproject_interfaces__action__TaskAction_FeedbackMessage__init(&output->data[i])) {
        // If initialization of any new item fails, roll back
        // all previously initialized items. Existing items
        // in output are to be left unmodified.
        for (; i-- > output->capacity; ) {
          boxproject_interfaces__action__TaskAction_FeedbackMessage__fini(&output->data[i]);
        }
        return false;
      }
    }
    output->capacity = input->size;
  }
  output->size = input->size;
  for (size_t i = 0; i < input->size; ++i) {
    if (!boxproject_interfaces__action__TaskAction_FeedbackMessage__copy(
        &(input->data[i]), &(output->data[i])))
    {
      return false;
    }
  }
  return true;
}
