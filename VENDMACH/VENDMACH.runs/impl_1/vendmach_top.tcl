proc start_step { step } {
  set stopFile ".stop.rst"
  if {[file isfile .stop.rst]} {
    puts ""
    puts "*** Halting run - EA reset detected ***"
    puts ""
    puts ""
    return -code error
  }
  set beginFile ".$step.begin.rst"
  set platform "$::tcl_platform(platform)"
  set user "$::tcl_platform(user)"
  set pid [pid]
  set host ""
  if { [string equal $platform unix] } {
    if { [info exist ::env(HOSTNAME)] } {
      set host $::env(HOSTNAME)
    }
  } else {
    if { [info exist ::env(COMPUTERNAME)] } {
      set host $::env(COMPUTERNAME)
    }
  }
  set ch [open $beginFile w]
  puts $ch "<?xml version=\"1.0\"?>"
  puts $ch "<ProcessHandle Version=\"1\" Minor=\"0\">"
  puts $ch "    <Process Command=\".planAhead.\" Owner=\"$user\" Host=\"$host\" Pid=\"$pid\">"
  puts $ch "    </Process>"
  puts $ch "</ProcessHandle>"
  close $ch
}

proc end_step { step } {
  set endFile ".$step.end.rst"
  set ch [open $endFile w]
  close $ch
}

proc step_failed { step } {
  set endFile ".$step.error.rst"
  set ch [open $endFile w]
  close $ch
}

set_msg_config -id {HDL 9-1061} -limit 100000
set_msg_config -id {HDL 9-1654} -limit 100000

start_step place_design
set ACTIVE_STEP place_design
set rc [catch {
  create_msg_db place_design.pb
  open_checkpoint vendmach_top_opt.dcp
  set_property webtalk.parent_dir C:/FPGA_EGR680/VENDMACH/VENDMACH.cache/wt [current_project]
  implement_debug_core 
  place_design 
  write_checkpoint -force vendmach_top_placed.dcp
  catch { report_io -file vendmach_top_io_placed.rpt }
  catch { report_utilization -file vendmach_top_utilization_placed.rpt -pb vendmach_top_utilization_placed.pb }
  catch { report_control_sets -verbose -file vendmach_top_control_sets_placed.rpt }
  close_msg_db -file place_design.pb
} RESULT]
if {$rc} {
  step_failed place_design
  return -code error $RESULT
} else {
  end_step place_design
  unset ACTIVE_STEP 
}

start_step route_design
set ACTIVE_STEP route_design
set rc [catch {
  create_msg_db route_design.pb
  route_design 
  write_checkpoint -force vendmach_top_routed.dcp
  catch { report_drc -file vendmach_top_drc_routed.rpt -pb vendmach_top_drc_routed.pb -rpx vendmach_top_drc_routed.rpx }
  catch { report_methodology -file vendmach_top_methodology_drc_routed.rpt -rpx vendmach_top_methodology_drc_routed.rpx }
  catch { report_power -file vendmach_top_power_routed.rpt -pb vendmach_top_power_summary_routed.pb -rpx vendmach_top_power_routed.rpx }
  catch { report_route_status -file vendmach_top_route_status.rpt -pb vendmach_top_route_status.pb }
  catch { report_clock_utilization -file vendmach_top_clock_utilization_routed.rpt }
  catch { report_timing_summary -warn_on_violation -max_paths 10 -file vendmach_top_timing_summary_routed.rpt -rpx vendmach_top_timing_summary_routed.rpx }
  close_msg_db -file route_design.pb
} RESULT]
if {$rc} {
  write_checkpoint -force vendmach_top_routed_error.dcp
  step_failed route_design
  return -code error $RESULT
} else {
  end_step route_design
  unset ACTIVE_STEP 
}

