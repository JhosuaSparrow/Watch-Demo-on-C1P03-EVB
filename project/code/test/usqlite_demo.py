import usqlite
import utime as time

con = usqlite.connect("usr/data1.db")  # 打开&创建
cur = con.cursor()
cur.executemany(
    "BEGIN TRANSACTION;" 
    "CREATE TABLE IF NOT EXISTS data (name TEXT, year INT);" +
    "INSERT INTO data VALUES ('Larry', 1902);" +
    "INSERT INTO data VALUES ('Curly', 1903);" +
    "INSERT INTO data VALUES ('Moe', 1897);" +
    "INSERT INTO data VALUES ('Shemp', 1895);" + "COMMIT;"
)  # 添加数据

count = 0

start_time = 0
name_test = 'Lily'

while 1:
    if count == 0:
        start_time = time.ticks_ms()

    count += 1
    result = cur.execute("INSERT INTO data (name, year) VALUES (?, ?)", (name_test, count))
    if result:
        # print("Found match:", result)
        pass
    else:
        print("No matches found")
    # print("stooge:", count)
    if count == 100:
        end_time = time.ticks_ms()
        count = 0
        elapsed_time = time.ticks_diff(end_time, start_time) / 1000
        print("100次写入用的时间为S=:", elapsed_time)
        # print("count: %s gc=%s"%(count, gc.mem_free()))

    time.sleep_us(1)

con.close()  # 关闭
