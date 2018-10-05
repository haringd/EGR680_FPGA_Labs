module decoder(
    input SW0,
    input SW1,
    input BTN0,
    input BTN1,
    input BTN2,
    input BTN3, 
    input clk,
    output [6:0] seg0,
    output [6:0] seg1,
    output cat0,
    output cat1
    //output digit
    );

reg [6:0] seg0;
reg [6:0] seg1;
reg cat0;
reg cat1;

always @(posedge clk )
begin
case({BTN3,BTN2,BTN1,BTN0})
 4'b0000:
 begin
 seg0 = 7'b0000000;
 seg1 = 7'b0000000;
 end
 /*------------------------------------------------*/
 4'b0001:
        begin
        cat0 <= 1'b0;
             case ({SW1, SW0}) //case statement
               
             2'b00 : seg0 =  7'b0111111;//0
             2'b01 : seg0 =  7'b0000110;//1
             2'b10 : seg0 =  7'b1011011;//2
             2'b11 : seg0 =  7'b1001111;//3
            endcase
        end
4'b0010:
        begin
        cat0 <= 1'b1;
             case ({SW1, SW0}) //case statement
               
             2'b00 : seg0 =  7'b0111111;//0
             2'b01 : seg0 =  7'b0000110;//1
             2'b10 : seg0 =  7'b1011011;//2
             2'b11 : seg0 =  7'b1001111;//3
            endcase
        end
 4'b0100:
         begin
         cat1 <= 1'b0;
              case ({SW1, SW0}) //case statement
                
              2'b00 : seg1 =  7'b0111111;//0
              2'b01 : seg1 =  7'b0000110;//1
              2'b10 : seg1 =  7'b1011011;//2
              2'b11 : seg1 =  7'b1001111;//3
             endcase
         end
  4'b1000:
          begin
          cat1 <= 1'b1;
               case ({SW1, SW0}) //case statement
                 
                   2'b00 : seg1 =  7'b0111111;//0
                   2'b01 : seg1 =  7'b0000110;//1
                   2'b10 : seg1 =  7'b1011011;//2
                   2'b11 : seg1 =  7'b1001111;//3
              endcase
          end
  default : 
  begin
  seg0 = 7'b0000000;
  seg1 = 7'b0000000;
  end
  
  endcase
end
endmodule