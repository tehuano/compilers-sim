#include <msp430.h>
#include "mpu6050.h"
#include "uart_msp430f5529.h"

int main(void) {
    WDTCTL = WDTPW + WDTHOLD;                 // Stop WDT
    unsigned char ret;
    unsigned char counter = 0;
    unsigned int temperature;
    accelerometer_t acc_t;
    gyroscope_t gyro_t;

    __bis_SR_register(GIE);

    mpu6050_init();
    uart_init();

    while (1) {
       // get information from the sensor
       // temperature value
       mpu6050_read_temperature(&temperature);
       // get accelerometer data
       mpu6050_read_accelerometer(&acc_t);
       // get gyroscope data
       mpu6050_read_gyroscope(&gyro_t);
       // send information by using uart
       uart_handshake();
       // send temperature info
       uart_send_byte(UINT_H(temperature));
       uart_send_byte(UINT_L(temperature));
       // send accelerometer info
       uart_send_byte(UINT_H(acc_t.xout));
       uart_send_byte(UINT_L(acc_t.xout));
       uart_send_byte(UINT_H(acc_t.yout));
       uart_send_byte(UINT_L(acc_t.yout));
       uart_send_byte(UINT_H(acc_t.zout));
       uart_send_byte(UINT_L(acc_t.zout));
       // send gyroscope info
       uart_send_byte(UINT_H(gyro_t.xout));
       uart_send_byte(UINT_L(gyro_t.xout));
       uart_send_byte(UINT_H(gyro_t.yout));
       uart_send_byte(UINT_L(gyro_t.yout));
       uart_send_byte(UINT_H(gyro_t.zout));
       uart_send_byte(UINT_L(gyro_t.zout));
    }
}
