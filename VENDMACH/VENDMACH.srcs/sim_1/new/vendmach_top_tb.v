`timescale 1ns / 1ns
//////////////////////////////////////////////////////////////////////////////////
// Company: 
// Engineer: 
// 
// Create Date: 22.09.2018 15:24:22
// Design Name: 
// Module Name: vendmach_top_tb
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


module vendmach_top_tb;
//    wire clk_out;
reg NICKEL, DIME, GUM, APPLE, YOGURT, CLOCK, RESET;
wire cat0, cat1;
wire [3:0] CHANGE;
wire [6:0] seg0;
wire [6:0] seg1;

vendmach_top vm_t(NICKEL, DIME, GUM, APPLE, YOGURT, RESET, CLOCK, seg0, seg1, cat0, cat1, CHANGE );

initial //set inputs to a known state
begin
    CLOCK = 0;
    RESET = 0;
    DIME = 0;
    NICKEL = 0;
    GUM = 0;
    APPLE = 0;
    YOGURT = 0;
end

always #10 CLOCK =  ~CLOCK; // simulated clock signal

initial #50 RESET = 1;
initial #100 RESET = 0;
initial #200 NICKEL = 1;
initial #300 NICKEL = 0;
initial #400 DIME = 1;
initial #500 DIME = 0;

initial #600 GUM = 1;
initial #700 GUM = 0;

//initial #600 APPLE = 1;
//initial #700 APPLE = 0;

//initial #600 YOGURTUM = 1;
//initial #700 YOGURT = 0;

initial #1000 $finish;
endmodule
