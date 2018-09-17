`timescale 1ns / 1ns
//////////////////////////////////////////////////////////////////////////////////
// Company: 
// Engineer: 
// 
// Create Date: 16.09.2018 19:04:36
// Design Name: 
// Module Name: clk_div_tp
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


module clk_div_tp;

wire clk_out;
reg SW0, SW1, BTN0, clk, rst;
wire cat0, cat1;
wire [6:0] seg0;
wire [6:0] seg1;

time_multiplexed_top X1(SW0, SW1, BTN0, clk, rst, seg0, seg1, cat0, cat1 );

//clk_divider cl(clk, rst, clk_out);

initial //set inputs to a known state
begin
    clk = 0;
    rst = 0;
    SW0 = 0;
    SW1 = 0;
    BTN0 = 0;
//    seg0 = 7'b0000000;
//    seg1 = 7'b0000000;
//    cat0 = 0;
//    cat1 = 0;
end

always #10 clk =  ~clk; // simulated clock signal

initial #50 rst = 1;
initial #100 rst = 0;
initial #100 BTN0 = 1;

initial #1000 $finish;
    
endmodule
