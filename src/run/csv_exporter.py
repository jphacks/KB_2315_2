from time import sleep
from kb_2315_2.func.data_sampler import sampler

s = sampler()

while True:
    s.sampler()
    sleep(3)
    # 時間割込みでないため，正確ではない
    # センサ数が3の時，処理におよそ2秒かかるため，5秒間隔で更新するために3に設定
