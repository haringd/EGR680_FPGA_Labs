`timescale 1ns / 1ps
//////////////////////////////////////////////////////////////////////////////////
// Company: 
// Engineer: 
// 
// Create Date: 03.09.2018 18:23:57
// Design Name: 
// Module Name: counter_tb
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


module counter_tb(

    );
    
reg clk;
reg rst;
wire [3:0] ledout;

counter_verilog cl(clk,rst,ledout); //module instantiation

always #10 clk =~ clk; // simulated clock signal

initial //set inputs to a known state

begin
    clk = 0;
    rst = 0;
end

initial #99 rst = 1; //enable reset to start simulation

//initial #200 rst = 0;
//initial #300 rst = 1; //enable reset to start simulation
initial #500 $finish;
endmodule
