module clk_divider(
    input clk,
    input rst,
    input div_val,
    output reg clk_out
    );

reg [31:0] clk_temp;

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
   if (clk_temp >= div_val) // 500000 divide = f1 / (f2 * 2) = 125 MHz / (125 Hz * 2)
   begin
   clk_out <= ~clk_out; // no clue why this line does not toggle the clk_out
   clk_temp <= 0;
   end
end // else rst
end // always
endmodule