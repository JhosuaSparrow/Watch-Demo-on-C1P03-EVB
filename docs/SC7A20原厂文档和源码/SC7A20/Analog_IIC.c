#include "Analog_IIC.h"

/*

  @16M---��ȷ��ʱ��΢��

*/
void Analog_IIC_Delay(u8 n)//@16M---��ȷ��ʱ��΢��
{
  n = n;
  nop(); 
  nop();
  nop();
}
/*

  ģ��IIC���ŷ�������

*/
void Analog_IIC_Pin_Init(void)
{
  GPIOC->DDR |= ((uint8_t)0x01);//PC0 IIC_SDA  ���
  GPIOC->CR1 |= ((uint8_t)0x01);//PC0 IIC_SDA  ����

  GPIOC->DDR |= ((uint8_t)0x02);//PC1 IIC_SCL  ���
  GPIOC->CR1 |= ((uint8_t)0x02);//PC1 IIC_SCL  ����
  
  IIC_SCL_1;  //����ʱ����
  IIC_SDA_1;  //����������
}
/*

  ģ��IIC_SDA���ŷ�������
  ����ֵ  1			���
          0			����

*/
void IIC_SDA_Dir(u8 d)
{
  if(d == 1)//���
  {
    GPIOC->DDR |= ((uint8_t)0x01);//PC0 IIC_SDA  ���
    GPIOC->CR1 |= ((uint8_t)0x01);//PC0 IIC_SDA  ����
  }
  else if(d == 0)//����
  {
    GPIOC->DDR &= ((uint8_t)~0x01);//PC0 IIC_SDA  ����
    GPIOC->CR1 &= ((uint8_t)~0x01);//PC0 IIC_SDA  ����
  }
}
//����IIC��ʼ�ź�
void IIC_Start(void)
{
  IIC_SDA_Dir(1);//IIC_SDA�����
  IIC_SDA_1;	 //���������� 	  
  IIC_SCL_1;	 //����ʱ����	
  Analog_IIC_Delay(10);
  IIC_SDA_0;   //����������
  Analog_IIC_Delay(10);
  IIC_SCL_0;   //����ʱ����  ����IIC���߿�ʼ�ź�
}	  
//����IICֹͣ�ź�
void IIC_Stop(void)
{
  IIC_SDA_Dir(1);//IIC_SDA�����
  IIC_SCL_0;   //����ʱ���� 
  IIC_SDA_0;   //����������
  Analog_IIC_Delay(10);
  IIC_SCL_1;   //����ʱ����	  
  Analog_IIC_Delay(10);
  IIC_SDA_1;   //����������  ����IIC����ֹͣ�ź�	
  Analog_IIC_Delay(10);							   	
}
//����ACKӦ��
void IIC_Ack(void)
{
  IIC_SCL_0;   //����ʱ���� 
  IIC_SDA_Dir(1);//IIC_SDA�����
  IIC_SDA_0;   //����������
  Analog_IIC_Delay(10);
  IIC_SCL_1;   //����ʱ����
  Analog_IIC_Delay(10);
  IIC_SCL_0;   //����ʱ���� 
}
//������ACKӦ��		    
void IIC_NAck(void)
{
  IIC_SCL_0;   //����ʱ���� 
  IIC_SDA_Dir(1);//IIC_SDA�����
  IIC_SDA_1;   //����������
  Analog_IIC_Delay(10);
  IIC_SCL_1;   //����ʱ����
  Analog_IIC_Delay(10);
  IIC_SCL_0;   //����ʱ���� 
}
//�ȴ�Ӧ���źŵ���
//����ֵ:1		����Ӧ��ʧ��
//       0	        ����Ӧ��ɹ�
u8 IIC_Wait_Ack(void)
{
  u8 Wait_TOut_Cnt = 0;//���õȴ�Ӧ���źų�ʱ����
  IIC_SDA_Dir(0); 		 //IIC_SDA������
  IIC_SDA_1;		     //����������
  Analog_IIC_Delay(10);	   
  IIC_SCL_1;         //����ʱ����  �ȴ�Ӧ���ź�	
  Analog_IIC_Delay(10);	 
  while(IIC_SDA)
  {
    Wait_TOut_Cnt++;
    if(Wait_TOut_Cnt > 250)
    {
      IIC_Stop();			 //�ȴ�Ӧ���źų�ʱ  ����IIC����ֹͣ�ź�	
      return 1;
    }
  }
  IIC_SCL_0;				 //����ʱ����  ����Ӧ���ź�	
  return 0;  
} 					 				     
//IIC����һ���ֽ�		  
void IIC_Write_Byte(u8 WByte)
{                        
  u8 Wb_Cnt = 0; //д����λ����    
  IIC_SDA_Dir(1);//IIC_SDA����� 	    
  IIC_SCL_0;   //����ʱ����    ��ʼ���ݴ���
  for(Wb_Cnt=0; Wb_Cnt<8; Wb_Cnt++)
  {
    if(WByte&0x80)
    {
      IIC_SDA_1;    
    }
    else
    {
      IIC_SDA_0;
    }
    WByte <<= 1; //������λ
    Analog_IIC_Delay(10);
    IIC_SCL_1; //����ʱ����
    Analog_IIC_Delay(10); 
    IIC_SCL_0; //����ʱ����   ׼����ʼ��������λ	
    Analog_IIC_Delay(10);
  }	 
} 	    
//IIC��ȡһ���ֽ�
//����ֵ:1		����Ack
//       0	        ������Ack
u8 IIC_Read_Byte(u8 SF_Ack)
{
  u8 Rb_Cnt = 0; //������λ���� 
  u8 RByte  = 0; //���ֽ�
  IIC_SDA_Dir(0);//SDA����Ϊ����
  for(Rb_Cnt=0; Rb_Cnt<8; Rb_Cnt++)
  {
    IIC_SCL_0; //����ʱ����   ׼����ʼ��������λ 
    Analog_IIC_Delay(10);
    IIC_SCL_1; //����ʱ����
    RByte <<= 1; //������λ
    if(IIC_SDA)
    {
      RByte++;
    }			
    Analog_IIC_Delay(10); 
  }					 
  if(!SF_Ack)    //0	������Ack
  {
    IIC_NAck();  //����NAck
  }
  else           //1		����Ack
  {
    IIC_Ack();   //����Ack
  }		
  return RByte;
}
/*

  дһ���ֽ�

*/
void Sensor_Write_Byte(u8 RAddr, u8 *WData)
{
  IIC_Start();								 		//����IIC��ʼ�ź�
  IIC_Write_Byte(Sensor_Wr_Addr1);//����IICд��ַ
  IIC_Wait_Ack();							 		//�ȴ�IICӦ���ź�	
  IIC_Write_Byte(RAddr);   		 		//����IIC�Ĵ�����ַ
  IIC_Wait_Ack(); 	 					 		//�ȴ�IICӦ���ź�					  		   
  IIC_Write_Byte(*WData);      		//����д��Ĵ���������					   
  IIC_Wait_Ack();  		    	   		//�ȴ�IICӦ���ź�			 
  IIC_Stop();									 		//����IICֹͣ�ź�	
}
/*

  дN���ֽ�

*/
void Sensor_Write_NByte(u8 RAddr, u8 *WData, u8 WLen)
{
  u8 WB_Cnt = 0;
  IIC_Start();								 		//����IIC��ʼ�ź�
  IIC_Write_Byte(Sensor_Wr_Addr1);//����IICд��ַ
  IIC_Wait_Ack();							 		//�ȴ�IICӦ���ź�	
  IIC_Write_Byte(RAddr);   		 		//����IIC�Ĵ�����ַ
  IIC_Wait_Ack(); 	 					 		//�ȴ�IICӦ���ź�					  		   
  for(WB_Cnt=0; WB_Cnt<WLen; WB_Cnt++)
  {
    IIC_Write_Byte(WData[WB_Cnt]);//������ȡ�Ĵ���������		�ȴ�Ӧ���ź�	  
    IIC_Wait_Ack();  		    	   		//�ȴ�IICӦ���ź�			 
  }  
  IIC_Stop();									 		//����IICֹͣ�ź�	
}
/*

  ��һ���ֽ�

*/
void Sensor_Read_Byte(u8 RAddr, u8 *RData)
{
  IIC_Start();								 		//����IIC��ʼ�ź�
  IIC_Write_Byte(Sensor_Wr_Addr1);//����IICд��ַ
  IIC_Wait_Ack();  						 		//�ȴ�IICӦ���ź�
  IIC_Write_Byte(RAddr);   		 		//����IIC�Ĵ�����ַ
  IIC_Wait_Ack();	    				 		//�ȴ�IICӦ���ź�	
  IIC_Start();  	 	   				 		//����IIC��ʼ�ź�
  IIC_Write_Byte(Sensor_Rd_Addr1);//����IIC����ַ	   
  IIC_Wait_Ack();	 						 		//�ȴ�IICӦ���ź�		
  *RData = IIC_Read_Byte(0);	 		//��ȡ�Ĵ���������	   
  IIC_Stop();									 		//����IICֹͣ�ź�	
}
/*

  ��N���ֽ�

*/
void Sensor_Read_NByte(u8 RAddr, u8 *RData, u8 RLen)
{
  u8 RB_Cnt = 0;							 		   //���ֽڼ���
  IIC_Start();								 		   //����IIC��ʼ�ź�
  IIC_Write_Byte(Sensor_Wr_Addr1);   //����IICд��ַ
  IIC_Wait_Ack();							 		   //�ȴ�IICӦ���ź�	
  IIC_Write_Byte(RAddr);			 			 //����IIC�Ĵ�����ַ
  IIC_Wait_Ack();	    				 			 //�ȴ�IICӦ���ź�		
  IIC_Start();  	 	   				 			 //����IIC��ʼ�ź�
  IIC_Write_Byte(Sensor_Rd_Addr1);	 //����IIC����ַ	   
  IIC_Wait_Ack();							 			 //�ȴ�IICӦ���ź�		
  for(RB_Cnt=0; RB_Cnt<(RLen-1); RB_Cnt++)
  {
    RData[RB_Cnt] = IIC_Read_Byte(1);//������ȡ�Ĵ���������		�ȴ�Ӧ���ź�	  
  }
  RData[RB_Cnt] = IIC_Read_Byte(0);  //��ȡ�Ĵ������һ������	���ȴ�Ӧ���ź�
  IIC_Stop();										     //����IICֹͣ�ź�	
}

