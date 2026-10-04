// FDA DoD-17 PAPER radar fixture (ALERT type)
// Authority: XQ&XS Gem 指南 Type B (警示腳本) + DOC-04 CrossOver function form
// ret=1 triggers; retmsg for push; NO OutputField; NO delayed-field direct calls
if CrossOver(Close, Average(Close, 20)) and Volume > Volume[1] then begin
    ret = 1;
    retmsg = "FDA-PAPER-ALERT close=" + NumToStr(Close, 2);
end;
