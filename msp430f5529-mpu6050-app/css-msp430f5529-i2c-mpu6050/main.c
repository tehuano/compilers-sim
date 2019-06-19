#include <msp430.h>
#include "mpu6050.h"


int main(void) {

    WDTCTL = WDTPW + WDTHOLD;                 // Stop WDT
    unsigned char ret;
    unsigned int temperature;
    accelerometer_t acc_t;
    gyroscope_t gyro_t;

    __bis_SR_register(GIE);

    // stablish device address
    mpu6050_set_device_address(ADDR_MPU6050);

    // read who am i register
    ret = mpu6050_read_register(WHO_AM_I);
    // test pwr mgmt reg
    ret = mpu6050_read_register(PWR_MGMT_1);
    // wake up the sensor
    mpu6050_write_register(PWR_MGMT_1, ret & ~0x40);
    // test pwr mgmt reg
    ret = mpu6050_read_register(PWR_MGMT_1);
    // temperature value
    mpu6050_read_temperature(&temperature);
    // get accelerometer data
    mpu6050_read_accelerometer(&acc_t);
    // get gyroscope data
    mpu6050_read_gyroscope(&gyro_t);
    // loop
    while (1);
}
