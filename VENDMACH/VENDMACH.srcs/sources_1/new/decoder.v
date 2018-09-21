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
     seg0 =  seg01;
     end
    
   2'b01 :  
     begin    
    cat0 <= 1'b0;
    seg0 =  seg02;
    end    
    
   2'b10 :  
      begin      
    cat1 <= 1'b1;
   seg1 =  seg11;
   end    
       
   2'b11 :  
      begin      
    cat1 <= 1'b0;
    seg1 =  seg12;
   end     
   endcase           
end
end // else rst
endmodule