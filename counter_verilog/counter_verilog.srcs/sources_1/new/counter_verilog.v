`timescale 1ns / 1ps
//////////////////////////////////////////////////////////////////////////////////
// Company: 
// Engineer: 
// 
// Create Date: 03.09.2018 18:08:25
// Design Name: 
// Module Name: counter_verilog
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


module counter_verilog(
    input clk,
    input rst,
    output [3:0] ledout
    );
    
/*
input clk,rst;
output [3:0] ledout;
*/

reg [3:0] ledout;
reg [30:0] ledtemp;

always @(posedge clk or negedge rst)
begin
    if(rst != 1)
    begin
        ledtemp <= 0;
    end
    else 
        ledtemp <= ledtemp +1; // Incerement ledtemp only on rising edge of clk
end

always @(posedge ledtemp[26] or negedge rst)
begin
    if(rst != 1)
        ledout <= 0;
    else
        ledout <= ledout + 1;
end
endmodule
