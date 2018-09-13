`timescale 1ns / 1ns
//////////////////////////////////////////////////////////////////////////////////
// Company: 
// Engineer: 
// 
// Create Date: 12.09.2018 19:51:24
// Design Name: 
// Module Name: decoder_tb
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


module decoder_tb;

reg SW0, SW1, BTN0, clk, rst;
wire [6:0] seg;
wire digit;
    
decoder X1(SW0, SW1, BTN0, clk, rst, seg, digit);  // Initialistaion

initial 
begin
    SW0 = 0;
    SW1 = 0;
    BTN0 = 0;
    clk = 0;
    rst = 0;
end

always #10 clk = ~clk;
 
initial begin
   #100;
   rst = 1; #50;
   rst = 0; #50;
   SW0 = 0; SW1 = 0; BTN0 = 1; #100;
   BTN0 = 0; #50;
   rst = 0; SW0 = 1; SW1 = 0; BTN0 = 1; #100;
    BTN0 = 0; #50;
   rst = 0; SW0 = 0; SW1 = 1; BTN0 = 1; #100;
    BTN0 = 0; #50;
   rst = 0; SW0 = 1; SW1 = 1; BTN0 = 1; #100;
    BTN0 = 0; 
    
end
initial #1000 $finish;
endmodule
