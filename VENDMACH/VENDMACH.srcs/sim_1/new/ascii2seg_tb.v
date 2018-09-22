`timescale 1ns / 1ns
//////////////////////////////////////////////////////////////////////////////////
// Company: 
// Engineer: 
// 
// Create Date: 22.09.2018 13:52:29
// Design Name: 
// Module Name: ascii2seg_tb
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


module ascii2seg_tb;

reg clk;
reg rst;
reg [7:0] char;
reg [6:0] seg;

ascii2seg a2s(clk, rst, char, seg);

initial //set inputs to a known state
begin
    clk = 0;
    rst = 0;
    char = 0;
    seg = 0;
end

always #10 clk =  ~clk; // simulated clock signal

initial #50 rst = 1;
initial #100 rst = 0;
initial #120 char = 8'h00;
initial #140 char = 8'h30;
//initial #20 char = 8'h31;
//initial #20 char = 8'h32;
//initial #20 char = 8'h33;
//initial #20 char = 8'h34;
//initial #20 char = 8'h35;
//initial #20 char = 8'h36;
//initial #20 char = 8'h37;
//initial #20 char = 8'h38;
//initial #20 char = 8'h39;
//initial #20 char = 8'h40;
//initial #20 char = 8'h41;
//initial #20 char = 8'h42;
//initial #20 char = 8'h43;
//initial #20 char = 8'h44;
//initial #20 char = 8'h45;
//initial #20 char = 8'h46;
//initial #20 char = 8'h47;
//initial #20 char = 8'h48;
//initial #20 char = 8'h49;
//initial #20 char = 8'h4A;
//initial #20 char = 8'h4B;
//initial #20 char = 8'h4C;
//initial #20 char = 8'h4D;
//initial #20 char = 8'h4E;
//initial #20 char = 8'h4F;
//initial #20 char = 8'h50;
//initial #20 char = 8'h51;
//initial #20 char = 8'h52;
//initial #20 char = 8'h53;
//initial #20 char = 8'h54;
//initial #20 char = 8'h55;
//initial #20 char = 8'h56;
//initial #20 char = 8'h57;
//initial #20 char = 8'h58;
//initial #20 char = 8'h59;
//initial #20 char = 8'h5A;
//initial #20 char = 8'h5F;

initial #1000 $finish;
endmodule
