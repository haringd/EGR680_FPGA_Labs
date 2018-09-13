`timescale 1ns / 1ps
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
    input rst,
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

decoder dec1(SW0, SW1, BTN0, clk, rst, seg0, ~BTN0); 
//     decoder(
//       input SW0,
//       input SW1,
//       input BTN0,
//       input clk,
//       input rst,
//       output [6:0] seg,
//       output digit
//       );
always @(BTN0 or BTN1) 
    begin
    if (BTN0) dec1;
end
endmodule
