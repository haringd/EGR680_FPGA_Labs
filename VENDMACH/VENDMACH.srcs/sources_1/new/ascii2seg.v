`timescale 1ns / 1ns
//////////////////////////////////////////////////////////////////////////////////
// Company: 
// Engineer: 
// 
// Create Date: 22.09.2018 13:31:38
// Design Name: 
// Module Name: ascii2seg
// Project Name: 
// Target Devices: 
// Tool Versions: 
// Description: 
// 
// Dependencies: 
// 
// Revision:
// Revision 0.01 - File Created
// Additional Comments: This module is build for the Grove seven-segment displays
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
    |   -----  � |       |   -----  � |   |   |   -----  � |      |   -----  � |
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

module ascii2seg(
    input clk,
    input rst,
    input [7:0] char,
    output reg [6:0] seg
    );
        
    always @(posedge clk or negedge rst)
    if(!rst) begin
        seg = 7'b0000000; 
    end else begin                                                   
          case (char)                                    
             8'h00: seg <= 7'b0000000;         //      seg      
             8'h30: seg <= 7'b0111111;//0      // +------------+
             8'h31: seg <= 7'b0000110;//1      // |     A      |
             8'h32: seg <= 7'b1011011;//2      // |   -----    |
             8'h33: seg <= 7'b1001111;//3      // |  |     |   |
             8'h34: seg <= 7'b1100110;//4      // | F|     |B  |
             8'h35: seg <= 7'b1101101;//5      // |  |  G  |   |
             8'h36: seg <= 7'b1111100;//6      // |   -----    |
             8'h37: seg <= 7'b0000111;//7      // |  |     |   |
             8'h38: seg <= 7'b1111111;//8      // | E|     |C  |
             8'h39: seg <= 7'b1100111;//9      // |  |     |   |
             8'h40: seg <= 7'b0000000;//SPACE  // |   -----  � |
             8'h41: seg <= 7'b1110111;//A      // |     D      |
             8'h42: seg <= 7'b1111100;//b      // +------------+
             8'h43: seg <= 7'b0111001;//C
             8'h44: seg <= 7'b1011110;//d
             8'h45: seg <= 7'b1111001;//E
             8'h46: seg <= 7'b1110001;//F
             8'h47: seg <= 7'b1101111;//g
             8'h48: seg <= 7'b1110110;//H      //      seg      
             8'h49: seg <= 7'b0000110;//I      // +------------+
             8'h4A: seg <= 7'b0011110;//J      // |     A      |
             8'h4B: seg <= 7'b1110101;//k      // |   -----    |
             8'h4C: seg <= 7'b0111000;//L      // |  |     |   |
             8'h4D: seg <= 7'b0010101;//M      // | F|     |B  |
             8'h4E: seg <= 7'b1010100;//n      // |  |  G  |   |
             8'h4F: seg <= 7'b0111111;//O      // |   -----    |
             8'h50: seg <= 7'b1110011;//P      // |  |     |   |
             8'h51: seg <= 7'b1100111;//q      // | E|     |C  |
             8'h52: seg <= 7'b1010000;//r      // |  |     |   |
             8'h53: seg <= 7'b1101101;//S      // |   -----  � |
             8'h54: seg <= 7'b1111000;//t      // |     D      |
             8'h55: seg <= 7'b0011100;//u      // +------------+
             8'h56: seg <= 7'b0111110;//V
             8'h57: seg <= 7'b0101010;//W 
             8'h58: seg <= 7'b1110110;//X
             8'h59: seg <= 7'b1101110;//y
             8'h5A: seg <= 7'b1011011;//Z
             8'h5F: seg <= 7'b0001000;//_
             default: seg <= 7'b0000000; //<value>;
          endcase
     end // else if rst
endmodule
