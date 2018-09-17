module clk_divider(
    input clk,
    input rst,
    output clk_out
    );

reg [31:0] clk_temp;
reg clk_out;

always @(posedge clk or negedge rst)
begin

if (rst==1)
begin
  clk_temp = 0;
  clk_out = 0;
end
else
begin
    
   clk_temp <= clk_temp + 1;
   if (clk_temp >= 500000) 
   //if (clk_temp >= 2) // Used for testbench
   begin
   clk_out <= ~clk_out; // no clue why this line does not toggle the clk_out
   if (clk_out == 0) 
   begin
   clk_out=1;
   end 
   else
   begin
   clk_out=0;
   end
   clk_temp <= 0;
   end
end // else rst
   clk_out <= clk_out;
end // always
endmodule