module clk_divider(
    input clk,
    input rst,
    output clk_out
    );

reg [31:0] clk_temp;
reg clk_out;

always @(posedge clk or negedge rst)
begin

if (rst)
begin
  clk_temp = 0;
  clk_out = 0;
end
else
begin
    
   clk_temp <= clk_temp + 1;
   if (clk_temp >= 500000) 
   begin
   clk_out <= ~clk_out;
   clk_temp <= 0;
   end
end // else rst
   clk_out <= clk_out;
end // always
endmodule