`timescale 1ns / 1ns
//////////////////////////////////////////////////////////////////////////////////
// Company: 
// Engineer: 
// 
// Create Date: 19.09.2018 23:44:18
// Design Name: 
// Module Name: state_machine_tb
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


module state_machine_tb;
    
//    wire clk_out;
reg NICKEL, DIME, GUM, CLOCK, RESET;
wire cat0, cat1;
wire [6:0] seg01;
wire [6:0] seg02;
wire [6:0] seg11;
wire [6:0] seg12;
wire [3:0] CHANGE;
wire [6:0] seg0;
wire [6:0] seg1;
state_machine sm(CLOCK, RESET, DIME, NICKEL, GUM, seg0, seg1, ledout );
//clk_divider clk_div1(CLOCK, RESET, 4, clk_seg);
// dec(seg01, seg02, seg11, seg12, RESET, clk_seg, seg0, seg1, cat0, cat1);

//state_machine sm(CLOCK, RESET, DIME, NICKEL, GUM, seg01, seg02, seg11, seg12, CHANGE);
//vendmach_top vm_t(NICKEL, DIME, GUM, APPLE, YOGURT, RESET, CLOCK, seg0, seg1, cat0, cat1, CHANGE );

//clk_divider clk_div1(CLOCK, RESET, 500000, clk_seg);
//decoder dec(seg, clk_seg, RESET, seg0, seg1, cat0, cat1);
//state_machine sm(CLOCK, RESET, DIME, NICKEL, GUM, seg, CHANGE);

initial //set inputs to a known state
begin
    CLOCK = 0;
    RESET = 0;
    DIME = 0;
    NICKEL = 0;
    GUM = 0;
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

initial #1000 $finish;
    
endmodule