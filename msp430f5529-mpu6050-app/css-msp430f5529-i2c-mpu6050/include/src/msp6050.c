/*
 * msp6050.c
 *
 *  Created on: 17 Jun 2019
 *      Author: disorder
 */

#include "mpu6050.h"
#include "i2c_msp430f5529.h"

static unsigned char tx_buffer[8];
static unsigned char rx_buffer[8];

static unsigned char device_addr = 0;

void mpu6050_set_device_address(unsigned char addr) {
    device_addr = addr;
}

unsigned char mpu6050_read_register(unsigned char reg_addr) {
    tx_buffer[0] = reg_addr;
    master_transmitter_mode_init(device_addr);
    while (i2c_notready());
    transmit_data(1,tx_buffer);
    while (i2c_notready());
    master_receiver_mode_init(device_addr);
    while (i2c_notready());
    receive_data(1,rx_buffer);
    while (i2c_notready());
    return rx_buffer[0];
}

void mpu6050_write_register(unsigned char addr, unsigned char data) {
    // write pwr mgmt reg
    tx_buffer[0] = addr;
    tx_buffer[1] = data;
    master_transmitter_mode_init(device_addr);
    while (i2c_notready());
    transmit_data(2,tx_buffer);
    while (i2c_notready());
}

void mpu6050_read_temperature(unsigned int *temperature) {
    unsigned int rh = 0, rl = 0;
    rh = mpu6050_read_register(TEMP_OUT_H);
    rl = mpu6050_read_register(TEMP_OUT_L);
    *temperature = ((rh << REG_SIZE) | rl);
}

void mpu6050_read_accelerometer(accelerometer_t *acc) {
    unsigned int rh = 0, rl = 0;
    rh = mpu6050_read_register(ACCEL_XOUT_H);
    rl = mpu6050_read_register(ACCEL_XOUT_L);
    acc->xout = ((rh << REG_SIZE) | rl);
    rh = mpu6050_read_register(ACCEL_YOUT_H);
    rl = mpu6050_read_register(ACCEL_YOUT_L);
    acc->yout = ((rh << REG_SIZE) | rl);
    rh = mpu6050_read_register(ACCEL_ZOUT_H);
    rl = mpu6050_read_register(ACCEL_ZOUT_L);
    acc->zout = ((rh << REG_SIZE) | rl);
}

void mpu6050_read_gyroscope(gyroscope_t *acc) {
    unsigned int rh = 0, rl = 0;
    rh = mpu6050_read_register(GYRO_XOUT_H);
    rl = mpu6050_read_register(GYRO_XOUT_L);
    acc->xout = ((rh << REG_SIZE) | rl);
    rh = mpu6050_read_register(GYRO_YOUT_H);
    rl = mpu6050_read_register(GYRO_YOUT_L);
    acc->yout = ((rh << REG_SIZE) | rl);
    rh = mpu6050_read_register(GYRO_ZOUT_H);
    rl = mpu6050_read_register(GYRO_ZOUT_L);
    acc->zout = ((rh << REG_SIZE) | rl);
}
