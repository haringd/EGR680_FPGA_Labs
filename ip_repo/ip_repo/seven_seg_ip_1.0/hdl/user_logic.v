`timescale 1ns / 1ps
//////////////////////////////////////////////////////////////////////////////////
// Company: 
// Engineer: 
// 
// Create Date: 04.10.2018 15:08:18
// Design Name: 
// Module Name: user_logic
// Project Name: 
// Target Devices: 
// Tool Versions: 
// Description: 
// 
// Dependencies: 
// 
// Revision:
// Revision 0.01 - File Created
// Additional Comments:
// 
//////////////////////////////////////////////////////////////////////////////////


module user_logic # (
    parameter SEVEN_SEG_WIDTH = 7 
        )
    (
    input S_AXI_ACLK,
    input slv_reg_wren,
    input [2:0] axi_awaddr,
    input [31:0] S_AXI_WDATA,
    input S_AXI_ARESETN,
    output wire [SEVEN_SEG_WIDTH-1:0] SEG,
    output wire CAT
    );
          
    reg [7:0] value;
    reg cat;
    
    always @( posedge S_AXI_ACLK )
    begin
        if ( S_AXI_ARESETN == 1'b0 )
        begin
            value <= 7'b0;
            cat <= 1'b0;
            end
        else
        if (slv_reg_wren && (axi_awaddr == 3'h0))
//            SEG <= S_AXI_WDATA[SEVEN_SEG_WIDTH-1:0];
//            CAT <= S_AXI_WDATA[8];

            value <= S_AXI_WDATA[2-1:0];
            cat <= S_AXI_WDATA[8];
        end
        
//        input clk,
//        input rst,
//        input [31:0] div_val,
//        output reg clk_out
        clk_divider clk_slow(.clk(S_AXI_ACLK), .rst(S_AXI_ARESETN), .div_val(50000), .clk_out(clk_out));
//        input SW0,
//        input SW1,
//        input BTN0,
//        input BTN1,
//        input BTN2,
//        input BTN3, 
//        input clk,
//        output [6:0] seg0,
//        output [6:0] seg1,
//        output cat0,
//        output cat1
        decoder dec1(.SW0(S_AXI_WDATA[0]), .SW1(S_AXI_WDATA[1]), .BTN0(cat), .BTN1(!cat), .BTN2(0), .BTN3(0), .clk(clk_out), .seg0(SEG), .cat0(CAT));


endmodule
