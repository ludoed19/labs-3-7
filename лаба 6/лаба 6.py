import math, time
import matplotlib.pyplot as plt

# --------- итеративная ---------
def F_iter_fast(n:int)->float:
    if n<2: return 1.0
    f2,f1,fact,sign,cos_=1.0,1.0,1,1,math.cos
    for i in range(2,n+1):
        fact*=(2*i-1)*(2*i)          # факториал (2i)! считаем из предыдущего значения
        cur=sign*(f1/fact - cos_(f2+2.0))
        f2,f1=f1,cur
        sign=-sign                    # отдельная переменная для чередования знака
    return f1

# --------- рекурсивная ---------
def F_rec_fast(n:int)->float:
    def fact2(k:int)->float:
        if k==0: return 1.0
        return fact2(k-1)*(2*k-1)*(2*k)  # факториал (2k)! реализован рекурсивно
    if n<2: return 1.0
    s=1.0 if n%2==0 else -1.0
    return s*(F_rec_fast(n-1)/fact2(n)-math.cos(F_rec_fast(n-2)+2.0))

if __name__=="__main__":
    N_MAX,REC_TIMEOUT=25,0.25
    ns=list(range(N_MAX+1)); t_it=[]; t_rec=[]
    for n in ns:
        t0=time.perf_counter(); F_iter_fast(n); t_it.append(time.perf_counter()-t0)
        t0=time.perf_counter()
        try:
            F_rec_fast(n); tr=time.perf_counter()-t0
            t_rec.append(tr if tr<=REC_TIMEOUT else None)
        except Exception:
            t_rec.append(None)

    print(" n | t_iter(s) | t_rec(s)")
    print("-"*26)
    for n,ti,tr in zip(ns,t_it,t_rec):
        print(f"{n:2d} | {ti:9.6f} | {('-' if tr is None else f'{tr:8.6f}')}")

    plt.figure(figsize=(6,4))
    plt.plot(ns,t_it,marker="o",label="Итеративный")
    ns_ok=[n for n,x in zip(ns,t_rec) if x is not None]
    tr_ok=[x for x in t_rec if x is not None]
    if ns_ok: plt.plot(ns_ok,tr_ok,marker="o",label="Рекурсивный")
    plt.xlabel("n"); plt.ylabel("Время, с"); plt.title("F(n): время вычисления"); plt.legend(); plt.tight_layout(); plt.show()
