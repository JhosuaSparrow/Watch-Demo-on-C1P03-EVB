#include "Analog_IIC.h"
#include "drv_l1_gsensor.h"
u8 SC7A20_Msg = 8;
u8 SC7A20_REG[10] = {0x2f,0x04,0x98,0x05,0x08,0x02,0x05,0x01,0x15,0x80};
s8 Acc_Data[3];

void G_Sensor_SC7A20_Init(u8 *Acc_Int_Thr)
{
	u8  temp1;
       
	Sensor_Read_Byte(CHIPID,&temp1);   
	USART1_printf("Chip_ID = %x\r\n", temp1);
        
	USART1_printf("G_Sensor_SC7A20_Init \r\n");
	if(temp1 != 0x11)// I2C address fixed --> ��ȡϵͳID������쳣����Ҫ����д��ԭ��������
	{
            USART1_printf("Error\r\n");		
	}
	
        /*click */
        Sensor_Write_Byte(0x20,&SC7A20_REG[0]);  //odr 10Hz
        Sensor_Write_Byte(0x21,&SC7A20_REG[1]);  //fds -->������ͨ�˲���(�˵�����G)(һ��Ҫ������������ֵҪ����1G�����Ҷ���ҲҪ����1G)
        Sensor_Write_Byte(0x23,&SC7A20_REG[2]);  //range bdu  0x20--0xA8
        //SDO �ӵ�
        Sensor_Write_Byte(0x1e,&SC7A20_REG[3]);  //�������ƿ���
        Sensor_Write_Byte(0x57,&SC7A20_REG[4]);  //�ر�SDO�ܽ��ϵ���������
        
        Sensor_Write_Byte(0x25,&SC7A20_REG[5]); //selects active level low for pin INT �����Ǹߵ�ƽ����Ч��ʱ���ǵ͵�ƽ
        Sensor_Write_Byte(0x3a,Acc_Int_Thr);    //�趨�ж���ֵ(������ֵ) 
        Sensor_Write_Byte(0x3b,&SC7A20_REG[6]);

        Sensor_Write_Byte(0x3c,&SC7A20_REG[7]);
        Sensor_Write_Byte(0x38,&SC7A20_REG[8]); //ǰһ���жϺͺ�һ���жϵı���ʱ��(1���Ǳ���1��ODR��2����2��ODR(����10HZ��2����ÿ���жϱ���200mS��200mS�ڼ���жϲ���Ӧ))
        Sensor_Write_Byte(0x22,&SC7A20_REG[9]);
       
//	g_sensor_write(G_SlaveAddr,0x20,0x2f);  //odr
//	g_sensor_write(G_SlaveAddr,0x21,0x04);  //fds -->������ͨ�˲���(�˵�����G)(һ��Ҫ������������ֵҪ����1G�����Ҷ���ҲҪ����1G)
//	g_sensor_write(G_SlaveAddr,0x23,0x98);  //range bdu  0x20--0xA8
//        
//        //SDO �ӵ�
//        g_sensor_write(G_SlaveAddr,0x1e,0x05);  //�������ƿ���
//        g_sensor_write(G_SlaveAddr,0x57,0x08);  //�ر�SDO�ܽ��ϵ���������
        
        /*AOI*/
//	g_sensor_write(G_SlaveAddr,0x20,0x2f);  //����odr
//	g_sensor_write(G_SlaveAddr,0x23,0x98);  //��������range bdu  0x20--0xA8
}

/*read accelertion data */
u8 read_acceler_data(s8 *buf)
{
  u8 i;
  u8 cd[6];
  for(i=0;i<6;i++){
    Sensor_Read_Byte(0x28+i,&cd[i]);  
  }
  buf[0]=cd[1];
  buf[1]=cd[3];
  buf[2]=cd[5];
  
// if(((buf[0]==0)&&(buf[1]==0)&&(buf[2]==0))
//      ||((buf[0]==-1)&&(buf[1]==-1)&&(buf[2]==-1))
//     )
//  {
//    return 1;
//  }
  
  return 0;   
}

/*read accelertion data , only X and Y axis*/
u8 Read_XY_Data(s8 *buf)
{
  u8 cd[2];
  Sensor_Read_Byte(0x28+1,&cd[0]);  
  Sensor_Read_Byte(0x28+3,&cd[1]);
  buf[0]=cd[0];
  buf[1]=cd[1];
  return 0;   
}