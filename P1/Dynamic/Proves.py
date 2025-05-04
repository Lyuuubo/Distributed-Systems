import subprocess
import time

p = subprocess.Popen(["python", "Main.py"])
#                      ,stdout=subprocess.DEVNULL)
print("PID del proceso:", p.pid)
print(p.poll())
time.sleep(5)
p.terminate()
time.sleep(0.5)
print(p.poll())

# Esperar a que termine (si quieres)
exit_code = p.wait()
print("Código de salida:", exit_code)
