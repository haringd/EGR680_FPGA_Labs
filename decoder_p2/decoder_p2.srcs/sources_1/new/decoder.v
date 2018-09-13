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
    // my code
    digit = ~BTN0;
        if (BTN0 == 1) begin
             case ({SW1, SW0}) //case statement
                2'b00 : seg =  7'b0111111; //~7'b0000001;
                2'b01 : seg =  7'b0000110;
                2'b10 : seg =  7'b1011011;
                2'b11 : seg =  7'b1001111;
                default : seg = 7'b0000000; 
            endcase
        end
        else begin
        seg = 7'b0000000; 
        end  
    end
end
endmodule