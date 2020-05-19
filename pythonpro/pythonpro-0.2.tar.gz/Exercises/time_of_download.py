"""
Faça um programa que peça o tamanho de um arquivo para download (em MB) e
 calcule e informe o tempo aproximado de download do arquivo .

"""


import speedtest
st = speedtest.Speedtest()
pesoDoarquivo = int(input('Cuanto pesa o arquivo em MB?\n'))
time = pesoDoarquivo/int(str(st.download())[:2])
print('Para descargar un archivo de ', pesoDoarquivo, 'MB\n'
      'Con una velocidad de', int(str(st.download())[:2]), 'Mbps\n'
      'Tardará', int(str(int(time))[:2]), 'Segundos\n\t\t\t...🙄')
