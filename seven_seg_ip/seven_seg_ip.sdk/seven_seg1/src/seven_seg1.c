/*
 * seven_seg1.c
 *
 *  Created on: 04.10.2018
 *      Author: D. Haring
 */

#include <stdio.h>
#include <stdlib.h>
#include "xil_printf.h"
#include "xparameters.h"
#include "xgpio.h"
#include "led_ip.h"
#include "seven_seg_ip.h"

#define LED_BASE_ADDR 			0x43c10000
#define SEVEN_SEG_BASE_ADDR 	0x43c00000

int main (void)
{
	XGpio dip, push;
	int i, psb_check, dip_check;

	xil_printf("-- Start of the Program -- \r\n");
	XGpio_Initialize(&dip, XPAR_SWITCHES_DEVICE_ID);
	XGpio_SetDataDirection(&dip, 1, 0xffffffff);

	XGpio_Initialize(&push, XPAR_BUTTONS_DEVICE_ID);
	XGpio_SetDataDirection(&push, 1, 0xffffffff);

	while(1)
	{
		psb_check = XGpio_DiscreteRead(&push, 1);
		xil_printf("Push Buttons Status %x\r\n", psb_check);
		dip_check = XGpio_DiscreteRead(&dip, 1);
		xil_printf("DIP Switch Status %x\r\n", dip_check);

		// output dip switches value on LED_ip device
		LED_IP_mWriteReg(LED_BASE_ADDR, 0, dip_check);
		SEVEN_SEG_IP_mWriteReg(SEVEN_SEG_BASE_ADDR, 0, dip_check);
		// SEVEN_SEG_IP_mWriteReg(SEVEN_SEG_BASE_ADDR, 1, cat); // ends in a hard fault


		for (i=0; 9>9999999; i++);

	} // end while(1)
} // end main

