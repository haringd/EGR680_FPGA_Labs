module decoder(
    input SW0,
    input SW1,
    input BTN0,
    input clk,
    input rst, // BTN3
    output [6:0] seg0,
    output [6:0] seg1,
    output cat0,
    output cat1
    );

reg [6:0] seg0;
reg [6:0] seg1;
reg cat0;
reg cat1;
reg [1:0] shift = 2'b00;

always @(posedge clk or negedge rst)
begin

if (rst)
begin
  seg0 = 7'b0000000;
  seg1 = 7'b0000000;
  shift = 2'b00;
end
else
begin

shift = shift + 1;

case (shift)
   2'b00 :  
   begin
     cat0 <= 1'b1;
     case ({SW1, SW0, BTN0}) //case statement
     3'b000 : seg0 =  7'b0000000;//  OFF 
     3'b001 : seg0 =  7'b1110011;// (P)YNQ
     3'b011 : seg0 =  7'b1110001;// FPGA
     3'b101 : seg0 =  7'b0000000;//  IS
     3'b111 : seg0 =  7'b0111001;// COOL
     default : 
     begin
       seg0 = 7'b0000000;
       seg1 = 7'b0000000;
       end
     endcase
     end
    
   2'b01 :  
     begin    
    cat0 <= 1'b0;
    case ({SW1, SW0, BTN0}) //case statement
    3'b000 : seg0 =  7'b0000000;//  OFF 
    3'b001 : seg0 =  7'b1110010;// P(Y)NQ
    3'b011 : seg0 =  7'b1110011;// FPGA
    3'b101 : seg0 =  7'b0000110;//  IS
    3'b111 : seg0 =  7'b0111111;// COOL
        default : 
    begin
      seg0 = 7'b0000000;
      seg1 = 7'b0000000;
      end
    endcase
    end    
    
   2'b10 :  
      begin      
    cat1 <= 1'b1;
    case ({SW1, SW0, BTN0}) //case statement
    3'b000 : seg1 =  7'b0000000;//  OFF 
    3'b001 : seg1 =  7'b0110111;// P(Y)NQ
    3'b011 : seg1 =  7'b1111101;// FPGA
    3'b101 : seg1 =  7'b1101101;//  IS
    3'b111 : seg1 =  7'b0111111;// COOL
    default : 
    begin
      seg0 = 7'b0000000;
      seg1 = 7'b0000000;
      end    
    endcase
   end    
       
   2'b11 :  
      begin      
    cat1 <= 1'b0;
    case ({SW1, SW0, BTN0}) //case statement
    3'b000 : seg1 =  7'b0000000;//  OFF 
    3'b001 : seg1 =  7'b1100111;// P(Y)NQ
    3'b011 : seg1 =  7'b1110111;// FPGA
    3'b101 : seg1 =  7'b0000000;//  IS
    3'b111 : seg1 =  7'b0111000;// COOL
    default : 
    begin
      seg0 = 7'b0000000;
      seg1 = 7'b0000000;
      end
    endcase
   end     
   endcase           
end
end // else rst
endmodule