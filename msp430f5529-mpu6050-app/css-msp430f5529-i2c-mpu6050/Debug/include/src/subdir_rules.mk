################################################################################
# Automatically-generated file. Do not edit!
################################################################################

SHELL = cmd.exe

# Each subdirectory must supply rules for building sources it contributes
include/src/%.obj: ../include/src/%.c $(GEN_OPTS) | $(GEN_FILES)
	@echo 'Building file: "$<"'
	@echo 'Invoking: MSP430 Compiler'
	"C:/ti/ccs900/ccs/tools/compiler/ti-cgt-msp430_18.12.1.LTS/bin/cl430" -vmspx --data_model=restricted --use_hw_mpy=F5 --include_path="C:/ti/ccs900/ccs/ccs_base/msp430/include" --include_path="C:/Users/Rommel/Documents/Documents/Master/Compilers/Proyects/compilers-sim/msp430f5529-mpu6050-app/css-msp430f5529-i2c-mpu6050" --include_path="C:/Users/Rommel/Documents/Documents/Master/Compilers/Proyects/compilers-sim/msp430f5529-mpu6050-app/css-msp430f5529-i2c-mpu6050/include" --include_path="C:/ti/ccs900/ccs/tools/compiler/ti-cgt-msp430_18.12.1.LTS/include" --advice:power="all" --define=__MSP430F5529__ -g --printf_support=minimal --diag_warning=225 --diag_wrap=off --display_error_number --silicon_errata=CPU21 --silicon_errata=CPU22 --silicon_errata=CPU23 --silicon_errata=CPU40 --preproc_with_compile --preproc_dependency="include/src/$(basename $(<F)).d_raw" --obj_directory="include/src" $(GEN_OPTS__FLAG) "$<"
	@echo 'Finished building: "$<"'
	@echo ' '

