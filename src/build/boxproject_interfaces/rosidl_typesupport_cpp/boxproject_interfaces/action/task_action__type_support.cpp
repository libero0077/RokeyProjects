// generated from rosidl_typesupport_cpp/resource/idl__type_support.cpp.em
// with input from boxproject_interfaces:action/TaskAction.idl
// generated code does not contain a copyright notice

#include "cstddef"
#include "rosidl_runtime_c/message_type_support_struct.h"
#include "boxproject_interfaces/action/detail/task_action__struct.hpp"
#include "rosidl_typesupport_cpp/identifier.hpp"
#include "rosidl_typesupport_cpp/message_type_support.hpp"
#include "rosidl_typesupport_c/type_support_map.h"
#include "rosidl_typesupport_cpp/message_type_support_dispatch.hpp"
#include "rosidl_typesupport_cpp/visibility_control.h"
#include "rosidl_typesupport_interface/macros.h"

namespace boxproject_interfaces
{

namespace action
{

namespace rosidl_typesupport_cpp
{

typedef struct _TaskAction_Goal_type_support_ids_t
{
  const char * typesupport_identifier[2];
} _TaskAction_Goal_type_support_ids_t;

static const _TaskAction_Goal_type_support_ids_t _TaskAction_Goal_message_typesupport_ids = {
  {
    "rosidl_typesupport_fastrtps_cpp",  // ::rosidl_typesupport_fastrtps_cpp::typesupport_identifier,
    "rosidl_typesupport_introspection_cpp",  // ::rosidl_typesupport_introspection_cpp::typesupport_identifier,
  }
};

typedef struct _TaskAction_Goal_type_support_symbol_names_t
{
  const char * symbol_name[2];
} _TaskAction_Goal_type_support_symbol_names_t;

#define STRINGIFY_(s) #s
#define STRINGIFY(s) STRINGIFY_(s)

static const _TaskAction_Goal_type_support_symbol_names_t _TaskAction_Goal_message_typesupport_symbol_names = {
  {
    STRINGIFY(ROSIDL_TYPESUPPORT_INTERFACE__MESSAGE_SYMBOL_NAME(rosidl_typesupport_fastrtps_cpp, boxproject_interfaces, action, TaskAction_Goal)),
    STRINGIFY(ROSIDL_TYPESUPPORT_INTERFACE__MESSAGE_SYMBOL_NAME(rosidl_typesupport_introspection_cpp, boxproject_interfaces, action, TaskAction_Goal)),
  }
};

typedef struct _TaskAction_Goal_type_support_data_t
{
  void * data[2];
} _TaskAction_Goal_type_support_data_t;

static _TaskAction_Goal_type_support_data_t _TaskAction_Goal_message_typesupport_data = {
  {
    0,  // will store the shared library later
    0,  // will store the shared library later
  }
};

static const type_support_map_t _TaskAction_Goal_message_typesupport_map = {
  2,
  "boxproject_interfaces",
  &_TaskAction_Goal_message_typesupport_ids.typesupport_identifier[0],
  &_TaskAction_Goal_message_typesupport_symbol_names.symbol_name[0],
  &_TaskAction_Goal_message_typesupport_data.data[0],
};

static const rosidl_message_type_support_t TaskAction_Goal_message_type_support_handle = {
  ::rosidl_typesupport_cpp::typesupport_identifier,
  reinterpret_cast<const type_support_map_t *>(&_TaskAction_Goal_message_typesupport_map),
  ::rosidl_typesupport_cpp::get_message_typesupport_handle_function,
};

}  // namespace rosidl_typesupport_cpp

}  // namespace action

}  // namespace boxproject_interfaces

namespace rosidl_typesupport_cpp
{

template<>
ROSIDL_TYPESUPPORT_CPP_PUBLIC
const rosidl_message_type_support_t *
get_message_type_support_handle<boxproject_interfaces::action::TaskAction_Goal>()
{
  return &::boxproject_interfaces::action::rosidl_typesupport_cpp::TaskAction_Goal_message_type_support_handle;
}

#ifdef __cplusplus
extern "C"
{
#endif

ROSIDL_TYPESUPPORT_CPP_PUBLIC
const rosidl_message_type_support_t *
ROSIDL_TYPESUPPORT_INTERFACE__MESSAGE_SYMBOL_NAME(rosidl_typesupport_cpp, boxproject_interfaces, action, TaskAction_Goal)() {
  return get_message_type_support_handle<boxproject_interfaces::action::TaskAction_Goal>();
}

#ifdef __cplusplus
}
#endif
}  // namespace rosidl_typesupport_cpp

// already included above
// #include "cstddef"
// already included above
// #include "rosidl_runtime_c/message_type_support_struct.h"
// already included above
// #include "boxproject_interfaces/action/detail/task_action__struct.hpp"
// already included above
// #include "rosidl_typesupport_cpp/identifier.hpp"
// already included above
// #include "rosidl_typesupport_cpp/message_type_support.hpp"
// already included above
// #include "rosidl_typesupport_c/type_support_map.h"
// already included above
// #include "rosidl_typesupport_cpp/message_type_support_dispatch.hpp"
// already included above
// #include "rosidl_typesupport_cpp/visibility_control.h"
// already included above
// #include "rosidl_typesupport_interface/macros.h"

namespace boxproject_interfaces
{

namespace action
{

namespace rosidl_typesupport_cpp
{

typedef struct _TaskAction_Result_type_support_ids_t
{
  const char * typesupport_identifier[2];
} _TaskAction_Result_type_support_ids_t;

static const _TaskAction_Result_type_support_ids_t _TaskAction_Result_message_typesupport_ids = {
  {
    "rosidl_typesupport_fastrtps_cpp",  // ::rosidl_typesupport_fastrtps_cpp::typesupport_identifier,
    "rosidl_typesupport_introspection_cpp",  // ::rosidl_typesupport_introspection_cpp::typesupport_identifier,
  }
};

typedef struct _TaskAction_Result_type_support_symbol_names_t
{
  const char * symbol_name[2];
} _TaskAction_Result_type_support_symbol_names_t;

#define STRINGIFY_(s) #s
#define STRINGIFY(s) STRINGIFY_(s)

static const _TaskAction_Result_type_support_symbol_names_t _TaskAction_Result_message_typesupport_symbol_names = {
  {
    STRINGIFY(ROSIDL_TYPESUPPORT_INTERFACE__MESSAGE_SYMBOL_NAME(rosidl_typesupport_fastrtps_cpp, boxproject_interfaces, action, TaskAction_Result)),
    STRINGIFY(ROSIDL_TYPESUPPORT_INTERFACE__MESSAGE_SYMBOL_NAME(rosidl_typesupport_introspection_cpp, boxproject_interfaces, action, TaskAction_Result)),
  }
};

typedef struct _TaskAction_Result_type_support_data_t
{
  void * data[2];
} _TaskAction_Result_type_support_data_t;

static _TaskAction_Result_type_support_data_t _TaskAction_Result_message_typesupport_data = {
  {
    0,  // will store the shared library later
    0,  // will store the shared library later
  }
};

static const type_support_map_t _TaskAction_Result_message_typesupport_map = {
  2,
  "boxproject_interfaces",
  &_TaskAction_Result_message_typesupport_ids.typesupport_identifier[0],
  &_TaskAction_Result_message_typesupport_symbol_names.symbol_name[0],
  &_TaskAction_Result_message_typesupport_data.data[0],
};

static const rosidl_message_type_support_t TaskAction_Result_message_type_support_handle = {
  ::rosidl_typesupport_cpp::typesupport_identifier,
  reinterpret_cast<const type_support_map_t *>(&_TaskAction_Result_message_typesupport_map),
  ::rosidl_typesupport_cpp::get_message_typesupport_handle_function,
};

}  // namespace rosidl_typesupport_cpp

}  // namespace action

}  // namespace boxproject_interfaces

namespace rosidl_typesupport_cpp
{

template<>
ROSIDL_TYPESUPPORT_CPP_PUBLIC
const rosidl_message_type_support_t *
get_message_type_support_handle<boxproject_interfaces::action::TaskAction_Result>()
{
  return &::boxproject_interfaces::action::rosidl_typesupport_cpp::TaskAction_Result_message_type_support_handle;
}

#ifdef __cplusplus
extern "C"
{
#endif

ROSIDL_TYPESUPPORT_CPP_PUBLIC
const rosidl_message_type_support_t *
ROSIDL_TYPESUPPORT_INTERFACE__MESSAGE_SYMBOL_NAME(rosidl_typesupport_cpp, boxproject_interfaces, action, TaskAction_Result)() {
  return get_message_type_support_handle<boxproject_interfaces::action::TaskAction_Result>();
}

#ifdef __cplusplus
}
#endif
}  // namespace rosidl_typesupport_cpp

// already included above
// #include "cstddef"
// already included above
// #include "rosidl_runtime_c/message_type_support_struct.h"
// already included above
// #include "boxproject_interfaces/action/detail/task_action__struct.hpp"
// already included above
// #include "rosidl_typesupport_cpp/identifier.hpp"
// already included above
// #include "rosidl_typesupport_cpp/message_type_support.hpp"
// already included above
// #include "rosidl_typesupport_c/type_support_map.h"
// already included above
// #include "rosidl_typesupport_cpp/message_type_support_dispatch.hpp"
// already included above
// #include "rosidl_typesupport_cpp/visibility_control.h"
// already included above
// #include "rosidl_typesupport_interface/macros.h"

namespace boxproject_interfaces
{

namespace action
{

namespace rosidl_typesupport_cpp
{

typedef struct _TaskAction_Feedback_type_support_ids_t
{
  const char * typesupport_identifier[2];
} _TaskAction_Feedback_type_support_ids_t;

static const _TaskAction_Feedback_type_support_ids_t _TaskAction_Feedback_message_typesupport_ids = {
  {
    "rosidl_typesupport_fastrtps_cpp",  // ::rosidl_typesupport_fastrtps_cpp::typesupport_identifier,
    "rosidl_typesupport_introspection_cpp",  // ::rosidl_typesupport_introspection_cpp::typesupport_identifier,
  }
};

typedef struct _TaskAction_Feedback_type_support_symbol_names_t
{
  const char * symbol_name[2];
} _TaskAction_Feedback_type_support_symbol_names_t;

#define STRINGIFY_(s) #s
#define STRINGIFY(s) STRINGIFY_(s)

static const _TaskAction_Feedback_type_support_symbol_names_t _TaskAction_Feedback_message_typesupport_symbol_names = {
  {
    STRINGIFY(ROSIDL_TYPESUPPORT_INTERFACE__MESSAGE_SYMBOL_NAME(rosidl_typesupport_fastrtps_cpp, boxproject_interfaces, action, TaskAction_Feedback)),
    STRINGIFY(ROSIDL_TYPESUPPORT_INTERFACE__MESSAGE_SYMBOL_NAME(rosidl_typesupport_introspection_cpp, boxproject_interfaces, action, TaskAction_Feedback)),
  }
};

typedef struct _TaskAction_Feedback_type_support_data_t
{
  void * data[2];
} _TaskAction_Feedback_type_support_data_t;

static _TaskAction_Feedback_type_support_data_t _TaskAction_Feedback_message_typesupport_data = {
  {
    0,  // will store the shared library later
    0,  // will store the shared library later
  }
};

static const type_support_map_t _TaskAction_Feedback_message_typesupport_map = {
  2,
  "boxproject_interfaces",
  &_TaskAction_Feedback_message_typesupport_ids.typesupport_identifier[0],
  &_TaskAction_Feedback_message_typesupport_symbol_names.symbol_name[0],
  &_TaskAction_Feedback_message_typesupport_data.data[0],
};

static const rosidl_message_type_support_t TaskAction_Feedback_message_type_support_handle = {
  ::rosidl_typesupport_cpp::typesupport_identifier,
  reinterpret_cast<const type_support_map_t *>(&_TaskAction_Feedback_message_typesupport_map),
  ::rosidl_typesupport_cpp::get_message_typesupport_handle_function,
};

}  // namespace rosidl_typesupport_cpp

}  // namespace action

}  // namespace boxproject_interfaces

namespace rosidl_typesupport_cpp
{

template<>
ROSIDL_TYPESUPPORT_CPP_PUBLIC
const rosidl_message_type_support_t *
get_message_type_support_handle<boxproject_interfaces::action::TaskAction_Feedback>()
{
  return &::boxproject_interfaces::action::rosidl_typesupport_cpp::TaskAction_Feedback_message_type_support_handle;
}

#ifdef __cplusplus
extern "C"
{
#endif

ROSIDL_TYPESUPPORT_CPP_PUBLIC
const rosidl_message_type_support_t *
ROSIDL_TYPESUPPORT_INTERFACE__MESSAGE_SYMBOL_NAME(rosidl_typesupport_cpp, boxproject_interfaces, action, TaskAction_Feedback)() {
  return get_message_type_support_handle<boxproject_interfaces::action::TaskAction_Feedback>();
}

#ifdef __cplusplus
}
#endif
}  // namespace rosidl_typesupport_cpp

// already included above
// #include "cstddef"
// already included above
// #include "rosidl_runtime_c/message_type_support_struct.h"
// already included above
// #include "boxproject_interfaces/action/detail/task_action__struct.hpp"
// already included above
// #include "rosidl_typesupport_cpp/identifier.hpp"
// already included above
// #include "rosidl_typesupport_cpp/message_type_support.hpp"
// already included above
// #include "rosidl_typesupport_c/type_support_map.h"
// already included above
// #include "rosidl_typesupport_cpp/message_type_support_dispatch.hpp"
// already included above
// #include "rosidl_typesupport_cpp/visibility_control.h"
// already included above
// #include "rosidl_typesupport_interface/macros.h"

namespace boxproject_interfaces
{

namespace action
{

namespace rosidl_typesupport_cpp
{

typedef struct _TaskAction_SendGoal_Request_type_support_ids_t
{
  const char * typesupport_identifier[2];
} _TaskAction_SendGoal_Request_type_support_ids_t;

static const _TaskAction_SendGoal_Request_type_support_ids_t _TaskAction_SendGoal_Request_message_typesupport_ids = {
  {
    "rosidl_typesupport_fastrtps_cpp",  // ::rosidl_typesupport_fastrtps_cpp::typesupport_identifier,
    "rosidl_typesupport_introspection_cpp",  // ::rosidl_typesupport_introspection_cpp::typesupport_identifier,
  }
};

typedef struct _TaskAction_SendGoal_Request_type_support_symbol_names_t
{
  const char * symbol_name[2];
} _TaskAction_SendGoal_Request_type_support_symbol_names_t;

#define STRINGIFY_(s) #s
#define STRINGIFY(s) STRINGIFY_(s)

static const _TaskAction_SendGoal_Request_type_support_symbol_names_t _TaskAction_SendGoal_Request_message_typesupport_symbol_names = {
  {
    STRINGIFY(ROSIDL_TYPESUPPORT_INTERFACE__MESSAGE_SYMBOL_NAME(rosidl_typesupport_fastrtps_cpp, boxproject_interfaces, action, TaskAction_SendGoal_Request)),
    STRINGIFY(ROSIDL_TYPESUPPORT_INTERFACE__MESSAGE_SYMBOL_NAME(rosidl_typesupport_introspection_cpp, boxproject_interfaces, action, TaskAction_SendGoal_Request)),
  }
};

typedef struct _TaskAction_SendGoal_Request_type_support_data_t
{
  void * data[2];
} _TaskAction_SendGoal_Request_type_support_data_t;

static _TaskAction_SendGoal_Request_type_support_data_t _TaskAction_SendGoal_Request_message_typesupport_data = {
  {
    0,  // will store the shared library later
    0,  // will store the shared library later
  }
};

static const type_support_map_t _TaskAction_SendGoal_Request_message_typesupport_map = {
  2,
  "boxproject_interfaces",
  &_TaskAction_SendGoal_Request_message_typesupport_ids.typesupport_identifier[0],
  &_TaskAction_SendGoal_Request_message_typesupport_symbol_names.symbol_name[0],
  &_TaskAction_SendGoal_Request_message_typesupport_data.data[0],
};

static const rosidl_message_type_support_t TaskAction_SendGoal_Request_message_type_support_handle = {
  ::rosidl_typesupport_cpp::typesupport_identifier,
  reinterpret_cast<const type_support_map_t *>(&_TaskAction_SendGoal_Request_message_typesupport_map),
  ::rosidl_typesupport_cpp::get_message_typesupport_handle_function,
};

}  // namespace rosidl_typesupport_cpp

}  // namespace action

}  // namespace boxproject_interfaces

namespace rosidl_typesupport_cpp
{

template<>
ROSIDL_TYPESUPPORT_CPP_PUBLIC
const rosidl_message_type_support_t *
get_message_type_support_handle<boxproject_interfaces::action::TaskAction_SendGoal_Request>()
{
  return &::boxproject_interfaces::action::rosidl_typesupport_cpp::TaskAction_SendGoal_Request_message_type_support_handle;
}

#ifdef __cplusplus
extern "C"
{
#endif

ROSIDL_TYPESUPPORT_CPP_PUBLIC
const rosidl_message_type_support_t *
ROSIDL_TYPESUPPORT_INTERFACE__MESSAGE_SYMBOL_NAME(rosidl_typesupport_cpp, boxproject_interfaces, action, TaskAction_SendGoal_Request)() {
  return get_message_type_support_handle<boxproject_interfaces::action::TaskAction_SendGoal_Request>();
}

#ifdef __cplusplus
}
#endif
}  // namespace rosidl_typesupport_cpp

// already included above
// #include "cstddef"
// already included above
// #include "rosidl_runtime_c/message_type_support_struct.h"
// already included above
// #include "boxproject_interfaces/action/detail/task_action__struct.hpp"
// already included above
// #include "rosidl_typesupport_cpp/identifier.hpp"
// already included above
// #include "rosidl_typesupport_cpp/message_type_support.hpp"
// already included above
// #include "rosidl_typesupport_c/type_support_map.h"
// already included above
// #include "rosidl_typesupport_cpp/message_type_support_dispatch.hpp"
// already included above
// #include "rosidl_typesupport_cpp/visibility_control.h"
// already included above
// #include "rosidl_typesupport_interface/macros.h"

namespace boxproject_interfaces
{

namespace action
{

namespace rosidl_typesupport_cpp
{

typedef struct _TaskAction_SendGoal_Response_type_support_ids_t
{
  const char * typesupport_identifier[2];
} _TaskAction_SendGoal_Response_type_support_ids_t;

static const _TaskAction_SendGoal_Response_type_support_ids_t _TaskAction_SendGoal_Response_message_typesupport_ids = {
  {
    "rosidl_typesupport_fastrtps_cpp",  // ::rosidl_typesupport_fastrtps_cpp::typesupport_identifier,
    "rosidl_typesupport_introspection_cpp",  // ::rosidl_typesupport_introspection_cpp::typesupport_identifier,
  }
};

typedef struct _TaskAction_SendGoal_Response_type_support_symbol_names_t
{
  const char * symbol_name[2];
} _TaskAction_SendGoal_Response_type_support_symbol_names_t;

#define STRINGIFY_(s) #s
#define STRINGIFY(s) STRINGIFY_(s)

static const _TaskAction_SendGoal_Response_type_support_symbol_names_t _TaskAction_SendGoal_Response_message_typesupport_symbol_names = {
  {
    STRINGIFY(ROSIDL_TYPESUPPORT_INTERFACE__MESSAGE_SYMBOL_NAME(rosidl_typesupport_fastrtps_cpp, boxproject_interfaces, action, TaskAction_SendGoal_Response)),
    STRINGIFY(ROSIDL_TYPESUPPORT_INTERFACE__MESSAGE_SYMBOL_NAME(rosidl_typesupport_introspection_cpp, boxproject_interfaces, action, TaskAction_SendGoal_Response)),
  }
};

typedef struct _TaskAction_SendGoal_Response_type_support_data_t
{
  void * data[2];
} _TaskAction_SendGoal_Response_type_support_data_t;

static _TaskAction_SendGoal_Response_type_support_data_t _TaskAction_SendGoal_Response_message_typesupport_data = {
  {
    0,  // will store the shared library later
    0,  // will store the shared library later
  }
};

static const type_support_map_t _TaskAction_SendGoal_Response_message_typesupport_map = {
  2,
  "boxproject_interfaces",
  &_TaskAction_SendGoal_Response_message_typesupport_ids.typesupport_identifier[0],
  &_TaskAction_SendGoal_Response_message_typesupport_symbol_names.symbol_name[0],
  &_TaskAction_SendGoal_Response_message_typesupport_data.data[0],
};

static const rosidl_message_type_support_t TaskAction_SendGoal_Response_message_type_support_handle = {
  ::rosidl_typesupport_cpp::typesupport_identifier,
  reinterpret_cast<const type_support_map_t *>(&_TaskAction_SendGoal_Response_message_typesupport_map),
  ::rosidl_typesupport_cpp::get_message_typesupport_handle_function,
};

}  // namespace rosidl_typesupport_cpp

}  // namespace action

}  // namespace boxproject_interfaces

namespace rosidl_typesupport_cpp
{

template<>
ROSIDL_TYPESUPPORT_CPP_PUBLIC
const rosidl_message_type_support_t *
get_message_type_support_handle<boxproject_interfaces::action::TaskAction_SendGoal_Response>()
{
  return &::boxproject_interfaces::action::rosidl_typesupport_cpp::TaskAction_SendGoal_Response_message_type_support_handle;
}

#ifdef __cplusplus
extern "C"
{
#endif

ROSIDL_TYPESUPPORT_CPP_PUBLIC
const rosidl_message_type_support_t *
ROSIDL_TYPESUPPORT_INTERFACE__MESSAGE_SYMBOL_NAME(rosidl_typesupport_cpp, boxproject_interfaces, action, TaskAction_SendGoal_Response)() {
  return get_message_type_support_handle<boxproject_interfaces::action::TaskAction_SendGoal_Response>();
}

#ifdef __cplusplus
}
#endif
}  // namespace rosidl_typesupport_cpp

// already included above
// #include "cstddef"
#include "rosidl_runtime_c/service_type_support_struct.h"
// already included above
// #include "boxproject_interfaces/action/detail/task_action__struct.hpp"
// already included above
// #include "rosidl_typesupport_cpp/identifier.hpp"
#include "rosidl_typesupport_cpp/service_type_support.hpp"
// already included above
// #include "rosidl_typesupport_c/type_support_map.h"
#include "rosidl_typesupport_cpp/service_type_support_dispatch.hpp"
// already included above
// #include "rosidl_typesupport_cpp/visibility_control.h"
// already included above
// #include "rosidl_typesupport_interface/macros.h"

namespace boxproject_interfaces
{

namespace action
{

namespace rosidl_typesupport_cpp
{

typedef struct _TaskAction_SendGoal_type_support_ids_t
{
  const char * typesupport_identifier[2];
} _TaskAction_SendGoal_type_support_ids_t;

static const _TaskAction_SendGoal_type_support_ids_t _TaskAction_SendGoal_service_typesupport_ids = {
  {
    "rosidl_typesupport_fastrtps_cpp",  // ::rosidl_typesupport_fastrtps_cpp::typesupport_identifier,
    "rosidl_typesupport_introspection_cpp",  // ::rosidl_typesupport_introspection_cpp::typesupport_identifier,
  }
};

typedef struct _TaskAction_SendGoal_type_support_symbol_names_t
{
  const char * symbol_name[2];
} _TaskAction_SendGoal_type_support_symbol_names_t;

#define STRINGIFY_(s) #s
#define STRINGIFY(s) STRINGIFY_(s)

static const _TaskAction_SendGoal_type_support_symbol_names_t _TaskAction_SendGoal_service_typesupport_symbol_names = {
  {
    STRINGIFY(ROSIDL_TYPESUPPORT_INTERFACE__SERVICE_SYMBOL_NAME(rosidl_typesupport_fastrtps_cpp, boxproject_interfaces, action, TaskAction_SendGoal)),
    STRINGIFY(ROSIDL_TYPESUPPORT_INTERFACE__SERVICE_SYMBOL_NAME(rosidl_typesupport_introspection_cpp, boxproject_interfaces, action, TaskAction_SendGoal)),
  }
};

typedef struct _TaskAction_SendGoal_type_support_data_t
{
  void * data[2];
} _TaskAction_SendGoal_type_support_data_t;

static _TaskAction_SendGoal_type_support_data_t _TaskAction_SendGoal_service_typesupport_data = {
  {
    0,  // will store the shared library later
    0,  // will store the shared library later
  }
};

static const type_support_map_t _TaskAction_SendGoal_service_typesupport_map = {
  2,
  "boxproject_interfaces",
  &_TaskAction_SendGoal_service_typesupport_ids.typesupport_identifier[0],
  &_TaskAction_SendGoal_service_typesupport_symbol_names.symbol_name[0],
  &_TaskAction_SendGoal_service_typesupport_data.data[0],
};

static const rosidl_service_type_support_t TaskAction_SendGoal_service_type_support_handle = {
  ::rosidl_typesupport_cpp::typesupport_identifier,
  reinterpret_cast<const type_support_map_t *>(&_TaskAction_SendGoal_service_typesupport_map),
  ::rosidl_typesupport_cpp::get_service_typesupport_handle_function,
};

}  // namespace rosidl_typesupport_cpp

}  // namespace action

}  // namespace boxproject_interfaces

namespace rosidl_typesupport_cpp
{

template<>
ROSIDL_TYPESUPPORT_CPP_PUBLIC
const rosidl_service_type_support_t *
get_service_type_support_handle<boxproject_interfaces::action::TaskAction_SendGoal>()
{
  return &::boxproject_interfaces::action::rosidl_typesupport_cpp::TaskAction_SendGoal_service_type_support_handle;
}

}  // namespace rosidl_typesupport_cpp

// already included above
// #include "cstddef"
// already included above
// #include "rosidl_runtime_c/message_type_support_struct.h"
// already included above
// #include "boxproject_interfaces/action/detail/task_action__struct.hpp"
// already included above
// #include "rosidl_typesupport_cpp/identifier.hpp"
// already included above
// #include "rosidl_typesupport_cpp/message_type_support.hpp"
// already included above
// #include "rosidl_typesupport_c/type_support_map.h"
// already included above
// #include "rosidl_typesupport_cpp/message_type_support_dispatch.hpp"
// already included above
// #include "rosidl_typesupport_cpp/visibility_control.h"
// already included above
// #include "rosidl_typesupport_interface/macros.h"

namespace boxproject_interfaces
{

namespace action
{

namespace rosidl_typesupport_cpp
{

typedef struct _TaskAction_GetResult_Request_type_support_ids_t
{
  const char * typesupport_identifier[2];
} _TaskAction_GetResult_Request_type_support_ids_t;

static const _TaskAction_GetResult_Request_type_support_ids_t _TaskAction_GetResult_Request_message_typesupport_ids = {
  {
    "rosidl_typesupport_fastrtps_cpp",  // ::rosidl_typesupport_fastrtps_cpp::typesupport_identifier,
    "rosidl_typesupport_introspection_cpp",  // ::rosidl_typesupport_introspection_cpp::typesupport_identifier,
  }
};

typedef struct _TaskAction_GetResult_Request_type_support_symbol_names_t
{
  const char * symbol_name[2];
} _TaskAction_GetResult_Request_type_support_symbol_names_t;

#define STRINGIFY_(s) #s
#define STRINGIFY(s) STRINGIFY_(s)

static const _TaskAction_GetResult_Request_type_support_symbol_names_t _TaskAction_GetResult_Request_message_typesupport_symbol_names = {
  {
    STRINGIFY(ROSIDL_TYPESUPPORT_INTERFACE__MESSAGE_SYMBOL_NAME(rosidl_typesupport_fastrtps_cpp, boxproject_interfaces, action, TaskAction_GetResult_Request)),
    STRINGIFY(ROSIDL_TYPESUPPORT_INTERFACE__MESSAGE_SYMBOL_NAME(rosidl_typesupport_introspection_cpp, boxproject_interfaces, action, TaskAction_GetResult_Request)),
  }
};

typedef struct _TaskAction_GetResult_Request_type_support_data_t
{
  void * data[2];
} _TaskAction_GetResult_Request_type_support_data_t;

static _TaskAction_GetResult_Request_type_support_data_t _TaskAction_GetResult_Request_message_typesupport_data = {
  {
    0,  // will store the shared library later
    0,  // will store the shared library later
  }
};

static const type_support_map_t _TaskAction_GetResult_Request_message_typesupport_map = {
  2,
  "boxproject_interfaces",
  &_TaskAction_GetResult_Request_message_typesupport_ids.typesupport_identifier[0],
  &_TaskAction_GetResult_Request_message_typesupport_symbol_names.symbol_name[0],
  &_TaskAction_GetResult_Request_message_typesupport_data.data[0],
};

static const rosidl_message_type_support_t TaskAction_GetResult_Request_message_type_support_handle = {
  ::rosidl_typesupport_cpp::typesupport_identifier,
  reinterpret_cast<const type_support_map_t *>(&_TaskAction_GetResult_Request_message_typesupport_map),
  ::rosidl_typesupport_cpp::get_message_typesupport_handle_function,
};

}  // namespace rosidl_typesupport_cpp

}  // namespace action

}  // namespace boxproject_interfaces

namespace rosidl_typesupport_cpp
{

template<>
ROSIDL_TYPESUPPORT_CPP_PUBLIC
const rosidl_message_type_support_t *
get_message_type_support_handle<boxproject_interfaces::action::TaskAction_GetResult_Request>()
{
  return &::boxproject_interfaces::action::rosidl_typesupport_cpp::TaskAction_GetResult_Request_message_type_support_handle;
}

#ifdef __cplusplus
extern "C"
{
#endif

ROSIDL_TYPESUPPORT_CPP_PUBLIC
const rosidl_message_type_support_t *
ROSIDL_TYPESUPPORT_INTERFACE__MESSAGE_SYMBOL_NAME(rosidl_typesupport_cpp, boxproject_interfaces, action, TaskAction_GetResult_Request)() {
  return get_message_type_support_handle<boxproject_interfaces::action::TaskAction_GetResult_Request>();
}

#ifdef __cplusplus
}
#endif
}  // namespace rosidl_typesupport_cpp

// already included above
// #include "cstddef"
// already included above
// #include "rosidl_runtime_c/message_type_support_struct.h"
// already included above
// #include "boxproject_interfaces/action/detail/task_action__struct.hpp"
// already included above
// #include "rosidl_typesupport_cpp/identifier.hpp"
// already included above
// #include "rosidl_typesupport_cpp/message_type_support.hpp"
// already included above
// #include "rosidl_typesupport_c/type_support_map.h"
// already included above
// #include "rosidl_typesupport_cpp/message_type_support_dispatch.hpp"
// already included above
// #include "rosidl_typesupport_cpp/visibility_control.h"
// already included above
// #include "rosidl_typesupport_interface/macros.h"

namespace boxproject_interfaces
{

namespace action
{

namespace rosidl_typesupport_cpp
{

typedef struct _TaskAction_GetResult_Response_type_support_ids_t
{
  const char * typesupport_identifier[2];
} _TaskAction_GetResult_Response_type_support_ids_t;

static const _TaskAction_GetResult_Response_type_support_ids_t _TaskAction_GetResult_Response_message_typesupport_ids = {
  {
    "rosidl_typesupport_fastrtps_cpp",  // ::rosidl_typesupport_fastrtps_cpp::typesupport_identifier,
    "rosidl_typesupport_introspection_cpp",  // ::rosidl_typesupport_introspection_cpp::typesupport_identifier,
  }
};

typedef struct _TaskAction_GetResult_Response_type_support_symbol_names_t
{
  const char * symbol_name[2];
} _TaskAction_GetResult_Response_type_support_symbol_names_t;

#define STRINGIFY_(s) #s
#define STRINGIFY(s) STRINGIFY_(s)

static const _TaskAction_GetResult_Response_type_support_symbol_names_t _TaskAction_GetResult_Response_message_typesupport_symbol_names = {
  {
    STRINGIFY(ROSIDL_TYPESUPPORT_INTERFACE__MESSAGE_SYMBOL_NAME(rosidl_typesupport_fastrtps_cpp, boxproject_interfaces, action, TaskAction_GetResult_Response)),
    STRINGIFY(ROSIDL_TYPESUPPORT_INTERFACE__MESSAGE_SYMBOL_NAME(rosidl_typesupport_introspection_cpp, boxproject_interfaces, action, TaskAction_GetResult_Response)),
  }
};

typedef struct _TaskAction_GetResult_Response_type_support_data_t
{
  void * data[2];
} _TaskAction_GetResult_Response_type_support_data_t;

static _TaskAction_GetResult_Response_type_support_data_t _TaskAction_GetResult_Response_message_typesupport_data = {
  {
    0,  // will store the shared library later
    0,  // will store the shared library later
  }
};

static const type_support_map_t _TaskAction_GetResult_Response_message_typesupport_map = {
  2,
  "boxproject_interfaces",
  &_TaskAction_GetResult_Response_message_typesupport_ids.typesupport_identifier[0],
  &_TaskAction_GetResult_Response_message_typesupport_symbol_names.symbol_name[0],
  &_TaskAction_GetResult_Response_message_typesupport_data.data[0],
};

static const rosidl_message_type_support_t TaskAction_GetResult_Response_message_type_support_handle = {
  ::rosidl_typesupport_cpp::typesupport_identifier,
  reinterpret_cast<const type_support_map_t *>(&_TaskAction_GetResult_Response_message_typesupport_map),
  ::rosidl_typesupport_cpp::get_message_typesupport_handle_function,
};

}  // namespace rosidl_typesupport_cpp

}  // namespace action

}  // namespace boxproject_interfaces

namespace rosidl_typesupport_cpp
{

template<>
ROSIDL_TYPESUPPORT_CPP_PUBLIC
const rosidl_message_type_support_t *
get_message_type_support_handle<boxproject_interfaces::action::TaskAction_GetResult_Response>()
{
  return &::boxproject_interfaces::action::rosidl_typesupport_cpp::TaskAction_GetResult_Response_message_type_support_handle;
}

#ifdef __cplusplus
extern "C"
{
#endif

ROSIDL_TYPESUPPORT_CPP_PUBLIC
const rosidl_message_type_support_t *
ROSIDL_TYPESUPPORT_INTERFACE__MESSAGE_SYMBOL_NAME(rosidl_typesupport_cpp, boxproject_interfaces, action, TaskAction_GetResult_Response)() {
  return get_message_type_support_handle<boxproject_interfaces::action::TaskAction_GetResult_Response>();
}

#ifdef __cplusplus
}
#endif
}  // namespace rosidl_typesupport_cpp

// already included above
// #include "cstddef"
// already included above
// #include "rosidl_runtime_c/service_type_support_struct.h"
// already included above
// #include "boxproject_interfaces/action/detail/task_action__struct.hpp"
// already included above
// #include "rosidl_typesupport_cpp/identifier.hpp"
// already included above
// #include "rosidl_typesupport_cpp/service_type_support.hpp"
// already included above
// #include "rosidl_typesupport_c/type_support_map.h"
// already included above
// #include "rosidl_typesupport_cpp/service_type_support_dispatch.hpp"
// already included above
// #include "rosidl_typesupport_cpp/visibility_control.h"
// already included above
// #include "rosidl_typesupport_interface/macros.h"

namespace boxproject_interfaces
{

namespace action
{

namespace rosidl_typesupport_cpp
{

typedef struct _TaskAction_GetResult_type_support_ids_t
{
  const char * typesupport_identifier[2];
} _TaskAction_GetResult_type_support_ids_t;

static const _TaskAction_GetResult_type_support_ids_t _TaskAction_GetResult_service_typesupport_ids = {
  {
    "rosidl_typesupport_fastrtps_cpp",  // ::rosidl_typesupport_fastrtps_cpp::typesupport_identifier,
    "rosidl_typesupport_introspection_cpp",  // ::rosidl_typesupport_introspection_cpp::typesupport_identifier,
  }
};

typedef struct _TaskAction_GetResult_type_support_symbol_names_t
{
  const char * symbol_name[2];
} _TaskAction_GetResult_type_support_symbol_names_t;

#define STRINGIFY_(s) #s
#define STRINGIFY(s) STRINGIFY_(s)

static const _TaskAction_GetResult_type_support_symbol_names_t _TaskAction_GetResult_service_typesupport_symbol_names = {
  {
    STRINGIFY(ROSIDL_TYPESUPPORT_INTERFACE__SERVICE_SYMBOL_NAME(rosidl_typesupport_fastrtps_cpp, boxproject_interfaces, action, TaskAction_GetResult)),
    STRINGIFY(ROSIDL_TYPESUPPORT_INTERFACE__SERVICE_SYMBOL_NAME(rosidl_typesupport_introspection_cpp, boxproject_interfaces, action, TaskAction_GetResult)),
  }
};

typedef struct _TaskAction_GetResult_type_support_data_t
{
  void * data[2];
} _TaskAction_GetResult_type_support_data_t;

static _TaskAction_GetResult_type_support_data_t _TaskAction_GetResult_service_typesupport_data = {
  {
    0,  // will store the shared library later
    0,  // will store the shared library later
  }
};

static const type_support_map_t _TaskAction_GetResult_service_typesupport_map = {
  2,
  "boxproject_interfaces",
  &_TaskAction_GetResult_service_typesupport_ids.typesupport_identifier[0],
  &_TaskAction_GetResult_service_typesupport_symbol_names.symbol_name[0],
  &_TaskAction_GetResult_service_typesupport_data.data[0],
};

static const rosidl_service_type_support_t TaskAction_GetResult_service_type_support_handle = {
  ::rosidl_typesupport_cpp::typesupport_identifier,
  reinterpret_cast<const type_support_map_t *>(&_TaskAction_GetResult_service_typesupport_map),
  ::rosidl_typesupport_cpp::get_service_typesupport_handle_function,
};

}  // namespace rosidl_typesupport_cpp

}  // namespace action

}  // namespace boxproject_interfaces

namespace rosidl_typesupport_cpp
{

template<>
ROSIDL_TYPESUPPORT_CPP_PUBLIC
const rosidl_service_type_support_t *
get_service_type_support_handle<boxproject_interfaces::action::TaskAction_GetResult>()
{
  return &::boxproject_interfaces::action::rosidl_typesupport_cpp::TaskAction_GetResult_service_type_support_handle;
}

}  // namespace rosidl_typesupport_cpp

// already included above
// #include "cstddef"
// already included above
// #include "rosidl_runtime_c/message_type_support_struct.h"
// already included above
// #include "boxproject_interfaces/action/detail/task_action__struct.hpp"
// already included above
// #include "rosidl_typesupport_cpp/identifier.hpp"
// already included above
// #include "rosidl_typesupport_cpp/message_type_support.hpp"
// already included above
// #include "rosidl_typesupport_c/type_support_map.h"
// already included above
// #include "rosidl_typesupport_cpp/message_type_support_dispatch.hpp"
// already included above
// #include "rosidl_typesupport_cpp/visibility_control.h"
// already included above
// #include "rosidl_typesupport_interface/macros.h"

namespace boxproject_interfaces
{

namespace action
{

namespace rosidl_typesupport_cpp
{

typedef struct _TaskAction_FeedbackMessage_type_support_ids_t
{
  const char * typesupport_identifier[2];
} _TaskAction_FeedbackMessage_type_support_ids_t;

static const _TaskAction_FeedbackMessage_type_support_ids_t _TaskAction_FeedbackMessage_message_typesupport_ids = {
  {
    "rosidl_typesupport_fastrtps_cpp",  // ::rosidl_typesupport_fastrtps_cpp::typesupport_identifier,
    "rosidl_typesupport_introspection_cpp",  // ::rosidl_typesupport_introspection_cpp::typesupport_identifier,
  }
};

typedef struct _TaskAction_FeedbackMessage_type_support_symbol_names_t
{
  const char * symbol_name[2];
} _TaskAction_FeedbackMessage_type_support_symbol_names_t;

#define STRINGIFY_(s) #s
#define STRINGIFY(s) STRINGIFY_(s)

static const _TaskAction_FeedbackMessage_type_support_symbol_names_t _TaskAction_FeedbackMessage_message_typesupport_symbol_names = {
  {
    STRINGIFY(ROSIDL_TYPESUPPORT_INTERFACE__MESSAGE_SYMBOL_NAME(rosidl_typesupport_fastrtps_cpp, boxproject_interfaces, action, TaskAction_FeedbackMessage)),
    STRINGIFY(ROSIDL_TYPESUPPORT_INTERFACE__MESSAGE_SYMBOL_NAME(rosidl_typesupport_introspection_cpp, boxproject_interfaces, action, TaskAction_FeedbackMessage)),
  }
};

typedef struct _TaskAction_FeedbackMessage_type_support_data_t
{
  void * data[2];
} _TaskAction_FeedbackMessage_type_support_data_t;

static _TaskAction_FeedbackMessage_type_support_data_t _TaskAction_FeedbackMessage_message_typesupport_data = {
  {
    0,  // will store the shared library later
    0,  // will store the shared library later
  }
};

static const type_support_map_t _TaskAction_FeedbackMessage_message_typesupport_map = {
  2,
  "boxproject_interfaces",
  &_TaskAction_FeedbackMessage_message_typesupport_ids.typesupport_identifier[0],
  &_TaskAction_FeedbackMessage_message_typesupport_symbol_names.symbol_name[0],
  &_TaskAction_FeedbackMessage_message_typesupport_data.data[0],
};

static const rosidl_message_type_support_t TaskAction_FeedbackMessage_message_type_support_handle = {
  ::rosidl_typesupport_cpp::typesupport_identifier,
  reinterpret_cast<const type_support_map_t *>(&_TaskAction_FeedbackMessage_message_typesupport_map),
  ::rosidl_typesupport_cpp::get_message_typesupport_handle_function,
};

}  // namespace rosidl_typesupport_cpp

}  // namespace action

}  // namespace boxproject_interfaces

namespace rosidl_typesupport_cpp
{

template<>
ROSIDL_TYPESUPPORT_CPP_PUBLIC
const rosidl_message_type_support_t *
get_message_type_support_handle<boxproject_interfaces::action::TaskAction_FeedbackMessage>()
{
  return &::boxproject_interfaces::action::rosidl_typesupport_cpp::TaskAction_FeedbackMessage_message_type_support_handle;
}

#ifdef __cplusplus
extern "C"
{
#endif

ROSIDL_TYPESUPPORT_CPP_PUBLIC
const rosidl_message_type_support_t *
ROSIDL_TYPESUPPORT_INTERFACE__MESSAGE_SYMBOL_NAME(rosidl_typesupport_cpp, boxproject_interfaces, action, TaskAction_FeedbackMessage)() {
  return get_message_type_support_handle<boxproject_interfaces::action::TaskAction_FeedbackMessage>();
}

#ifdef __cplusplus
}
#endif
}  // namespace rosidl_typesupport_cpp

#include "action_msgs/msg/goal_status_array.hpp"
#include "action_msgs/srv/cancel_goal.hpp"
// already included above
// #include "boxproject_interfaces/action/detail/task_action__struct.hpp"
// already included above
// #include "rosidl_typesupport_cpp/visibility_control.h"
#include "rosidl_runtime_c/action_type_support_struct.h"
#include "rosidl_typesupport_cpp/action_type_support.hpp"
// already included above
// #include "rosidl_typesupport_cpp/message_type_support.hpp"
// already included above
// #include "rosidl_typesupport_cpp/service_type_support.hpp"

namespace boxproject_interfaces
{

namespace action
{

namespace rosidl_typesupport_cpp
{

static rosidl_action_type_support_t TaskAction_action_type_support_handle = {
  NULL, NULL, NULL, NULL, NULL};

}  // namespace rosidl_typesupport_cpp

}  // namespace action

}  // namespace boxproject_interfaces

namespace rosidl_typesupport_cpp
{

template<>
ROSIDL_TYPESUPPORT_CPP_PUBLIC
const rosidl_action_type_support_t *
get_action_type_support_handle<boxproject_interfaces::action::TaskAction>()
{
  using ::boxproject_interfaces::action::rosidl_typesupport_cpp::TaskAction_action_type_support_handle;
  // Thread-safe by always writing the same values to the static struct
  TaskAction_action_type_support_handle.goal_service_type_support = get_service_type_support_handle<::boxproject_interfaces::action::TaskAction::Impl::SendGoalService>();
  TaskAction_action_type_support_handle.result_service_type_support = get_service_type_support_handle<::boxproject_interfaces::action::TaskAction::Impl::GetResultService>();
  TaskAction_action_type_support_handle.cancel_service_type_support = get_service_type_support_handle<::boxproject_interfaces::action::TaskAction::Impl::CancelGoalService>();
  TaskAction_action_type_support_handle.feedback_message_type_support = get_message_type_support_handle<::boxproject_interfaces::action::TaskAction::Impl::FeedbackMessage>();
  TaskAction_action_type_support_handle.status_message_type_support = get_message_type_support_handle<::boxproject_interfaces::action::TaskAction::Impl::GoalStatusMessage>();
  return &TaskAction_action_type_support_handle;
}

}  // namespace rosidl_typesupport_cpp
