module time_multiplexed_top(
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

//wire clk_out;

clk_divider clk_div(clk, rst, clk_out);
decoder dec(SW0, SW1, BTN0,clk_out, rst, seg0, seg1, cat0, cat1 ); 

endmodule