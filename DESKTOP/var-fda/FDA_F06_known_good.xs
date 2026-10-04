// FDA F06 known-good indicator fixture
// Source: XQ&XS 專業技術文檔 DOC-03 CH-02.2 SOURCE-DERIVED_XSCRIPT (authority syntax)
// NOT_RUNTIME_VERIFIED marker retained per DOC-03; compile is the verification step.
Input: length(20);
Variable: ma(0);

ma = Average(Close, length);
if Close CrossOver ma then
    Plot1(ma);
