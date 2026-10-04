{@type:sensor}
// FDA DoD-17 PAPER radar fixture — parameterized trigger probe
// Authority: XQ&XS 官方語法 (Input/SetInputName) + xq_alert.py contract
Input: Trigger(1);
SetInputName(1, "1觸發，0不觸發");
if Trigger = 1 then ret = 1;
