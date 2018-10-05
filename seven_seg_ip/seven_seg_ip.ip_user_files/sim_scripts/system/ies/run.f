-makelib ies/xil_defaultlib -sv \
  "C:/Xilinx/Vivado/2017.2/data/ip/xpm/xpm_cdc/hdl/xpm_cdc.sv" \
  "C:/Xilinx/Vivado/2017.2/data/ip/xpm/xpm_memory/hdl/xpm_memory.sv" \
-endlib
-makelib ies/xpm \
  "C:/Xilinx/Vivado/2017.2/data/ip/xpm/xpm_VCOMP.vhd" \
-endlib
-makelib ies/xil_defaultlib \
  "../../../bd/system/ip/system_processing_system7_0_0/system_processing_system7_0_0_sim_netlist.v" \
  "../../../bd/system/ip/system_axi_gpio_0_0/system_axi_gpio_0_0_sim_netlist.v" \
  "../../../bd/system/ip/system_rst_ps7_0_100M_0/system_rst_ps7_0_100M_0_sim_netlist.v" \
  "../../../bd/system/ip/system_axi_gpio_0_1/system_axi_gpio_0_1_sim_netlist.v" \
-endlib
-makelib ies/generic_baseblocks_v2_1_0 \
  "../../../../seven_seg_ip.srcs/sources_1/bd/system/ipshared/f9c1/hdl/generic_baseblocks_v2_1_vl_rfs.v" \
-endlib
-makelib ies/axi_infrastructure_v1_1_0 \
  "../../../../seven_seg_ip.srcs/sources_1/bd/system/ipshared/7e3a/hdl/axi_infrastructure_v1_1_vl_rfs.v" \
-endlib
-makelib ies/axi_register_slice_v2_1_13 \
  "../../../../seven_seg_ip.srcs/sources_1/bd/system/ipshared/55c0/hdl/axi_register_slice_v2_1_vl_rfs.v" \
-endlib
-makelib ies/fifo_generator_v13_1_4 \
  "../../../../seven_seg_ip.srcs/sources_1/bd/system/ipshared/ebc2/simulation/fifo_generator_vlog_beh.v" \
-endlib
-makelib ies/fifo_generator_v13_1_4 \
  "../../../../seven_seg_ip.srcs/sources_1/bd/system/ipshared/ebc2/hdl/fifo_generator_v13_1_rfs.vhd" \
-endlib
-makelib ies/fifo_generator_v13_1_4 \
  "../../../../seven_seg_ip.srcs/sources_1/bd/system/ipshared/ebc2/hdl/fifo_generator_v13_1_rfs.v" \
-endlib
-makelib ies/axi_data_fifo_v2_1_12 \
  "../../../../seven_seg_ip.srcs/sources_1/bd/system/ipshared/95b9/hdl/axi_data_fifo_v2_1_vl_rfs.v" \
-endlib
-makelib ies/axi_crossbar_v2_1_14 \
  "../../../../seven_seg_ip.srcs/sources_1/bd/system/ipshared/f582/hdl/axi_crossbar_v2_1_vl_rfs.v" \
-endlib
-makelib ies/xil_defaultlib \
  "../../../bd/system/ip/system_xbar_0/sim/system_xbar_0.v" \
  "../../../bd/system/hdl/system.v" \
  "../../../bd/system/ipshared/29f7/src/clk_divider.v" \
  "../../../bd/system/ipshared/29f7/src/decoder.v" \
  "../../../bd/system/ipshared/29f7/hdl/seven_seg_ip_v1_0_S_AXI.v" \
  "../../../bd/system/ipshared/29f7/hdl/user_logic.v" \
  "../../../bd/system/ipshared/29f7/hdl/seven_seg_ip_v1_0.v" \
  "../../../bd/system/ip/system_seven_seg_ip_0_0/sim/system_seven_seg_ip_0_0.v" \
  "../../../bd/system/ipshared/90e0/hdl/led_ip_v1_0_S_AXI.v" \
  "../../../bd/system/ipshared/90e0/hdl/user_logic.v" \
  "../../../bd/system/ipshared/90e0/hdl/led_ip_v1_0.v" \
  "../../../bd/system/ip/system_led_ip_0_0/sim/system_led_ip_0_0.v" \
  "../../../bd/system/ip/system_axi_bram_ctrl_0_0/system_axi_bram_ctrl_0_0_sim_netlist.v" \
  "../../../bd/system/ip/system_blk_mem_gen_0_0/system_blk_mem_gen_0_0_sim_netlist.v" \
-endlib
-makelib ies/axi_protocol_converter_v2_1_13 \
  "../../../../seven_seg_ip.srcs/sources_1/bd/system/ipshared/f0ae/hdl/axi_protocol_converter_v2_1_vl_rfs.v" \
-endlib
-makelib ies/xil_defaultlib \
  "../../../bd/system/ip/system_auto_pc_3/sim/system_auto_pc_3.v" \
  "../../../bd/system/ip/system_auto_pc_2/sim/system_auto_pc_2.v" \
  "../../../bd/system/ip/system_auto_pc_1/sim/system_auto_pc_1.v" \
  "../../../bd/system/ip/system_auto_pc_0/sim/system_auto_pc_0.v" \
  "../../../bd/system/ip/system_auto_pc_4/sim/system_auto_pc_4.v" \
-endlib
-makelib ies/xil_defaultlib \
  glbl.v
-endlib

