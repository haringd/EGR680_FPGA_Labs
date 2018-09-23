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
       
       statem.v
       
       module statem(clk, in, reset, out);
       
       input clk, in, reset;
       output [3:0] out;
       
       reg [3:0] out;
       reg [1:0] state;
       
       parameter zero=0, one=1, two=2, three=3;
       
       always @(state) 
            begin
                 case (state)
                      zero:
                           out = 4'b0000;
                      one:
                           out = 4'b0001;
                      two:
                           out = 4'b0010;
                      three:
                           out = 4'b0100;
                      default:
                           out = 4'b0000;
                 endcase
            end
       
       always @(posedge clk or posedge reset)
            begin
                 if (reset)
                      state = zero;
                 else
                      case (state)
                           zero:
                                state = one;
                           one:
                                if (in)
                                     state = zero;
                                else
                                     state = two;
                           two:
                                state = three;
                           three:
                                state = zero;
                      endcase
            end
       
       endmodule                 
*********************************************************************************/

//`define RESET   4'b0000 // 0
//`define IDLE    4'b0001 // 1
//`define DELAY   4'b0010 // 2
//`define COIN    4'b0011 // 3
//`define GUM     4'b0100 // 4
//`define APPLE   4'b0101 // 5
//`define YOGURT  4'b0110 // 6
//`define VENT    4'b0111 // 7

module state_machine(
    input clk,
    input rst,
    input DIME,
    input NICKEL,
    input GUM,
    input APPLE,
    input YOGURT,
    output reg [7:0] char01, 
    output reg [7:0] char02, 
    output reg [7:0] char11, 
    output reg [7:0] char12,
    output reg [3:0] ledout
    );
    parameter p_idle=0, p_delay=1, p_coin=2, p_gum=3, p_apple=4, p_yogurt=5, p_vent=6; 
    // parameter could be used instead of `define
        
    reg [2:0] state = 3'b000;
    //reg [2:0] nextState = 3'b001;
//    reg [2:0] coin_val;
   // integer coin_val;
    integer coin_val = 0;
    reg nickel_add=0;
    reg dime_add=0;
    
    always @( state ) begin
    case (state)
        p_idle : begin
            char01 = " ";
            char02 = " ";
            char11 = " ";
            char12 = " ";
            ledout = 0;
        end
    p_delay : begin
        #10; // 3s delay
    end
    p_coin : begin      

        
        case (coin_val) 
            0: begin
                char11 = "0";
                char12 = "0";
                end 
            5: begin
                char11 = "0";
                char12 = "5";
                end 
            10: begin
                char11 = "1";
                char12 = "0";
                end 
            15: begin
                char11 = "1";
                char12 = "5";
                end 
            20: begin
                char11 = "2";
                char12 = "0";
                end 
            default: begin
                char11 = "9";
                char12 = "9";
                end
        endcase
    end
    p_gum : begin        
        char01 = "G";
        char02 = " ";
        ledout <= coin_val%10;
        end
    p_vent : begin  
        char01 = "V";
        char02 = "E";
        char11 = "N";
        char12 = "T";      
    end
    default: begin
        char01 = "D";
        char02 = "E";
        char11 = "F";
        char12 = "U";   
        ledout = 8; 
    end
    endcase
    end // always
  
   
   
     always @( posedge clk or negedge rst) begin
     //...........................
 //    nxtState = current; 
     if( rst ) state <= p_idle;
     else begin
     case (state)
     p_idle : begin
//         if(nickel_add) state <= p_coin;
//         else if ( dime_add ) state <= p_coin;
//         else state <= p_idle;
          coin_val <= 0;
          state <= p_coin;
         end
     p_delay : begin
         //#10; // 3s delay
         
         state <= p_idle;
     end
     p_coin : begin        
        if ( nickel_add )       coin_val <= coin_val + 5;
        else if ( dime_add )    coin_val <= coin_val + 10;
        else                    coin_val <= coin_val + 0;
     
         if ( GUM ) state <= p_gum;
         else if (APPLE) state <= p_apple;
         else if (YOGURT) state <= p_yogurt;
         else  state <= p_coin;
     end
     p_gum : begin        
         if ( coin_val >= 10) state <= p_vent;        
         else state <= p_gum;
     end
     p_vent : begin     
         state <= p_delay;
     end
     default: begin
     state <= p_idle;  end
     endcase
     end // else synchrones rst
     end // always 
   
 reg deb1, deb2, deb3, deb4;  
   // counter or shift reg to debounce
//     always @( negedge NICKEL )
//     begin
//         if (state==p_idle || state == p_coin) nickel_add = 1;
//         else nickel_add = 0;
//     end 
     always @( posedge clk )
       begin
       deb1 <= NICKEL;
       deb2 <= deb1;
       if (deb1 == 1 && deb2 == 0) nickel_add = 1;
       else nickel_add = 0;
       
       deb3 <= DIME;
       deb4 <= deb3;
       if (deb3 == 1 && deb4 == 0) dime_add = 1;
       else dime_add = 0;
       end 
//     always @( negedge DIME )
//     begin
//         if (state==p_idle || state == p_coin) dime_add = 1;
//         else dime_add = 0;
//     end    
   
//   always @( negedge NICKEL )
//   begin
//   nextState <= p_gum;
//   if ( coin_val >= 20 ) begin
//       //coin_val <= coin_val;
//   end else begin
//     nickel_add = 1;
//   end
//   end
   
//   always @( negedge DIME )
//   begin
//   nextState <= p_gum;
//   if ( coin_val >= 20 ) begin
//      // coin_val <= coin_val;
//   end else begin
//        coin_val <= coin_val + 10;
//        dime_add = 1;
//       end
//   end // if ( coin_val >= 20 ) begin


endmodule

