/*
 * GPIO_game.c
 * Implements a game show with four buttons and the uart console named
 * Let's Make a Deal!
 *
 *  Created on: 01.10.2018
 *      Author: D. H�ring
 *
 *
 */

 /*   *************************************************************
 *   ** FSM State machine                                       **
 *   *************************************************************
 *                      000
 *   +---------------------+
 *   | Idle                |
 *   | Display user input  |<--------+
 *   |                     |         |
 *   +---------------------+         |
 *       |                           |
 *       |                           |
 *       |              001          |
 *   +---------------------+         |
 *   |                     |         |
 *   | Wait for button     |         |
 *   | coin_val on Pmod A  |         |
 *   +---------------------+         |
 *       |                           |
 *       |                           |
 *       |              002          |
 *   +---------------------+         |
 *   | user output         |         |
 *   | if (rnd == door)    |---------+
 *   | Display output      |
 *   +---------------------+
 * *************************************************************/


#include "xparameters.h"
#include "xgpio.h"
#include "xtime_l.h"
#include "sleep.h"

int main (void)
{
	XGpio dip, push;
	int psb_check, state, door, rnd; //dip_check,
	XTime startTime, stopTime, deltaTime;

	xil_printf("\r\n\r\n -- Start of the Program Let's Make a Deal -- \r\n");
	XGpio_Initialize(&dip, XPAR_SWITCHES_DEVICE_ID);
	XGpio_SetDataDirection(&dip, 1, 0xffffffff);

	XGpio_Initialize(&push, XPAR_BUTTONS_DEVICE_ID);
	XGpio_SetDataDirection(&push, 1, 0xffffffff);

	state = 0; 	// set default state
	door = 0;	// set default door value
	rnd = 0;	// set default rnd value
	startTime = 0;		// set default startTime value
	stopTime = 0;		// set default stopTime value
	deltaTime = 0;		// set default deltaTime value

	while(1)
	{

		psb_check = XGpio_DiscreteRead(&push, 1);

		switch (state) {
		case 0:// Idle state
			xil_printf("\r\n\r\n***********************************\r\n");
			xil_printf("---Welcome to Let's Make a Deal!---\r\n");
			xil_printf("***********************************\r\n");
			xil_printf("Select between 1 and 4 to seed the Random Number Generator: ");
			door = 0;	// set default door value
			rnd = 0;	// set default rnd value
			startTime = 0;		// set default startTime value
			stopTime = 0;		// set default stopTime value
			deltaTime = 0;		// set default deltaTime value
			XTime_GetTime(&startTime); // get start time
			state = 1;
			break;
		case 1: // wait for door to be chosen
			if (door){
				XTime_GetTime(&stopTime);
				if (startTime < stopTime) // handle eventual overflow
					deltaTime = stopTime - startTime;
				else
					deltaTime = startTime - stopTime;
				rnd = deltaTime % 4;
				rnd = rnd + 1;
				xil_printf("  %d\r\n", door);
//				xil_printf("  --> Debug: deltaTime %08x \r\n", deltaTime); // debug only
				usleep(400000); // from GVSU EE EGR326 2015 Fall lab 02
				state=2;
			}
			else
				state=1;

			break;
		case 2: // print result after player chose door
			xil_printf("\r\nComputer chose %d\r\n", rnd);
			xil_printf("---------------------\r\n");
			if (rnd == door)
				xil_printf("You Win!\r\n");
			else
				xil_printf("You suck !!!\r\n");
			xil_printf("---------------------\r\n");


			door = 0;	// set default door value
			rnd = 0;	// set default rnd value
			startTime = 0;		// set default startTime value
			stopTime = 0;		// set default stopTime value
			deltaTime = 0;		// set default deltaTime value
			state = 0; 			// set default state
			break;
		default:
			xil_printf("  --> Debug: %d %s\r\n", __FILE__, __LINE__);
			break;
		}

		switch (psb_check) {
		usleep(800000); // from GVSU EE EGR326 2015 Fall lab 02
		case 1:
			door = 1;
			break;
		case 2:
			door = 2;
			break;
		case 4:
			door = 3;
			break;
		case 8:
			door = 4;
			break;
		default:
			break;
		}

	} // end while(1)
} // end main

