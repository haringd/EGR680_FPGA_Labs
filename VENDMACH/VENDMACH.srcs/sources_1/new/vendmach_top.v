module vendmach_top(
    input NICKEL,
    input DIME,
    input GUM,
    input APPLE,
    input YOGURT,
    input RESET,
    input CLOCK,
    output [6:0] seg0,
    output [6:0] seg1, // ? Pmod B
    output cat0,
    output cat1,
    output [3:0] CHANGE
    );

wire clk_seg;
wire [6:0] seg01;
wire [6:0] seg02;
wire [6:0] seg11;
wire [6:0] seg12;

    clk_divider clk_div1(CLOCK, RESET, 500000, clk_seg);
    decoder dec(seg01, seg02, seg11, seg12, RESET, clk_seg, seg0, seg1, cat0, cat1);
    state_machine sm(CLOCK, RESET, DIME, NICKEL, GUM, seg01, seg02, seg11, seg12, CHANGE);
    
    
endmodule