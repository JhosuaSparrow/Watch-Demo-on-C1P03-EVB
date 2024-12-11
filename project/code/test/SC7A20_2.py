from machine import I2C
import utime
from sensor import VC9202
from machine import Timer
from machine import Pin


class CustomError(Exception):
    def __init__(self, ErrorInfo):
        super().__init__(self)
        self.errorinfo=ErrorInfo

    def __str__(self):
        return self.errorinfo

class SC7A20(object):
    # register
    REG_WHO_AM_I      = 0x0F
    REG_NVM_WR        = 0X1E
    REG_accd_CFG      = 0X1F
    REG_CTRL_1        = 0x20
    REG_CTRL_2        = 0x21
    REG_CTRL_3        = 0x22
    REG_CTRL_4        = 0x23
    REG_CTRL_5        = 0X24
    REG_CTRL_6        = 0X25
    REG_REFERENCE     = 0X26
    REG_STATUS_REG    = 0X27
    REG_X_L           = 0x28
    REG_X_H           = 0x29
    REG_Y_L           = 0x2A
    REG_Y_H           = 0x2B
    REG_Z_L           = 0x2C
    REG_Z_H           = 0x2D
    REG_FIFO_CTRL_REG = 0X2E
    REG_FIFO_SRC_REG  = 0X2F
    REG_INT1_CFG      = 0X30
    REG_INT1_SOURCE   = 0X31
    REG_INT1_THS      = 0X32
    REG_INT1_DURATION = 0X33
    REG_INT2_CFG      = 0X34
    REG_INT2_SOURCE   = 0X35
    REG_INT2_THS      = 0X36
    REG_INT2_DURATION = 0X37
    REG_CLICK_CFG     = 0X38
    REG_CLICK_SRC     = 0X39
    REG_CLICK_THS     = 0X3A
    REG_TIME_LIMIT    = 0X3B
    REG_TIME_LATENCY  = 0X3C
    REG_TIME_WINDOW   = 0X3D
    REG_ACT_THS       = 0X3E
    REG_ACT_DURATION  = 0X3F

    def __init__(self):
        #self._child = child
        print(3)
        self._write_data(0X1E,0X05)
        self._write_data(0X57,0X00)
        self._write_data(0X1E,0X00)
        
        self._write_data(0X2E,0X00)
        self._write_data(0X20,0X47)
        self._write_data(0X23,0X98)
        self._write_data(0X24,0XC0)
        self._write_data(0X2E,0X4F)
        
        print(4)
        r_data1 = self._read_data(0X2E, 1)
        r_data2 = self._read_data(0X20, 1)
        r_data3 = self._read_data(0X23, 1)
        r_data4 = self._read_data(0X24, 1)
        r_data5 = self._read_data(0X2E, 1)
        print(5)
        print("data1:{}data2:{}data3:{}data4:{}data5:{}".format(
        [hex(x) for x in r_data1],
        [hex(x) for x in r_data2],
        [hex(x) for x in r_data3],
        [hex(x) for x in r_data4],
        [hex(x) for x in r_data5]
        ))
        print(6)
        if self._read_data(self.REG_WHO_AM_I,1)[0]!=0x11:
            raise CustomError("chip id err.")
        print(7)
    def do_difff_calibrate(self):
        '''
        校准,设置三轴的offset
        芯片需保持水平
        '''
        totalx = 0
        totaly = 0
        totalz = 0

        for i in range(20):
            x,y,z = self.read_data()
            totalx += x
            totaly += y
            totalz += z
            utime.sleep_ms(5)

        self.offset_x = totalx / 20 - 0
        self.offset_y = totaly / 20 - 0
        print(totalz / 20)
        
        if totalz > 0:
            self.offset_z = totalz / 20 - self.SENSITIVITY
        else:
            self.offset_z = totalz / 20 + self.SENSITIVITY

        print(self.offset_x,self.offset_y,self.offset_z)

    def set_power_off(self):
        """
        set chip power off
        """
        self._write_data(self.REG_CTRL_1,0x00)

    def set_deta_output_speed(self,speed_level):
        """
        Set the data output speed
        :param: speed_level:1:1Hz
                            2:10Hz
                            3:25Hz
                            4:50Hz
                            5:100Hz
                            6:200Hz
                            7:400Hz
        """
        r_data = self._read_data(self.REG_CTRL_1,1)[0]
        r_data &= 0x0F
        r_data |= speed_level<<4   
        self._write_data(self.REG_CTRL_1,r_data)
        
    def set_filter(self,High_pass_filter_mode,filter_selection,CLICK_filter_en,INT2_AOI_en,INT1_AOI_en):
        """
        设置滤波模式
        :param: High_pass_filter_mode:  0:正常模式 (读高通滤波自动复位)
                                        1:滤波参考信号
                                        2:正常模式
                                        3:中断事件自动复位
                filter_selection:   0:跳过内部滤波
                                    1:内部滤波以后的数据输出到数据寄存器或 FIFO
                CLICK_filter_en :   0:禁止
                                    1:使能
                INT2_AOI_en :       0:禁止
                                    1:使能
                INT1_AOI_en :       0:禁止
                                    1:使能
        """
        w_data = 0x00
        w_data = High_pass_filter_mode<<6 | filter_selection<<3 | CLICK_filter_en<<2 | INT2_AOI_en<<1 | INT1_AOI_en
        self._write_data(self.REG_CTRL_2,w_data)
        
    def set_range(self,range):
        '''
        设置量程
        :param range: 0:+/-2g
                      1:+/-4g
                      2:+/-8g
                      3:+/-16g
        '''
        r_data = self._read_data(self.REG_CTRL_4,1)[0]
        r_data &= 0xCF
        r_data |= range<<4
        self._write_data(self.REG_CTRL_4,r_data)

    def read_data(self,vc_obj):
        '''
        Read three axis data
        :return: 三轴数据元祖
        '''
        vc_obj.vc9202_lock_iic()
        for i in range(1):
            r_data = [0]*6
            r_data = self._read_data(self.REG_X_L|0x80, 6)

        self._read_data(self.REG_WHO_AM_I,1)
        vc_obj.vc9202_unlock_iic()
        x = (((r_data[1] << 8 | r_data[0])) &0x0fff)/1
        y = (((r_data[3] << 8 | r_data[2])) &0x0fff)/1 
        z = (((r_data[5] << 8 | r_data[4])) &0x0fff)/1 
        #print(utime.ticks_ms())
        #print(r_data[1] << 8 | r_data[0])
        #print(r_data[3] << 8 | r_data[2])
        #print(r_data[5] << 8 | r_data[4])
       
        print("X轴数据{} Y轴数据{} Z轴数据{}".format(x,y,z))
        #print(utime.ticks_ms())
        return (x, y, z)
        
    def read_fifo(self,vc_obj):
        '''
        Read three axis data
        :return: 三轴数据元祖
        '''
        #vc_obj.vc9202_lock_iic()
        print(type(vc_obj), " ", id(vc_obj))
        fifo_len = self._read_data(0X2F, 1)[0] & 0x1f
        print("fifo len{} ".format(fifo_len))
        data_x=[0]*fifo_len
        data_y=[0]*fifo_len
        data_z=[0]*fifo_len
        for i in range(fifo_len):
            data = [0]*6
            data = self._read_data(0XA0, 6)
            print("reg0x20: 0x{:x} reg0x21: 0x{:x} reg0x22: 0x{:x} reg0x23: 0x{:x} reg0x24: 0x{:x} reg0x24: 0x{:x}"
            .format(data[0],data[1],data[2],data[3],data[4],data[5]))
            #utime.sleep_ms(100)
            r_data = [0]*6
            r_data = self._read_data(0XA8, 6)
            x = (((r_data[1] << 8 | r_data[0])) ) 
            y = (((r_data[3] << 8 | r_data[2])) )
            z = (((r_data[5] << 8 | r_data[4])) ) 
            x = x >> 4
            y = y >> 4
            z = z >> 4
            data_x[i]=x
            data_y[i]=y
            data_z[i]=z
            print("数据x 0x{:x} 数据y 0x{:x} 数据z 0x{:x}".format(x,y,z))
        self._write_data(0x2e,0x00)
        self._write_data(0x2e,0x4f)  
        vc_obj.update_gsensor_data(fifo_len,data_x,data_y,data_z)
        #vc_obj.vc9202_unlock_iic()
        return (100, 100, 100)
    def read_acc(self,vc_obj):
        '''
        读取三轴加速度数据
        :return: (acc_x,acc_y,acc_z)
        '''
        print(type(vc_obj), " ", id(vc_obj))
        x,y,z = self.read_fifo(vc_obj)
        x = x / 1024
        y = y / 1024
        z = z / 1024
        #print("X轴j数据{} Y轴j数据{} Z轴j数据{}".format(x,y,z))
        return (x,y,z)

    def set_interrupt_1(self, CLICK,AOI1,AOI2,DRDY1,DRDY2,FIFO_watermark,FIFO_overflow):
        """
        设置中断在INT1上
        :all param: 1 使能
                    0 禁止
        """
        w_data = 0x00
        w_data = CLICK<<7 | AOI1<<6 | AOI2<<5 | DRDY1<<4 | DRDY2<<3 | FIFO_watermark<<2 | FIFO_overflow<<1
        self._write_data(self.REG_CTRL_3,w_data)

    def set_interrupt_2(self, CLICK,AOI1,AOI2,BOOT,H_LACTIVE):
        """
        设置中断在INT2上
        :param: 1 使能
                0 禁止
                H_LACTIVE:  0:高电平触发中断
                            1:低电平触发中断
        """
        w_data = 0x00
        w_data = CLICK<<7 | AOI1<<6 | AOI2<<5 | BOOT<<4 | H_LACTIVE<<1
        self._write_data(self.REG_CTRL_6,w_data)

    def read_status(self):
        """
        读取三轴数据状态
        """
        r_data = self._read_data(self.REG_STATUS_REG,1)[0]
        return r_data

    def set_interrupt_1_enable(self,AOI_6D,ZH_INT,ZL_INT,YH_INT,YL_INT,XH_INT,XL_INT):
        """
        设置中断1使能
        """
        w_data = 0x00
        w_data = AOI_6D<<6|ZH_INT<<5|ZL_INT<<4|YH_INT<<3|YL_INT<<2|XH_INT<<1|XL_INT
        self._write_data(self.REG_INT1_CFG,w_data)

    def read_interrupt_1_status(self):
        """
        中断1状态检测
        """
        r_data = self._read_data(self.REG_INT1_SOURCE,1)[0]
        return r_data

    def set_interrupt_1_threshold(self,threshold):
        """
        设置中断1阈值
        """
        self._write_data(self.REG_INT1_THS,threshold)

    def set_interrupt_1_duration(self,duration):
        """
        设置中断1持续时间
        """
        self._write_data(self.REG_INT1_DURATION,duration)

    def set_interrupt_2_enable(self,AOI_6D,ZH_INT,ZL_INT,YH_INT,YL_INT,XH_INT,XL_INT):
        """
        设置中断2使能
        """
        w_data = 0x00
        w_data = AOI_6D<<6|ZH_INT<<5|ZL_INT<<4|YH_INT<<3|YL_INT<<2|XH_INT<<1|XL_INT
        self._write_data(self.REG_INT2_CFG,w_data)

    def read_interrupt_2_status(self):
        """
        中断2状态检测
        """
        r_data = self._read_data(self.REG_INT2_SOURCE,1)[0]
        return r_data
    
    def set_interrupt_2_threshold(self,threshold):
        """
        设置中断2阈值
        """
        self._write_data(self.REG_INT2_THS,threshold)

    def set_interrupt_2_duration(self,duration):
        """
        设置中断2持续时间
        """
        self._write_data(self.REG_INT2_DURATION,duration)
    
class Sensor_i2c(SC7A20):
    def __init__(self,i2c):
        print(1)
        self._i2c = i2c
        self._dev_addr = 0x19  
        print(2)        
        super().__init__()

    def _read_data(self, regaddr, datalen):
        '''
        i2c读数据
        :param regaddr: 寄存器地址
        :param datalen: 读取的长度
        :return: 列表类型的data
        '''
        r_data = bytearray(datalen)
        reg_addres = bytearray([regaddr])
        self._i2c.read(self._dev_addr, reg_addres, 1, r_data, datalen, 0)
        ret_data = list(r_data)
        return ret_data

    def _write_data(self, regaddr, data):
        '''
        i2c写数据
        :param regaddr: 寄存器地址
        :param datalen: 写入的数据
        '''
        addr = bytearray([regaddr])
        w_data = bytearray([data])
        self._i2c.write(self._dev_addr, addr, len(addr), w_data, len(w_data))

    def _mask_write(self, regaddr, mask, data):
        '''
        i2c写mask位
        :param regaddr: 寄存器地址
        :param mask: 要写的位(如最高位0x80)
        :param data: 数据(0或1)
        '''
        r_data = self._read_data(regaddr,1)[0]
        if data == 0:
            r_data &= ~mask
        elif data ==1:
            r_data |= mask
        self._write_data(regaddr,r_data)

def fun(args):
    #print(utime.ticks_ms())
    print(args)

vc9202_obj= VC9202(2,29,fun)
obj_timer = Timer(Timer.Timer1)
gpio1 = Pin(Pin.GPIO1, Pin.OUT, Pin.PULL_DISABLE, 1)
print(type(vc9202_obj), " ", id(vc9202_obj)) 
print(type(obj_timer), " ", id(obj_timer))   
print(type(gpio1), " ", id(gpio1))   
def timer_fun(args):  
     print(type(vc9202_obj), " ", id(vc9202_obj))
     x,y,z = sc7a20.read_acc(vc9202_obj)
     print((x,y,z))

if __name__ == "__main__":
    print(type(vc9202_obj), " ", id(vc9202_obj))  
    print(type(obj_timer), " ", id(obj_timer)) 
    print(type(gpio1), " ", id(gpio1))       
    i2c_obj = I2C(I2C.I2C2, I2C.FAST_MODE)  # 返回i2c对象
    print(type(vc9202_obj), " ", id(vc9202_obj))
    print(type(obj_timer), " ", id(obj_timer))  
    print(type(gpio1), " ", id(gpio1))   
    #sc7a20 = Sensor_i2c(i2c_obj)
    #utime.sleep_ms(600)
    print(type(vc9202_obj), " ", id(vc9202_obj))
    print(type(obj_timer), " ", id(obj_timer)) 
    print(type(gpio1), " ", id(gpio1))  
    print(type(i2c_obj), " ", id(i2c_obj))     
    sc7a20 = Sensor_i2c(i2c_obj)
    print(type(vc9202_obj), " ", id(vc9202_obj))
    vc9202_obj.set_gsensor_type(50,2,12)
    vc9202_obj.start_samp()
    

    obj_timer.start(period=400, mode=obj_timer.PERIODIC, callback=timer_fun)
    #utime.sleep_ms(200)
    
    #utime.sleep_ms(100)
    while True:
        utime.sleep_ms(400)
        #x,y,z = sc7a20.read_acc(vc9202_obj)

            
        #print("X轴加速度{}g Y轴加速度{}g Z轴加速度{}g".format(x,y,z))
       