function [procent1, msqe1, procent2, msqe2] = call_script(M , frek, th)
[procent1, msqe1] = lms_vss_mult(M, frek, th)
[procent2, msqe2] = lms_romer_mult(M, frek, th)
end