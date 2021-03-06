## Clock signal 125 MHz
set_property -dict { PACKAGE_PIN H16  IOSTANDARD LVCMOS33 } [get_ports { clk }];
create_clock -add -name sys_clk_pin -period 8.00 -waveform {0 4} [get_ports { clk }];

## Pmod A
set_property -dict { PACKAGE_PIN Y18  IOSTANDARD LVCMOS33 } [get_ports { seg0[0] }];
set_property -dict { PACKAGE_PIN Y19  IOSTANDARD LVCMOS33 } [get_ports { seg0[1] }];
set_property -dict { PACKAGE_PIN Y16  IOSTANDARD LVCMOS33 } [get_ports { seg0[2] }];
set_property -dict { PACKAGE_PIN Y17  IOSTANDARD LVCMOS33 } [get_ports { seg0[3] }];
set_property -dict { PACKAGE_PIN U18  IOSTANDARD LVCMOS33 } [get_ports { seg0[4] }];
set_property -dict { PACKAGE_PIN U19  IOSTANDARD LVCMOS33 } [get_ports { seg0[5] }];
set_property -dict { PACKAGE_PIN W18  IOSTANDARD LVCMOS33 } [get_ports { seg0[6] }];
set_property -dict { PACKAGE_PIN W19  IOSTANDARD LVCMOS33 } [get_ports { cat0 }];

## Pmod B
set_property -dict { PACKAGE_PIN W14  IOSTANDARD LVCMOS33 } [get_ports { seg1[0] }];
set_property -dict { PACKAGE_PIN Y14  IOSTANDARD LVCMOS33 } [get_ports { seg1[1] }];
set_property -dict { PACKAGE_PIN T11  IOSTANDARD LVCMOS33 } [get_ports { seg1[2] }];
set_property -dict { PACKAGE_PIN T10  IOSTANDARD LVCMOS33 } [get_ports { seg1[3] }];
set_property -dict { PACKAGE_PIN V16  IOSTANDARD LVCMOS33 } [get_ports { seg1[4] }];
set_property -dict { PACKAGE_PIN W16  IOSTANDARD LVCMOS33 } [get_ports { seg1[5] }];
set_property -dict { PACKAGE_PIN V12  IOSTANDARD LVCMOS33 } [get_ports { seg1[6] }];
set_property -dict { PACKAGE_PIN W13  IOSTANDARD LVCMOS33 } [get_ports { cat1 }];

## Buttons
set_property -dict { PACKAGE_PIN D19  IOSTANDARD LVCMOS33 } [get_ports { BTN0 }];
set_property -dict { PACKAGE_PIN D20  IOSTANDARD LVCMOS33 } [get_ports { BTN1 }];
set_property -dict { PACKAGE_PIN L20  IOSTANDARD LVCMOS33 } [get_ports { BTN2 }];
set_property -dict { PACKAGE_PIN L19  IOSTANDARD LVCMOS33 } [get_ports { BTN3 }];

## Switches
set_property -dict { PACKAGE_PIN M20  IOSTANDARD LVCMOS33 } [get_ports { SW0 }];
set_property -dict { PACKAGE_PIN M19  IOSTANDARD LVCMOS33 } [get_ports { SW1 }];