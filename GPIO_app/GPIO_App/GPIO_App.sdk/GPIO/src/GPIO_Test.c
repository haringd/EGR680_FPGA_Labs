/*
 * GPIO_Test.c
 *
 *  Created on: Sep 22, 2018
 *      Author: Chirag
 */

/*
 * GPIO_Test.c
 *
 *  Created on: Oct 15, 2017
 *      Author: Chirag
 */


#include <stdio.h>
#include <stdlib.h>
#include "xil_printf.h"
#include "xparameters.h"
#include "xgpio.h"
#include "xtime_l.h"


int main()
{
    XGpio dip, push;
    XTime tStart, tEnd;

    int i, psb_check=0, dip_check, sel, cpu;

    XGpio_Initialize(&dip, XPAR_SWITCHES_DEVICE_ID);
    XGpio_SetDataDirection(&dip, 1, 0xffffffff);

    XGpio_Initialize(&push, XPAR_BUTTONS_DEVICE_ID);
    XGpio_SetDataDirection(&push, 1, 0xffffffff);


    XTime_GetTime(&tStart);
    print("---Welcome to Number Guesser Game----\n\r");
    printf("Select between 1 and 5 to seed the Random Number Generator:");
    scanf("%d",sel);
    XTime_GetTime(&tEnd);

    srand(tEnd - tStart);

   	cpu = rand()%4;
   	switch(cpu)
   	{
   	 case 0: cpu = 1; break;
   	 case 1: cpu = 2; break;
     case 2: cpu = 4; break;
   	 case 3: cpu = 8; break;
   	}
   	xil_printf("\n\rComputer chose %d\n\r",cpu);

   	while(psb_check == 0)
   		  psb_check = XGpio_DiscreteRead(&push, 1);

   	if(psb_check == cpu)
   	{
      xil_printf("--------------------\n\r");
   	  xil_printf("You can read my mind\n\r");
   	  xil_printf("--------------------\n\r");
   	}
   	else
   	{
   	  xil_printf("--------------------\n\r");
   	  xil_printf("You suck !!!\n\r");
   	  xil_printf("--------------------\n\r");
   	}



    	/*while(1)
    	{
    		psb_check = XGpio_DiscreteRead(&push, 1);
    		xil_printf("Push Buttons Status %x\r\n", psb_check);
    		dip_check = XGpio_DiscreteRead(&dip, 1);
    		xil_printf("DIP Switch Status %x\r\n", dip_check);

    		for(i=0; i<9999999; i++);
    	}*/
        return 0;
}

