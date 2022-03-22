#include "K1921VK01T.h"
#include "retarget_conf.h"
#include "system_K1921VK01T.h"
#include "niietcm4.h"

#define LED_PIN (GPIO_Pin_8)
#define LED_PORT (NT_GPIOF)

void periph_init()
{
    SystemCoreClockUpdate();
    retarget_init();//UART0 used for printf
    SysTick_Config(10000000);//5 Hz

    GPIO_Init_TypeDef gpio_init_struct;
    GPIO_StructInit(&gpio_init_struct);
    gpio_init_struct.GPIO_AltFunc = GPIO_AltFunc_1;
    gpio_init_struct.GPIO_Dir = GPIO_Dir_Out;
    gpio_init_struct.GPIO_Mode = GPIO_Mode_IO;
    gpio_init_struct.GPIO_Out =  GPIO_Out_En;
    gpio_init_struct.GPIO_OutMode = GPIO_OutMode_PP;
    gpio_init_struct.GPIO_Pin = LED_PIN; 
    GPIO_Init(LED_PORT,&gpio_init_struct);
}

volatile int a = 0;
//-- Main ----------------------------------------------------------------------
int main()
{
    periph_init();
    printf("K1921VK01T> All periph inited\n");
    printf("K1921VK01T> CPU frequency is %lu MHz\n", SystemCoreClock / (int)1E6);

    while(1){
       // __WFI();
    }
    return 0;
}

void SysTick_Handler()
{
    GPIO_ToggleBits(LED_PORT, LED_PIN);
    printf("led state %d\n", GPIO_ReadBit(LED_PORT, LED_PIN));
    a++;// You can use debug breakpoint there to see value of variable
}