@echo off
set xv_path=C:\\Xilinx\\Vivado\\2017.2\\bin
call %xv_path%/xsim counter_tb_behav -key {Behavioral:sim_1:Functional:counter_tb} -tclbatch counter_tb.tcl -view C:/FPGA_EGR680/counter_verilog/counter_tb_behav.wcfg -log simulate.log
if "%errorlevel%"=="0" goto SUCCESS
if "%errorlevel%"=="1" goto END
:END
exit 1
:SUCCESS
exit 0
