`timescale 1ns / 1ns
//////////////////////////////////////////////////////////////////////////////////
// Company: 
// Engineer: 
// 
// Create Date: 12.09.2018 23:03:22
// Design Name: 
// Module Name: decoder_top
// Project Name: 
// Target Devices: 
// Tool Versions: 
// Description: 
// 
// Dependencies: 
// 
// Revision:
// Revision 0.01 - File Created
// Additional Comments:
// 
//////////////////////////////////////////////////////////////////////////////////

module decoder_top(
    input clk,
    //input rst,
    input SW0,
    input SW1,
    input BTN0,
    input BTN1,
    input BTN2,
    input BTN3,
    output cat0,
    output cat1,
    output [6:0] seg0,
    output [6:0] seg1
    );

/* Intaniate modules */
decoder dec1(SW0, SW1, BTN0, BTN1,BTN2,BTN3,clk, seg0,seg1, cat0,cat1 ); 
endmodule