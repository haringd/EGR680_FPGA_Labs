# 
# Synthesis run script generated by Vivado
# 

set_msg_config -id {Common 17-41} -limit 10000000
set_msg_config -id {HDL 9-1061} -limit 100000
set_msg_config -id {HDL 9-1654} -limit 100000
set_msg_config  -ruleid {1}  -id {Synth 8-1717}  -string {{ERROR: [Synth 8-1717] cannot access memory seg directly [C:/FPGA_EGR680/VENDMACH/VENDMACH.srcs/sources_1/new/vendmach_top.v:21]}}  -suppress 
create_project -in_memory -part xc7z020clg400-1

set_param project.singleFileAddWarning.threshold 0
set_param project.compositeFile.enableAutoGeneration 0
set_param synth.vivado.isSynthRun true
set_property webtalk.parent_dir C:/FPGA_EGR680/VENDMACH/VENDMACH.cache/wt [current_project]
set_property parent.project_path C:/FPGA_EGR680/VENDMACH/VENDMACH.xpr [current_project]
set_property default_lib xil_defaultlib [current_project]
set_property target_language Verilog [current_project]
set_property ip_output_repo c:/FPGA_EGR680/VENDMACH/VENDMACH.cache/ip [current_project]
set_property ip_cache_permissions {read write} [current_project]
read_verilog -library xil_defaultlib {
  C:/FPGA_EGR680/VENDMACH/VENDMACH.srcs/sources_1/new/ascii2seg.v
  C:/FPGA_EGR680/VENDMACH/VENDMACH.srcs/sources_1/new/clk_divider.v
  C:/FPGA_EGR680/VENDMACH/VENDMACH.srcs/sources_1/new/decoder.v
  C:/FPGA_EGR680/VENDMACH/VENDMACH.srcs/sources_1/new/state_machine.v
  C:/FPGA_EGR680/VENDMACH/VENDMACH.srcs/sources_1/new/vendmach_top.v
}
# Mark all dcp files as not used in implementation to prevent them from being
# stitched into the results of this synthesis run. Any black boxes in the
# design are intentionally left as such for best results. Dcp files will be
# stitched into the design at a later time, either when this synthesis run is
# opened, or when it is stitched into a dependent implementation run.
foreach dcp [get_files -quiet -all -filter file_type=="Design\ Checkpoint"] {
  set_property used_in_implementation false $dcp
}
read_xdc C:/FPGA_EGR680/VENDMACH/VENDMACH.srcs/constrs_1/new/vendmach_pins.xdc
set_property used_in_implementation false [get_files C:/FPGA_EGR680/VENDMACH/VENDMACH.srcs/constrs_1/new/vendmach_pins.xdc]


synth_design -top vendmach_top -part xc7z020clg400-1


write_checkpoint -force -noxdef vendmach_top.dcp

catch { report_utilization -file vendmach_top_utilization_synth.rpt -pb vendmach_top_utilization_synth.pb }
