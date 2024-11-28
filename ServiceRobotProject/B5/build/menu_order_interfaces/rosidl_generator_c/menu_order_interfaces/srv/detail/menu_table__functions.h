// generated from rosidl_generator_c/resource/idl__functions.h.em
// with input from menu_order_interfaces:srv/MenuTable.idl
// generated code does not contain a copyright notice

#ifndef MENU_ORDER_INTERFACES__SRV__DETAIL__MENU_TABLE__FUNCTIONS_H_
#define MENU_ORDER_INTERFACES__SRV__DETAIL__MENU_TABLE__FUNCTIONS_H_

#ifdef __cplusplus
extern "C"
{
#endif

#include <stdbool.h>
#include <stdlib.h>

#include "rosidl_runtime_c/visibility_control.h"
#include "menu_order_interfaces/msg/rosidl_generator_c__visibility_control.h"

#include "menu_order_interfaces/srv/detail/menu_table__struct.h"

/// Initialize srv/MenuTable message.
/**
 * If the init function is called twice for the same message without
 * calling fini inbetween previously allocated memory will be leaked.
 * \param[in,out] msg The previously allocated message pointer.
 * Fields without a default value will not be initialized by this function.
 * You might want to call memset(msg, 0, sizeof(
 * menu_order_interfaces__srv__MenuTable_Request
 * )) before or use
 * menu_order_interfaces__srv__MenuTable_Request__create()
 * to allocate and initialize the message.
 * \return true if initialization was successful, otherwise false
 */
ROSIDL_GENERATOR_C_PUBLIC_menu_order_interfaces
bool
menu_order_interfaces__srv__MenuTable_Request__init(menu_order_interfaces__srv__MenuTable_Request * msg);

/// Finalize srv/MenuTable message.
/**
 * \param[in,out] msg The allocated message pointer.
 */
ROSIDL_GENERATOR_C_PUBLIC_menu_order_interfaces
void
menu_order_interfaces__srv__MenuTable_Request__fini(menu_order_interfaces__srv__MenuTable_Request * msg);

/// Create srv/MenuTable message.
/**
 * It allocates the memory for the message, sets the memory to zero, and
 * calls
 * menu_order_interfaces__srv__MenuTable_Request__init().
 * \return The pointer to the initialized message if successful,
 * otherwise NULL
 */
ROSIDL_GENERATOR_C_PUBLIC_menu_order_interfaces
menu_order_interfaces__srv__MenuTable_Request *
menu_order_interfaces__srv__MenuTable_Request__create();

/// Destroy srv/MenuTable message.
/**
 * It calls
 * menu_order_interfaces__srv__MenuTable_Request__fini()
 * and frees the memory of the message.
 * \param[in,out] msg The allocated message pointer.
 */
ROSIDL_GENERATOR_C_PUBLIC_menu_order_interfaces
void
menu_order_interfaces__srv__MenuTable_Request__destroy(menu_order_interfaces__srv__MenuTable_Request * msg);

/// Check for srv/MenuTable message equality.
/**
 * \param[in] lhs The message on the left hand size of the equality operator.
 * \param[in] rhs The message on the right hand size of the equality operator.
 * \return true if messages are equal, otherwise false.
 */
ROSIDL_GENERATOR_C_PUBLIC_menu_order_interfaces
bool
menu_order_interfaces__srv__MenuTable_Request__are_equal(const menu_order_interfaces__srv__MenuTable_Request * lhs, const menu_order_interfaces__srv__MenuTable_Request * rhs);

/// Copy a srv/MenuTable message.
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
menu_order_interfaces__srv__MenuTable_Request__copy(
  const menu_order_interfaces__srv__MenuTable_Request * input,
  menu_order_interfaces__srv__MenuTable_Request * output);

/// Initialize array of srv/MenuTable messages.
/**
 * It allocates the memory for the number of elements and calls
 * menu_order_interfaces__srv__MenuTable_Request__init()
 * for each element of the array.
 * \param[in,out] array The allocated array pointer.
 * \param[in] size The size / capacity of the array.
 * \return true if initialization was successful, otherwise false
 * If the array pointer is valid and the size is zero it is guaranteed
 # to return true.
 */
ROSIDL_GENERATOR_C_PUBLIC_menu_order_interfaces
bool
menu_order_interfaces__srv__MenuTable_Request__Sequence__init(menu_order_interfaces__srv__MenuTable_Request__Sequence * array, size_t size);

/// Finalize array of srv/MenuTable messages.
/**
 * It calls
 * menu_order_interfaces__srv__MenuTable_Request__fini()
 * for each element of the array and frees the memory for the number of
 * elements.
 * \param[in,out] array The initialized array pointer.
 */
ROSIDL_GENERATOR_C_PUBLIC_menu_order_interfaces
void
menu_order_interfaces__srv__MenuTable_Request__Sequence__fini(menu_order_interfaces__srv__MenuTable_Request__Sequence * array);

/// Create array of srv/MenuTable messages.
/**
 * It allocates the memory for the array and calls
 * menu_order_interfaces__srv__MenuTable_Request__Sequence__init().
 * \param[in] size The size / capacity of the array.
 * \return The pointer to the initialized array if successful, otherwise NULL
 */
ROSIDL_GENERATOR_C_PUBLIC_menu_order_interfaces
menu_order_interfaces__srv__MenuTable_Request__Sequence *
menu_order_interfaces__srv__MenuTable_Request__Sequence__create(size_t size);

/// Destroy array of srv/MenuTable messages.
/**
 * It calls
 * menu_order_interfaces__srv__MenuTable_Request__Sequence__fini()
 * on the array,
 * and frees the memory of the array.
 * \param[in,out] array The initialized array pointer.
 */
ROSIDL_GENERATOR_C_PUBLIC_menu_order_interfaces
void
menu_order_interfaces__srv__MenuTable_Request__Sequence__destroy(menu_order_interfaces__srv__MenuTable_Request__Sequence * array);

/// Check for srv/MenuTable message array equality.
/**
 * \param[in] lhs The message array on the left hand size of the equality operator.
 * \param[in] rhs The message array on the right hand size of the equality operator.
 * \return true if message arrays are equal in size and content, otherwise false.
 */
ROSIDL_GENERATOR_C_PUBLIC_menu_order_interfaces
bool
menu_order_interfaces__srv__MenuTable_Request__Sequence__are_equal(const menu_order_interfaces__srv__MenuTable_Request__Sequence * lhs, const menu_order_interfaces__srv__MenuTable_Request__Sequence * rhs);

/// Copy an array of srv/MenuTable messages.
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
menu_order_interfaces__srv__MenuTable_Request__Sequence__copy(
  const menu_order_interfaces__srv__MenuTable_Request__Sequence * input,
  menu_order_interfaces__srv__MenuTable_Request__Sequence * output);

/// Initialize srv/MenuTable message.
/**
 * If the init function is called twice for the same message without
 * calling fini inbetween previously allocated memory will be leaked.
 * \param[in,out] msg The previously allocated message pointer.
 * Fields without a default value will not be initialized by this function.
 * You might want to call memset(msg, 0, sizeof(
 * menu_order_interfaces__srv__MenuTable_Response
 * )) before or use
 * menu_order_interfaces__srv__MenuTable_Response__create()
 * to allocate and initialize the message.
 * \return true if initialization was successful, otherwise false
 */
ROSIDL_GENERATOR_C_PUBLIC_menu_order_interfaces
bool
menu_order_interfaces__srv__MenuTable_Response__init(menu_order_interfaces__srv__MenuTable_Response * msg);

/// Finalize srv/MenuTable message.
/**
 * \param[in,out] msg The allocated message pointer.
 */
ROSIDL_GENERATOR_C_PUBLIC_menu_order_interfaces
void
menu_order_interfaces__srv__MenuTable_Response__fini(menu_order_interfaces__srv__MenuTable_Response * msg);

/// Create srv/MenuTable message.
/**
 * It allocates the memory for the message, sets the memory to zero, and
 * calls
 * menu_order_interfaces__srv__MenuTable_Response__init().
 * \return The pointer to the initialized message if successful,
 * otherwise NULL
 */
ROSIDL_GENERATOR_C_PUBLIC_menu_order_interfaces
menu_order_interfaces__srv__MenuTable_Response *
menu_order_interfaces__srv__MenuTable_Response__create();

/// Destroy srv/MenuTable message.
/**
 * It calls
 * menu_order_interfaces__srv__MenuTable_Response__fini()
 * and frees the memory of the message.
 * \param[in,out] msg The allocated message pointer.
 */
ROSIDL_GENERATOR_C_PUBLIC_menu_order_interfaces
void
menu_order_interfaces__srv__MenuTable_Response__destroy(menu_order_interfaces__srv__MenuTable_Response * msg);

/// Check for srv/MenuTable message equality.
/**
 * \param[in] lhs The message on the left hand size of the equality operator.
 * \param[in] rhs The message on the right hand size of the equality operator.
 * \return true if messages are equal, otherwise false.
 */
ROSIDL_GENERATOR_C_PUBLIC_menu_order_interfaces
bool
menu_order_interfaces__srv__MenuTable_Response__are_equal(const menu_order_interfaces__srv__MenuTable_Response * lhs, const menu_order_interfaces__srv__MenuTable_Response * rhs);

/// Copy a srv/MenuTable message.
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
menu_order_interfaces__srv__MenuTable_Response__copy(
  const menu_order_interfaces__srv__MenuTable_Response * input,
  menu_order_interfaces__srv__MenuTable_Response * output);

/// Initialize array of srv/MenuTable messages.
/**
 * It allocates the memory for the number of elements and calls
 * menu_order_interfaces__srv__MenuTable_Response__init()
 * for each element of the array.
 * \param[in,out] array The allocated array pointer.
 * \param[in] size The size / capacity of the array.
 * \return true if initialization was successful, otherwise false
 * If the array pointer is valid and the size is zero it is guaranteed
 # to return true.
 */
ROSIDL_GENERATOR_C_PUBLIC_menu_order_interfaces
bool
menu_order_interfaces__srv__MenuTable_Response__Sequence__init(menu_order_interfaces__srv__MenuTable_Response__Sequence * array, size_t size);

/// Finalize array of srv/MenuTable messages.
/**
 * It calls
 * menu_order_interfaces__srv__MenuTable_Response__fini()
 * for each element of the array and frees the memory for the number of
 * elements.
 * \param[in,out] array The initialized array pointer.
 */
ROSIDL_GENERATOR_C_PUBLIC_menu_order_interfaces
void
menu_order_interfaces__srv__MenuTable_Response__Sequence__fini(menu_order_interfaces__srv__MenuTable_Response__Sequence * array);

/// Create array of srv/MenuTable messages.
/**
 * It allocates the memory for the array and calls
 * menu_order_interfaces__srv__MenuTable_Response__Sequence__init().
 * \param[in] size The size / capacity of the array.
 * \return The pointer to the initialized array if successful, otherwise NULL
 */
ROSIDL_GENERATOR_C_PUBLIC_menu_order_interfaces
menu_order_interfaces__srv__MenuTable_Response__Sequence *
menu_order_interfaces__srv__MenuTable_Response__Sequence__create(size_t size);

/// Destroy array of srv/MenuTable messages.
/**
 * It calls
 * menu_order_interfaces__srv__MenuTable_Response__Sequence__fini()
 * on the array,
 * and frees the memory of the array.
 * \param[in,out] array The initialized array pointer.
 */
ROSIDL_GENERATOR_C_PUBLIC_menu_order_interfaces
void
menu_order_interfaces__srv__MenuTable_Response__Sequence__destroy(menu_order_interfaces__srv__MenuTable_Response__Sequence * array);

/// Check for srv/MenuTable message array equality.
/**
 * \param[in] lhs The message array on the left hand size of the equality operator.
 * \param[in] rhs The message array on the right hand size of the equality operator.
 * \return true if message arrays are equal in size and content, otherwise false.
 */
ROSIDL_GENERATOR_C_PUBLIC_menu_order_interfaces
bool
menu_order_interfaces__srv__MenuTable_Response__Sequence__are_equal(const menu_order_interfaces__srv__MenuTable_Response__Sequence * lhs, const menu_order_interfaces__srv__MenuTable_Response__Sequence * rhs);

/// Copy an array of srv/MenuTable messages.
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
menu_order_interfaces__srv__MenuTable_Response__Sequence__copy(
  const menu_order_interfaces__srv__MenuTable_Response__Sequence * input,
  menu_order_interfaces__srv__MenuTable_Response__Sequence * output);

#ifdef __cplusplus
}
#endif

#endif  // MENU_ORDER_INTERFACES__SRV__DETAIL__MENU_TABLE__FUNCTIONS_H_
