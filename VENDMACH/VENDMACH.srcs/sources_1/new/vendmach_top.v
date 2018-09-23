`timescale 1ns / 1ns
module vendmach_top(
    input NICKEL,
    input DIME,
    input GUM,
    input APPLE,
    input YOGURT,
    input RESET,
    input clk,
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
wire [7:0] char01;
wire [7:0] char02;
wire [7:0] char11;
wire [7:0] char12;

    clk_divider clk_div1(clk, RESET, 500000, clk_seg);
    ascii2seg aseg01(clk, RESET, char01, seg01);
    ascii2seg aseg02(clk, RESET, char02, seg02);
    ascii2seg aseg11(clk, RESET, char11, seg11);
    ascii2seg aseg12(clk, RESET, char12, seg12);
    decoder dec(seg01, seg02, seg11, seg12, RESET, clk_seg, seg0, seg1, cat0, cat1);
    state_machine sm(clk, RESET, DIME, NICKEL, GUM, APPLE, YOGURT, char01, char02, char11, char12, CHANGE);
      
endmodule