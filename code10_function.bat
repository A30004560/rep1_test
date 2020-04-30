  
call "C:\ProgramData\Anaconda3\Scripts\activate.bat"
call pushd "\\glawi222\data$\Data\Common\New Energy\Commercial Development\Data strategy and analytics\12 vppsa-move-and-churn-check\rep1_test\"
call activate myenv_test1
call python -m code10_function "P:/New Energy/Churn Moveout Report/Input_file/Full VPPSA Site List V3.xlsx" "P:/New Energy/Churn Moveout Report/Output_file" "javad.jazaeri@gmail.com"
call popd
