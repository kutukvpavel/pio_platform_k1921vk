#include <FreeRTOS.h>
#include <message_buffer.h>
#include <queue.h>

void printf_ths_init();
void printf_ths(const char* str, ...);
void printf_ths_Task(void* pvParameters);

#ifndef printf_ths_MAX_LEN
#define printf_ths_MAX_LEN 500
#endif