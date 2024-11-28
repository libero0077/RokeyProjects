// generated from rosidl_generator_c/resource/idl__functions.h.em
// with input from menu_order_interfaces:action/Serve.idl
// generated code does not contain a copyright notice

#ifndef MENU_ORDER_INTERFACES__ACTION__DETAIL__SERVE__FUNCTIONS_H_
#define MENU_ORDER_INTERFACES__ACTION__DETAIL__SERVE__FUNCTIONS_H_

#ifdef __cplusplus
extern "C"
{
#endif

#include <stdbool.h>
#include <stdlib.h>

#include "rosidl_runtime_c/visibility_control.h"
#include "menu_order_interfaces/msg/rosidl_generator_c__visibility_control.h"

#include "menu_order_interfaces/action/detail/serve__struct.h"

/// Initialize action/Serve message.
/**
 * If the init function is called twice for the same message without
 * calling fini inbetween previously allocated memory will be leaked.
 * \param[in,out] msg The previously allocated message pointer.
 * Fields without a default value will not be initialized by this function.
 * You might want to call memset(msg, 0, sizeof(
 * menu_order_interfaces__action__Serve_Goal
 * )) before or use
 * menu_order_interfaces__action__Serve_Goal__create()
 * to allocate and initialize the message.
 * \return true if initialization was successful, otherwise false
 */
ROSIDL_GENERATOR_C_PUBLIC_menu_order_interfaces
bool
menu_order_interfaces__action__Serve_Goal__init(menu_order_interfaces__action__Serve_Goal * msg);

/// Finalize action/Serve message.
/**
 * \param[in,out] msg The allocated message pointer.
 */
ROSIDL_GENERATOR_C_PUBLIC_menu_order_interfaces
void
menu_order_interfaces__action__Serve_Goal__fini(menu_order_interfaces__action__Serve_Goal * msg);

/// Create action/Serve message.
/**
 * It allocates the memory for the message, sets the memory to zero, and
 * calls
 * menu_order_interfaces__action__Serve_Goal__init().
 * \return The pointer to the initialized message if successful,
 * otherwise NULL
 */
ROSIDL_GENERATOR_C_PUBLIC_menu_order_interfaces
menu_order_interfaces__action__Serve_Goal *
menu_order_interfaces__action__Serve_Goal__create();

/// Destroy action/Serve message.
/**
 * It calls
 * menu_order_interfaces__action__Serve_Goal__fini()
 * and frees the memory of the message.
 * \param[in,out] msg The allocated message pointer.
 */
ROSIDL_GENERATOR_C_PUBLIC_menu_order_interfaces
void
menu_order_interfaces__action__Serve_Goal__destroy(menu_order_interfaces__action__Serve_Goal * msg);

/// Check for action/Serve message equality.
/**
 * \param[in] lhs The message on the left hand size of the equality operator.
 * \param[in] rhs The message on the right hand size of the equality operator.
 * \return true if messages are equal, otherwise false.
 */
ROSIDL_GENERATOR_C_PUBLIC_menu_order_interfaces
bool
menu_order_interfaces__action__Serve_Goal__are_equal(const menu_order_interfaces__action__Serve_Goal * lhs, const menu_order_interfaces__action__Serve_Goal * rhs);

/// Copy a action/Serve message.
/**
 * This functions performs a deep copy, as opposed to the shallow copy that
 * plain assignment yields.
 *
 * \param[in] input The source message pointer.
 * \param[out] output The target message pointer, which must
 *   have been initialized before calling this function.
 * \return true if successful, or false if either pointer is null
 *   or memory allocation fails.
 */
ROSIDL_GENERATOR_C_PUBLIC_menu_order_interfaces
bool
menu_order_interfaces__action__Serve_Goal__copy(
  const menu_order_interfaces__action__Serve_Goal * input,
  menu_order_interfaces__action__Serve_Goal * output);

/// Initialize array of action/Serve messages.
/**
 * It allocates the memory for the number of elements and calls
 * menu_order_interfaces__action__Serve_Goal__init()
 * for each element of the array.
 * \param[in,out] array The allocated array pointer.
 * \param[in] size The size / capacity of the array.
 * \return true if initialization was successful, otherwise false
 * If the array pointer is valid and the size is zero it is guaranteed
 # to return true.
 */
ROSIDL_GENERATOR_C_PUBLIC_menu_order_interfaces
bool
menu_order_interfaces__action__Serve_Goal__Sequence__init(menu_order_interfaces__action__Serve_Goal__Sequence * array, size_t size);

/// Finalize array of action/Serve messages.
/**
 * It calls
 * menu_order_interfaces__action__Serve_Goal__fini()
 * for each element of the array and frees the memory for the number of
 * elements.
 * \param[in,out] array The initialized array pointer.
 */
ROSIDL_GENERATOR_C_PUBLIC_menu_order_interfaces
void
menu_order_interfaces__action__Serve_Goal__Sequence__fini(menu_order_interfaces__action__Serve_Goal__Sequence * array);

/// Create array of action/Serve messages.
/**
 * It allocates the memory for the array and calls
 * menu_order_interfaces__action__Serve_Goal__Sequence__init().
 * \param[in] size The size / capacity of the array.
 * \return The pointer to the initialized array if successful, otherwise NULL
 */
ROSIDL_GENERATOR_C_PUBLIC_menu_order_interfaces
menu_order_interfaces__action__Serve_Goal__Sequence *
menu_order_interfaces__action__Serve_Goal__Sequence__create(size_t size);

/// Destroy array of action/Serve messages.
/**
 * It calls
 * menu_order_interfaces__action__Serve_Goal__Sequence__fini()
 * on the array,
 * and frees the memory of the array.
 * \param[in,out] array The initialized array pointer.
 */
ROSIDL_GENERATOR_C_PUBLIC_menu_order_interfaces
void
menu_order_interfaces__action__Serve_Goal__Sequence__destroy(menu_order_interfaces__action__Serve_Goal__Sequence * array);

/// Check for action/Serve message array equality.
/**
 * \param[in] lhs The message array on the left hand size of the equality operator.
 * \param[in] rhs The message array on the right hand size of the equality operator.
 * \return true if message arrays are equal in size and content, otherwise false.
 */
ROSIDL_GENERATOR_C_PUBLIC_menu_order_interfaces
bool
menu_order_interfaces__action__Serve_Goal__Sequence__are_equal(const menu_order_interfaces__action__Serve_Goal__Sequence * lhs, const menu_order_interfaces__action__Serve_Goal__Sequence * rhs);

/// Copy an array of action/Serve messages.
/**
 * This functions performs a deep copy, as opposed to the shallow copy that
 * plain assignment yields.
 *
 * \param[in] input The source array pointer.
 * \param[out] output The target array pointer, which must
 *   have been initialized before calling this function.
 * \return true if successful, or false if either pointer
 *   is null or memory allocation fails.
 */
ROSIDL_GENERATOR_C_PUBLIC_menu_order_interfaces
bool
menu_order_interfaces__action__Serve_Goal__Sequence__copy(
  const menu_order_interfaces__action__Serve_Goal__Sequence * input,
  menu_order_interfaces__action__Serve_Goal__Sequence * output);

/// Initialize action/Serve message.
/**
 * If the init function is called twice for the same message without
 * calling fini inbetween previously allocated memory will be leaked.
 * \param[in,out] msg The previously allocated message pointer.
 * Fields without a default value will not be initialized by this function.
 * You might want to call memset(msg, 0, sizeof(
 * menu_order_interfaces__action__Serve_Result
 * )) before or use
 * menu_order_interfaces__action__Serve_Result__create()
 * to allocate and initialize the message.
 * \return true if initialization was successful, otherwise false
 */
ROSIDL_GENERATOR_C_PUBLIC_menu_order_interfaces
bool
menu_order_interfaces__action__Serve_Result__init(menu_order_interfaces__action__Serve_Result * msg);

/// Finalize action/Serve message.
/**
 * \param[in,out] msg The allocated message pointer.
 */
ROSIDL_GENERATOR_C_PUBLIC_menu_order_interfaces
void
menu_order_interfaces__action__Serve_Result__fini(menu_order_interfaces__action__Serve_Result * msg);

/// Create action/Serve message.
/**
 * It allocates the memory for the message, sets the memory to zero, and
 * calls
 * menu_order_interfaces__action__Serve_Result__init().
 * \return The pointer to the initialized message if successful,
 * otherwise NULL
 */
ROSIDL_GENERATOR_C_PUBLIC_menu_order_interfaces
menu_order_interfaces__action__Serve_Result *
menu_order_interfaces__action__Serve_Result__create();

/// Destroy action/Serve message.
/**
 * It calls
 * menu_order_interfaces__action__Serve_Result__fini()
 * and frees the memory of the message.
 * \param[in,out] msg The allocated message pointer.
 */
ROSIDL_GENERATOR_C_PUBLIC_menu_order_interfaces
void
menu_order_interfaces__action__Serve_Result__destroy(menu_order_interfaces__action__Serve_Result * msg);

/// Check for action/Serve message equality.
/**
 * \param[in] lhs The message on the left hand size of the equality operator.
 * \param[in] rhs The message on the right hand size of the equality operator.
 * \return true if messages are equal, otherwise false.
 */
ROSIDL_GENERATOR_C_PUBLIC_menu_order_interfaces
bool
menu_order_interfaces__action__Serve_Result__are_equal(const menu_order_interfaces__action__Serve_Result * lhs, const menu_order_interfaces__action__Serve_Result * rhs);

/// Copy a action/Serve message.
/**
 * This functions performs a deep copy, as opposed to the shallow copy that
 * plain assignment yields.
 *
 * \param[in] input The source message pointer.
 * \param[out] output The target message pointer, which must
 *   have been initialized before calling this function.
 * \return true if successful, or false if either pointer is null
 *   or memory allocation fails.
 */
ROSIDL_GENERATOR_C_PUBLIC_menu_order_interfaces
bool
menu_order_interfaces__action__Serve_Result__copy(
  const menu_order_interfaces__action__Serve_Result * input,
  menu_order_interfaces__action__Serve_Result * output);

/// Initialize array of action/Serve messages.
/**
 * It allocates the memory for the number of elements and calls
 * menu_order_interfaces__action__Serve_Result__init()
 * for each element of the array.
 * \param[in,out] array The allocated array pointer.
 * \param[in] size The size / capacity of the array.
 * \return true if initialization was successful, otherwise false
 * If the array pointer is valid and the size is zero it is guaranteed
 # to return true.
 */
ROSIDL_GENERATOR_C_PUBLIC_menu_order_interfaces
bool
menu_order_interfaces__action__Serve_Result__Sequence__init(menu_order_interfaces__action__Serve_Result__Sequence * array, size_t size);

/// Finalize array of action/Serve messages.
/**
 * It calls
 * menu_order_interfaces__action__Serve_Result__fini()
 * for each element of the array and frees the memory for the number of
 * elements.
 * \param[in,out] array The initialized array pointer.
 */
ROSIDL_GENERATOR_C_PUBLIC_menu_order_interfaces
void
menu_order_interfaces__action__Serve_Result__Sequence__fini(menu_order_interfaces__action__Serve_Result__Sequence * array);

/// Create array of action/Serve messages.
/**
 * It allocates the memory for the array and calls
 * menu_order_interfaces__action__Serve_Result__Sequence__init().
 * \param[in] size The size / capacity of the array.
 * \return The pointer to the initialized array if successful, otherwise NULL
 */
ROSIDL_GENERATOR_C_PUBLIC_menu_order_interfaces
menu_order_interfaces__action__Serve_Result__Sequence *
menu_order_interfaces__action__Serve_Result__Sequence__create(size_t size);

/// Destroy array of action/Serve messages.
/**
 * It calls
 * menu_order_interfaces__action__Serve_Result__Sequence__fini()
 * on the array,
 * and frees the memory of the array.
 * \param[in,out] array The initialized array pointer.
 */
ROSIDL_GENERATOR_C_PUBLIC_menu_order_interfaces
void
menu_order_interfaces__action__Serve_Result__Sequence__destroy(menu_order_interfaces__action__Serve_Result__Sequence * array);

/// Check for action/Serve message array equality.
/**
 * \param[in] lhs The message array on the left hand size of the equality operator.
 * \param[in] rhs The message array on the right hand size of the equality operator.
 * \return true if message arrays are equal in size and content, otherwise false.
 */
ROSIDL_GENERATOR_C_PUBLIC_menu_order_interfaces
bool
menu_order_interfaces__action__Serve_Result__Sequence__are_equal(const menu_order_interfaces__action__Serve_Result__Sequence * lhs, const menu_order_interfaces__action__Serve_Result__Sequence * rhs);

/// Copy an array of action/Serve messages.
/**
 * This functions performs a deep copy, as opposed to the shallow copy that
 * plain assignment yields.
 *
 * \param[in] input The source array pointer.
 * \param[out] output The target array pointer, which must
 *   have been initialized before calling this function.
 * \return true if successful, or false if either pointer
 *   is null or memory allocation fails.
 */
ROSIDL_GENERATOR_C_PUBLIC_menu_order_interfaces
bool
menu_order_interfaces__action__Serve_Result__Sequence__copy(
  const menu_order_interfaces__action__Serve_Result__Sequence * input,
  menu_order_interfaces__action__Serve_Result__Sequence * output);

/// Initialize action/Serve message.
/**
 * If the init function is called twice for the same message without
 * calling fini inbetween previously allocated memory will be leaked.
 * \param[in,out] msg The previously allocated message pointer.
 * Fields without a default value will not be initialized by this function.
 * You might want to call memset(msg, 0, sizeof(
 * menu_order_interfaces__action__Serve_Feedback
 * )) before or use
 * menu_order_interfaces__action__Serve_Feedback__create()
 * to allocate and initialize the message.
 * \return true if initialization was successful, otherwise false
 */
ROSIDL_GENERATOR_C_PUBLIC_menu_order_interfaces
bool
menu_order_interfaces__action__Serve_Feedback__init(menu_order_interfaces__action__Serve_Feedback * msg);

/// Finalize action/Serve message.
/**
 * \param[in,out] msg The allocated message pointer.
 */
ROSIDL_GENERATOR_C_PUBLIC_menu_order_interfaces
void
menu_order_interfaces__action__Serve_Feedback__fini(menu_order_interfaces__action__Serve_Feedback * msg);

/// Create action/Serve message.
/**
 * It allocates the memory for the message, sets the memory to zero, and
 * calls
 * menu_order_interfaces__action__Serve_Feedback__init().
 * \return The pointer to the initialized message if successful,
 * otherwise NULL
 */
ROSIDL_GENERATOR_C_PUBLIC_menu_order_interfaces
menu_order_interfaces__action__Serve_Feedback *
menu_order_interfaces__action__Serve_Feedback__create();

/// Destroy action/Serve message.
/**
 * It calls
 * menu_order_interfaces__action__Serve_Feedback__fini()
 * and frees the memory of the message.
 * \param[in,out] msg The allocated message pointer.
 */
ROSIDL_GENERATOR_C_PUBLIC_menu_order_interfaces
void
menu_order_interfaces__action__Serve_Feedback__destroy(menu_order_interfaces__action__Serve_Feedback * msg);

/// Check for action/Serve message equality.
/**
 * \param[in] lhs The message on the left hand size of the equality operator.
 * \param[in] rhs The message on the right hand size of the equality operator.
 * \return true if messages are equal, otherwise false.
 */
ROSIDL_GENERATOR_C_PUBLIC_menu_order_interfaces
bool
menu_order_interfaces__action__Serve_Feedback__are_equal(const menu_order_interfaces__action__Serve_Feedback * lhs, const menu_order_interfaces__action__Serve_Feedback * rhs);

/// Copy a action/Serve message.
/**
 * This functions performs a deep copy, as opposed to the shallow copy that
 * plain assignment yields.
 *
 * \param[in] input The source message pointer.
 * \param[out] output The target message pointer, which must
 *   have been initialized before calling this function.
 * \return true if successful, or false if either pointer is null
 *   or memory allocation fails.
 */
ROSIDL_GENERATOR_C_PUBLIC_menu_order_interfaces
bool
menu_order_interfaces__action__Serve_Feedback__copy(
  const menu_order_interfaces__action__Serve_Feedback * input,
  menu_order_interfaces__action__Serve_Feedback * output);

/// Initialize array of action/Serve messages.
/**
 * It allocates the memory for the number of elements and calls
 * menu_order_interfaces__action__Serve_Feedback__init()
 * for each element of the array.
 * \param[in,out] array The allocated array pointer.
 * \param[in] size The size / capacity of the array.
 * \return true if initialization was successful, otherwise false
 * If the array pointer is valid and the size is zero it is guaranteed
 # to return true.
 */
ROSIDL_GENERATOR_C_PUBLIC_menu_order_interfaces
bool
menu_order_interfaces__action__Serve_Feedback__Sequence__init(menu_order_interfaces__action__Serve_Feedback__Sequence * array, size_t size);

/// Finalize array of action/Serve messages.
/**
 * It calls
 * menu_order_interfaces__action__Serve_Feedback__fini()
 * for each element of the array and frees the memory for the number of
 * elements.
 * \param[in,out] array The initialized array pointer.
 */
ROSIDL_GENERATOR_C_PUBLIC_menu_order_interfaces
void
menu_order_interfaces__action__Serve_Feedback__Sequence__fini(menu_order_interfaces__action__Serve_Feedback__Sequence * array);

/// Create array of action/Serve messages.
/**
 * It allocates the memory for the array and calls
 * menu_order_interfaces__action__Serve_Feedback__Sequence__init().
 * \param[in] size The size / capacity of the array.
 * \return The pointer to the initialized array if successful, otherwise NULL
 */
ROSIDL_GENERATOR_C_PUBLIC_menu_order_interfaces
menu_order_interfaces__action__Serve_Feedback__Sequence *
menu_order_interfaces__action__Serve_Feedback__Sequence__create(size_t size);

/// Destroy array of action/Serve messages.
/**
 * It calls
 * menu_order_interfaces__action__Serve_Feedback__Sequence__fini()
 * on the array,
 * and frees the memory of the array.
 * \param[in,out] array The initialized array pointer.
 */
ROSIDL_GENERATOR_C_PUBLIC_menu_order_interfaces
void
menu_order_interfaces__action__Serve_Feedback__Sequence__destroy(menu_order_interfaces__action__Serve_Feedback__Sequence * array);

/// Check for action/Serve message array equality.
/**
 * \param[in] lhs The message array on the left hand size of the equality operator.
 * \param[in] rhs The message array on the right hand size of the equality operator.
 * \return true if message arrays are equal in size and content, otherwise false.
 */
ROSIDL_GENERATOR_C_PUBLIC_menu_order_interfaces
bool
menu_order_interfaces__action__Serve_Feedback__Sequence__are_equal(const menu_order_interfaces__action__Serve_Feedback__Sequence * lhs, const menu_order_interfaces__action__Serve_Feedback__Sequence * rhs);

/// Copy an array of action/Serve messages.
/**
 * This functions performs a deep copy, as opposed to the shallow copy that
 * plain assignment yields.
 *
 * \param[in] input The source array pointer.
 * \param[out] output The target array pointer, which must
 *   have been initialized before calling this function.
 * \return true if successful, or false if either pointer
 *   is null or memory allocation fails.
 */
ROSIDL_GENERATOR_C_PUBLIC_menu_order_interfaces
bool
menu_order_interfaces__action__Serve_Feedback__Sequence__copy(
  const menu_order_interfaces__action__Serve_Feedback__Sequence * input,
  menu_order_interfaces__action__Serve_Feedback__Sequence * output);

/// Initialize action/Serve message.
/**
 * If the init function is called twice for the same message without
 * calling fini inbetween previously allocated memory will be leaked.
 * \param[in,out] msg The previously allocated message pointer.
 * Fields without a default value will not be initialized by this function.
 * You might want to call memset(msg, 0, sizeof(
 * menu_order_interfaces__action__Serve_SendGoal_Request
 * )) before or use
 * menu_order_interfaces__action__Serve_SendGoal_Request__create()
 * to allocate and initialize the message.
 * \return true if initialization was successful, otherwise false
 */
ROSIDL_GENERATOR_C_PUBLIC_menu_order_interfaces
bool
menu_order_interfaces__action__Serve_SendGoal_Request__init(menu_order_interfaces__action__Serve_SendGoal_Request * msg);

/// Finalize action/Serve message.
/**
 * \param[in,out] msg The allocated message pointer.
 */
ROSIDL_GENERATOR_C_PUBLIC_menu_order_interfaces
void
menu_order_interfaces__action__Serve_SendGoal_Request__fini(menu_order_interfaces__action__Serve_SendGoal_Request * msg);

/// Create action/Serve message.
/**
 * It allocates the memory for the message, sets the memory to zero, and
 * calls
 * menu_order_interfaces__action__Serve_SendGoal_Request__init().
 * \return The pointer to the initialized message if successful,
 * otherwise NULL
 */
ROSIDL_GENERATOR_C_PUBLIC_menu_order_interfaces
menu_order_interfaces__action__Serve_SendGoal_Request *
menu_order_interfaces__action__Serve_SendGoal_Request__create();

/// Destroy action/Serve message.
/**
 * It calls
 * menu_order_interfaces__action__Serve_SendGoal_Request__fini()
 * and frees the memory of the message.
 * \param[in,out] msg The allocated message pointer.
 */
ROSIDL_GENERATOR_C_PUBLIC_menu_order_interfaces
void
menu_order_interfaces__action__Serve_SendGoal_Request__destroy(menu_order_interfaces__action__Serve_SendGoal_Request * msg);

/// Check for action/Serve message equality.
/**
 * \param[in] lhs The message on the left hand size of the equality operator.
 * \param[in] rhs The message on the right hand size of the equality operator.
 * \return true if messages are equal, otherwise false.
 */
ROSIDL_GENERATOR_C_PUBLIC_menu_order_interfaces
bool
menu_order_interfaces__action__Serve_SendGoal_Request__are_equal(const menu_order_interfaces__action__Serve_SendGoal_Request * lhs, const menu_order_interfaces__action__Serve_SendGoal_Request * rhs);

/// Copy a action/Serve message.
/**
 * This functions performs a deep copy, as opposed to the shallow copy that
 * plain assignment yields.
 *
 * \param[in] input The source message pointer.
 * \param[out] output The target message pointer, which must
 *   have been initialized before calling this function.
 * \return true if successful, or false if either pointer is null
 *   or memory allocation fails.
 */
ROSIDL_GENERATOR_C_PUBLIC_menu_order_interfaces
bool
menu_order_interfaces__action__Serve_SendGoal_Request__copy(
  const menu_order_interfaces__action__Serve_SendGoal_Request * input,
  menu_order_interfaces__action__Serve_SendGoal_Request * output);

/// Initialize array of action/Serve messages.
/**
 * It allocates the memory for the number of elements and calls
 * menu_order_interfaces__action__Serve_SendGoal_Request__init()
 * for each element of the array.
 * \param[in,out] array The allocated array pointer.
 * \param[in] size The size / capacity of the array.
 * \return true if initialization was successful, otherwise false
 * If the array pointer is valid and the size is zero it is guaranteed
 # to return true.
 */
ROSIDL_GENERATOR_C_PUBLIC_menu_order_interfaces
bool
menu_order_interfaces__action__Serve_SendGoal_Request__Sequence__init(menu_order_interfaces__action__Serve_SendGoal_Request__Sequence * array, size_t size);

/// Finalize array of action/Serve messages.
/**
 * It calls
 * menu_order_interfaces__action__Serve_SendGoal_Request__fini()
 * for each element of the array and frees the memory for the number of
 * elements.
 * \param[in,out] array The initialized array pointer.
 */
ROSIDL_GENERATOR_C_PUBLIC_menu_order_interfaces
void
menu_order_interfaces__action__Serve_SendGoal_Request__Sequence__fini(menu_order_interfaces__action__Serve_SendGoal_Request__Sequence * array);

/// Create array of action/Serve messages.
/**
 * It allocates the memory for the array and calls
 * menu_order_interfaces__action__Serve_SendGoal_Request__Sequence__init().
 * \param[in] size The size / capacity of the array.
 * \return The pointer to the initialized array if successful, otherwise NULL
 */
ROSIDL_GENERATOR_C_PUBLIC_menu_order_interfaces
menu_order_interfaces__action__Serve_SendGoal_Request__Sequence *
menu_order_interfaces__action__Serve_SendGoal_Request__Sequence__create(size_t size);

/// Destroy array of action/Serve messages.
/**
 * It calls
 * menu_order_interfaces__action__Serve_SendGoal_Request__Sequence__fini()
 * on the array,
 * and frees the memory of the array.
 * \param[in,out] array The initialized array pointer.
 */
ROSIDL_GENERATOR_C_PUBLIC_menu_order_interfaces
void
menu_order_interfaces__action__Serve_SendGoal_Request__Sequence__destroy(menu_order_interfaces__action__Serve_SendGoal_Request__Sequence * array);

/// Check for action/Serve message array equality.
/**
 * \param[in] lhs The message array on the left hand size of the equality operator.
 * \param[in] rhs The message array on the right hand size of the equality operator.
 * \return true if message arrays are equal in size and content, otherwise false.
 */
ROSIDL_GENERATOR_C_PUBLIC_menu_order_interfaces
bool
menu_order_interfaces__action__Serve_SendGoal_Request__Sequence__are_equal(const menu_order_interfaces__action__Serve_SendGoal_Request__Sequence * lhs, const menu_order_interfaces__action__Serve_SendGoal_Request__Sequence * rhs);

/// Copy an array of action/Serve messages.
/**
 * This functions performs a deep copy, as opposed to the shallow copy that
 * plain assignment yields.
 *
 * \param[in] input The source array pointer.
 * \param[out] output The target array pointer, which must
 *   have been initialized before calling this function.
 * \return true if successful, or false if either pointer
 *   is null or memory allocation fails.
 */
ROSIDL_GENERATOR_C_PUBLIC_menu_order_interfaces
bool
menu_order_interfaces__action__Serve_SendGoal_Request__Sequence__copy(
  const menu_order_interfaces__action__Serve_SendGoal_Request__Sequence * input,
  menu_order_interfaces__action__Serve_SendGoal_Request__Sequence * output);

/// Initialize action/Serve message.
/**
 * If the init function is called twice for the same message without
 * calling fini inbetween previously allocated memory will be leaked.
 * \param[in,out] msg The previously allocated message pointer.
 * Fields without a default value will not be initialized by this function.
 * You might want to call memset(msg, 0, sizeof(
 * menu_order_interfaces__action__Serve_SendGoal_Response
 * )) before or use
 * menu_order_interfaces__action__Serve_SendGoal_Response__create()
 * to allocate and initialize the message.
 * \return true if initialization was successful, otherwise false
 */
ROSIDL_GENERATOR_C_PUBLIC_menu_order_interfaces
bool
menu_order_interfaces__action__Serve_SendGoal_Response__init(menu_order_interfaces__action__Serve_SendGoal_Response * msg);

/// Finalize action/Serve message.
/**
 * \param[in,out] msg The allocated message pointer.
 */
ROSIDL_GENERATOR_C_PUBLIC_menu_order_interfaces
void
menu_order_interfaces__action__Serve_SendGoal_Response__fini(menu_order_interfaces__action__Serve_SendGoal_Response * msg);

/// Create action/Serve message.
/**
 * It allocates the memory for the message, sets the memory to zero, and
 * calls
 * menu_order_interfaces__action__Serve_SendGoal_Response__init().
 * \return The pointer to the initialized message if successful,
 * otherwise NULL
 */
ROSIDL_GENERATOR_C_PUBLIC_menu_order_interfaces
menu_order_interfaces__action__Serve_SendGoal_Response *
menu_order_interfaces__action__Serve_SendGoal_Response__create();

/// Destroy action/Serve message.
/**
 * It calls
 * menu_order_interfaces__action__Serve_SendGoal_Response__fini()
 * and frees the memory of the message.
 * \param[in,out] msg The allocated message pointer.
 */
ROSIDL_GENERATOR_C_PUBLIC_menu_order_interfaces
void
menu_order_interfaces__action__Serve_SendGoal_Response__destroy(menu_order_interfaces__action__Serve_SendGoal_Response * msg);

/// Check for action/Serve message equality.
/**
 * \param[in] lhs The message on the left hand size of the equality operator.
 * \param[in] rhs The message on the right hand size of the equality operator.
 * \return true if messages are equal, otherwise false.
 */
ROSIDL_GENERATOR_C_PUBLIC_menu_order_interfaces
bool
menu_order_interfaces__action__Serve_SendGoal_Response__are_equal(const menu_order_interfaces__action__Serve_SendGoal_Response * lhs, const menu_order_interfaces__action__Serve_SendGoal_Response * rhs);

/// Copy a action/Serve message.
/**
 * This functions performs a deep copy, as opposed to the shallow copy that
 * plain assignment yields.
 *
 * \param[in] input The source message pointer.
 * \param[out] output The target message pointer, which must
 *   have been initialized before calling this function.
 * \return true if successful, or false if either pointer is null
 *   or memory allocation fails.
 */
ROSIDL_GENERATOR_C_PUBLIC_menu_order_interfaces
bool
menu_order_interfaces__action__Serve_SendGoal_Response__copy(
  const menu_order_interfaces__action__Serve_SendGoal_Response * input,
  menu_order_interfaces__action__Serve_SendGoal_Response * output);

/// Initialize array of action/Serve messages.
/**
 * It allocates the memory for the number of elements and calls
 * menu_order_interfaces__action__Serve_SendGoal_Response__init()
 * for each element of the array.
 * \param[in,out] array The allocated array pointer.
 * \param[in] size The size / capacity of the array.
 * \return true if initialization was successful, otherwise false
 * If the array pointer is valid and the size is zero it is guaranteed
 # to return true.
 */
ROSIDL_GENERATOR_C_PUBLIC_menu_order_interfaces
bool
menu_order_interfaces__action__Serve_SendGoal_Response__Sequence__init(menu_order_interfaces__action__Serve_SendGoal_Response__Sequence * array, size_t size);

/// Finalize array of action/Serve messages.
/**
 * It calls
 * menu_order_interfaces__action__Serve_SendGoal_Response__fini()
 * for each element of the array and frees the memory for the number of
 * elements.
 * \param[in,out] array The initialized array pointer.
 */
ROSIDL_GENERATOR_C_PUBLIC_menu_order_interfaces
void
menu_order_interfaces__action__Serve_SendGoal_Response__Sequence__fini(menu_order_interfaces__action__Serve_SendGoal_Response__Sequence * array);

/// Create array of action/Serve messages.
/**
 * It allocates the memory for the array and calls
 * menu_order_interfaces__action__Serve_SendGoal_Response__Sequence__init().
 * \param[in] size The size / capacity of the array.
 * \return The pointer to the initialized array if successful, otherwise NULL
 */
ROSIDL_GENERATOR_C_PUBLIC_menu_order_interfaces
menu_order_interfaces__action__Serve_SendGoal_Response__Sequence *
menu_order_interfaces__action__Serve_SendGoal_Response__Sequence__create(size_t size);

/// Destroy array of action/Serve messages.
/**
 * It calls
 * menu_order_interfaces__action__Serve_SendGoal_Response__Sequence__fini()
 * on the array,
 * and frees the memory of the array.
 * \param[in,out] array The initialized array pointer.
 */
ROSIDL_GENERATOR_C_PUBLIC_menu_order_interfaces
void
menu_order_interfaces__action__Serve_SendGoal_Response__Sequence__destroy(menu_order_interfaces__action__Serve_SendGoal_Response__Sequence * array);

/// Check for action/Serve message array equality.
/**
 * \param[in] lhs The message array on the left hand size of the equality operator.
 * \param[in] rhs The message array on the right hand size of the equality operator.
 * \return true if message arrays are equal in size and content, otherwise false.
 */
ROSIDL_GENERATOR_C_PUBLIC_menu_order_interfaces
bool
menu_order_interfaces__action__Serve_SendGoal_Response__Sequence__are_equal(const menu_order_interfaces__action__Serve_SendGoal_Response__Sequence * lhs, const menu_order_interfaces__action__Serve_SendGoal_Response__Sequence * rhs);

/// Copy an array of action/Serve messages.
/**
 * This functions performs a deep copy, as opposed to the shallow copy that
 * plain assignment yields.
 *
 * \param[in] input The source array pointer.
 * \param[out] output The target array pointer, which must
 *   have been initialized before calling this function.
 * \return true if successful, or false if either pointer
 *   is null or memory allocation fails.
 */
ROSIDL_GENERATOR_C_PUBLIC_menu_order_interfaces
bool
menu_order_interfaces__action__Serve_SendGoal_Response__Sequence__copy(
  const menu_order_interfaces__action__Serve_SendGoal_Response__Sequence * input,
  menu_order_interfaces__action__Serve_SendGoal_Response__Sequence * output);

/// Initialize action/Serve message.
/**
 * If the init function is called twice for the same message without
 * calling fini inbetween previously allocated memory will be leaked.
 * \param[in,out] msg The previously allocated message pointer.
 * Fields without a default value will not be initialized by this function.
 * You might want to call memset(msg, 0, sizeof(
 * menu_order_interfaces__action__Serve_GetResult_Request
 * )) before or use
 * menu_order_interfaces__action__Serve_GetResult_Request__create()
 * to allocate and initialize the message.
 * \return true if initialization was successful, otherwise false
 */
ROSIDL_GENERATOR_C_PUBLIC_menu_order_interfaces
bool
menu_order_interfaces__action__Serve_GetResult_Request__init(menu_order_interfaces__action__Serve_GetResult_Request * msg);

/// Finalize action/Serve message.
/**
 * \param[in,out] msg The allocated message pointer.
 */
ROSIDL_GENERATOR_C_PUBLIC_menu_order_interfaces
void
menu_order_interfaces__action__Serve_GetResult_Request__fini(menu_order_interfaces__action__Serve_GetResult_Request * msg);

/// Create action/Serve message.
/**
 * It allocates the memory for the message, sets the memory to zero, and
 * calls
 * menu_order_interfaces__action__Serve_GetResult_Request__init().
 * \return The pointer to the initialized message if successful,
 * otherwise NULL
 */
ROSIDL_GENERATOR_C_PUBLIC_menu_order_interfaces
menu_order_interfaces__action__Serve_GetResult_Request *
menu_order_interfaces__action__Serve_GetResult_Request__create();

/// Destroy action/Serve message.
/**
 * It calls
 * menu_order_interfaces__action__Serve_GetResult_Request__fini()
 * and frees the memory of the message.
 * \param[in,out] msg The allocated message pointer.
 */
ROSIDL_GENERATOR_C_PUBLIC_menu_order_interfaces
void
menu_order_interfaces__action__Serve_GetResult_Request__destroy(menu_order_interfaces__action__Serve_GetResult_Request * msg);

/// Check for action/Serve message equality.
/**
 * \param[in] lhs The message on the left hand size of the equality operator.
 * \param[in] rhs The message on the right hand size of the equality operator.
 * \return true if messages are equal, otherwise false.
 */
ROSIDL_GENERATOR_C_PUBLIC_menu_order_interfaces
bool
menu_order_interfaces__action__Serve_GetResult_Request__are_equal(const menu_order_interfaces__action__Serve_GetResult_Request * lhs, const menu_order_interfaces__action__Serve_GetResult_Request * rhs);

/// Copy a action/Serve message.
/**
 * This functions performs a deep copy, as opposed to the shallow copy that
 * plain assignment yields.
 *
 * \param[in] input The source message pointer.
 * \param[out] output The target message pointer, which must
 *   have been initialized before calling this function.
 * \return true if successful, or false if either pointer is null
 *   or memory allocation fails.
 */
ROSIDL_GENERATOR_C_PUBLIC_menu_order_interfaces
bool
menu_order_interfaces__action__Serve_GetResult_Request__copy(
  const menu_order_interfaces__action__Serve_GetResult_Request * input,
  menu_order_interfaces__action__Serve_GetResult_Request * output);

/// Initialize array of action/Serve messages.
/**
 * It allocates the memory for the number of elements and calls
 * menu_order_interfaces__action__Serve_GetResult_Request__init()
 * for each element of the array.
 * \param[in,out] array The allocated array pointer.
 * \param[in] size The size / capacity of the array.
 * \return true if initialization was successful, otherwise false
 * If the array pointer is valid and the size is zero it is guaranteed
 # to return true.
 */
ROSIDL_GENERATOR_C_PUBLIC_menu_order_interfaces
bool
menu_order_interfaces__action__Serve_GetResult_Request__Sequence__init(menu_order_interfaces__action__Serve_GetResult_Request__Sequence * array, size_t size);

/// Finalize array of action/Serve messages.
/**
 * It calls
 * menu_order_interfaces__action__Serve_GetResult_Request__fini()
 * for each element of the array and frees the memory for the number of
 * elements.
 * \param[in,out] array The initialized array pointer.
 */
ROSIDL_GENERATOR_C_PUBLIC_menu_order_interfaces
void
menu_order_interfaces__action__Serve_GetResult_Request__Sequence__fini(menu_order_interfaces__action__Serve_GetResult_Request__Sequence * array);

/// Create array of action/Serve messages.
/**
 * It allocates the memory for the array and calls
 * menu_order_interfaces__action__Serve_GetResult_Request__Sequence__init().
 * \param[in] size The size / capacity of the array.
 * \return The pointer to the initialized array if successful, otherwise NULL
 */
ROSIDL_GENERATOR_C_PUBLIC_menu_order_interfaces
menu_order_interfaces__action__Serve_GetResult_Request__Sequence *
menu_order_interfaces__action__Serve_GetResult_Request__Sequence__create(size_t size);

/// Destroy array of action/Serve messages.
/**
 * It calls
 * menu_order_interfaces__action__Serve_GetResult_Request__Sequence__fini()
 * on the array,
 * and frees the memory of the array.
 * \param[in,out] array The initialized array pointer.
 */
ROSIDL_GENERATOR_C_PUBLIC_menu_order_interfaces
void
menu_order_interfaces__action__Serve_GetResult_Request__Sequence__destroy(menu_order_interfaces__action__Serve_GetResult_Request__Sequence * array);

/// Check for action/Serve message array equality.
/**
 * \param[in] lhs The message array on the left hand size of the equality operator.
 * \param[in] rhs The message array on the right hand size of the equality operator.
 * \return true if message arrays are equal in size and content, otherwise false.
 */
ROSIDL_GENERATOR_C_PUBLIC_menu_order_interfaces
bool
menu_order_interfaces__action__Serve_GetResult_Request__Sequence__are_equal(const menu_order_interfaces__action__Serve_GetResult_Request__Sequence * lhs, const menu_order_interfaces__action__Serve_GetResult_Request__Sequence * rhs);

/// Copy an array of action/Serve messages.
/**
 * This functions performs a deep copy, as opposed to the shallow copy that
 * plain assignment yields.
 *
 * \param[in] input The source array pointer.
 * \param[out] output The target array pointer, which must
 *   have been initialized before calling this function.
 * \return true if successful, or false if either pointer
 *   is null or memory allocation fails.
 */
ROSIDL_GENERATOR_C_PUBLIC_menu_order_interfaces
bool
menu_order_interfaces__action__Serve_GetResult_Request__Sequence__copy(
  const menu_order_interfaces__action__Serve_GetResult_Request__Sequence * input,
  menu_order_interfaces__action__Serve_GetResult_Request__Sequence * output);

/// Initialize action/Serve message.
/**
 * If the init function is called twice for the same message without
 * calling fini inbetween previously allocated memory will be leaked.
 * \param[in,out] msg The previously allocated message pointer.
 * Fields without a default value will not be initialized by this function.
 * You might want to call memset(msg, 0, sizeof(
 * menu_order_interfaces__action__Serve_GetResult_Response
 * )) before or use
 * menu_order_interfaces__action__Serve_GetResult_Response__create()
 * to allocate and initialize the message.
 * \return true if initialization was successful, otherwise false
 */
ROSIDL_GENERATOR_C_PUBLIC_menu_order_interfaces
bool
menu_order_interfaces__action__Serve_GetResult_Response__init(menu_order_interfaces__action__Serve_GetResult_Response * msg);

/// Finalize action/Serve message.
/**
 * \param[in,out] msg The allocated message pointer.
 */
ROSIDL_GENERATOR_C_PUBLIC_menu_order_interfaces
void
menu_order_interfaces__action__Serve_GetResult_Response__fini(menu_order_interfaces__action__Serve_GetResult_Response * msg);

/// Create action/Serve message.
/**
 * It allocates the memory for the message, sets the memory to zero, and
 * calls
 * menu_order_interfaces__action__Serve_GetResult_Response__init().
 * \return The pointer to the initialized message if successful,
 * otherwise NULL
 */
ROSIDL_GENERATOR_C_PUBLIC_menu_order_interfaces
menu_order_interfaces__action__Serve_GetResult_Response *
menu_order_interfaces__action__Serve_GetResult_Response__create();

/// Destroy action/Serve message.
/**
 * It calls
 * menu_order_interfaces__action__Serve_GetResult_Response__fini()
 * and frees the memory of the message.
 * \param[in,out] msg The allocated message pointer.
 */
ROSIDL_GENERATOR_C_PUBLIC_menu_order_interfaces
void
menu_order_interfaces__action__Serve_GetResult_Response__destroy(menu_order_interfaces__action__Serve_GetResult_Response * msg);

/// Check for action/Serve message equality.
/**
 * \param[in] lhs The message on the left hand size of the equality operator.
 * \param[in] rhs The message on the right hand size of the equality operator.
 * \return true if messages are equal, otherwise false.
 */
ROSIDL_GENERATOR_C_PUBLIC_menu_order_interfaces
bool
menu_order_interfaces__action__Serve_GetResult_Response__are_equal(const menu_order_interfaces__action__Serve_GetResult_Response * lhs, const menu_order_interfaces__action__Serve_GetResult_Response * rhs);

/// Copy a action/Serve message.
/**
 * This functions performs a deep copy, as opposed to the shallow copy that
 * plain assignment yields.
 *
 * \param[in] input The source message pointer.
 * \param[out] output The target message pointer, which must
 *   have been initialized before calling this function.
 * \return true if successful, or false if either pointer is null
 *   or memory allocation fails.
 */
ROSIDL_GENERATOR_C_PUBLIC_menu_order_interfaces
bool
menu_order_interfaces__action__Serve_GetResult_Response__copy(
  const menu_order_interfaces__action__Serve_GetResult_Response * input,
  menu_order_interfaces__action__Serve_GetResult_Response * output);

/// Initialize array of action/Serve messages.
/**
 * It allocates the memory for the number of elements and calls
 * menu_order_interfaces__action__Serve_GetResult_Response__init()
 * for each element of the array.
 * \param[in,out] array The allocated array pointer.
 * \param[in] size The size / capacity of the array.
 * \return true if initialization was successful, otherwise false
 * If the array pointer is valid and the size is zero it is guaranteed
 # to return true.
 */
ROSIDL_GENERATOR_C_PUBLIC_menu_order_interfaces
bool
menu_order_interfaces__action__Serve_GetResult_Response__Sequence__init(menu_order_interfaces__action__Serve_GetResult_Response__Sequence * array, size_t size);

/// Finalize array of action/Serve messages.
/**
 * It calls
 * menu_order_interfaces__action__Serve_GetResult_Response__fini()
 * for each element of the array and frees the memory for the number of
 * elements.
 * \param[in,out] array The initialized array pointer.
 */
ROSIDL_GENERATOR_C_PUBLIC_menu_order_interfaces
void
menu_order_interfaces__action__Serve_GetResult_Response__Sequence__fini(menu_order_interfaces__action__Serve_GetResult_Response__Sequence * array);

/// Create array of action/Serve messages.
/**
 * It allocates the memory for the array and calls
 * menu_order_interfaces__action__Serve_GetResult_Response__Sequence__init().
 * \param[in] size The size / capacity of the array.
 * \return The pointer to the initialized array if successful, otherwise NULL
 */
ROSIDL_GENERATOR_C_PUBLIC_menu_order_interfaces
menu_order_interfaces__action__Serve_GetResult_Response__Sequence *
menu_order_interfaces__action__Serve_GetResult_Response__Sequence__create(size_t size);

/// Destroy array of action/Serve messages.
/**
 * It calls
 * menu_order_interfaces__action__Serve_GetResult_Response__Sequence__fini()
 * on the array,
 * and frees the memory of the array.
 * \param[in,out] array The initialized array pointer.
 */
ROSIDL_GENERATOR_C_PUBLIC_menu_order_interfaces
void
menu_order_interfaces__action__Serve_GetResult_Response__Sequence__destroy(menu_order_interfaces__action__Serve_GetResult_Response__Sequence * array);

/// Check for action/Serve message array equality.
/**
 * \param[in] lhs The message array on the left hand size of the equality operator.
 * \param[in] rhs The message array on the right hand size of the equality operator.
 * \return true if message arrays are equal in size and content, otherwise false.
 */
ROSIDL_GENERATOR_C_PUBLIC_menu_order_interfaces
bool
menu_order_interfaces__action__Serve_GetResult_Response__Sequence__are_equal(const menu_order_interfaces__action__Serve_GetResult_Response__Sequence * lhs, const menu_order_interfaces__action__Serve_GetResult_Response__Sequence * rhs);

/// Copy an array of action/Serve messages.
/**
 * This functions performs a deep copy, as opposed to the shallow copy that
 * plain assignment yields.
 *
 * \param[in] input The source array pointer.
 * \param[out] output The target array pointer, which must
 *   have been initialized before calling this function.
 * \return true if successful, or false if either pointer
 *   is null or memory allocation fails.
 */
ROSIDL_GENERATOR_C_PUBLIC_menu_order_interfaces
bool
menu_order_interfaces__action__Serve_GetResult_Response__Sequence__copy(
  const menu_order_interfaces__action__Serve_GetResult_Response__Sequence * input,
  menu_order_interfaces__action__Serve_GetResult_Response__Sequence * output);

/// Initialize action/Serve message.
/**
 * If the init function is called twice for the same message without
 * calling fini inbetween previously allocated memory will be leaked.
 * \param[in,out] msg The previously allocated message pointer.
 * Fields without a default value will not be initialized by this function.
 * You might want to call memset(msg, 0, sizeof(
 * menu_order_interfaces__action__Serve_FeedbackMessage
 * )) before or use
 * menu_order_interfaces__action__Serve_FeedbackMessage__create()
 * to allocate and initialize the message.
 * \return true if initialization was successful, otherwise false
 */
ROSIDL_GENERATOR_C_PUBLIC_menu_order_interfaces
bool
menu_order_interfaces__action__Serve_FeedbackMessage__init(menu_order_interfaces__action__Serve_FeedbackMessage * msg);

/// Finalize action/Serve message.
/**
 * \param[in,out] msg The allocated message pointer.
 */
ROSIDL_GENERATOR_C_PUBLIC_menu_order_interfaces
void
menu_order_interfaces__action__Serve_FeedbackMessage__fini(menu_order_interfaces__action__Serve_FeedbackMessage * msg);

/// Create action/Serve message.
/**
 * It allocates the memory for the message, sets the memory to zero, and
 * calls
 * menu_order_interfaces__action__Serve_FeedbackMessage__init().
 * \return The pointer to the initialized message if successful,
 * otherwise NULL
 */
ROSIDL_GENERATOR_C_PUBLIC_menu_order_interfaces
menu_order_interfaces__action__Serve_FeedbackMessage *
menu_order_interfaces__action__Serve_FeedbackMessage__create();

/// Destroy action/Serve message.
/**
 * It calls
 * menu_order_interfaces__action__Serve_FeedbackMessage__fini()
 * and frees the memory of the message.
 * \param[in,out] msg The allocated message pointer.
 */
ROSIDL_GENERATOR_C_PUBLIC_menu_order_interfaces
void
menu_order_interfaces__action__Serve_FeedbackMessage__destroy(menu_order_interfaces__action__Serve_FeedbackMessage * msg);

/// Check for action/Serve message equality.
/**
 * \param[in] lhs The message on the left hand size of the equality operator.
 * \param[in] rhs The message on the right hand size of the equality operator.
 * \return true if messages are equal, otherwise false.
 */
ROSIDL_GENERATOR_C_PUBLIC_menu_order_interfaces
bool
menu_order_interfaces__action__Serve_FeedbackMessage__are_equal(const menu_order_interfaces__action__Serve_FeedbackMessage * lhs, const menu_order_interfaces__action__Serve_FeedbackMessage * rhs);

/// Copy a action/Serve message.
/**
 * This functions performs a deep copy, as opposed to the shallow copy that
 * plain assignment yields.
 *
 * \param[in] input The source message pointer.
 * \param[out] output The target message pointer, which must
 *   have been initialized before calling this function.
 * \return true if successful, or false if either pointer is null
 *   or memory allocation fails.
 */
ROSIDL_GENERATOR_C_PUBLIC_menu_order_interfaces
bool
menu_order_interfaces__action__Serve_FeedbackMessage__copy(
  const menu_order_interfaces__action__Serve_FeedbackMessage * input,
  menu_order_interfaces__action__Serve_FeedbackMessage * output);

/// Initialize array of action/Serve messages.
/**
 * It allocates the memory for the number of elements and calls
 * menu_order_interfaces__action__Serve_FeedbackMessage__init()
 * for each element of the array.
 * \param[in,out] array The allocated array pointer.
 * \param[in] size The size / capacity of the array.
 * \return true if initialization was successful, otherwise false
 * If the array pointer is valid and the size is zero it is guaranteed
 # to return true.
 */
ROSIDL_GENERATOR_C_PUBLIC_menu_order_interfaces
bool
menu_order_interfaces__action__Serve_FeedbackMessage__Sequence__init(menu_order_interfaces__action__Serve_FeedbackMessage__Sequence * array, size_t size);

/// Finalize array of action/Serve messages.
/**
 * It calls
 * menu_order_interfaces__action__Serve_FeedbackMessage__fini()
 * for each element of the array and frees the memory for the number of
 * elements.
 * \param[in,out] array The initialized array pointer.
 */
ROSIDL_GENERATOR_C_PUBLIC_menu_order_interfaces
void
menu_order_interfaces__action__Serve_FeedbackMessage__Sequence__fini(menu_order_interfaces__action__Serve_FeedbackMessage__Sequence * array);

/// Create array of action/Serve messages.
/**
 * It allocates the memory for the array and calls
 * menu_order_interfaces__action__Serve_FeedbackMessage__Sequence__init().
 * \param[in] size The size / capacity of the array.
 * \return The pointer to the initialized array if successful, otherwise NULL
 */
ROSIDL_GENERATOR_C_PUBLIC_menu_order_interfaces
menu_order_interfaces__action__Serve_FeedbackMessage__Sequence *
menu_order_interfaces__action__Serve_FeedbackMessage__Sequence__create(size_t size);

/// Destroy array of action/Serve messages.
/**
 * It calls
 * menu_order_interfaces__action__Serve_FeedbackMessage__Sequence__fini()
 * on the array,
 * and frees the memory of the array.
 * \param[in,out] array The initialized array pointer.
 */
ROSIDL_GENERATOR_C_PUBLIC_menu_order_interfaces
void
menu_order_interfaces__action__Serve_FeedbackMessage__Sequence__destroy(menu_order_interfaces__action__Serve_FeedbackMessage__Sequence * array);

/// Check for action/Serve message array equality.
/**
 * \param[in] lhs The message array on the left hand size of the equality operator.
 * \param[in] rhs The message array on the right hand size of the equality operator.
 * \return true if message arrays are equal in size and content, otherwise false.
 */
ROSIDL_GENERATOR_C_PUBLIC_menu_order_interfaces
bool
menu_order_interfaces__action__Serve_FeedbackMessage__Sequence__are_equal(const menu_order_interfaces__action__Serve_FeedbackMessage__Sequence * lhs, const menu_order_interfaces__action__Serve_FeedbackMessage__Sequence * rhs);

/// Copy an array of action/Serve messages.
/**
 * This functions performs a deep copy, as opposed to the shallow copy that
 * plain assignment yields.
 *
 * \param[in] input The source array pointer.
 * \param[out] output The target array pointer, which must
 *   have been initialized before calling this function.
 * \return true if successful, or false if either pointer
 *   is null or memory allocation fails.
 */
ROSIDL_GENERATOR_C_PUBLIC_menu_order_interfaces
bool
menu_order_interfaces__action__Serve_FeedbackMessage__Sequence__copy(
  const menu_order_interfaces__action__Serve_FeedbackMessage__Sequence * input,
  menu_order_interfaces__action__Serve_FeedbackMessage__Sequence * output);

#ifdef __cplusplus
}
#endif

#endif  // MENU_ORDER_INTERFACES__ACTION__DETAIL__SERVE__FUNCTIONS_H_
