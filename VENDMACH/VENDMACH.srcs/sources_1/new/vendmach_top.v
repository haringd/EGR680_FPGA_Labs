`timescale 1ns / 1ns
module vendmach_top(
    input NICKEL,
    input DIME,
    input GUM,
    input APPLE,
    input YOGURT,
    input rst,
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
wire outNICKEL, outDIME, outGUM, outAPPLE, outYOGURT, clk_deb;


//    clk_divider clk_deb1(clk, !rst, 1, clk_deb); // used for testbench only
    clk_divider clk_deb1( clk,    !rst,     500000, clk_deb);
    debounce debNICKLE (  NICKEL, clk_deb, !rst, outNICKEL );
    debounce debDIME   (  DIME,   clk_deb, !rst, outDIME );
    debounce debGUM    (  GUM,    clk_deb, !rst, outGUM );
    debounce debAPPLE  (  APPLE,  clk_deb, !rst, outAPPLE );
    debounce debYOGURT (  YOGURT, clk_deb, !rst, outYOGURT );
    clk_divider clk_div1(clk, !rst, 50000, clk_seg); 
//    clk_divider clk_div1(clk, !rst, 1, clk_seg); // used for testbench only
    ascii2seg aseg01(clk, !rst, char01, seg01);
    ascii2seg aseg02(clk, !rst, char02, seg02);
    ascii2seg aseg11(clk, !rst, char11, seg11);
    ascii2seg aseg12(clk, !rst, char12, seg12);
    decoder dec(seg01, seg02, seg11, seg12, clk_seg, !rst,  seg0, seg1, cat0, cat1);
    state_machine sm(clk, !rst, outDIME, outNICKEL, outGUM, outAPPLE, outYOGURT, char01, char02, char11, char12, CHANGE);
      
endmodule