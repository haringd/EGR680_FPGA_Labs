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
       | Idle                |               |                     |
       | Display "VENT"      |<--------------| Reset               |<------+
       |                     |               | BTN3                |       |
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
       | & coin_val > 10     |--------------------------------->|                     |
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
       
       Intel example
       --------------------------------------------------------------
       // URL: https://www.intel.com/content/www/us/en/programmable/ ...
       // support/support-resources/design-examples/design-software/verilog.html#using
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
    
    parameter p_idle=3'b000, p_delay=3'b001, p_coin=3'b010, p_gum=3'b011, p_apple=3'b100, p_yogurt=3'b101, p_vent=3'b110; 

    reg [2:0] state;  
    initial state = p_idle;
    integer coin_val = 0;
    integer delay3s = 0;
    integer modulo = 0;
    reg nickel_add = 0;
    reg dime_add = 0;
    reg bt_gum = 0;
    reg bt_apple = 0;
    reg bt_yogurt = 0;
    
    always @( state ) begin : Output
    case (state)
        p_idle : begin
            char01 <= "V";
            char02 <= "E";
            char11 <= "N";
            char12 <= "T";
            ledout <= 4'b0000; 
        end
    p_delay : begin
    end
    p_coin : begin       
        char01 <= " ";
        char02 <= " ";
        case (coin_val) 
            0: begin
                char11 <= "0";
                char12 <= "0";
                end 
            5: begin
                char11 <= "0";
                char12 <= "5";
                end 
            10: begin
                char11 <= "1";
                char12 <= "0";
                end 
            15: begin
                char11 <= "1";
                char12 <= "5";
                end 
            20: begin
                char11 <= "2";
                char12 <= "0";
                end 
            default: begin
                char11 <= "9";
                char12 <= "9";
                end
        endcase
    end
    p_gum : begin        
        char01 <= "G";
        char02 <= " ";
        modulo <= 10;      
        end
    p_apple : begin        
        char01 <= "A";
        char02 <= " ";
        modulo <= 15;       
        end
    p_yogurt : begin        
        char01 <= "Y";
        char02 <= " ";
        modulo <= 20; 
        end
    p_vent : begin  
        ledout <= coin_val % modulo;  
    end
    default: begin
//        char01 <= "D";
//        char02 <= "E";
//        char11 <= "F";
//        char12 <= "U";   
//        ledout <= 4'b1111; 
    end
    endcase
    end // always
  
   
   
     always @( posedge clk or negedge rst) begin
     //...........................
 //    nxtState = current; 
     if( rst ) begin
        state <= p_idle;
        coin_val <= 0; 
     end else begin
     case (state)
     p_idle : begin
         if( nickel_add ) state <= p_coin;
         else if ( dime_add ) state <= p_coin;
         else state <= p_idle;
         end
     p_delay : begin // 3s delay
         if (delay3s <= 375000000 ) delay3s <= delay3s +1;
         else  begin
         delay3s <= 0;
         state <= p_idle;
         end
     end
     p_coin : begin        
     
         if ( coin_val >= 20 )   coin_val <= coin_val;
         else if ( nickel_add )  coin_val <= coin_val + 5; //else if ( nickel_add )  coin_val <= coin_val + 5; NICKEL
         else if ( dime_add )    coin_val <= coin_val + 10; //else if ( dime_add )    coin_val <= coin_val + 10;
         else                    coin_val <= coin_val;

        
         if ( bt_gum ) state <= p_gum;
         else if (bt_apple ) state <= p_apple;
         else if (bt_yogurt) state <= p_yogurt;
         else  state <= p_coin;
     end
     p_gum : begin        
         if ( coin_val >= 10) state <= p_vent;         
         else state <= p_coin;
     end
     p_vent : begin     
         state <= p_delay;
     end
     default: begin
     //state <= p_idle;  
     end
     endcase
     end // else synchrones rst
end // always 
   
 reg deb1, deb2, deb3, deb4, deb5, deb6, deb7, deb8, deb9, deb10;  
 
 //   Edge detector for incoming signals
     always @( posedge clk )
       begin
       deb1 <= NICKEL;
       deb2 <= deb1;
       if (deb1 == 1 && deb2 == 0) nickel_add <= 1;
       else nickel_add <= 0;
       
       deb3 <= DIME;
       deb4 <= deb3;
       if (deb3 == 1 && deb4 == 0) dime_add <= 1;
       else dime_add <= 0;
       
       deb5 <= GUM;
       deb6 <= deb5;
       if (deb5 == 1 && deb6 == 0) bt_gum <= 1;
       else bt_gum <= 0;
       
       deb7 <= APPLE;
       deb8 <= deb7;
       if (deb7 == 1 && deb8 == 0) bt_apple <= 1;
       else bt_apple <= 0;
       
       deb9 <= YOGURT;
       deb10 <= deb9;
       if (deb9 == 1 && deb10 == 0) bt_yogurt <= 1;
       else bt_yogurt <= 0;
     end  // always

endmodule

