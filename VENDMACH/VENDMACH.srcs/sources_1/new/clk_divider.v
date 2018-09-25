`timescale 1ns / 1ns

module clk_divider(
    input clk,
    input rst,
    input [31:0] div_val,
    output reg clk_out
    );

reg [31:0] clk_temp;

always @(posedge clk or negedge rst) begin

if (!rst) begin
    clk_temp = 0;
    clk_out = 0;
end else begin
    if (clk_temp >= div_val) begin // 500000 divide = f1 / (f2 * 2) = 125 MHz / (125 Hz * 2)
        clk_out <= ~clk_out; // no clue why this line does not toggle the clk_out
        clk_temp <= 0;
    end else begin
        clk_temp <= clk_temp + 1;
    end
end // else rst
end // always
endmodule