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

`define RESET   3'b000 // 0
`define IDLE    3'b001 // 1
`define DELAY   3'b010 // 2
`define COIN    3'b011 // 3
`define GUM     3'b100 // 4
`define APPLE   3'b101 // 5
`define YOGURT  3'b110 // 6
`define VENT    3'b111 // 7

module state_machine(
    input clk,
    input rst,
    input DIME,
    input NICKEL,
    input GUM,
    output reg [7:0] char01, 
    output reg [7:0] char02, 
    output reg [7:0] char11, 
    output reg [7:0] char12,
    output reg [3:0] ledout
    );
    // parameter reset=2'b0, got1=2'b01, got10=2'b10, got101=2'b11; 
    // parameter could be used instead of `define
    reg [2:0] current = 3'b001;
    //reg [2:0] nxtState = 3'b001;
//    reg [2:0] coin_val;
   // integer coin_val;
    reg [31:0] coin_val = 0;
    
    
    always @( posedge clk or negedge rst) begin
    //...........................
//    nxtState = current; 
    if( rst ) current <= `RESET;
    else begin
    case (current)
    `RESET : begin
        current <= `IDLE;
        coin_val <= 0;
        char01 = " ";
        char02 = " ";
        char11 = " ";
        char12 = " ";
        ledout = 0;
        end
    `IDLE : 
    begin
          char01 = "1";
          char02 = "2";
          char11 = "3";
          char12 = "4";
          ledout = 0;
//        seg01 = 7'b0000000; 
//        seg02 = 7'b0000000; 
//        seg11 = 7'b0000000; 
//        seg12 = 7'b0000000; 
//        if ( NICKEL || DIME ) begin
//        nxtState <= `COIN;
//        end
    end
    `DELAY : begin
        #10; // 3s delay
        current <= `RESET;
    end
    `COIN : begin        
        if ( GUM ) begin
        current <= `GUM;
        end else begin
        current <= `COIN;
        end
        
        case (coin_val) 
            5: begin
                char11 = "0";
                char12 = "5";
                end 
            10: begin
                char11 = "1";
                char12 = "0";
                end 
            default: begin
                char11 = "9";
                char12 = "9";
                end
        endcase
    end
    `GUM : begin        
        if ( coin_val >= 10) begin
        current <= `VENT;
        ledout <= coin_val%10;
        
        end else begin
        current <= `COIN;
        end
    end
     `VENT : begin  
        char01 = "V";
        char02 = "E";
        char11 = "N";
        char12 = "T";      
        current <= `DELAY;

    end
    default: begin
    current <= `RESET;  end
    endcase
    end // else synchrones rst
    end // always
  
   
   always @( negedge NICKEL )
   begin
   current <= `COIN;
   if ( coin_val > 20 ) begin
       coin_val <= coin_val;
   end else begin
    coin_val <= coin_val + 5;
   end
   end
   always @( negedge DIME )
   begin
   current <= `COIN;
   if ( coin_val > 20 ) begin
       coin_val <= coin_val;
   end else begin
        coin_val <= coin_val + 10;
       end
   end // if ( coin_val >= 20 ) begin
endmodule

