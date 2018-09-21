vlib work
vlib activehdl

vlib activehdl/xil_defaultlib

vmap xil_defaultlib activehdl/xil_defaultlib

vlog -work xil_defaultlib  -v2k5 "+incdir+../../../../UART_app.srcs/sources_1/bd/system/ipshared/7e3a/hdl" "+incdir+../../../../UART_app.srcs/sources_1/bd/system/ipshared/2ad9/hdl" "+incdir+../../../../UART_app.srcs/sources_1/bd/system/ipshared/39ca/hdl/verilog" "+incdir+../../../../UART_app.srcs/sources_1/bd/system/ipshared/6eb1/hdl" "+incdir+../../../../UART_app.srcs/sources_1/bd/system/ipshared/1d61/hdl" "+incdir+../../../../UART_app.srcs/sources_1/bd/system/ipshared/7e3a/hdl" "+incdir+../../../../UART_app.srcs/sources_1/bd/system/ipshared/2ad9/hdl" "+incdir+../../../../UART_app.srcs/sources_1/bd/system/ipshared/39ca/hdl/verilog" "+incdir+../../../../UART_app.srcs/sources_1/bd/system/ipshared/6eb1/hdl" "+incdir+../../../../UART_app.srcs/sources_1/bd/system/ipshared/1d61/hdl" \
"c:/FPGA_EGR680/UART_app/UART_app.srcs/sources_1/bd/system/ip/system_processing_system7_0_0/system_processing_system7_0_0_sim_netlist.v" \
"../../../bd/system/hdl/system.v" \


vlog -work xil_defaultlib \
"glbl.v"

