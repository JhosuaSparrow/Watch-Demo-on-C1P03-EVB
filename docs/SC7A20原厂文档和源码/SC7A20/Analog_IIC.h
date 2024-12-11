#ifndef __ANALOG_IIC_H__
#define __ANALOG_IIC_H__


#include "system.h"


#define IIC_SDA_0         GPIOC->ODR &= ((uint8_t)(~0x01))//PC0 IIC_SDA
#define IIC_SDA_1         GPIOC->ODR |= ((uint8_t)0x01)
#define IIC_SDA          (GPIOC->IDR & (uint8_t)0x01)//PC0 IIC_SDA
#define IIC_SCL_0         GPIOC->ODR &= ((uint8_t)(~0x02))//PC1 IIC_SCL
#define IIC_SCL_1         GPIOC->ODR |= ((uint8_t)0x02)


//Sensor RW Address
#define  Sensor_Wr_Addr1	0x30//DOUT_A1 level GND
#define  Sensor_Rd_Addr1	0x31
//#define  Sensor_Wr_Addr2	0xD8//DOUT_A1 level VDD
//#define  Sensor_Rd_Addr2	0xD9


extern void Analog_IIC_Delay(u8 n);
extern void Analog_IIC_Pin_Init(void);
extern void Sensor_Write_Byte(u8 RAddr, u8 *WData);
extern void Sensor_Write_NByte(u8 RAddr, u8 *WData, u8 WLen);
extern void Sensor_Read_Byte(u8 RAddr, u8 *RData);
extern void Sensor_Read_NByte(u8 RAddr, u8 *RData, u8 RLen);
extern void IIC_SDA_Dir(u8 d);

#endif

