#include "printf_ths.h"

#include "retarget_conf.h"

#include <stdarg.h>
#include <stdio.h>

MessageBufferHandle_t xMessageBufferPrintf;
void                  printf_ths_init() {
#define printf_ths_Task_STACK_SIZE (configMINIMAL_STACK_SIZE * 3)
#if configSUPPORT_STATIC_ALLOCATION == 1

    static StaticTask_t xPrintf_ths_Task;
    static StackType_t  ucPrintf_ths_Task_Stack[printf_ths_Task_STACK_SIZE];

    xTaskCreateStatic(printf_ths_Task, "printf_ths_Task", printf_ths_Task_STACK_SIZE, NULL, tskIDLE_PRIORITY, ucPrintf_ths_Task_Stack, &xPrintf_ths_Task);

    static uint8_t               ucStorageBufferPrintf_ths[printf_ths_MAX_LEN * 3];
    static StaticMessageBuffer_t xMessageBufferStructPrintf_ths;
    xMessageBufferPrintf = xMessageBufferCreateStatic(sizeof(ucStorageBufferPrintf_ths), ucStorageBufferPrintf_ths, &xMessageBufferStructPrintf_ths);
#else
    xTaskCreate(printf_ths_Task, "printf_ths_Task", printf_ths_Task_STACK_SIZE, NULL, tskIDLE_PRIORITY, NULL);
    xMessageBufferPrintf = xMessageBufferCreate(printf_ths_MAX_LEN * 3);
#endif
}

void printf_ths(const char* str, ...) {

    static char buf[printf_ths_MAX_LEN];
    va_list     arg_ptr;
    va_start(arg_ptr, str);
    size_t str_len = vsprintf(buf, str, arg_ptr);
    xMessageBufferSend(xMessageBufferPrintf, buf, str_len, portMAX_DELAY);
}

void printf_ths_Task(void* pvParameters) {
    static char buf[printf_ths_MAX_LEN];
    while (1) {
        size_t str_len = xMessageBufferReceive(xMessageBufferPrintf, buf, printf_ths_MAX_LEN, portMAX_DELAY);
        for (size_t i = 0; i < str_len; ++i) {
            retarget_put_char(buf[i]);
        }
    }
}