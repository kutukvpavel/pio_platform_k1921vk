#include "printf_ths.h"
#include "retarget_conf.h"

#include <FreeRTOS.h>
#include <K1921VK01T.h>
#include <message_buffer.h>
#include <niietcm4.h>
#include <system_K1921VK01T.h>
#include <task.h>

#define UNUSED(x) (void)(x)

#define LED0_PIN  (GPIO_Pin_8)
#define LED0_PORT (NT_GPIOG)

#define LED1_PIN  (GPIO_Pin_9)
#define LED1_PORT (NT_GPIOG)

volatile int a = 0;
//

void Led0Blink_task(void* pvParameters) {
    UNUSED(pvParameters);
    while (1) {
        GPIO_ToggleBits(LED0_PORT, LED0_PIN);
        printf_ths("led0 state %d\n", (int)GPIO_ReadBit(LED0_PORT, LED0_PIN));
        a++; // You can use debug breakpoint there to see value of variable
        vTaskDelay(500 / portTICK_PERIOD_MS);
    }
}

void Led1Blink_task(void* pvParameters) {
    UNUSED(pvParameters);
    while (1) {
        GPIO_ToggleBits(LED1_PORT, LED1_PIN);
        printf_ths("led1 state %d\n", (int)GPIO_ReadBit(LED1_PORT, LED1_PIN));
        a++; // You can use debug breakpoint there to see value of variable
        vTaskDelay(100 / portTICK_PERIOD_MS);
    }
}

void periph_init() {
    SystemCoreClockUpdate();
    retarget_init(); // UART0 used for printf

    GPIO_Init_TypeDef gpio_init_struct;
    GPIO_StructInit(&gpio_init_struct);
    gpio_init_struct.GPIO_AltFunc = GPIO_AltFunc_1;
    gpio_init_struct.GPIO_Dir     = GPIO_Dir_Out;
    gpio_init_struct.GPIO_Mode    = GPIO_Mode_IO;
    gpio_init_struct.GPIO_Out     = GPIO_Out_En;
    gpio_init_struct.GPIO_OutMode = GPIO_OutMode_PP;
    gpio_init_struct.GPIO_Pin     = LED0_PIN;
    GPIO_Init(LED0_PORT, &gpio_init_struct);

    GPIO_StructInit(&gpio_init_struct);
    gpio_init_struct.GPIO_AltFunc = GPIO_AltFunc_1;
    gpio_init_struct.GPIO_Dir     = GPIO_Dir_Out;
    gpio_init_struct.GPIO_Mode    = GPIO_Mode_IO;
    gpio_init_struct.GPIO_Out     = GPIO_Out_En;
    gpio_init_struct.GPIO_OutMode = GPIO_OutMode_PP;
    gpio_init_struct.GPIO_Pin     = LED1_PIN;
    GPIO_Init(LED1_PORT, &gpio_init_struct);
}

void freertos_init_objects() {
    printf_ths_init();
    // Dynamic task allocation
    xTaskCreate(Led0Blink_task, "Led0Blink_task", configMINIMAL_STACK_SIZE, NULL, tskIDLE_PRIORITY + 1, NULL);

// Static task allocation
#define Led1Blink_task_STACK_SIZE (configMINIMAL_STACK_SIZE)
    static StaticTask_t xLed1Blink_task;
    static StackType_t  ucLed1Blink_task_Stack[Led1Blink_task_STACK_SIZE];

    xTaskCreateStatic(Led1Blink_task, "Led1Blink_task", Led1Blink_task_STACK_SIZE, NULL, tskIDLE_PRIORITY + 1, ucLed1Blink_task_Stack, &xLed1Blink_task);
}

//-- Main ----------------------------------------------------------------------
int main() {
    periph_init();
    freertos_init_objects();
    printf("K1921VK01T> All periph inited\n");
    printf("K1921VK01T> CPU frequency is %lu MHz\n", SystemCoreClock / (int)1E6);

    vTaskStartScheduler();
    return 0;
}

// freertos hooks

void vApplicationStackOverflowHook(TaskHandle_t xTask, char* pcTaskName) {
    UNUSED(xTask);
    UNUSED(pcTaskName);
    configASSERT(0);
}

void vApplicationGetIdleTaskMemory(StaticTask_t** ppxIdleTaskTCBBuffer, StackType_t** ppxIdleTaskStackBuffer, uint32_t* pulIdleTaskStackSize) {
    static StaticTask_t Idle_TCB;
    static StackType_t  Idle_Stack[configMINIMAL_STACK_SIZE];

    *ppxIdleTaskTCBBuffer   = &Idle_TCB;
    *ppxIdleTaskStackBuffer = Idle_Stack;
    *pulIdleTaskStackSize   = configMINIMAL_STACK_SIZE;
}

void vApplicationGetTimerTaskMemory(StaticTask_t** ppxTimerTaskTCBBuffer, StackType_t** ppxTimerTaskStackBuffer, uint32_t* pulTimerTaskStackSize) {
    static StaticTask_t Timer_TCB;
    static StackType_t  Timer_Stack[configTIMER_TASK_STACK_DEPTH];

    *ppxTimerTaskTCBBuffer   = &Timer_TCB;
    *ppxTimerTaskStackBuffer = Timer_Stack;
    *pulTimerTaskStackSize   = configTIMER_TASK_STACK_DEPTH;
}