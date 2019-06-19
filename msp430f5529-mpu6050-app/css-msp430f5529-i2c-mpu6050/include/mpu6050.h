/*
 * mpu6050.h
 *
 *  Created on: 17 Jun 2019
 *      Author: disorder
 */

#ifndef INCLUDE_MPU6050_H_
#define INCLUDE_MPU6050_H_

#define ACCEL_BASE_ADDR 0x3B
#define ACCEL_XOUT_H  0x3B
#define ACCEL_XOUT_L  0x3C
#define ACCEL_YOUT_H  0x3D
#define ACCEL_YOUT_L  0x3E
#define ACCEL_ZOUT_H  0x3F
#define ACCEL_ZOUT_L  0x40

#define TEMP_BASE_ADDR 0x41
#define TEMP_OUT_H   0x41
#define TEMP_OUT_L   0x42

#define GYRO_BASE_ADDR 0x43
#define GYRO_XOUT_H 0x43
#define GYRO_XOUT_L 0x44
#define GYRO_YOUT_H 0x45
#define GYRO_YOUT_L 0x46
#define GYRO_ZOUT_H 0x47
#define GYRO_ZOUT_L 0x48


#define WHO_AM_I     0x75
#define PWR_MGMT_1   0x6B
#define ADDR_MPU6050 0b01101000

#define REG_SIZE 8

typedef struct {
    unsigned int xout;
    unsigned int yout;
    unsigned int zout;
} accelerometer_t;

typedef struct {
    unsigned int xout;
    unsigned int yout;
    unsigned int zout;
} gyroscope_t;

void mpu6050_set_device_address(unsigned char);
unsigned char mpu6050_read_register(unsigned char);
void mpu6050_write_register(unsigned char, unsigned char);
void mpu6050_read_temperature(unsigned int *temperature);
void mpu6050_read_accelerometer(accelerometer_t *acc);
void mpu6050_read_gyroscope(gyroscope_t *acc);

#endif /* INCLUDE_MPU6050_H_ */
