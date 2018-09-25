`timescale 1ns / 1ns
//////////////////////////////////////////////////////////////////////////////////
// Company: 
// Engineer: 
// 
// Create Date: 23.09.2018 20:47:25
// Design Name: 
// Module Name: debounce
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


module debounce(
    input in,
    input clk_slow,
    input rst,
    output reg out
    );
 reg deb1, deb2 ;
 initial deb1 = 0; 
 initial deb2 = 0;   
 
    always @( posedge clk_slow or negedge rst )
      begin
          if (!rst) begin
              deb1 <=0; 
              deb2 <=0; 
              out <=0; 
          end else begin

          deb1 <= in;
          deb2 <= deb1;
          if (deb1 == 1 && deb2 == 0) out <= 1;
          else out <= 0;      
          end// if else rst
     end  // always   
endmodule
