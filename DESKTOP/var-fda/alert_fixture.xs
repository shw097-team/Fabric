// FDA DoD-17 PAPER radar fixture (DOC-10 CH-13.05 ret/RetVal contract)
if CrossOver(Close, Average(Close, 20)) and Volume > Volume[1] then begin
    ret = 1;
    RetMsg = "FDA-PAPER-ALERT";
end;
