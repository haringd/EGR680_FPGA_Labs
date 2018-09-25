//////////////////////////////////////////////////////////////////////////////////
// Company: GVSU
// Engineer: D. Häring
// 
// Create Date: 22.09.2018 
// Design Name: 
// Module Name: decoder
// Project Name: VENDMACH
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
/*********************************************************************************
** Decoder for seven-segment desplay (seg) PmodA and PmodB                                                          **
**********************************************************************************
                                          |
                   Pmod A                 |                Pmod B
    --------------------------------------|--------------------------------------               
         seg01               seg02        |        se11               seg12
    +------------+       +------------+   |   +------------+      +------------+
    |     A      |       |     A      |   |   |     A      |      |     A      |
    |   -----    |       |   -----    |   |   |   -----    |      |   -----    |
    |  |     |   |       |  |     |   |   |   |  |     |   |      |  |     |   |
    | F|     |B  |       | F|     |B  |   |   | F|     |B  |      | F|     |B  |
    |  |  G  |   |       |  |  G  |   |   |   |  |  G  |   |      |  |  G  |   |
    |   -----    |       |   -----    |   |   |   -----    |      |   -----    |
    |  |     |   |       |  |     |   |   |   |  |     |   |      |  |     |   |
    | E|     |C  |       | E|     |C  |   |   | E|     |C  |      | E|     |C  |
    |  |     |   |       |  |     |   |   |   |  |     |   |      |  |     |   |
    |   -----  ° |       |   -----  ° |   |   |   -----  ° |      |   -----  ° |
    |     D      |       |     D      |   |   |     D      |      |     D      |
    +------------+       +------------+   |   +------------+      +------------+
              |                |                         |                |
        /|    |                |                   /|    |                |
cat0  /  |    |                |           cat1  /  |    |                |
-----    |o---+----------------+           -----    |o---+----------------+
      \  |                                       \  |                      
       \ |                                        \ |       
       
       example for using the seven-segment display
             [6:0]        GFEDCBA // MSB LSB definition
       2'b00 : seg0 =  7'b0111111;//0
       2'b01 : seg0 =  7'b0000110;//1
       2'b10 : seg0 =  7'b1011011;//2
       2'b11 : seg0 =  7'b1001111;//3              
*********************************************************************************/
`timescale 1ns / 1ns
module decoder(
    input [6:0] seg01, 
    input [6:0] seg02, 
    input [6:0] seg11, 
    input [6:0] seg12,
    input clk,
    input rst, // BTN3
    output reg [6:0] seg0,
    output reg [6:0] seg1,
    output reg cat0,
    output reg cat1
    );

reg [1:0] shift = 2'b00;

always @(posedge clk or negedge rst) begin
if (!rst) begin
  seg0 = 7'b0000000;
  seg1 = 7'b0000000;
  shift = 2'b00;
end else begin
shift = shift + 1;

case (shift)
   2'b00 :     begin
     cat0 <= 1'b1;
     seg0 =  seg01;
     end  
   2'b01 :     begin    
    cat0 <= 1'b0;
    seg0 =  seg02;
    end    
    
   2'b10 :     begin      
    cat1 <= 1'b1;
   seg1 =  seg11;
   end    
       
   2'b11 :     begin      
    cat1 <= 1'b0;
    seg1 =  seg12;
   end     
   default: begin
     seg0 = 7'b0000000;
     seg1 = 7'b0000000;
     end
   endcase           
end // else rst
end // always
endmodule