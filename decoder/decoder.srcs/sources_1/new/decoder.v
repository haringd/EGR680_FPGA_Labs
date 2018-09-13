`timescale 1ns / 1ns
//////////////////////////////////////////////////////////////////////////////////
// Company: 
// Engineer: 
// 
// Create Date: 12.09.2018 19:31:54
// Design Name: 
// Module Name: decoder
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


module decoder(
    input SW0,
    input SW1,
    input BTN0,
    input clk,
    input rst,
    output [6:0] seg,
    output digit
    );

reg [6:0] seg;
reg digit;

always @(posedge clk or posedge rst)
begin
    if(rst)
    begin
        seg <= 7'b0000000;
        digit <= 1'b1;  // Digit = 1 (7-segment OFF Digit= 0 (7-segment ON)
    end
    else
    begin
    // my code or from webpage http://verilogcodes.blogspot.com/2015/10/verilog-code-for-bcd-to-7-segment.html
    digit = ~BTN0;
        if (BTN0 == 1) begin
             case ({SW1, SW0}) //case statement
                2'b00 : seg =  7'b0111111; //~7'b0000001;
                2'b01 : seg =  7'b0000110;
                2'b10 : seg =  7'b1011011;
                2'b11 : seg =  7'b1001111;
                4 : seg = ~7'b1001100;
                5 : seg = ~7'b0100100;
                6 : seg = ~7'b0100000;
                7 : seg = ~7'b0001111;
                8 : seg = ~7'b0000000;
                9 : seg = ~7'b0000100;
                //switch off 7 segment character when the bcd digit is not a decimal number.
                default : seg = 7'b0000000; 
            endcase
        end
        else begin
        seg = 7'b0000000; 
        end  
    end
end
endmodule
