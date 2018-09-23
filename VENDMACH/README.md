# Vending Machine Lab 03 State Machine in Verilog
This lab is very long not because te content is complex, but Vivado 
shwows a lot of errors and warnings which takes forever to solve. Here 
is a list of use full links to some of the errors. The links are ordered 
according to the evility.

[https://wiki.nus.edu.sg/pages/viewpage.action?pageId=167808307]( [Place 
30-574] Poor placement for routing between an I/O pin and BUFG)

[https://forums.xilinx.com/t5/Implementation/ERROR-Common-17-69-Command-failed-Placer-could-not-place-all/td-p/595398]( ERROR: 
[Common 17-69] Command failed: Placer could not place all instances)

[https://www.xilinx.com/support/answers/64452.html]( Vivado 
Implementation - Error:[Place 30-574] Poor placement for routing 
between an I/O pin and BUFG)

[https://electronics.stackexchange.com/questions/26502/verilog-check-for-two-negedges-in-always-block](Verilog: 
Check for two negedges in always block
)

[https://www.intel.com/content/www/us/en/programmable/support/support-resources/design-examples/design-software/verilog/ver_statem.html](Intel, 
Verilog HDL: Synchronous State Machine)

[https://forums.xilinx.com/t5/Implementation/Rule-Violation-mutiple-driver-nets/td-p/723687](Rule 
Violation mutiple driver nets
)

[https://forums.xilinx.com/t5/7-Series-FPGAs/ERROR-Place-30-574-Sub-optimal-placement/td-p/344741/page/2](ERROR: 
[Place 30-574] 
Sub-optimal placement)

[https://forums.xilinx.com/t5/7-Series-FPGAs/Place-30-99-Errors-in-Place-Design/td-p/339013](Place 
30-99 Errors in Place Design)

[https://stackoverflow.com/questions/10005411/assign-a-synthesizable-initial-value-to-a-reg-in-verilog](Assign 
a synthesizable initial value to a reg in Verilog)

Now it seems this clock placment error that occures by implementing the 
project is somewhat related to the decoder. As the decoder module is 
commented out of the top level block the error is not there any more. 
Still the source or what pin shall causing the issue could not be 
lockated and was not found in one of many logs that are generated.
