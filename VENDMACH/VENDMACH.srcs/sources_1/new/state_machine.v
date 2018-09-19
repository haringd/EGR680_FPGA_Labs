`timescale 1ns / 1ns
//////////////////////////////////////////////////////////////////////////////////
// Company: GVSU
// Engineer: D. Häring
// 
// Create Date: 17.09.2018 23:14:32
// Design Name: 
// Module Name: state_machine
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
** FSM State machine                                                            **
**********************************************************************************
	                       001                                  000
       +---------------------+               +---------------------+
       |                     |               |                     |
       | Idle                |<--------------| Reset               |<------+
       | Display OFF         |               | BTN3                |       |
       +---------------------+               +---------------------+-      |
           |                                                               |
           |                                                               |
           |              003                                              |       002
       +---------------------+ Add to coin_val                  +---------------------+
       |                     |---------------+                  | Delay               |
       | Coin entered show   |               |                  | 3s                  |
       | coin_val on Pmod A  |<--------------+                  |                     |
       +---------------------+                                  +---------------------+
           |                                                              / \ 
           |                                                             / | \
           |              004                                              |       007
       +---------------------+                                  +---------------------+
       | IF value > Gum      |                                  | Vend                |
       | & coin_val > 10     |--------------------------------->| Display "VENT"      |
       | Display 'g' by BTN0 |                                  | Disp returned cents |
       +---------------------+                                  +---------------------+
           |                                                              / \ 
           |                                                             / | \
           |              005                                              |
       +---------------------+                                             |
       | IF value > Apple    |                                             |
       | & coin_val > 15     |------------------->------------------->-----+
       | Display 'A' by BTN1 |                                             |
       +---------------------+                                             |
           |                                                               |
           |                                                               |
           |              006                                              |
       +---------------------+                                             |
       | IF value > Yogurt   |                                             |
       | & coin_val > 20     |------------------->------------------->-----+
       | Display 'y' by BTN2 |                                           
       +---------------------+            
       
       
       Example code moor machine out of lecture FPGA class Fall 2018
       --------------------------------------------------------------
       module moore_detector (input x, rst, clk, output z);
       parameter reset=2'b0, got1=2'b01, got10=2'b10, got101=2'b11;
       reg [1:0] current;
       always @( posedge clk ) begin
       ...........................
       end
       assign z = (current==got101) ? 1 : 0;
       endmodule                               
*********************************************************************************/

`define RESET   3'b000
`define IDLE    3'b001
`define DELAY   3'b010
`define COIN    3'b011
`define GUM     3'b100
`define APPLE   3'b101
`define YOGURT  3'b110

module state_machine(
    input clk,
    input rst
    );
    // parameter reset=2'b0, got1=2'b01, got10=2'b10, got101=2'b11; 
    // parameter could be used instead of `define
    reg [2:0] current;
    //reg [2:0] state;

    always @( posedge clk or negedge rst) begin
    //...........................
    if( rst ) current <= `RESET;
    else begin
    case (current)
    `RESET : begin
        end
    default: begin
    current <= `RESET;  end
    endcase
    end // else synchrones rst
    end // always
    // Output logic
    // assign z = (current==got101) ? 1 : 0;
      
endmodule
